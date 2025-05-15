import os
import json
from BioMiner.commons.process_pdf import draw_bbox_xywh
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
try:
    from ultralytics import YOLO
except:
    print(f'ultralytics is not installed in this environment')

class ModelSingleton:
    _instance = None
    _det_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelSingleton, cls).__new__(cls)
        return cls._instance

    def get_model(self, YOLO_model, device):
        if self._det_model is None:
            try:
                if YOLO_model == 'MOL-v11l-241113.pt':
                    self._det_model = YOLO("BioMiner/commons/MOL-v11l-241113.pt").to(device)
                else:
                    self._det_model = YOLO("BioMiner/commons/moldet_yolo11l_960_doc.pt").to(device)
            except Exception as e:
                print(f"Failed to load YOLO model: {e}")
                self._det_model = None
        return self._det_model



def load_md_external_res(res_json_file):
    
    if not os.path.exists(res_json_file):
        return []
    
    with open(res_json_file, 'r') as f:
        molminer_bbox = json.load(f)

    return molminer_bbox

def run_yolo(imgs, save_paths, device, YOLO_model='moldet_yolo11l_960_doc', iou_threshold=0.85):

    det_model = ModelSingleton().get_model(YOLO_model, device)
    if det_model is None:
        print("Model loading failed, returning empty results")
        return [], []

    if YOLO_model == 'MOL-v11l-241113.pt':
        results1 = det_model.predict(imgs, imgsz=640, conf=0.5)  # 模型预测结果
    else:
        results1 = det_model.predict(imgs, imgsz=960, conf=0.5)  # 模型预测结果
    all_mols = []
    all_bboxes = []
    
    for idx in range(len(imgs)):
        result1 = results1[idx]
        img = imgs[idx]
        save_path = save_paths[idx]
        img_width, img_height = img.size
        img_area = img_width * img_height
        
        mols = []
        bboxes = []
        boxes1 = result1.boxes
        total_box_area = 0

        for xyxy in boxes1.xyxy:
            x1, y1, x2, y2 = xyxy.detach().cpu().numpy()
            box_area = (x2 - x1) * (y2 - y1)
            total_box_area += box_area

        if total_box_area / img_area > iou_threshold:
            mols.append(img)
            bboxes.append([0, 0, 1, 1])
        else:
            for xyxy in boxes1.xyxy:
                x1, y1, x2, y2 = xyxy.detach().cpu().numpy()
                mols.append(img.crop((x1, y1, x2, y2)))
                bboxes.append([x1 / img_width, y1 / img_height, (x2-x1)/ img_width, (y2-y1)/img_height])

            index = 0
            for xyxy in boxes1.xyxy:
                x1, y1, x2, y2 = xyxy.detach().cpu().numpy()
                draw_bbox_xywh(img, x1 / img_width, y1 / img_height, (x2-x1)/ img_width, (y2-y1)/img_height, index)
                index += 1

        if len(bboxes) > 0:
            img.save(save_path)

        all_mols.append(mols)
        all_bboxes.append(bboxes)

    return all_mols, all_bboxes

def run_yolo_single(image_path, save_dir, device):
    save_path = os.path.join(save_dir, os.path.basename(image_path))
    img = Image.open(image_path)
    _, bboxes = run_yolo([img], [save_path], device)
    return bboxes


def run_yolo_batch(name, image_path_batch, save_dir, device, batch_size=64):
    os.makedirs(os.path.join(save_dir, name), exist_ok=True)

    total_imgs, total_all_bboxes = [], []
    for idx in range(0, len(image_path_batch), batch_size):
        iamge_paths_temp = image_path_batch[idx:idx + batch_size]

        imgs = [Image.open(img_path) for img_path in iamge_paths_temp]
        total_imgs.extend(imgs)
        save_paths = [os.path.join(save_dir, name, os.path.basename(img_path))  for img_path in iamge_paths_temp]

        _, all_bboxes = run_yolo(imgs, save_paths, device)
        total_all_bboxes.extend(all_bboxes)

    return total_all_bboxes


def check_bbox_cross_area(bbox, area_bbox):
    if not check_bbox_in_area(bbox, area_bbox) and not check_bbox_not_in_area(bbox, area_bbox):
        return True
    else:
        return False

def check_bbox_not_in_area(bbox, area_bbox):
    # print(area_bbox)
    x, y, w, h = bbox
    a_x, a_y, a_w, a_h = area_bbox

    xmin = x
    ymin = y
    xmax = x + w
    ymax = y + h
    a_xmin = a_x
    a_ymin = a_y
    a_xmax = a_x + a_w
    a_ymax = a_y + a_h

    if xmin > a_xmax or xmax < a_xmin or ymin > a_ymax or ymax < a_ymin:
        return True
    else:
        return False

def check_bbox_in_area(bbox, area_bbox):
    # print(area_bbox)
    x, y, w, h = bbox
    a_x, a_y, a_w, a_h = area_bbox

    xmin = x
    ymin = y
    xmax = x + w
    ymax = y + h
    a_xmin = a_x
    a_ymin = a_y
    a_xmax = a_x + a_w
    a_ymax = a_y + a_h

    if xmin >= a_xmin and xmax<=a_xmax and ymin>=a_ymin and ymax <= a_ymax:
        return True
    else:
        return False

def scale_yolo_bbox(bbox, area_bbox):
    # different ratio between full page and segmented table
    x, y, w, h = bbox
    a_x, a_y, a_w, a_h = area_bbox

    new_x = a_x + x * a_w
    new_y = a_y + y * a_h
    new_w = w * a_w
    new_h = h * a_h

    # input(f'scale bbox {bbox}, table bbox {area_bbox}, new bbox {[new_x, new_y, new_w, new_h]}')
    return [new_x, new_y, new_w, new_h]


def merge_full_page_and_seg_table_bbox(full_page_bboxes, seg_table_bboxes):
    full_page_2_bbox = defaultdict(list)

    for bbox in full_page_bboxes:
        bbox_line = bbox['bbox']
        page = int(bbox['page'])
        full_page_2_bbox[page].append(bbox_line)
    
    # print(molminer_bbox_path)
    for table in seg_table_bboxes:
        page_idx = int(table['page'])
        table_layout_bbox = table['tb_layout_bbox']

        if page_idx not in full_page_2_bbox.keys():
            continue

        exist_cross_box_flag = False

        for full_page_bbox in full_page_2_bbox[page_idx]:
            if check_bbox_cross_area(full_page_bbox, table_layout_bbox):
                exist_cross_box_flag = True
                break
        
        if exist_cross_box_flag:
            continue
        
        merge_bboxes = [scale_yolo_bbox(bbox, table_layout_bbox) for bbox in table['bboxes']]

        for full_page_bbox in full_page_2_bbox[page_idx]:
            if not check_bbox_in_area(full_page_bbox, table_layout_bbox):
                merge_bboxes.append(full_page_bbox)

        full_page_2_bbox[page_idx] = merge_bboxes
    
    new_page_bbox = []
    global_index = 0
    for page in full_page_2_bbox.keys():
        page_bboxes = full_page_2_bbox[page]
        page_bboxes.sort(key=lambda x:x[1])
        
        for index, bbox in enumerate(page_bboxes):
            new_page_bbox.append({'index':global_index,
                                    'page':page,
                                    'bbox':bbox
                                    })
            global_index += 1

    return new_page_bbox