# BioMiner项目文件

## 文件结构分析

### 1. `BioMiner/__init__.py`
这是Python包的初始化文件，作用是：
- 将BioMiner定义为一个可导入的Python包
- 从`interface`模块中导入主要的`BioMiner`类，使其可以直接通过`from BioMiner import BioMiner`调用

### 2. `BioMiner/interface.py` 
这是项目的**核心接口文件**，实现了完整的多模态生物活性数据挖掘pipeline。主要包含：

## 核心组件分析

### 主要类定义

**1. `BioMiner`类 - 主系统类**
实现了你提到的四个专属代理的完整功能：

#### 数据预处理代理 (`agent_preprocess`)
- PDF页面转图像：`pdf_load_pypdf_images`
- 布局分析：使用MinerU进行文档布局分析和阅读顺序确定
- 文本提取：提取PDF中的文本内容
- 表格和图像区域识别：识别包含表格和图形的页面区域

#### 化学结构提取代理 (`agent_chemical_structure`)
- **分子检测**：
  - 全页面分子检测：支持外部模型或YOLO
  - 分割表格检测：对表格区域进行分子检测
  - 结果合并：整合全页面和分割检测结果
- **光学化学结构识别(OCSR)**：
  - 支持外部OCSR模型或MolScribe
  - 生成SMILES字符串
- **MLLM推理**：使用多模态大语言模型进行结构理解和验证

#### 生物活性测量提取代理 (`agent_bioactivity_measurement`)
- 文本模态：从文档文本中提取生物活性数据
- 视觉模态：从图像和表格中提取生物活性信息
- 合并策略：整合多模态提取的结果

#### 数据后处理代理 (`agent_postprocess`)
- 数据匹配：将化学结构与生物活性数据进行关联
- 三元组构建：形成完整的蛋白质-配体-生物活性三元组
- 结果保存：保存最终的结构化数据

**2. `BioMiner_Markush_Infernce`类**
专门用于处理Markush结构的推理，这是化学专利中常见的通用结构表示。

### 关键方法功能

#### 主要工作流程方法
- `extract_pdf()`: **主要入口方法**，完整执行从PDF到结构化数据的全流程
- `opensource_stage_one()`: 执行第一阶段（预处理+分子检测）
- `opensource_stage_two()`: 执行第二阶段（OCSR+MLLM推理+数据提取）

#### 支撑功能
- `init_pred_dir()`: 初始化输出目录结构
- `init_biominer()`: 配置模型参数和提示词策略
- `evaluate_biovista()`: 使用BiOVISTa数据集进行性能评估

## 技术特点

### 1. 模块化设计
每个代理都有独立的处理函数，支持并行处理和灵活配置

### 2. 多模型支持
- 分子检测：支持YOLO、外部模型等
- OCSR：支持MolScribe、外部OCSR模型  
- MLLM：支持多种文本和视觉语言模型

### 3. 并行处理
使用`pmap_multi`实现多进程并行处理，提高处理效率

### 4. 灵活配置
通过配置文件控制各种处理策略、模型选择和参数设置

## 在项目中的核心作用

这个`interface.py`文件是整个BioMiner系统的**统一接口层**，它：
1. 封装了所有底层的处理模块
2. 提供了简洁的API供用户调用
3. 实现了完整的数据处理pipeline
4. 支持分阶段处理和评估功能

用户只需要实例化`BioMiner`类并调用`extract_pdf()`方法，就能完成从PDF文献到结构化生物活性数据的完整转换过程。
