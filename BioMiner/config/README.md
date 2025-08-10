# 文件夹内配置文件作用

## 配置文件作用分析

这两个YAML文件是BioMiner系统的**核心配置文件**，用于控制整个多模态代理系统的运行参数和模型选择。

### 1. **文件差异与用途**

**`default.yaml`** - 标准配置
- 使用外部/商业模型：`mol_detection_model: external`, `ocsr_model: external`
- 适合有API访问权限或商业模型的场景

**`default_open_source.yaml`** - 开源配置  
- 使用开源模型：`mol_detection_model: yolo`, `ocsr_model: molscribe`
- 适合完全开源部署的场景

### 2. **配置结构解析**

#### **基础设置**
```yaml
device: cuda:4          # GPU设备选择
output_dir: ./BioMiner/example_log  # 输出目录
n_jobs: 64             # 并行处理任务数
```

#### **数据预处理代理配置**
```yaml
data:
  parse_text_method: mineru     # 文本解析方法
  parse_image_method: mineru_contain  # 图像解析方法
  no_text_table: false         # 是否包含无文本表格
```

#### **模型代理配置**
- **化学结构提取代理**：
  - `mol_detection_model`: 分子检测模型选择
  - `ocsr_model`: 光学化学结构识别模型
  
- **多模态语言模型**：
  - `text_mllm_type: gemini-2.0-flash`: 文本处理MLLM
  - `vision_mllm_type: gemini-2.0-flash`: 视觉处理MLLM

- **策略配置**：
  - `bioactivity_text_strategy: updated`: 文本生物活性提取策略
  - `structure_full_strategy: updated-with-box-index`: 完整结构提取策略

#### **测试评估配置**
```yaml
test:
  comprehensive_evaluate: true    # 综合评估
  complex_specific_evaluate: true # 复杂特定评估
  top_n: 20                      # Top-N评估
```

### 3. **在系统架构中的作用**

这些配置文件控制着BioMiner四个专属代理的具体行为：

1. **数据预处理代理**：通过`parse_text_method`和`parse_image_method`控制PDF解析策略
2. **化学结构提取代理**：通过`mol_detection_model`和`structure_*_strategy`控制分子检测和结构提取
3. **生物活性测量提取代理**：通过`bioactivity_*_strategy`控制生物活性数据提取
4. **数据后处理代理**：通过`merge_strategy`控制数据整合方式

### 4. **灵活性设计**

配置文件体现了BioMiner的**模块化和可配置性**：
- 支持不同的模型后端（开源vs商业）
- 可调整处理策略和参数
- 支持不同的评估模式
- 便于研究和生产环境的切换

这种设计使得用户可以根据具体需求和资源情况选择合适的配置，体现了该系统良好的工程实践和用户友好性。
