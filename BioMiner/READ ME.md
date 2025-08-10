# Runner文件夹内文件分析

## 文件架构分析

### 1. **`runner/__init__.py`**
**作用：包管理模块**
- 定义了`runner`包的对外接口
- 导入核心模块：`extractor`, `metric_fn`, `mllm`, `visualize_fn`
- 为整个数据提取流水线提供统一的入口点

### 2. **`extractor.py`**
**作用：核心数据提取引擎**

这是系统的核心模块，实现了多个专业代理的功能：

**主要功能模块：**
- **图像处理与分割**：
  ```python
  image_segment_given_box_xywh()  # 基于边界框分割图像
  draw_bbox_xywh()  # 绘制分子结构边界框
  segment_image_by_layout()  # 基于版面布局分割
  ```

- **生物活性数据提取**：
  ```python
  extraction_text_bioactivity_step()    # 从文本提取生物活性
  extraction_image_bioactivity_step()   # 从图像提取生物活性  
  extraction_bioactivity_step()         # 综合提取流程
  ```

- **化学结构提取**：
  ```python
  extraction_ligand_structure_full_step()  # 提取完整分子结构
  extraction_ligand_structure_part_step()  # 提取Markush结构
  ```

- **数据存储与管理**：
  ```python
  save_bioactivity_results()  # 保存生物活性结果
  save_structure_results()    # 保存结构结果
  ```

### 3. **`mllm.py`**
**作用：多模态大语言模型接口**

负责与各种MLLM模型的交互：

- **API调用管理**：
  ```python
  call_api_text()   # 文本模态API调用
  call_api_image()  # 图像模态API调用
  get_api_client()  # 获取API客户端
  ```

- **数据格式转换**：
  ```python
  bioactivity_data_api_output_to_list()     # 生物活性数据格式转换
  full_structure_data_api_putput_to_list()  # 完整结构数据转换
  part_structure_data_api_putput_to_list()  # 部分结构数据转换
  ```

- **化学结构处理**：
  ```python
  zip_molecule()  # 分子片段组装
  convert_molminer_scaffold_smiles_for_zip()  # 骨架SMILES转换
  ```

### 4. **`metric_fn.py`**
**作用：评估与验证系统**

提供完整的数据质量评估框架：

- **核心评估类**：
  ```python
  class resulter():  # 结果评估管理器
      - initialize_evaluating_result()  # 初始化评估
      - update_evaluating_result()      # 更新评估结果
      - output_evaluating_result()      # 输出评估报告
  ```

- **专项评估函数**：
  ```python
  evaluate_bioactivity()              # 生物活性数据评估
  evaluate_structure()                # 化学结构评估  
  evaluate_bioactivity_structure_together()  # 综合评估
  ```

- **数据验证**：
  ```python
  check_smiles_validity()    # SMILES有效性检查
  check_valid_bioactivity_data()  # 生物活性数据验证
  ```

### 5. **`ocsr.py`**
**作用：光学化学结构识别**

专门处理文献中的化学结构图像：

- **分子检测与分割**：
  ```python
  segment_openchemie()  # 使用OpenChemIE进行分子检测
  draw_bbox()          # 绘制分子边界框
  ```

- **结构识别**：
  ```python
  ocsr()  # 光学化学结构识别主函数
  pre_process_smiles()  # SMILES预处理
  ```

- **集成MolScribe模型**进行结构-SMILES转换

### 6. **`utils.py` & `visualize_fn.py`**
**作用：工具与可视化模块**
- 目前为空文件，预留用于扩展功能
- 可能用于数据可视化和通用工具函数

## 系统架构中的角色

这些文件共同实现了BioMiner的四个专属代理：

1. **数据预处理代理** ← `extractor.py`中的图像分割和布局分析
2. **化学结构提取代理** ← `ocsr.py` + `extractor.py`结构提取 + `mllm.py`模型调用
3. **生物活性测量提取代理** ← `extractor.py`生物活性提取 + `mllm.py`
4. **数据后处理代理** ← `metric_fn.py`评估验证 + `extractor.py`数据整合

整个系统通过`runner`包的模块化设计，实现了从PDF文献到结构化生物活性数据的端到端自动化提取流水线。
