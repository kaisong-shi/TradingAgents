<p align="center">
  <img src="tradingagents/assets/tauric-logo.svg" width="60%" alt="Tauric Research">
</p>

# TradingAgents：多智能体 LLM 金融交易框架

> 📖 英文版：[README.md](README.md)

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<br>
<div align="center">
  <a href="https://github.com/TauricResearch" target="_blank"><img alt="TradingAgents #1 Repository of the Day" src="https://trendshift.io/api/badge/repositories/16192" width="250" height="55"/></a>
</div>

## 最新：[Trading-R1](https://github.com/TauricResearch/Trading-R1) 现已开放早期访问

在社区的大量请求之下，Trading-R1 已正式发布！

<p align="center">
  <a href="https://github.com/TauricResearch/Trading-R1" target="_blank"><img src="https://raw.githubusercontent.com/TauricResearch/Trading-R1/main/assets/trading-r1.gif" alt="Trading-R1 在终端中回答研究问题" width="100%"></a>
</p>

<h3 align="center"><a href="https://github.com/TauricResearch/Trading-R1" target="_blank">注册早期访问 ↗</a></h3>

## 新闻

<!-- news:start -->
- [2026-11] **Trading-R1 v0.1.0** 发布，[早期访问](https://github.com/TauricResearch/Trading-R1) 已开放。
- [2026-10] **TradingAgents v0.7.1** 发布：决策仅按最终收盘价评分，并可跨长时间市场休市完成结算；修复了模型日期未补零时可能读取运行日期之后提交文件的问题；修复了投资组合、价格、SEC 报表和报告相关问题。
- [2026-10] **TradingAgents v0.7.0** 发布：支持使用你自己的 ChatGPT Plus 或 Pro 套餐运行；回测从每次决策后的首个收盘价开始评分；启动时提示有新版本；每个 GitHub Release 附带 wheel 包。

<details>
<summary>更早的新闻</summary>

- [2026-10] **TradingAgents v0.6.0** 发布：报告保存为单个 HTML 页面；可按模型层级分别配置提供商，使管理层和分析师运行在不同模型上；分析期间为所有股票代码结算历史决策；在 Yahoo 新闻源不可用期间，从 Yahoo 搜索读取公司新闻。
- [2026-09] **TradingAgents v0.5.2** 发布：并行运行分析师以加快分析；CLI 可通过 `--ticker`、`--date` 等参数无提示运行；每次报告都记录本次运行的设置；回测只能看到各分析日期之前已发布的数据。
- [2026-09] **TradingAgents v0.5.1** 发布：包结构按模块内容重新组织（导入路径变更）；可选的 Jev 社交媒体帖子筛查；默认模型为 GPT-6 Sol 和 Luna；修复了运行隔离和 SEC EDGAR 报表问题。
- [2026-09] **TradingAgents v0.5.0** 发布：所有带日期的数据路径均具备时点完整性；SEC EDGAR 基本面数据按申报原文提供；支持在股票代码与日期网格上回测；支持感知投资组合的运行；各提供商均采用当前模型阵容。
- [2026-08] **TradingAgents v0.4.0** 发布：修复 FRED 宏观数据、社交情绪和决策日志记忆中的前视/时点问题；更清晰的决策信号；可用的 CLI 检查点恢复；Trader 价格锚定；新增 GPT-5.6 和 GLM-5.3 模型。
- [2026-07] **TradingAgents v0.3.1** 发布，修复正确性与稳定性问题：Alpha Vantage 前视过滤、图路由崩溃安全、感知图结构的检查点恢复、可用的加密情绪来源、可配置的 LLM 重试预算、Bedrock API Key 认证，以及 Claude Sonnet 5 / Fable 5 支持。
- [2026-06] **TradingAgents v0.3.0** 发布：经过验证的数据访问契约、扩展的提供商注册表（NVIDIA、Kimi、Groq、Mistral、Bedrock 以及任意 OpenAI 兼容端点）、FRED 和 Polymarket 数据供应商、当代模型目录，以及 CI 门禁。
- [2026-05] **TradingAgents v0.2.5** 发布：有数据支撑的情绪分析师、GPT-5.5 等模型覆盖、Qwen/GLM/MiniMax 双区域支持、支持 `TRADINGAGENTS_*` 环境变量配置及 API Key 自动检测、远程 Ollama 支持、非美国 alpha 基准，以及股票代码路径穿越加固。
- [2026-04] **TradingAgents v0.2.4** 发布：结构化输出智能体（研究经理、Trader、投资组合经理）、LangGraph 检查点恢复、持久化决策日志、DeepSeek/Qwen/GLM/Azure 提供商支持、Docker 支持，以及 Windows UTF-8 编码修复。
- [2026-03] **TradingAgents v0.2.3** 发布：多语言支持、GPT-5.4 系列模型、统一模型目录、回测日期保真，以及代理支持。
- [2026-03] **TradingAgents v0.2.2** 发布：GPT-5.4/Gemini 3.1/Claude 4.6 模型覆盖、五档评级量表、OpenAI Responses API、Anthropic effort 控制，以及跨平台稳定性。
- [2026-02] **TradingAgents v0.2.0** 发布：多提供商 LLM 支持（GPT-5.x、Gemini 3.x、Claude 4.x、Grok 4.x）以及改进的系统架构。
- [2026-01] **Trading-R1** [技术报告](https://arxiv.org/abs/2509.11420) 发布，[Terminal](https://github.com/TauricResearch/Trading-R1) 预计很快推出。

</details>
<!-- news:end -->

<div align="center">

🚀 [TradingAgents](#tradingagents-framework) | ⚡ [安装与 CLI](#installation-and-cli) | 🎬 [演示](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [包用法](#tradingagents-package) | 🤝 [贡献](#contributing) | 📄 [引用](#citation)

</div>

> 🎉 **TradingAgents** 正式发布！我们收到了大量关于这项工作的咨询，衷心感谢社区的热情。
>
> 因此我们决定将框架完全开源。期待与你一起构建有影响力的项目！

<a id="tradingagents-framework"></a>
## TradingAgents 框架

TradingAgents 是一个多智能体交易框架，模拟真实交易公司的运作方式。通过部署由 LLM 驱动的专业智能体——从基本面分析师、情绪专家、技术分析师，到交易员和风险管理团队——平台协同评估市场状况并为交易决策提供依据。此外，这些智能体会进行动态讨论，以找出最优策略。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents 框架仅供研究用途。交易表现可能因多种因素而异，包括所选的主干语言模型、模型温度、交易时段、数据质量以及其他非确定性因素。[本框架不构成财务、投资或交易建议。](https://tauric.ai/disclaimer/)

我们的框架将复杂的交易任务分解为多个专业角色。

### 分析师团队
- 基本面分析师：评估公司财务和绩效指标，识别内在价值和潜在风险信号。
- 情绪分析师：汇总新闻标题、StockTwits 和 Reddit 讨论，形成统一的情绪判断，以衡量短期市场情绪。
- 新闻分析师：监测全球新闻和宏观经济指标，解读事件对市场状况的影响。
- 技术分析师：利用技术指标（如 MACD 和 RSI）识别交易模式并预测价格走势。

所选分析师同时工作，各自使用自己的工具；当所有报告齐备后，研究辩论随即开始。

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### 研究员团队
- 由看多和看空研究员组成，他们批判性地评估分析师团队提供的见解。通过结构化辩论，他们在潜在收益与内在风险之间取得平衡。

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 交易员智能体
- 综合分析师和研究员的报告，做出明智的交易决策，确定交易时机和规模。

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 风险管理和投资组合经理
- 通过评估市场波动性、流动性及其他风险因素，持续评估投资组合风险。风险管理团队评估并调整交易策略，向投资组合经理提供评估报告以做最终决策。
- 投资组合经理批准/拒绝交易提案。若获批准，订单将发送至模拟交易所并执行。

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

<a id="installation-and-cli"></a>
## 安装与 CLI

### 安装

克隆 TradingAgents：
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

TradingAgents 需要 Python 3.11 或更高版本。在你喜欢的环境管理器中创建虚拟环境：
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

或使用 [uv](https://docs.astral.sh/uv/)：
```bash
uv venv --python 3.13
source .venv/bin/activate
```

安装包及其依赖（使用 uv 时为 `uv pip install .`）：
```bash
pip install .
```

### Docker

或者使用 Docker 运行：
```bash
cp .env.example .env  # 添加你的 API Key
docker compose run --rm tradingagents
```

更新仓库后，使用 `docker compose build` 重新构建镜像。

结果、报告、记忆日志和缓存保存在 `tradingagents_data` 卷中。若要将它们保存在宿主机文件夹中，请创建该文件夹并将 `TRADINGAGENTS_DATA_DIR` 指向它，可在 `.env` 或 shell 中设置：`mkdir -p data && TRADINGAGENTS_DATA_DIR=./data docker compose run --rm tradingagents`。

使用 Ollama 运行本地模型：
```bash
docker compose --profile ollama run --rm tradingagents-ollama
```

### 必需的 API

TradingAgents 支持多个 LLM 提供商。请为你选择的提供商设置 API Key：

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export DEEPSEEK_API_KEY=...        # DeepSeek
export DASHSCOPE_API_KEY=...       # Qwen（国际站，dashscope-intl.aliyuncs.com）
export DASHSCOPE_CN_API_KEY=...    # Qwen（中国站，dashscope.aliyuncs.com）
export ZHIPU_API_KEY=...           # GLM via Z.AI（国际站）
export ZHIPU_CN_API_KEY=...        # GLM via BigModel（中国站，open.bigmodel.cn）
export MINIMAX_API_KEY=...         # MiniMax（全球，api.minimax.io）
export MINIMAX_CN_API_KEY=...      # MiniMax（中国，api.minimaxi.com）
export OPENROUTER_API_KEY=...      # OpenRouter
export MISTRAL_API_KEY=...         # Mistral
export MOONSHOT_API_KEY=...        # Kimi (Moonshot)
export GROQ_API_KEY=...            # Groq
export NVIDIA_API_KEY=...          # NVIDIA NIM
export FRED_API_KEY=...            # FRED 宏观数据（免费，可选）
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage
export TYPESAFE_API_KEY=...        # Jev 社交帖子筛查（可选）
```

对于 Azure OpenAI，请将 `.env.enterprise.example` 复制为 `.env.enterprise` 并填写你的凭据。使用 Docker 时，请将这些 Key 放入 `.env`：镜像不包含 `.env` 文件。

若要使用你的 ChatGPT Plus 或 Pro 套餐而不是 API Key 运行，请在 CLI 的提供商菜单中选择“Subscription”，或设置 `llm_provider: "chatgpt"`。使用 `tradingagents login chatgpt` 登录一次：它会打印一个需要在浏览器中打开的地址，该地址会回到本机的 `127.0.0.1`。如果浏览器运行在另一台机器上，或 TradingAgents 运行在 Docker 中（`docker compose run --rm tradingagents login chatgpt`），请粘贴浏览器最终到达的地址。登录信息保存在 `~/.tradingagents/chatgpt-auth.json`，`tradingagents logout chatgpt` 会撤销它。运行会计入你套餐的使用限制，且套餐不接受 `temperature` 或 `max_tokens`。

对于 AWS Bedrock，使用 `pip install ".[bedrock]"` 安装额外依赖，设置 `llm_provider: "bedrock"`，配置 AWS 凭据（环境变量、`~/.aws/credentials` 或 IAM 角色）以及 `AWS_DEFAULT_REGION`，并使用 Bedrock 模型 ID，例如 `us.anthropic.claude-opus-5-5`。

对于本地模型，使用 `llm_provider: "ollama"` 配置 Ollama。默认端点为 `http://localhost:11434/v1`；设置 `OLLAMA_BASE_URL` 可指向远程 `ollama-serve`。使用 `ollama pull <name>` 拉取模型，对于默认未列出的模型，在 CLI 中选择“Custom model ID”。

对于任何其他 OpenAI 兼容服务器（vLLM、LM Studio、llama.cpp 或自定义中继），使用 `llm_provider: "openai_compatible"` 并通过 `backend_url`（或 `TRADINGAGENTS_LLM_BACKEND_URL`）设置端点，例如 vLLM 使用 `http://localhost:8000/v1`，LM Studio 使用 `http://localhost:1234/v1`。模型由你的服务器提供。本地服务器无需 Key；当端点需要时设置 `OPENAI_COMPATIBLE_API_KEY`。

设置 `TYPESAFE_API_KEY` 后，情绪分析师在读取 StockTwits 和 Reddit 帖子之前会先用 TypeSafe 的 Jev 进行筛查。与公司无关的帖子会被丢弃，每个来源开头会给出剩余帖子按立场（看多、看空、中性或不明）的计数。没有 Key 时，帖子未经筛查直接通过。`jev-latest` 会随新版本更新；将 `TYPESAFE_DEFAULT_MODEL` 设为带版本号的 ID（如 `jev-1.13.0`）即可在多次运行间固定版本。若要通过 OpenRouter 访问 Jev，请将 OpenRouter Key 放入 `TYPESAFE_API_KEY` 并设置 `TYPESAFE_BASE_URL=https://openrouter.ai/api`。

或者，将 `.env.example` 复制为 `.env` 并填入你的 Key：
```bash
cp .env.example .env
```

### CLI 用法

启动交互式 CLI：
```bash
tradingagents          # 已安装的命令
python -m cli.main     # 备选：直接从源码运行
```
你将看到一个界面，可选择所需的股票代码、分析日期、LLM 提供商、研究深度等。上次运行的答案会作为默认值返回，因此按 Enter 即可接受。`.env` 中的 `TRADINGAGENTS_*` 变量仍会完全跳过对应的步骤。

若要在计划任务或脚本中无提问运行，可用参数回答每次运行的问题，其余用 `TRADINGAGENTS_*` 变量：
```bash
export TRADINGAGENTS_LLM_PROVIDER=openai TRADINGAGENTS_QUICK_THINK_LLM=gpt-6-luna TRADINGAGENTS_DEEP_THINK_LLM=gpt-6-sol
export TRADINGAGENTS_OUTPUT_LANGUAGE=English TRADINGAGENTS_MAX_DEBATE_ROUNDS=1 TRADINGAGENTS_MAX_RISK_ROUNDS=1
tradingagents --ticker NVDA --date 2026-09-23 --analysts market,news,fundamentals --save --no-show
```
每个参数只跳过它对应的问题。在没有终端的情况下运行，缺少答案会在运行开始前中止，并指出需要设置的参数或变量。

启动时，交互式 CLI 会提示新版本以及来自 Tauric Research 的通知。它每天最多在后台检查一次，不会发送任何关于你运行的信息；设置 `TRADINGAGENTS_NO_UPDATE_CHECK=1` 可关闭。没有终端的运行永远不会检查。

保存的报告还包含 `complete_report.html`，即把报告作为单个页面，并在文本旁列出各章节，便于在浏览器、手机或打印时阅读。在提示中回答保存问题后，还会询问是否生成该页面并可在浏览器中打开；`--no-html` 会跳过，Python 中的 `ta.save_reports(state, "NVDA", html=False)` 也会跳过。

### 市场与股票代码

TradingAgents 适用于 Yahoo Finance 覆盖的任何市场，使用带交易所后缀的股票代码。公司身份和 alpha 基准会按市场自动解析。

- 美国：`AAPL`、`SPY`
- 香港：`0700.HK` · 东京：`7203.T` · 伦敦：`AZN.L`
- 印度：`RELIANCE.NS`、`.BO` · 加拿大：`.TO` · 澳大利亚：`.AX`
- 中国 A 股：上海 `.SS`、深圳 `.SZ`（例如贵州茅台 `600519.SS`）
- 加密货币：`BTC-USD`、`ETH-USD`

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

界面会在结果加载时显示它们，让你跟踪智能体的运行进度。

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<a id="tradingagents-package"></a>
## TradingAgents 包

### 实现细节

我们使用 LangGraph 构建 TradingAgents，以确保灵活性和模块化。框架支持多个 LLM 提供商：OpenAI、Google、Anthropic、xAI、DeepSeek、Qwen（阿里 DashScope，国际和中国端点）、GLM（智谱）、MiniMax（全球 + 中国）、OpenRouter、用于本地模型的 Ollama、面向企业的 Azure OpenAI，以及你自己的 ChatGPT 套餐。

### Python 用法

要在代码中使用 TradingAgents，可以导入 `tradingagents` 模块并初始化 `TradingAgentsGraph()` 对象。`.propagate()` 函数将返回一个决策。你可以运行 `main.py`，下面是一个快速示例：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 前向传播
state, decision = ta.propagate("NVDA", "2026-09-01")
print(decision)

# 与 CLI 保存相同的报告树，位于 results_dir/reports 下
ta.save_reports(state, "NVDA")
```

你也可以调整默认配置，设置自己选择的 LLM、辩论轮数等。

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # 例如 openai、google、anthropic、deepseek、groq、ollama；openai_compatible 覆盖任何 OpenAI 兼容端点（vLLM、LM Studio、llama.cpp 等）
config["deep_think_llm"] = "gpt-6-sol"    # 用于复杂推理的模型
config["quick_think_llm"] = "gpt-6-luna"   # 用于快速任务的模型
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-09-01")
print(decision)
```

快速模型服务于分析师、研究员、辩论者和交易员；深度模型服务于研究经理和投资组合经理。每个模型可以运行在各自的提供商上，例如管理层使用 Claude，其余使用 OpenAI：

```python
config["deep_think_provider"] = "anthropic"
config["deep_think_llm"] = "claude-opus-5-5"
```

某个层级使用自己的提供商时，会使用该提供商的 Key 和默认端点；为本地或中继端点设置 `quick_think_backend_url` 或 `deep_think_backend_url`。`TRADINGAGENTS_DEEP_THINK_PROVIDER` 和 `TRADINGAGENTS_QUICK_THINK_PROVIDER` 变量可为 CLI 设置它们，并配合该层级的模型变量。

所有配置选项见 `tradingagents/default_config.py`。

### 按申报原文提供的基本面数据

美国公司报表来自 SEC EDGAR，它记录了每个数字的申报日期。以过去日期运行的分析会读取该日报表的原貌：一个已结束但尚未申报的财年不会被提供，后来重述的数字仍按首次报告读取。苹果 2008 年的总资产申报为 396 亿美元，并在 2010 年重述为 362 亿美元，因此在这两个日期之间运行会读到 396 亿美元。EDGAR 无需账户或 API Key。

其他公司的报表来自 Yahoo Finance，它按报表覆盖的期间而非发布时间来确定日期。以今天日期运行会读取它们；以过去日期运行则会被告知这些数据被保留，因为 Yahoo 无法说明哪些数字在当时已公开。

内幕交易按发生时间而非申报时间确定日期，因此以过去日期运行也会被告知这些数据被保留。

SEC 要求调用者表明身份，并拒绝没有联系地址的请求，因此会发送一个默认地址。请设置你自己的地址，以便 SEC 能联系你而不是项目：

```bash
SEC_EDGAR_USER_AGENT="Your Name your@email.com"
```

它覆盖向 SEC 申报的公司，包括在美国上市的外国公司。其他情况，例如香港或 A 股上市，会落到链中的下一个供应商。EDGAR 的机器可读申报始于 2009 年，第四季度会报告为不可用而不是推导得出，因为申报者只在年度数字中公布它。

### 当前持仓

默认情况下，智能体不知道你持有什么，因此其建议是写给将其应用于自身持仓的读者。传入一个投资组合，可让交易员、风险分析师和投资组合经理针对你的实际持仓工作。

```python
from tradingagents.portfolio import PortfolioContext

portfolio = PortfolioContext.model_validate({
    "cash": 25000.0,
    "currency": "USD",
    "positions": [{"ticker": "NVDA", "quantity": 120, "average_price": 150.0}],
})
_, decision = ta.propagate("NVDA", "2026-09-01", portfolio=portfolio)
```

CLI 接受相同内容的 JSON 文件：`tradingagents --portfolio my_book.json`。

空的 `positions` 列表表示空仓，这与不传入任何内容不同。没有传入投资组合的运行绝不会被视为空仓。

## 持久化与恢复

TradingAgents 在多次运行之间持久化两类状态。

### 记忆日志

记忆日志始终开启。每次完成的运行都会将其决策追加到 `~/.tradingagents/memory/trading_memory.md`。当后续运行的分析师工作时，TradingAgents 会为每条持有期已过的已记录决策进行结算：获取实际回报（原始回报，以及相对于该工具区域基准的 alpha）并生成一段反思。随后投资组合经理会读取同一股票代码的最近决策以及其他股票代码的近期经验教训，使每次分析都继承哪些有效、哪些无效。如果结算失败，运行会继续，并在报告中说明。

可通过 `TRADINGAGENTS_MEMORY_LOG_PATH` 覆盖路径。

若要在不运行分析的情况下结算决策（例如计划任务），调用 `ta.settle_all_pending()`；它会返回已结算的决策以及无法结算的决策。

### 检查点恢复

检查点恢复通过 `--checkpoint` 选择性启用。启用后，LangGraph 会在每个节点后保存状态，使崩溃或中断的运行从最后一个成功步骤继续，而不是重新开始。运行视图会说明是恢复了已保存的运行还是全新开始。成功完成后检查点会自动清除。

每个股票代码的 SQLite 数据库位于 `~/.tradingagents/cache/checkpoints/<TICKER>.db`（可通过 `TRADINGAGENTS_CACHE_DIR` 覆盖基础目录）。使用 `--clear-checkpoints` 在运行前重置所有检查点。

```bash
tradingagents --checkpoint           # 为本次运行启用
tradingagents --clear-checkpoints    # 运行前重置
```

```python
config = DEFAULT_CONFIG.copy()
config["checkpoint_enabled"] = True
ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("NVDA", "2026-09-01")
```

## 随时间评估决策

一次运行只给出一个决策，无法告诉你系统决策是否良好。`run_backtest` 在股票代码和日期的网格上运行相同的流水线，写入自己的记忆日志，并为持有窗口已经交易过的决策评分。

```python
from tradingagents.backtest import iter_grid, run_backtest, summarize

dates = iter_grid("2026-06-01", "2026-08-01", every_n_days=7)
result = run_backtest(["NVDA", "AAPL"], dates, config, selected_analysts=["market", "news"])
print(summarize(result).render())
```

从 CLI：

```bash
tradingagents backtest NVDA,AAPL --start 2026-06-01 --end 2026-08-01 --every 7
```

每个单元按相对于该工具区域基准的实际 alpha 评分，并按评级分组。决策在其日期后的首个收盘价入场，因为运行会读取当日收盘后发布的新闻。你自己的记忆日志永远不会被写入，使用 `run_id=result.run_id` 重新运行相同网格会跳过已运行的单元，因此中断的扫描会从中断处继续。

## 可复现性

TradingAgents 由 LLM 驱动，因此同一股票代码和日期的两次运行可能不同。对于基于语言模型的研究工具而言这是预期行为，而非缺陷。这种变化来自几个不同来源，区分它们会有所帮助。

语言模型采样是非确定性的。即使在固定温度下，提供商也不保证跨调用输出逐字节一致，而推理模型（默认的 GPT-6 系列以及任何 thinking 模式模型）变化最大，因为其内部推理本身也是采样的。

实时数据会变化。新闻、StockTwits 和 Reddit 会随时间返回不同内容，因此今天的运行与上周的运行即使历史交易日期相同，看到的输入也不同。固定分析日期可以固定价格和指标窗口，但社交和新闻来源仍反映“现在”。

要减少变化，可以降低采样温度。在配置中设置 `temperature`（或 `.env` 中的 `TRADINGAGENTS_TEMPERATURE`）；较低的值会使遵循它的模型更可重复。当前精选模型以推理为主，基本忽略温度，因此若要求更严格的可复现性，请在配置中或通过 `TRADINGAGENTS_DEEP_THINK_LLM` 和 `TRADINGAGENTS_QUICK_THINK_LLM` 指定非推理模型。你的提供商提供的任何模型 ID 都会被接受，无论选择器是否列出。

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["temperature"] = 0.0
# 推理模型会忽略 temperature。若要求更严格的可复现性，请在
# deep_think_llm / quick_think_llm 中指定非推理模型。
```

已经不再变化的部分：被分析的公司身份会在任何智能体运行之前由股票代码确定性解析，市场分析师会将确切的价格和指标陈述锚定在经验证的数据快照上。此前关于跨运行“不同公司”或编造价格水平的报告已通过这两个机制得到解决。

回测结果不保证与任何已公布的数字一致。回报取决于模型、温度、日期范围、数据质量以及上述采样。请将本框架视为研究多智能体分析的研究脚手架，而不是具有固定、可复制回报的策略。

<a id="contributing"></a>
## 贡献

欢迎贡献：缺陷修复、文档和功能想法；过往贡献会按版本记录在 [`CHANGELOG_CN.md`](CHANGELOG_CN.md) 中。

<a id="citation"></a>
## 引用

如果你觉得 *TradingAgents* 对你有所帮助，请引用我们的工作 :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
