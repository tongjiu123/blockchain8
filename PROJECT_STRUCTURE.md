# 项目结构文档

**最后更新时间**: 2025-07-15

**项目状态**: 实验脚本 `simulation.py` 正在进行最终调试。实验1和2可成功运行，但实验3因“证书已存在”错误而失败，导致后续实验无法执行。正在定位并修复此问题。

本项目包含基于区块链的学术认证系统研究论文及其配套代码实现。论文使用IEEE标准格式（IEEEtran模板）编写，并通过本地模拟实验验证系统的性能与可行性。

## 目录结构

### 根目录

- `readme.md` - 项目指南与任务说明
- `PROJECT_STRUCTURE.md` - 本文件，描述项目结构

### 原始论文和获奖情况/

存放只读的原始资料：

- `Design of Academic Authentication System Based on Blockchain-Zongyou Yang.pdf` - 原始论文
- `CertificateOnChain.sol`: A baseline contract for comparison, storing all data on-chain.
  - `BaselineRevocation.sol`: 用于对比撤销机制性能的基线合约。
- `获奖证书.jpg` - 竞赛获奖证书

### paper improved/

论文工作区，包含改进后的论文文件：

- `iccip.tex` - 论文主稿件（IEEE tran模板）
- `reference.bib` - BibTeX参考文献库
- `figures/` - 图表目录
  - `README.md` - 图表说明文件

本项目包含两个核心部分：论文草稿 (`paper improved/`) 和实验代码 (`code_exp/`)。

## 根目录结构

```
./
├── paper improved/   # 存放论文的 LaTeX 或 Word 文档
├── code_exp/         # 存放所有实验相关的代码、脚本和数据
├── PROJECT_STRUCTURE.md  # 本文件，提供项目结构的顶层视图
└── readme.md         # 项目的顶层介绍和入口
```

## `code_exp` 目录详解

这是项目的核心，包含了所有用于复现论文实验的代码。**详细的运行指南请务必参考 `code_exp/README.md`**。

```
code_exp/
├── contracts/              # Solidity 智能合约
│   ├── Certificate.sol         # 核心合约 (混合存储模型)
│   ├── CertificateOnChain.sol  # 基线1: 完全链上存储合约，用于成本对比
│   └── BaselineRevocation.sol  # 基线2: 传统撤销机制合约，用于效率对比
├── scripts/                # Python 自动化脚本
│   ├── run_experiments_separately.py # ✅ **主执行脚本**: 自动化运行所有实验
│   ├── simulation.py         # 实验 1-5 的核心业务逻辑
│   ├── fault_tolerance_test.py # 实验 6 (节点容错) 的核心业务逻辑
│   ├── analyze_results.py    # 分析实验数据并生成图表
│   ├── generate_dataset.py   # 生成模拟证书数据集
│   └── node_manager.py       # (辅助) 管理多个Hardhat节点的工具
├── dataset/                # (生成) 存放模拟数据集
├── data/                   # (生成) 存放实验原始数据 (CSV)
├── analysis/               # (生成) 存放最终的分析报告和图表
├── log/                    # (生成) 存放实验运行日志
├── .env.example            # 环境变量示例文件
├── requirements.txt        # Python 依赖
├── package.json            # Node.js 依赖
├── CLEANUP.md              # (新增) 文件清理建议说明
└── README.md               # 核心说明文档，包含详细的实验流程
```

### 核心脚本工作流程

当前的实验流程已完全自动化，统一由 `run_experiments_separately.py` 脚本调度。

1.  **`scripts/run_experiments_separately.py`**: **这是唯一的实验执行入口**。它会自动完成以下所有步骤：
    *   按需生成数据集 (`generate_dataset.py`)。
    *   管理Hardhat节点的启动与关闭，为每个实验提供隔离环境。
    *   按顺序执行 `simulation.py` (实验1-5) 和 `fault_tolerance_test.py` (实验6)。
    *   最后调用 `analyze_results.py` 处理数据并生成图表。

### 关于代码清理

在 `code_exp` 目录下，我们提供了一个 `CLEANUP.md` 文件。该文件详细列出了项目中所有可被安全删除的旧脚本和冗余目录（例如 `scripts/run_all_experiments.py`），并解释了原因。您可以参考此文件来精简您的项目代码。

## 文件功能说明

*   **`readme.md` (顶层)**: 项目的入口点，提供一个高级别的概览，并引导用户到 `code_exp/README.md` 获取详细信息。
*   **`PROJECT_STRUCTURE.md`**: 您正在阅读的这个文件，它提供了文件和目录的静态视图，帮助快速理解代码的组织方式。
*   **`code_exp/README.md`**: 这是项目的**主文档**。它包含了所有您需要知道的关于如何设置环境、运行实验、理解代码和分析结果的详细信息。
*   **`code_exp/scripts/run_experiments_separately.py`**: 这是运行整个实验套件的**推荐方式**。它会自动处理Hardhat节点的启动与关闭，并按顺序执行所有实验。

## 工作流程

1.  **环境准备**: 参考 `code_exp/README.md` 中的指南，安装 Conda, Node.js, 和 Python 依赖，并配置好 `.env` 文件。
2.  **执行实验**: 运行 `python scripts/run_experiments_separately.py` 来启动完整的自动化实验流程。
3.  **查看结果**: 实验完成后，原始数据保存在 `data/` 目录，生成的图表和分析摘要保存在 `analysis/` 目录。
