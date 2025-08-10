# 系统启动和工作时使用的 GitHub 仓库内文件详解

## 1. **准备阶段（系统启动前：安装和配置）**
   这个阶段涉及创建环境、下载模型和配置参数。系统不直接“启动”应用程序，而是通过脚本执行，因此准备是关键。

   - **环境创建和依赖安装文件**：
     - `scripts/conda_env.sh`：用于最佳性能版本的 Conda 环境创建脚本（Python 3.10）。作用：安装核心包如 RDKit、OPSIN、tqdm 等。使用：在命令行运行 `bash ./scripts/conda_env.sh` 来设置 BioMiner 环境。
     - `scripts/conda_molscribe.sh`：用于完全开源版本的额外 Conda 环境创建脚本（Python 3.7，针对 MolScribe）。作用：解决包冲突，安装 MolScribe 依赖。使用：在命令行运行 `bash ./scripts/conda_molscribe.sh` 创建 BioMiner_MolScribe 环境。
     - `environment.yml`：Conda 环境配置文件（YAML 格式）。作用：定义依赖包列表，用于一键创建环境。使用：运行 `conda env create -f environment.yml` 安装最佳性能版本的环境。
     - `magic-pdf.json`：MinerU 工具的配置文件（JSON 格式）。作用：配置 PDF 解析参数，如布局识别和 OCR 设置。使用：复制到用户主目录（`mv magic-pdf.json ~`），然后在 MinerU 安装后用于 PDF 处理。

   - **模型下载和检查点文件**：
     - `download_models.py`：Python 脚本，用于下载 MinerU 模型检查点。作用：获取 GPU 版本的预训练模型，用于 PDF 解析加速。使用：在安装 MinerU 后运行 `python download_models.py`。
     - `BioMiner/MolScribe/ckpts/swin_base_char_aux_1m680k.pth`：MolScribe 模型检查点文件（完全开源版本）。作用：预训练权重，用于 OCSR（光学化学结构识别）。使用：下载到该路径后，在开源版本的脚本中加载进行结构提取。注意：仓库提供标准版和 Markush 增强版的下载选项。

   - **配置参数文件**：
     - `BioMiner/config/default.yaml`：最佳性能版本的默认配置文件（YAML 格式）。作用：设置 MLLM（如 Gemini-1.5-flash）的 API 密钥（`api_key`）、基 URL（`base_url`），以及其他参数如路径和阈值。使用：编辑后作为 `--config_path` 参数传入主脚本。
     - `BioMiner/config/default_open_source.yaml`：完全开源版本的配置文件（YAML 格式）。作用：类似 default.yaml，但调整为开源模型（如 MolDet 和 MolScribe）。使用：编辑后传入开源版本脚本。

   - **其他辅助文件**：
     - `LICENSE`：MIT 许可文件。作用：定义使用条款。使用：安装时参考，无需直接执行。

## 2. **系统启动（运行主脚本）**
   系统通过执行 Python 脚本“启动”，加载配置并初始化代理。启动命令如 `python3 example.py ...`，此时系统开始处理 PDF。

   - **主运行脚本文件**：
     - `example.py`：最佳性能版本的主脚本（Python 文件）。作用：处理单个 PDF 或目录，调用四个代理，输出提取结果。使用：命令如 `python3 example.py --config_path=BioMiner/config/default.yaml --pdf=example/pdfs/40_6s8a.pdf --external_full_md_res_dir=example/full_md_molminer --external_ocsr_res_dir=example/ocsr_molparser`。加载 `default.yaml`，读取 PDF 输入，并可选启用 BioVista 评估。
     - `example_open_source_one.py`：完全开源版本的第一部分脚本（Python 文件）。作用：处理预处理和部分提取（在 BioMiner 环境中）。使用：命令如 `python3 example_open_source_one.py --config_path=BioMiner/config/default_open_source.yaml --pdf=example/pdfs/40_6s8a.pdf`。加载 `default_open_source.yaml`，初始化开源模型。
     - `example_open_source_two.py`：完全开源版本的第二部分脚本（Python 文件）。作用：完成 OCSR 和后续提取（在 BioMiner_MolScribe 环境中）。使用：命令如 `python3 example_open_source_two.py --config_path=BioMiner/config/default_open_source.yaml --pdf=example/pdfs/40_6s8a.pdf`。依赖第一部分输出，加载 MolScribe 检查点。

   - **输入和外部结果文件（启动时读取）**：
     - `example/pdfs/40_6s8a.pdf`（以及目录下其他 PDF，如示例中的开放访问论文）：输入 PDF 文件。作用：作为 `--pdf` 参数的输入源。使用：脚本读取这些文件开始处理。
     - `example/full_md_molminer/`（目录）：MolMiner 分子检测的外部结果文件（JSON 或 Markdown 格式的文件，具体文件名为 PDF 对应的输出，如 40_6s8a.json）。作用：提供分子边界框和布局信息。使用：作为 `--external_full_md_res_dir` 参数传入最佳性能版本。
     - `example/ocsr_molparser/`（目录）：MolParser OCSR 的外部结果文件（SMILES 输出文件，如 40_6s8a_smiles.json）。作用：提供结构识别结果。使用：作为 `--external_ocsr_res_dir` 参数传入最佳性能版本。

   - **可视化文件（可选，启动时不直接使用，但可参考）**：
     - `visualization/framework_new.png`：BioMiner 框架概览图。
     - `visualization/benchmark_new.png`：BioVista 性能图。
     - `visualization/table_1.png`：MLLM 性能表格图。这些文件在 README 中引用，用于理解系统，但不直接在启动中加载。

## 3. **详细工作步骤（PDF 处理流程中使用的文件）**
   一旦启动，系统通过四个代理协作。每个步骤涉及特定脚本和输出文件（系统内部生成临时文件，如 JSON 输出，但仓库不存储它们）。

   - **步骤 1: 数据预处理代理**：
     - 使用文件：`magic-pdf.json`（配置 MinerU）、`download_models.py` 下载的检查点、`example/full_md_molminer/` 中的结果文件。脚本内部调用 MinerU 生成布局 JSON。
     - 相关脚本：`example.py` 或 `example_open_source_one.py` 中的预处理逻辑。开源版还涉及 `BioVista/component_inference/molecule_detection/moldetect_inference_batch.py`（分子检测批处理脚本，用于 MolDet）。

   - **步骤 2: 化学结构提取代理**：
     - 使用文件：`BioMiner/MolScribe/ckpts/swin_base_char_aux_1m680k.pth`（MolScribe 检查点）、`example/ocsr_molparser/` 中的结果文件。
     - 相关脚本：`BioVista/component_inference/ocsr/molscribe_inference_batch.py`（OCSR 批处理，用于 MolScribe）；`BioVista/component_inference/full_coreference/coreference_inference_batch_with_index_split_image_layout.py`（全结构共指识别批处理）；`BioVista/component_inference/markush_enumerate/markush_zip_inference_batch_with_index_layout.py`（Markush 枚举批处理）。这些在主脚本中被调用。

   - **步骤 3: 生物活性测量提取代理**：
     - 使用文件：`BioMiner/config/default.yaml` 中的 MLLM 设置（API 调用，无本地文件）。
     - 相关脚本：主脚本（如 `example.py`）中的提取逻辑，内部使用 RDKit（从环境安装）验证。

   - **步骤 4: 数据后处理代理**：
     - 使用文件：`BioVista/config/evaluate.yaml`（BioVista 评估配置，如果启用 `--biovista_evaluate`）；BioVista 数据集文件（下载到 `./BioVista/`，如 bioactivity_triplet_extraction.json 等，仓库不包含，但脚本引用）。
     - 相关脚本：`biovista_component_evaluate.py`（组件级评估脚本，用于运行 `python3 biovista_component_evaluate.py --config_path=BioVista/config/evaluate.yaml` 输出指标）。

## 附加说明
- **未直接使用的文件**：`README.md`（文档参考，不在运行中加载）；BioVista 数据集需外部下载 unzip 到 `./BioVista/`。
- **文件总数和更新**：仓库约 20+ 个核心文件，无新发布（No releases published）。如果 MolGlyph 已发布（原计划 2025.06-07），仓库可能添加新文件夹如 MolGlyph/，但当前未见更新。
- 这个列表覆盖了启动和工作中的所有关键文件。如果需要特定文件的代码内容或进一步工具调用，请提供更多细节！

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

