# BioMiner项目文件的具体作用

### 1. **example.py** - 主要使用入口
```python
# 最佳性能版本的主要执行脚本
model = BioMiner(config, biovista_evaluate=args.biovista_evaluate, 
                 external_full_md_res_dir=args.external_ocsr_res_dir,
                 external_ocsr_res_dir=args.external_ocsr_res_dir)
```
- 支持单个PDF文件或目录批量处理
- 集成外部模型（MolMiner和MolParser）以获得最佳性能
- 输出提取的化学结构和生物活性数据

### 2. **开源版本脚本**
- **example_open_source_one.py**：完全开源版本的第一阶段（BioMiner环境）
- **example_open_source_two.py**：完全开源版本的第二阶段（BioMiner_MolScribe环境）

由于包版本冲突，开源版本需要两个conda环境分别运行。

### 3. **biovista_component_evaluate.py** - 评估系统
包含四个专门的评估器：
- **MoleculeDetectionEvaluator**：分子检测性能评估（使用COCO格式）
- **OCSREvaluator**：光学化学结构识别准确性评估  
- **FullMoleculeCoreferenceEvaluator**：全结构共指消解评估
- **MarkushZipEvaluator**：Markush结构枚举评估

### 4. **download_models.py** - 模型下载器
```python
# 自动下载MinerU所需的模型组件
mineru_patterns = [
    "models/Layout/YOLO/*",      # 布局检测
    "models/MFD/YOLO/*",         # 数学公式检测  
    "models/MFR/unimernet_hf_small_2503/*",  # 公式识别
    "models/OCR/paddleocr_torch/*",  # OCR识别
]
```

### 5. **magic-pdf.json** - MinerU配置
MinerU PDF解析工具的配置文件，包含：
- 模型路径配置
- 设备模式（CUDA）
- 布局、公式、表格识别的具体配置
- LLM辅助功能配置

### 6. **LICENSE** - MIT开源许可证
允许自由使用、修改和分发代码。

## 系统架构理解

基于这些文件，BioMiner采用**模块化代理架构**：

1. **数据预处理** → 使用MinerU进行PDF解析和布局分析
2. **化学结构提取** → 集成分子检测和OCSR模型  
3. **生物活性提取** → 使用MLLM从多模态数据中提取
4. **数据后处理** → 匹配和整合形成最终三元组

这是一个相当完整的生物信息学文献挖掘系统，既提供了最佳性能版本（集成商业模型），也提供了完全开源的替代方案。
