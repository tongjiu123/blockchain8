
### **Agent指导方案 (V4.7 - 最终版)**

**Agent，你好。**

这是你本次任务的最终指导方案。核心任务是将学生竞赛论文**《Design of Academic Authentication System Based on Blockchain》**打磨成一篇具备冲击国际高水平**学术期刊（Journal）**或**顶级会议（Conference）**标准的论文。

> **重要更新**：本项目现已提供一套完整的本地模拟实验方案，包括详细的实验设计文档和可执行的仿真代码。你的任务将聚焦于**运行这套实验、分析结果，并将其整合进论文**，而非从零设计实验。**实验六：节点故障恢复测试 (Node Fault Recovery Test) 已经完成**。

### **0. 项目核心团队 (Core Project Team)**

- **杨宗祐 (Zongyou Yang)**: 伦敦大学学院 (UCL) 研究生。Zongyou Yang is currently pursuing the M.Sc. degree in Computer Graphics, Vision and Imaging at University College London (UCL). He received the B.Sc. (Eng.) degree with First Class Honours in telecommunications engineering with management from Queen Mary University of London, in a joint program with the Beijing University of Posts and Telecommunications (BUPT). His research interests include machine learning and deep learning, with particular focus on computer vision, human pose estimation, Large Language Model, behavior analysis for healthcare applications, and multimodal data fusion.
- **张洲赫 (Zhouhe Zhang)**: 北京邮电大学 (BUPT) 人工智能学院研究生。He received the B.Sc. (Eng.) degree with First Class Honours in telecommunications engineering with management from Queen Mary University of London, in a joint program with the Beijing University of Posts and Telecommunications (BUPT).
- **王子杰 (Zijie Wang)**: 王子杰 (Zijie Wang): 昆仑数智(CNPC) 算法工程师。He received the B.Sc. (Eng.) degree with Second Class Honours in telecommunications engineering with management from Queen Mary University of London, in a joint program with the Beijing University of Posts and Telecommunications (BUPT).His research interests include Deep Learning, Large Language Model, and Data Science.

### **1. 任务目标 (Task Goal)**

通过深度的技术创新、严谨的系统设计和全面的**本地模拟实验**，将现有的概念性论文提升为一篇符合**IEEE标准格式**（`IEEEtran`模板）的、具备高水平学术发表潜力的研究论文。

### **2. 具体改进路线 (Updated Improvement Route)**

> **重要起点 (Important Starting Point)**: 本项目已有初步的修改成果，存放于 `paper improved/iccip.tex` 和 `paper improved/reference.bib`。你的工作是**迭代和提升 (iterate and enhance)**，而非重写。

#### **目录与文件约定 (Directory & File Agreement)**

- `PROJECT_STRUCTURE.md`: 位于项目根目录，用于维护和说明整个项目的文件结构。
- `原始论文和获奖情况/`:# 基于区块链的学术凭证系统 - 项目文档

## 1. 项目简介 (Introduction)

本项目是论文 **《Design of a Secure Academic Authentication System Based on Blockchain and Decentralized Storage》** 的官方代码库。

我们提出并实现了一个基于区块链和混合存储的学术凭证系统，旨在解决传统学历认证流程中存在的效率低下、成本高昂和数据易被篡改等问题。系统利用区块链的不可篡改性和去中心化特性保证凭证的真实性，同时采用链下存储方案优化成本和性能。

## 2. 项目目标 (Objectives)

- **复现性**: 提供完整的、可运行的实验代码，以复现论文中的所有实验结果。
- **模块化**: 清晰地划分智能合约、实验脚本和数据分析等模块，便于理解和扩展。
- **自动化**: 提供一键式运行所有实验的自动化脚本，简化研究人员的复现工作。

## 3. 如何开始 (Getting Started)

1.  **理解项目结构**: 首先，请阅读 `PROJECT_STRUCTURE.md` 文件，它提供了对整个代码库目录和文件组织的高层概览。

2.  **运行实验**: 如果您希望运行实验并复现结果，请进入 `code_exp/` 目录，并仔细阅读其内部的 `README.md` 文件。该文件是**最核心、最详细的文档**，包含了完整的环境设置、依赖安装和自动化实验运行指南。

## 4. 核心目录快速导航

- `paper improved/`: 包含论文的 LaTeX 源文件和相关图表。
- `code_exp/`: 包含所有实验的源代码、脚本、数据和详细文档。**这是项目的核心技术部分**。
- `PROJECT_STRUCTURE.md`: 项目的结构地图。

---
*如果您在复现过程中遇到任何问题，请优先查阅 `code_exp/README.md` 中的详细说明。*
  - `result/`:存放实验结果，存放经过分析处理后的结果和图表
  - `log/`:存放模拟运行时产生的日志文件。

#### **Step 1 – 引言、相关工作**

- **任务**: 继续执行原定计划，在`iccip.tex`的现有基础上，深化引言、相关工作和系统设计部分。
- **文献检索**: 检索2022-2025年间，关于区块链证书、去中心化身份（DID）、可验证凭证（VCs）的**英文或中文高影响力期刊和会议论文至少15篇**。
- **文献归档 (重要)**: 所有检索到的文献PDF都应下载并保存到 `references/` 文件夹中，并以“第一作者-年份-标题关键词”的格式命名（例如 `Buterin-2014-Ethereum.pdf`），便于管理和溯源。
- **深度分类综述**: 按技术路线（如：公链 vs. 联盟链）、隐私保护方案（如：ZKP vs. TEE）、数据模型（如：Blockcerts vs. W3C VC）等对现有工作进行分类比较，并系统性地分析其优缺点。
- **确立研究缺口 (Research Gap)**: 在综述的结尾，必须明确指出当前研究中存在的**一个或多个显著的研究空白**。
- **声明核心贡献 (Contributions)**: 基于上述缺口，清晰地列出本文的3-4条核心贡献。

**Step 2 系统设计**

- **形式化系统模型 (Formal System Model)**: 在详细设计前，首先定义系统的形式化模型。这包括：**参与方集合**（学生、机构、验证者）、**核心安全与隐私假设**、以及**系统设计目标**（如：正确性、防篡改性、隐私保护性）。这为后续的设计和分析提供了坚实的理论基础。
- **智能合约设计与实现**:
  - **技术选型**: 明确技术栈。推荐**Hyperledger Fabric**或**支持PoA共识的以太坊兼容链**。详细论述选择该技术栈的理由。
  - **给出实现**: 在论文中，提供关键数据结构和函数接口的**伪代码或经过简化的代码片段**。
  - **论述设计权衡 (Design Trade-offs)**: 必须详细论述设计中的权衡。例如，为什么某些功能在链上实现（保证可信），而另一些则在链下（保证效率和隐私）？
- **数据与存储方案**:
  - 详细说明“**链上存哈希/CID，链下存原文**”的方案，明确指出原文存储于**IPFS**网络。
  - （可选创新点）简要阐述“擦除码冗余算法”如何与IPFS结合，以增强数据的长期可用性和抗审查性。
- **更新图表**: 绘制全新的、更专业的**系统架构图**和**核心流程时序图**。



#### **Step 3 (核心调整) – 执行本地模拟实验与深度评估**

此步骤是论文质量提升的关键，必须严格、细致地执行。

**审阅实验方案**: 仔细阅读本文档后附的**《实验设计与执行方案》**，理解实验的目标、指标和流程。必须在 iccip这个 conda 虚拟环境里运行。实验运行的时候需要有进度条。

##### **1. 核心目标 (Core Objective)**

此步骤是论文质量提升的关键，必须严格、细致地执行，旨在通过可复现的本地模拟实验，定量评估系统的性能、成本、可扩展性，并为论文的`Evaluation`章节提供强有力的数据支撑和深度分析。

##### **2. 实验准备：数据集与环境 (Preparation: Dataset & Environment)**

1. **生成真实感数据集 (Generate Realistic Dataset)**:
   - **脚本**: 在 `code_exp/scripts/` 中创建一个名为 `generate_dataset.py` 的脚本。
   - **工具**: 使用 `Faker` 库来生成模拟数据。
   - **规模**: 生成一个包含 **100,000** 条记录的 `certificates_data.csv` 文件，并存放在 `code_exp/dataset/` 目录。
   - **字段**: 每条记录应包含 `student_name`, `degree_type`, `institution_name` 等字段，以模拟真实的证书信息。
2. **配置环境 (Configure Environment)**:
   - **位置**: 进入 `code_exp/` 目录，参考 `README.md` 文件。
   - **要求**: **必须在名为 `iccip` 的 Conda 虚拟环境中运行所有脚本**。确保已安装所有必要的Python和Node.js依赖。

##### **3. 实验设计与执行 (Experiment Design & Execution)**

**运行主仿真脚本**: 执行 `code_exp/scripts/simulation.py`。该脚本将按顺序执行以下所有实验，并将详细日志输出到 `log/simulation_run_{timestamp}.log`。

##### **实验一：基础性能评估 (Baseline Performance)**


- **目标**: 测量核心操作在无负载下的性能基线，并量化其链上成本。
- **假设**: 交易延迟主要由区块确认时间决定；Gas成本是固定的。
- **方法**:
  1. **延迟 (Latency)**: 顺序签发**1,000**份证书，使用`Certificate.sol`合约。精确记录每笔`issueCertificate`交易从发送到被打包确认的端到端时间。
  2. **成本 (Cost)**: 单独执行一次`issueCertificate`和`revokeCertificate`操作，精确记录其Gas消耗。
- **分析与可视化目标**:
  - 计算延迟的**平均值、中位数、标准差和99百分位**，并绘制**交易延迟分布图（小提琴图加散点图）**以展示数据的完整分布。
  - 将Gas成本与当前的ETH市价结合，估算出操作的**实际美元成本**，并制成表格。


##### **实验二：系统吞吐量测试 (Throughput Test)**

- **目标**: 评估系统在不同并发负载下的处理能力上限，并观察其在极端压力下的稳定性。
- **假设**: 随着并发用户数的增加，系统的TPS会先上升，然后达到饱和点后趋于平稳或因资源竞争而略有下降。
- **方法**:
  1. 设置一个固定的测试时长（例如 **60** 秒）。
  2. 模拟不同数量的并发机构（**例如 1, 10, 50, 100,150，200个**）使用`asyncio`等库同时持续发起`issueCertificate`交易。
  3. 统计在测试时长内被成功打包的总交易数，计算并记录每个并发水平下的实际TPS。
- **分析与可视化目标**:
  - 绘制**并发数 vs. TPS曲线图**。
  - 在论文中分析性能拐点出现的原因（如本地CPU瓶颈、网络I/O限制、节点交易池处理能力等），并讨论在超高并发下（如1000个并发）系统是否出现交易失败率显著增加等不稳定现象。


##### **实验三：系统可扩展性测试 (Scalability Test)**

- **目标**: 评估随着链上数据状态增长至百万级别，系统的关键操作性能是否保持稳定。
- **假设**: 由于我们采用了映射（mapping）数据结构，查询操作的性能应接近**O(1)**，不受证书总量的影响。
- **方法**:
  1. 分阶段向`Certificate.sol`合约中填充证书数据，使其状态达到不同的总量级（**1,000, 5,000, 10,000, 50,000, 100,000条， 500,000条**）。
  2. 在每个数据量级下，随机执行 **500** 次`verifyCertificate`（链上视图函数调用），并记录其平均查询时间。
- **分析与可视化目标**:
  - 绘制**证书总量 vs. 平均查询时间曲线图**（X轴使用对数坐标以更好地展示大规模数据）。
  - **产出**: `data/scalability_data.csv`，包含证书总量和对应的平均查询时间。
  - 通过分析曲线的平坦程度，来有力地验证我们系统设计的查询性能是否具有卓越的可扩展性，能够支撑真实世界的长期运行。
  
##### **实验四：存储成本对比分析 (Storage Cost Comparative Analysis)**

- **目标**: 通过与一个简化的基线模型对比，定量地证明本系统“链上哈希，链下存储”设计的巨大经济优势。
- **假设**: 本系统（混合存储）在存储成本上将远低于完全链上存储的基线模型，并且差距随数据复杂度增加而拉大。
- **方法**:
  1. 部署`CertificateOnChain.sol`合约，该合约将证书的所有信息（如`student_name`, `degree_type`）直接存储在链上。
  2. 对该合约执行与**实验一**中相同的**成本 (Cost)**测试，即记录签发一笔包含相同数据量的证书所需的Gas。
- **分析与可视化目标**:
  - 制作一个清晰的**对比表格**，展示本系统与基线系统在`issueCertificate`操作上的**Gas成本差异**（应有数倍甚至数十倍的差距）。
  - 在论文中分析并强调这种设计选择在保证数据完整性的同时，极大地降低了运行成本，是系统得以在现实中大规模部署的关键。

##### **实验五：撤销机制效率与可扩展性评估 (新增)**

- **核心创新点**: 本项目设计的核心创新之一是高效且保护隐私的凭证撤销机制（例如，使用密码学累加器）。此实验旨在量化其优势。
- **目标**:
  1. 定量证明我们提出的撤销机制在性能和成本上优于传统的链上撤销列表（On-chain Revocation List）。
  2. 评估该机制在撤销列表不断增长时的性能表现，验证其可扩展性。
- **方法**:
  1. **创建基线**: 在`contracts/`中创建一个简单的`BaselineRevocation.sol`合约，使用`mapping(bytes32 => bool)`记录撤销状态。
  2. **测量添加成本**: 分别测量在我们的主合约和基线合约中，“添加一个凭证到撤销集”的Gas成本。
  3. **测量验证成本与扩展性**: 分阶段向两个合约的撤销集中添加凭证（规模从1k到100k）。在每个量级下，测量“验证一个凭证未被撤销”的成本/时间。对于我们的方案，这对应于生成和验证“非成员关系证明”；对于基线方案，这对应于一次简单的映射读取。
- **分析与可视化目标**:
  - 绘制“**撤销集大小 vs. 验证成本/时间**”的曲线图，直观对比两种机制的扩展性。
  - **预期成果**: 证明我们的方案在验证成本上具有O(1)或O(log n)的卓越性能，不受撤销列表规模影响，而基线方案成本则会线性增长。这个实验结果将为论文的核心贡献提供最硬核的数据支撑。


##### **实验六：节点故障恢复测试 (Node Fault Recovery Test)**

- **核心目标**: 验证系统在分布式环境中的容错能力和故障恢复机制。
- **创新点**: 模拟真实区块链网络中的节点故障场景，评估系统的可用性和数据一致性保障。
- **方法**:
  1. **多节点环境搭建**: 启动4个Hardhat节点模拟分布式网络，每个节点运行在不同端口。
  2. **故障注入**: 随机关闭1-3个节点，模拟网络分区或硬件故障。
  3. **恢复测试**: 测量节点重新上线后的数据同步时间和一致性。
  4. **可用性测量**: 计算系统在故障期间的可用性百分比和交易成功率。

- **测试场景**:
  - **正常运行** (4/4节点): 建立基线性能指标。
  - **单节点故障** (3/4节点): 模拟常见的单点故障场景。
  - **双节点故障** (2/4节点): 模拟严重故障场景。
  - **极端故障** (1/4节点): 测试系统在最小可运行配置下的表现。

- **分析与可视化目标**:
  - 绘制"**系统可用性 vs. 故障节点数**"的关系图。
  - 绘制"**故障恢复时间 vs. 故障持续时间**"的分析图。
  - **预期成果**: 证明系统在不同故障场景下仍能保持一定程度的可用性，并在节点恢复后能快速同步数据，保证系统的整体可靠性。


#### **实验运行状态 (Experiment Status)**

| 实验编号 | 实验名称 | 状态 | 问题/备注 |
|---------|---------|------|--------|
| 实验一 | 基础性能评估 | ❌ 尝试运行但失败 | 需要修复临时脚本中的参数传递问题 |
| 实验二 | 吞吐量分析 | ❌ 尝试运行但失败 | 需要修复临时脚本中的参数传递问题 |
| 实验三 | 可扩展性分析 | ❌ 尝试运行但失败 | 需要修复临时脚本中的参数传递问题 |
| 实验四 | 存储成本对比分析 | ❌ 尝试运行但失败 | 需要修复临时脚本中的参数传递问题 |
| 实验五 | 撤销机制效率分析 | ❌ 尝试运行但失败 | 代码实现不完整，需要完成函数实现 |
| 实验六 | 节点故障恢复测试 | ✅ 已完成 | 成功生成数据和分析结果 |

#### **下一步计划 (Next Steps)**

1. **修复实验1-4的脚本问题**：
   - 更新`run_experiments_separately.py`中的临时脚本生成逻辑，确保正确传递所有必要参数
   - 解决路径和参数传递问题

2. **完成实验5的代码实现**：
   - 完成`run_experiment_5_revocation()`函数的实现
   - 创建必要的`BaselineRevocation.sol`合约进行对比测试

3. **重新运行所有实验**：
   - 确保所有实验都能成功运行并生成数据
   - 验证数据完整性和一致性

4. **整合分析结果**：
   - 更新分析脚本以处理所有实验数据
   - 生成完整的图表和报告

##### **4. 结果分析与可视化 (Result Analysis & Visualization)**

1. **编写分析脚本**: 在 `code_exp/scripts/` 中创建一个名为 `analyze_results.py` 的脚本。
2. **数据处理与统计**: 该脚本读取 `data/` 目录下的所有 `.csv` 文件，并进行统计分析（计算平均值、中位数、标准差等）。
3. **图表生成**:
   - 使用 `matplotlib` 和 `seaborn` 绘制高质量图表：
     - **图1：交易延迟分布图** (箱形图或小提琴图)。
     - **图2：系统吞吐量曲线图** (并发数 vs. TPS)。
     - **图3：查询性能扩展图** (证书总量 vs. 平均查询时间)。
   - 所有生成的图表（`.png`, `.pdf`格式）保存到 `paper improved/figures/` 目录。
4. **结果归档**: 将所有关键统计数据（如上述平均值、峰值TPS等）和生成的图表也复制一份到 `code_exp/result/` 目录，以便查阅和备份。

##### **5. 撰写评估章节 (Writing the Evaluation Section)**

- **实验设置**: 在论文的 `Evaluation` 章节中，首先详细描述实验设置（硬件、软件、数据集、关键性能指标KPMs）。
- **结果呈现与分析**:
  - 依次插入生成的图表，并对每个实验结果进行详细的解读。例如，分析延迟分布的原因，解释吞吐量曲线达到瓶颈的可能因素（如CPU、网络、区块Gas限制），并讨论查询性能是否满足实际应用需求。
  - 将Gas成本与当前以太坊主网的ETH价格结合，估算出操作的实际美元成本，使其更具说服力。
- **对比分析 (Comparative Analysis)**:
  - 选择1-2个来自“相关工作”章节的代表性系统作为基线。
  - 从业界公认的关键指标（如去中心化程度、隐私保护级别、可扩展性、交易成本）上，制作一个对比表格，清晰地展示本系统与基线系统的优劣。
- **安全与隐私分析 (Security and Privacy Analysis)**:
  - 构建一个**形式化的威胁模型** (如STRIDE)，并从理论上证明所提出应对策略的有效性。



#### **Step 4 – 完善结论与未来工作**

1. **总结贡献**: 在结论部分，再次清晰地总结本文在理论、设计和实现上的核心贡献。
2. **指出局限性**: 诚实地分析当前设计的局限性。
3. **展望未来**: 提出有价值的未来研究方向。

#### **Step 5 – 格式、润色与提交**

1. **格式规范**: 全文严格遵循`iccip.tex`中的**IEEE `tran`模板**。并且符合 latex 格式。
2. **文献管理**: 确保`reference.bib`中**总引用数不少于25条**，其中**近三年（2023-2025）的高质量文献占比超过60%**。
3. **语言润色**: 使用专业工具（如Grammarly Pro）对全文进行深度校对和润色。
4. **预印本提交**: 完成所有修改后，生成符合`arXiv`上传要求的压缩包，并提交到**cs.CR (Cryptography and Security)**或**cs.DC (Distributed, Parallel, and Cluster Computing)**分区。

### **3. Agent 任务清单 (Updated Checklist)**

| 优先级   | 任务                                                         | 负责人 | 目标文件/目录                 | 状态 |
| -------- | ------------------------------------------------------------ | ------ | ----------------------------- | ---- |
| 🔴 **P0** | **审阅与规划**: 审阅所有项目文件，特别是新增的实验方案和代码 | Agent  | `/` (整个项目)                | ☐    |
| 🔴 **P0** | **文献综述与归档**: 完成Step 1                               | Agent  | `paper improved/`             | ☐    |
| 🟠 **P1** | **核心设计与理论建模**: 完成Step 2                           | Agent  | `paper improved/`, `code_exp` | ☐    |
| 🟠 **P1** | **运行本地仿真**: 完成Step 3.2，运行脚本生成`.csv`数据       | Agent  | `code_exp/`                   | ☐    |
| 🟡 **P2** | **撰写评估与分析章节**: 完成Step 3.3 & 3.4，撰写Evaluation章节并绘图 | Agent  | `paper improved/`             | ☐    |
| 🟢 **P3** | **完成与终稿**: 完成Step 4 & 5，全文校对、润色并准备arXiv提交包 | Agent  | 最终压缩包                    | ☐    |