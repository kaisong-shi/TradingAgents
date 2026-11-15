# 更新日志

> 📖 英文版：[CHANGELOG.md](CHANGELOG.md)

TradingAgents 的所有重要变更都记录在此。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。
升级时需要采取行动的变更会列在对应版本的“从……升级”小节下。

## [0.7.1] — 2026-10-27

决策仅按最终收盘价评分，并可跨长时间市场休市完成结算；模型未补零的日期不再读取运行日期之后提交的申报文件；修复了投资组合、价格、SEC 报表、报告、Azure 和 Claude 设置相关问题。

### 从 0.7.0 升级

- Docker 镜像不再包含 `.env.enterprise`。若在 Docker 中使用 Azure OpenAI，请将其 Key 放入 `.env`。

### 修复

- 模型传入的未补零日期（如 `2024-7-5`）会按该日期读取。此前它可能被比较为晚于运行日期之后提交的申报，导致 SEC EDGAR 提供该申报。(#1488)
- 决策不再按仍在交易的交易时段 K 线评分；在超过一周的市场休市（如全国性假日）之前做出的决策，会在交易恢复后结算，而不是一直挂起。(#1548, #1539)
- 回测会报告其最后一次结算过程中的失败；同一秒内启动的两个回测不再共用同一个运行。(#1557, #1549)
- 按券商拼写记录的持仓（`BTCUSDT`、`700.HK`）会与被分析的标匹配；文件加载时，非有限数的投资组合数值会被拒绝。(#1556, #1509)
- 价格保留有效数字：不足一美分的收盘价不再打印为 0.00，货币对保留其点值。(#1567)
- SEC EDGAR 报表每个期间只列一行，因此模型在长历史中不再将某个数字读成错误的季度；低于一百万的数字不再打印为 0。(#1517, #1589)
- 将报告保存到此前使用过的文件夹时，会删除上一轮运行的章节。(#1566)
- 结束日期早于开始日期的日期窗口会返回给模型，而不是返回无数据。(#1595)
- 除年度或季度以外的报表频率会返回给模型，而不是在该名称下提供年度数字。(#1593)
- 记忆的最近经验教训以及轮换保留的条目按决策日期排序，因此回填更早日期时不再挤掉它们。(#1603)
- 预测市场赔率接近 0% 或 100% 时，会以两位有效数字显示其与该值的距离。(#1598)
- Azure OpenAI 会收到 `max_tokens` 和配置的端点。(#1584, #1600)
- Claude 的 effort 设置对于带日期的模型 ID（如 `claude-sonnet-4-20250514`）能正确判定。(#1585)
- CLI 使用与运行相同的规则检查股票代码，因此 `XAUUSD+` 会被接受，`..` 会在提示时被拒绝。(#1604)
- Docker 镜像不再包含任何文件夹中的 `.env` 文件。
- 修复了在 Windows 和 macOS 上因平台原因失败的测试。(#1506, #1485, #1541)

### 贡献者

[@alanfate3](https://github.com/alanfate3), [@aranlucas](https://github.com/aranlucas), [@BichengWang](https://github.com/BichengWang), [@Bortlesboat](https://github.com/Bortlesboat), [@hoffman988](https://github.com/hoffman988), [@jhill-cmd](https://github.com/jhill-cmd), [@muhib-karim](https://github.com/muhib-karim), [@pei711](https://github.com/pei711), [@peiji1981](https://github.com/peiji1981), [@rudycelekli](https://github.com/rudycelekli), [@Shubham-Padkonde](https://github.com/Shubham-Padkonde), [@stevexyz2003](https://github.com/stevexyz2003), [@SuperMarioYL](https://github.com/SuperMarioYL), [@sytfly](https://github.com/sytfly), [@yuv009](https://github.com/yuv009)。

## [0.7.0] — 2026-10-16

支持在你的 ChatGPT 套餐上运行；回测从每次决策后的首个收盘价开始评分；启动时提示有新版本；每个 GitHub Release 附带 wheel 包。

### 新增

- **你的 ChatGPT 套餐。** `chatgpt` 提供商通过 OpenAI 面向开源应用的登录方式，让你的 ChatGPT Plus 或 Pro 套餐运行 TradingAgents，而无需 API Key。在 CLI 的提供商菜单中选择“Subscription”；对于无人值守运行、Docker 和 Python（`llm_provider="chatgpt"`），使用 `tradingagents login chatgpt` 登录一次。`tradingagents logout chatgpt` 会撤销登录。CLI 会列出该套餐的模型，推理强度与 OpenAI 一样生效。(#1194, #1475)
- **启动时的新内容。** 交互式 CLI 会提示新版本，并在能判断 TradingAgents 安装方式时给出升级此安装的命令，同时显示针对当前运行版本的 Tauric Research 通知。它每天最多在后台检查一次，因此运行从不会等待它；没有终端的运行永远不会检查，`TRADINGAGENTS_NO_UPDATE_CHECK=1` 可将其关闭。
- **Release 下载。** 每个 GitHub Release 附带源码归档和 wheel 包，因此可以直接从发布页面用 `pip install` 安装某个版本，而无需克隆仓库。

### 从 0.6.0 升级

- 会安装 `cryptography` 42 和 `packaging` 24 或更高版本。
- 决策现在从其日期后的首个收盘价开始评分。记忆日志中已结算的结果保留较早的条目，即决策日期的收盘价，因此使用 `run_id` 恢复的回测会混合两者；若要同口径比较，请开始新的运行。

### 修复

- 决策不再依据其无法用于交易的新闻评分：日期为 *d* 的运行会读取 *d* 收盘后发布的新闻，因此记忆日志和回测在 *d* 之后的第一个收盘价入场，而不是 *d* 的收盘价。(#1518)
- 没有终端的运行（如计划任务或 CI）不再在启动前联系公告服务器。
- 当主提供商没有推理设置时，位于其他提供商上的模型层级会保留其配置的推理强度、thinking 级别或 Claude effort。(#1440)

### 贡献者

[@LeonWTW](https://github.com/LeonWTW), [@OleksanderSS](https://github.com/OleksanderSS), [@sovorn-c](https://github.com/sovorn-c)。

## [0.6.0] — 2026-10-03

HTML 报告；按模型层级配置提供商；分析期间为每个股票代码结算历史决策；在 Yahoo 新闻源不可用期间读取公司新闻。

### 新增

- **HTML 报告。** 保存的报告还包含 `complete_report.html`，即把报告作为单个页面，并在文本旁列出各章节，便于在浏览器、手机和打印时阅读。在提示中回答保存问题后，还会询问是否生成该页面并可在浏览器中打开；`--no-html` 或 `save_reports(..., html=False)` 会跳过。该页面是自包含的：不加载任何内容，也不运行任何内容。(#1419)
- **按模型层级配置提供商。** 快速模型和深度模型可以运行在不同的提供商上，例如管理层使用 Claude，分析师使用 OpenAI：设置 `deep_think_provider` 或 `quick_think_provider`（`TRADINGAGENTS_DEEP_THINK_PROVIDER`、`TRADINGAGENTS_QUICK_THINK_PROVIDER`）以及该层级的模型。报告头部会注明每个层级的提供商。(#1440)
- **历史决策与分析并行结算。** 在运行的分析师工作期间，所有持有期已过的已记录决策都会被结算，适用于任何股票代码，而不仅仅是正在分析的那个。如果结算失败，运行会继续，并在报告头部说明。(#1428, #1445)
- **Reddit 上的加密货币。** 对于加密货币股票代码，情绪分析师会读取 r/CryptoCurrency 和 r/CryptoMarkets，以及对应币种的 r/Bitcoin、r/ethereum 或 r/solana，而不是股票子版块。(#1461)
- `settle_all_pending()` 可在不运行分析的情况下结算所有到期决策，适用于计划任务；它和 `settle_pending()` 都会返回已结算的决策以及无法结算的决策。(#1445)
- 报告头部会注明本次运行的评级。
- 按名称提供的欧元区宏观序列：`ecb_deposit_rate`、`ecb_main_refi_rate`、`euro_hicp`、`euro_core_hicp`、`euro_real_gdp`、`germany_10y`、`france_10y` 和 `eur_usd`。(#1465)

### 模型

- Gemini 调用在 600 秒后超时，与 OpenAI 和 Anthropic 调用一致，因此停滞的调用不再挂起整个运行。(#1417)

### 从 0.5.2 升级

- 会安装 markdown-it-py 4.0 或更高版本。
- 保存的报告还会写入 `complete_report.html`；传入 `--no-html`，或对 `save_reports()` 传入 `html=False`，以仅保留 Markdown。
- 运行在开始前不再结算其股票代码的决策；记忆日志步骤会在运行期间结算每个股票代码的决策。
- `settle_pending()` 返回带有 `settled` 和 `failed` 的 `Settlement`（原为 `None`）。
- 0.5.2 的检查点不会被恢复。

### 修复

- 在 Yahoo 新闻源返回空内容期间，公司新闻会从 Yahoo 搜索读取。当 Yahoo 没有关于该符号的文章时，其新闻会报告为不可用而非不存在，并会尝试配置的下一个新闻供应商。(#1467, #1469)
- 引自他人的评级（如“Consensus rating: Buy”）不再替换投资组合经理自己的评级。(#1466)
- 包含空字段的 Yahoo 新闻文章不再导致该股票代码的新闻丢失。(#1458)
- 模型写入的带有杂散字符的开始日期会返回给模型更正，而不是使新闻或价格请求失败。(#1476)
- Alpha Vantage 拒绝的请求会报告为不可用，而不是作为数据提供；API Key 不会出现在任何 Alpha Vantage 错误中。(#1442)
- Yahoo 基本面数据会以各自的货币打印每个金额：伦敦价格以 GBp 表示，市值和每股数字以 GBP 表示，ADR 的收入数字以其报告货币表示，例如台积电使用 TWD。(#1456)
- Jev 筛查使用 `TYPESAFE_BASE_URL` 指定的端点，因此可以通过 OpenRouter 运行。(#1416)
- 共享记忆日志的多个运行会对每个决策只结算一次；中断的结算会保留其已完成的结果。
- 报告头部将情绪分析师命名为 `sentiment`，与 CLI 一致。
- `requirements.txt` 说明依赖已在 `pyproject.toml` 中声明。

### 贡献者

[@amitbhansali](https://github.com/amitbhansali), [@AyushJain-601](https://github.com/AyushJain-601), [@BichengWang](https://github.com/BichengWang), [@byte7m](https://github.com/byte7m), [@Dangerboi](https://github.com/Dangerboi), [@davidalmeida90](https://github.com/davidalmeida90), [@Jackzigen](https://github.com/Jackzigen), [@jhill-cmd](https://github.com/jhill-cmd), [@Recnelis0](https://github.com/Recnelis0), [@seaaxe](https://github.com/seaaxe), [@vaegev](https://github.com/vaegev)。

## [0.5.2] — 2026-09-29

并行分析师、无人值守的 CLI 运行、记录其生成条件的报告，
以及过去日期的运行只获得当时已知的数据。

### 新增

- **并行分析师。** 所选分析师同时运行，因此分析师阶段大约耗时最长的那一个；CLI 会在每个分析师完成时显示其进度和时间，所有报告齐备后辩论开始。(#1255, #433)
- **无人值守的 CLI 运行。** 参数回答每次运行的问题，`TRADINGAGENTS_*` 变量回答其余问题，因此计划任务或脚本无需任何提问：`tradingagents --ticker NVDA --date 2026-09-26 --analysts market,news --save --no-show`。没有终端时，缺少答案会在运行开始前中止，并指出需要设置的内容。(#1127, #1133)
- **报告记录其生成条件。** 每份报告开头都会列出分析日期、版本、提供商、模型、分析师、轮数和数据供应商；状态日志将其保存为 `run_settings`。(#752, #1197)
- **Docker 数据文件夹。** `TRADINGAGENTS_DATA_DIR` 将结果、报告和记忆日志保存在宿主机文件夹中。(#865)
- **分析师工具调用上限。** 经过 `max_tool_rounds` 轮（默认 20，`TRADINGAGENTS_MAX_TOOL_ROUNDS`）后，分析师会根据已有内容撰写报告。(#1420)
- `tradingagents backtest` 会在每个单元开始时显示它以及用于继续的 `--run-id`；`--analysts` 接受 `sentiment`。
- 台湾、韩国、新加坡和主要欧洲交易所的基准。(#1392)
- 支持 Python 3.14；Docker 镜像运行 Python 3.13。

### 模型

- `deepseek-flash` 被视为 thinking 模型，因此结构化输出可用。(#1388)

### 从 0.5.1 升级

- 需要 Python 3.11 或更高版本；会安装 pandas 3。
- 最低版本：yfinance 1.7.0、langchain-core 1.6.5、langchain-openai 1.6.6、langchain-anthropic 1.7.4、langchain-google-genai 4.4.0、langgraph 1.2.12、langgraph-checkpoint-sqlite 3.1.1、langchain-aws 1.7.9（`bedrock` 额外依赖）。
- 报表默认使用 SEC EDGAR，然后 Yahoo（`fundamental_data = "sec_edgar,yfinance"`）。
- 过去日期的运行不会获得 Yahoo 或 Alpha Vantage 的报表或内幕交易数据，因为它们没有申报日期；只会获得公司当前名称，并会标注这一点。
- 记忆日志是 `tradingagents.memory` 包（原为 `tradingagents.decision_log`）；结算和反思从 `tradingagents.graph` 移到这里，`Reflector` 不再从 `tradingagents.graph` 导出。
- `process_signal` 已移除；评级是 `propagate()` 的第二个返回值或 `final_state["final_rating"]`。
- 评级仅从其 `Rating:` 标签读取；没有该标签的自由文本决策为 `REVIEW`。
- 数据层函数使用 `as_of_date=`（原为 `curr_date=`）；`build_instrument_context` 和 `resolve_instrument_context` 使用 `trade_date=`。
- `VendorRateLimitError` 改为 `VendorUnavailableError`。
- 数据工具从运行状态获取标的；工具调用不再携带 `symbol` 或 `ticker`。
- 状态日志：`trader_investment_plan`（原为 `trader_investment_decision`），移除 `judge_decision`，新增 `final_rating` 和 `run_settings`。
- 0.5.1 的检查点，或在不同设置下保存的检查点，不会被恢复。

### 修复

- 数据工具提供运行中的标的，即使模型传入了另一个符号。
- 供应商请求失败会报告为不可用，而不是符号缺失或退市；一个供应商的“无数据”不再代表一个其中有其他供应商失败的链条。(#1386)
- 评级是投资组合经理自己的评级，而不是其论述中引用的评级 (#1383)；在其他输出语言中，其行仍保留英文标签 (#1435)。
- 重复给出的回测单元只运行一次 (#1415)，结算会在相同日期上比较决策与其基准。
- 没有价格的符号快照不再终止运行。
- 并发运行不再丢失记忆日志条目。
- SEC EDGAR 仅按年初至今申报的季度数字会被提供，并标注其跨度。
- Yahoo 股息收益率和债务权益比以百分比打印。(#1414)
- FRED 变化行会注明其跨度日期。(#1397)
- `stream_run` 将其工具提供图自身的配置。
- 测试套件不接触网络和用户文件，并且以任意顺序通过；集成测试使用 `-m integration` 运行。(#1395)

### 贡献者

[@1Wizzy](https://github.com/1Wizzy), [@BichengWang](https://github.com/BichengWang), [@Chaoqi31](https://github.com/Chaoqi31), [@davidalmeida90](https://github.com/davidalmeida90), [@djconnexion77](https://github.com/djconnexion77), [@fuzing](https://github.com/fuzing), [@hailampy123](https://github.com/hailampy123), [@hesam-shams](https://github.com/hesam-shams), [@HEYALT](https://github.com/HEYALT), [@Jackzigen](https://github.com/Jackzigen), [@kagura-agent](https://github.com/kagura-agent), [@loulanyue](https://github.com/loulanyue), [@mannubaveja007](https://github.com/mannubaveja007), [@olivergpt](https://github.com/olivergpt), [@rita112025-cpu](https://github.com/rita112025-cpu), [@shuyan-code](https://github.com/shuyan-code), [@SingTheCode](https://github.com/SingTheCode), [@sjq597](https://github.com/sjq597), [@xiaodu55](https://github.com/xiaodu55), [@Youholdme](https://github.com/Youholdme)。

## [0.5.1] — 2026-09-24

按模块内容组织的包结构；设置 Key 时由 TypeSafe 的 Jev 筛查社交帖子；
默认模型为 GPT-6 Sol 和 Luna；修复运行隔离、SEC EDGAR 报表和历史运行问题。

### 从 0.5.0 升级

部分模块已移动，旧导入路径已移除。请按如下方式更新导入：

- `tradingagents.dataflows.interface` 改为 `tradingagents.dataflows.router`，`dataflows.symbol_utils` 改为 `dataflows.symbols`。`dataflows.utils` 已移除：`get_current_date` 在 `dataflows.date_window`，`safe_ticker_component` 在 `dataflows.symbols`，`get_scrubbed` 和 `vendor_reachable` 在 `dataflows.net`。
- 供应商模块位于 `tradingagents.dataflows.vendors` 下：`yahoo`（`ohlcv`、`market`、`fundamentals`、`news`、`snapshot`，来自原 `stockstats_utils`、`y_finance`、`yfinance_news` 和 `market_data_validator`）、`alpha_vantage`（一个包，来自原 `alpha_vantage_*` 模块），以及 `sec_edgar`、`fred`、`polymarket`、`reddit`、`stocktwits`。
- `tradingagents.agents.utils` 已移除：智能体工具在 `agents.tools` 中，`agent_utils`、`agent_states`、`rating` 和 `structured` 分别改为 `agents.context`、`agents.state`、`agents.rating` 和 `agents.structured`。
- 决策日志为 `tradingagents.decision_log`（原为 `agents.utils.memory`），`cli.utils` 改为 `cli.prompts`。
- `backtest.summarize` 接受 `run_backtest` 的结果或决策日志路径，取代 `TradingMemoryLog`。
- 移除：`SignalProcessor`（评级由 `process_signal` 解析）、`create_social_media_analyst` 别名（使用 `create_sentiment_analyst`）、`symbol_utils.is_yahoo_safe`、未使用的 `project_dir` 配置键，以及保存上一轮运行状态的图属性 `curr_state`、`ticker` 和 `log_states_dict`。

### 新增

- **Jev 帖子筛查。** 设置 `TYPESAFE_API_KEY` 后，TypeSafe 的 Jev 会读取情绪分析师获取的每条 StockTwits 和 Reddit 帖子：与公司无关的帖子会被丢弃，每个来源开头会给出其余帖子按立场的计数。没有 Key 时一切不变。(#1376)
- B3 股票代码（`.SA`）以 Ibovespa 为基准。(#1366)

### 模型

- GPT-6 Sol 和 GPT-6 Luna 成为默认的深度和快速模型，Claude Opus 5.5 在选择器中替换 Opus 5。Opus 5 和 GPT-5.4 Mini 仍是有效的模型 ID。

### 修复

- 同一进程中的多个图各自读取自己的数据供应商。(#1369)
- SEC EDGAR 现金流量表能为将资本支出移到生产性资产购置的申报者找到该数据（NVIDIA 自 2022 财年、Amazon 自 2016 年），此前其近期期间读取为空。(#1370)
- SEC EDGAR 年度报表只列出财年。
- 历史运行不再在覆盖通知和标的上下文中被告知今天日期或运行之后的日期。
- 基本面分析师可以调用内幕交易工具。
- 内幕交易中 Yahoo 不可达会报告为不可用，而不是符号无数据。
- 跨运行复用的图（如回测中）不再保留每次运行的完整状态。
- 带检查点的 CLI 运行会说明是恢复还是全新开始。
- 空白路径变量（如 `TRADINGAGENTS_RESULTS_DIR`）保留默认路径。
- StockTwits 消息以纯文本而非 HTML 转义形式进入提示。
- 测试套件独立于开发者的 `.env`、时区和网络。(#1368, #1372)

### 贡献者

感谢所有报告这些问题或提交修复的人：

[@codify88](https://github.com/codify88), [@davidalmeida90](https://github.com/davidalmeida90), [@duongylinh](https://github.com/duongylinh), [@jccl2](https://github.com/jccl2), [@yuina368](https://github.com/yuina368)。

## [0.5.0] — 2026-09-18

每条带日期的路径均具备时点完整性；决策按做出时的原样记录；
在股票代码和日期网格上回测；调用者的投资组合作为运行输入；
SEC EDGAR 基本面数据按申报原文提供。

### 亮点

- **按申报原文提供的基本面数据。** SEC EDGAR 按运行日期的时点提供美国公司报表：已结束但尚未申报的期间不会被提供，后来重述的数字仍按首次报告读取。无需 Key，通过供应商链选择性启用。
- **回测。** `run_backtest` 在股票代码和日期网格上运行流水线并写入自己的决策日志，`summarize` 为已结算单元评分；`tradingagents backtest` 在 CLI 中做同样的事。
- **投资组合上下文。** `propagate(..., portfolio=...)` 和 `--portfolio` 让交易员、风险和投资组合智能体按真实持仓确定规模。没有传入投资组合的运行绝不会被视为空仓。
- **决策按做出时的原样记录。** 无法读取的决策在所有地方都会被标记为待审核，而不会变成可交易的 Hold；被论证反对的评级不再被读作最终判断。

### 时点与诚实的归因

- 带日期的工具从图状态获取运行日期，因此省略或更晚的日期无法到达供应商。(#1331, #1319, #1118)
- 内幕申报和预测市场赔率以运行日期为界；内幕记录会说明交易在其 Form 4 申报时公开。
- 从未观察到某个窗口的数据源会报告为不可用而非不存在，适用于新闻、Reddit 和 StockTwits。
- 解析出的公司身份会说明它描述的是今天还是运行日期。
- 验证快照引用供应商报告的价格，绝不使用填补的数值。
- 供应商失败就是供应商失败：yfinance 会抛出异常而不是将其错误作为文本返回；服务中断不会报告为公司无数据；当链中所有供应商都不可用时，会说明这一点而不是终止运行。
- 宏观数据版本固定会被限制在供应商自己的时钟上，因此以今天日期运行不会请求它没有的版本。
- 历史运行不会从两个基本面供应商中的任何一个获得当前公司简介。(#1300)

### 决策与评估

- 带标签的评级起决定作用，无论其间有什么分隔；提及多个评级的文本会被审核而不是猜测。
- 决策提示会说明其答案的形态，因此没有结构化输出的提供商仍会返回可读的决策。
- 未生成的报告会说明未生成，而不是显示为空章节。
- 回测评分会读取每个评级所主张的方向：Sell 且下跌为命中，Hold 不报告命中率。
- 结果窗口可配置（`holding_period_days`），反思会说明其判断的窗口。
- 已结算的决策不会被记录两次，反思失败也不再阻止下一次运行。(#645)
- 交易员以价格形式说明入场和止损水平，因此百分比不再使整个提案失败。(#1288)

### CLI

- `tradingagents backtest`，使用 `--run-id` 继续中断的扫描。(#1234)
- 上次运行的选择会作为提示默认值返回。(#1236, #920)
- 没有可读评级的运行会说明这一点；实时视图不再滚动；看起来像 Python 值的消息会被显示。(#649, #784)
- 状态日志保留非 ASCII 字符的可读性。(#1081)

### 数据源

- SEC EDGAR 基本面供应商（美国申报者，无需 Key）。
- 香港和上海股票代码会解析为 Yahoo 提供的符号。(#1342, #957, #1260)
- Reddit 每次运行作为一个合并请求获取。(#1286)
- 每个符号一个 OHLCV 缓存文件。(#1330)

### 模型

- 每个提供商的当前阵容：GPT-6 Astra 和 GPT-5.6 系列、Gemini 3.8 Flash、Claude Opus 5 和 Fable 5.1、Grok 4.6、DeepSeek Flash、Qwen 3.8、GLM-5.3、MiniMax M3、Kimi K3 以及当前 Mistral 快照。
- 每个提供商都接受选择器未列出的模型 ID。
- GLM 流量会发往其 Key 所属的平台，Ollama 结构化输出不再发送它拒绝的 tool_choice。(#1062)

### 变更

- 对于没有可读评级的决策，记忆日志记录 `REVIEW`，此前记录为 `Hold`。
- 模型未提供的可选字段会被注明未提供，而不是省略。
- 移除了没有任何导入的依赖：backtrader、redis、setuptools、langchain-experimental、parsel、tqdm。(#1353, #1070)

### 贡献者

感谢所有报告这些问题或提交修复的人：

[@akashkpfreelancer](https://github.com/akashkpfreelancer), [@angziii](https://github.com/angziii), [@anupamme](https://github.com/anupamme), [@AyushKar2005](https://github.com/AyushKar2005), [@bulkypanda](https://github.com/bulkypanda), [@CadeYu](https://github.com/CadeYu), [@chiang21fcb](https://github.com/chiang21fcb), [@dajiaohuang](https://github.com/dajiaohuang), [@dewrama](https://github.com/dewrama), [@DogInfantry](https://github.com/DogInfantry), [@emitov](https://github.com/emitov), [@farukerdem34](https://github.com/farukerdem34), [@flydragon2018](https://github.com/flydragon2018), [@fusshell](https://github.com/fusshell), [@Ganesh1729-ui](https://github.com/Ganesh1729-ui), [@gyx09212214-prog](https://github.com/gyx09212214-prog), [@hamzabudeir](https://github.com/hamzabudeir), [@ihsieh31](https://github.com/ihsieh31), [@jaylew20250206](https://github.com/jaylew20250206), [@kaushik-yadav](https://github.com/kaushik-yadav), [@kbnnf](https://github.com/kbnnf), [@kevinkda](https://github.com/kevinkda), [@LudwigJMarx](https://github.com/LudwigJMarx), [@lx7720](https://github.com/lx7720), [@malandrindev](https://github.com/malandrindev), [@mhd325ic-hash](https://github.com/mhd325ic-hash), [@minhdn90](https://github.com/minhdn90), [@miznan](https://github.com/miznan), [@mmssix](https://github.com/mmssix), [@mrbob-git](https://github.com/mrbob-git), [@newnewself](https://github.com/newnewself), [@prithvirajrh](https://github.com/prithvirajrh), [@PyriteResearch](https://github.com/PyriteResearch), [@Rajatendu1](https://github.com/Rajatendu1), [@Recnelis0](https://github.com/Recnelis0), [@Rodvask](https://github.com/Rodvask), [@samhoooo](https://github.com/samhoooo), [@sheiun-xu](https://github.com/sheiun-xu), [@shivsin25](https://github.com/shivsin25), [@SmileShaun](https://github.com/SmileShaun), [@SonnyRajagopalan](https://github.com/SonnyRajagopalan), [@taro0915](https://github.com/taro0915), [@wupengbo125](https://github.com/wupengbo125), [@wxggzz](https://github.com/wxggzz), [@Yixiang-Wu](https://github.com/Yixiang-Wu), [@ZahirBodrike](https://github.com/ZahirBodrike), [@ZHUYAWEI](https://github.com/ZHUYAWEI), [@zkwang616](https://github.com/zkwang616)。

## [0.4.0] — 2026-08-31

跨数据和记忆层的前视与时点修复；更清晰的决策信号；
可用的 CLI 检查点恢复；GPT-5.6 / GLM-5.3 模型。

### 修复

- **FRED 宏观前视。** 历史宏观请求此前从今天的数据版本提供，将后来的修订泄漏到回测中；现在观测值和元数据请求都会将版本固定到 as-of 日期。(#1275)
- **社交情绪前视。** StockTwits 和 Reddit 此前在没有日期的情况下获取，因此历史运行会显示今天的讨论，仿佛来自 as-of 日期；现在社交路径会裁剪到分析窗口，使用与新闻相同的共享 UTC 半开窗口规则（`dataflows/date_window`）。(#1220)
- **记忆时点保护。** `get_past_context` 此前会返回所有已解析的经验教训，而不论运行日期；现在每个已解析条目都会记录其结果已知的日期，历史运行只能看到在交易日期之前已解析的经验教训。(#1251)
- **过早反思。** 如果在其持有窗口完全交易之前重新运行，决策会基于部分回报结算；现在解析会等待完整窗口。(#1169)
- **最新 OHLCV K 线被丢弃。** 收盘价为 NaN 的最新 K 线会在日期截断前被静默丢弃，使前一个交易日看起来像最新日期；现在日期按元素规范化（对 DST 和非美国市场安全），缺失的最新收盘价会抛出异常而不是回退。(#1201)
- **辩论开场捏造。** 每轮辩论中的第一位发言者会反驳空的对手回应，从而捏造对方观点；现在当没有对手发言时，五位辩论者都会以自己的论点开场。(#1176)
- **静默 Hold。** 无法解析的投资组合经理评级（包括全角冒号）此前会被强制转为可交易的 Hold；现在会浮现 `REVIEW` 哨兵值，`parse_rating` 为兼容调用方保留其静默默认值。(#1170)
- **`--checkpoint` 在 CLI 上无效。** 检查点设置只存在于 `propagate()` 中；CLI 流式运行的是没有检查点的图。现在生命周期共享，恢复时会传入 `None`，使 LangGraph 继续被中断的运行而不是重复消息。(#1249)
- **通过 OpenRouter 使用 DeepSeek。** `deepseek/<id>` 此前会落到默认能力，并被强制使用对象形式的 `tool_choice`；现在会剥离官方命名空间，使其复用原生 DeepSeek 的特殊行为。(#1199)
- **Trader 价格锚定。** Trader 此前只看到提炼后的计划；现在它还会收到技术市场报告，使入场/止损水平锚定真实价格结构。(#1167)

### 新增

- **可配置的输出 token 上限。** `max_tokens` / `TRADINGAGENTS_MAX_TOKENS` 会转发给每个提供商（Gemini 使用 `max_output_tokens`），因此可以限制产生无限推理的模型，而不是挂起。(#1204)
- **最新模型。** 新增 GPT-5.6 系列（`gpt-5.6` / `gpt-5.6-terra` / `gpt-5.6-luna`）和 GLM-5.3（`glm-5.3`、`glm-5.3-flash`）。默认模型现为 `gpt-5.6`（深度）和 `gpt-5.6-luna`（快速）。

### 贡献者

感谢所有报告这些问题或提交修复的人：

[@PyriteResearch](https://github.com/PyriteResearch), [@yiran1268](https://github.com/yiran1268), [@fabiolenine](https://github.com/fabiolenine), [@lx7720](https://github.com/lx7720), [@taro0915](https://github.com/taro0915), [@Jaswanth-Sriram-Veturi](https://github.com/Jaswanth-Sriram-Veturi), [@ariesy](https://github.com/ariesy), [@liangzj1999](https://github.com/liangzj1999), [@zkwang616](https://github.com/zkwang616), [@aniketshukla1](https://github.com/aniketshukla1), [@loulanyue](https://github.com/loulanyue), [@hudsonwa](https://github.com/hudsonwa), [@daleselaji-dev](https://github.com/daleselaji-dev), [@wolfoswald777-crypto](https://github.com/wolfoswald777-crypto)。

## [0.3.1] — 2026-07-05

正确性与稳定性补丁：数据前视、图路由崩溃安全、
检查点身份、加密情绪来源，以及可配置的韧性。

### 修复

- **Alpha Vantage 前视过滤现在会运行。** 基本面 payload 是 JSON 字符串，因此仅针对 dict 的检查会跳过过滤，未来日期的报告会泄漏到历史运行中；现在先解析再过滤。(#1115, @zachthebird)
- **新闻分析师提示与工具一致。** 提示中宣传的是 `get_news(query, ...)`，但工具接受的是股票代码；现已对齐，以阻止幻觉的自由文本查询调用。(#1116, @shcheuk)
- **共享的辩论/风险路由不会在运行中途崩溃。** 两个路由器返回的目标多于任何单条边所映射的数量；现在每条边共享完整路径映射，因此提示/i18n/重构漂移下的落空仍可路由。(#1088, @Fr3ya, @sa7an7, @Sushanth012)
- **检查点恢复遵循图结构。** 线程 ID 会纳入所选分析师、辩论/风险深度和资产模式，因此在不同选择下恢复不再继续错误的图。(#1089, @bossjoker1, @Ghraven)
- **加密情绪来源可解析。** StockTwits 将加密货币列为 `<BASE>.X`（Yahoo 的 `BTC-USD` 会 404），Reddit 需要基础符号才能匹配；现在社交路径会为两者正确映射加密货币。(#1113, @suremadoreai)

### 新增

- **可配置的 LLM 重试预算。** `llm_max_retries` / `TRADINGAGENTS_LLM_MAX_RETRIES` 会转发给每个提供商，因此瞬时的 429 突发不再中止运行。(#1091, @yanggaome)
- **Bedrock API Key 认证。** `AWS_BEARER_TOKEN_BEDROCK` 无需 AWS 访问密钥即可认证 Amazon Bedrock，并优先于环境中的 `AWS_PROFILE`。(#1103, @praxstack)
- **最新 Claude 模型。** 新增 Claude Sonnet 5（`claude-sonnet-5`）和 Fable 5（`claude-fable-5`）；effort 控制现在覆盖 Claude 5 系列。

## [0.3.0] — 2026-06-22

稳定性和可扩展性版本：CI 门禁、统一的经验证数据访问契约、
提供商和数据供应商注册表，以及强化配置优先级、模型目录、
数据韧性和结构化输出的维护性清理。

### 新增

- **CI 门禁。** GitHub Actions 在 Python 3.10-3.13 上运行 pytest 套件、严格 `ruff`，以及干净安装冒烟测试（导入包和 CLI 以捕获未声明的依赖）。(#994, #197)
- **提供商注册表。** OpenAI 兼容提供商作为单个规范注册，通用 `openai_compatible` 端点覆盖 vLLM、LM Studio 和中继。新增 NVIDIA NIM、Kimi、Groq、Mistral 和原生 Amazon Bedrock 客户端。
- **宏观和预测市场供应商。** FRED 宏观指标和 Polymarket 事件概率，提供给新闻和宏观分析师。
- **编程式报告输出。** `TradingAgentsGraph.save_reports()` 写入与 CLI 相同的报告树，适用于无头运行和 API 运行。(#1037)
- **可通过环境变量配置的推理深度**：`TRADINGAGENTS_OPENAI_REASONING_EFFORT`、`TRADINGAGENTS_GOOGLE_THINKING_LEVEL` 和 `TRADINGAGENTS_ANTHROPIC_EFFORT`，各自仅对接受它的模型生效。

### 变更

- **经验证的数据访问契约。** 每条供应商路径上的符号规范化（身份、回报、CLI、新闻）；配置的供应商列表就是精确的解析链，不会静默回退到未选择的供应商；类型化的 `VendorError` 分类；前视安全的新闻窗口；过期 OHLCV 拒绝；yfinance 日期范围包含端点。
- **配置优先级。** 显式的 `TRADINGAGENTS_*` 值或 CLI 参数现在优先于辩论和风险轮数的交互默认值、`--checkpoint / --no-checkpoint` 以及 Docker 提供商配置；无效的布尔环境变量值会明确失败。(#975, #976, #977)
- **当代模型目录。** 刷新提供商阵容；退役 `gpt-4.1`、Claude Sonnet 4.5 和 Gemini 2.5 系列。
- **可选供应商降级**而不是中止运行：失败的宏观或预测市场查询返回无数据哨兵值。
- **分析师提示以当前日期开头**，使工具调用日期范围锚定运行日期而不是模型的训练截止日期。(#836)

### 修复

- **标的身份。** 确定性的股票代码到公司解析可防止错误公司的幻觉，经验证的市场数据快照可锚定价格和指标陈述。(#814, #830)
- **社交和市场数据源。** Reddit 优先 RSS 并带 429 退避；StockTwits 传输加固；Alpha Vantage 超时以及 Key 与速率限制的处理。
- **结构化输出。** 本地 OpenAI 兼容服务器不再拒绝对象形式的 `tool_choice`；返回无解析结果的 thinking 模型会回退到自由文本；可选价格字段中类似 null 的字符串会转换为 `None`。(#1038, #1051, #1057)

### 移除

- 无效的 `analyst_concurrency_limit` 配置项；并行分析师执行计划在后续版本中实现。(#979)
- 未使用且已提交的 `uv.lock`。(#1030)

### 贡献者

感谢所有通过代码、设计和报告塑造此版本的人：

[@CadeYu](https://github.com/CadeYu), [@Zavianx](https://github.com/Zavianx), [@weijianz-opc](https://github.com/weijianz-opc), [@naltun](https://github.com/naltun), [@brahmasky](https://github.com/brahmasky), [@nik2208](https://github.com/nik2208), [@thieucong98](https://github.com/thieucong98), [@Derekko-web](https://github.com/Derekko-web), [@LukiPrince](https://github.com/LukiPrince), [@Eddieargenal](https://github.com/Eddieargenal), [@Ghraven](https://github.com/Ghraven), [@ms32035](https://github.com/ms32035), [@yting27](https://github.com/yting27), [@nyxst4ck](https://github.com/nyxst4ck), [@KenCheung-AIxFinance](https://github.com/KenCheung-AIxFinance), [@yangyusheng2n](https://github.com/yangyusheng2n), [@fareloj](https://github.com/fareloj), [@haosenwang1018](https://github.com/haosenwang1018), [@octo-patch](https://github.com/octo-patch), [@seifenk](https://github.com/seifenk), [@CaoYuhaoCarl](https://github.com/CaoYuhaoCarl), [@mihailnica10](https://github.com/mihailnica10), [@Dado-hash](https://github.com/Dado-hash), [@Handsomemikezzz](https://github.com/Handsomemikezzz), [@ydhawesome](https://github.com/ydhawesome), [@macd2](https://github.com/macd2), [@AyushKar2005](https://github.com/AyushKar2005), [@wildhuman](https://github.com/wildhuman), [@robert23kim](https://github.com/robert23kim), [@bngness](https://github.com/bngness), [@tedix-rodrigo](https://github.com/tedix-rodrigo), [@malaccan](https://github.com/malaccan), [@rfalken78](https://github.com/rfalken78), [@dengli1971-droid](https://github.com/dengli1971-droid), [@proofconcept39](https://github.com/proofconcept39), [@prasta1](https://github.com/prasta1), [@liximin](https://github.com/liximin), [@jeffhuen](https://github.com/jeffhuen), [@mazar](https://github.com/mazar), [@soyangelromero](https://github.com/soyangelromero), [@CNQQC](https://github.com/CNQQC), [@dovetaill](https://github.com/dovetaill), [@fperdigon](https://github.com/fperdigon), [@gyx09212214-prog](https://github.com/gyx09212214-prog), [@RSXLX](https://github.com/RSXLX)。

## [0.2.5] — 2026-05-11

### 新增

- **有数据支撑的情绪分析师。** 更名后的 `sentiment_analyst` 现在会在生成报告前读取真实的 Yahoo News、StockTwits 和 Reddit 数据，取代此前可能在提示压力下捏造社交帖子的流程。(#557, #607)
- **MiniMax 提供商**，包含完整的 M2.x 目录（M2.7 / M2.5 / M2.1 / M2 以及 highspeed 变体，204K 上下文）。双区域：全球（`MINIMAX_API_KEY`）和中国（`MINIMAX_CN_API_KEY`）。
- **双区域 Qwen 和 GLM**，每个区域使用单独的 Key——国际（`DASHSCOPE_API_KEY`、`ZHIPU_API_KEY`）和中国（`DASHSCOPE_CN_API_KEY`、`ZHIPU_CN_API_KEY`），可通过次要区域提示选择。(#758)
- **`DEFAULT_CONFIG` 的 `TRADINGAGENTS_*` 环境变量配置。** 可通过 `.env` 覆盖 `llm_provider`、深度/快速模型 ID、`backend_url`、`output_language`、辩论轮数、检查点标志和基准股票代码，并具有类型感知的转换（string / int / bool）。(#602)
- **CLI 中的交互式 API Key 检测。** 当所选提供商的 Key 缺失时，CLI 会提示输入并将值持久化到 `.env`，使分析运行无需重启即可继续。
- **远程 Ollama 支持。** `OLLAMA_BASE_URL` 将 CLI 和编程客户端指向远程 `ollama-serve`。CLI 会显示解析出的端点，并对常见的错误输入发出警告。为通过 `ollama pull` 拉取的模型新增“Custom model ID”选项。(#648, #768)
- **可配置的新闻获取参数**（位于 `DEFAULT_CONFIG`）——每个股票代码的文章上限、宏观标题上限、回看窗口和宏观搜索查询。(#606, #683)
- **可配置的非美国股票代码 alpha 基准。** 用区域指数替换硬编码的 SPY，适用于 `.NS`（^NSEI）、`.T`（^N225）、`.HK`（^HSI）、`.L`（^FTSE）、`.TO`（^GSPTSE）、`.AX`（^AXJO）、`.BO`（^BSESN）；可显式覆盖 `benchmark_ticker`。消除了汇率漂移主导非美元上市 alpha 的问题。(#628, #684)
- **多语言输出覆盖所有面向用户的智能体**——研究员、风险辩论者、研究经理和交易员，终结此前部分本地化的报告。(#575)
- **模型目录刷新。** OpenAI GPT-5.5 frontier、Anthropic Claude Opus 4.7、Gemini 3.1 Flash-Lite GA、xAI Grok 4.20、Qwen 3.6 系列。仅使用带版本号的 ID；自动切换的别名移至“Custom model ID”选项。

### 变更

- **情绪分析师**现在在 CLI 下拉菜单、状态面板和最终报告中名称一致（此前后端已更名，但 CLI 仍显示“Social Analyst”）。为保存配置的后向兼容保留了 `AnalystType.SOCIAL = "social"` 的传输值。

### 修复

- **结构化输出在 DeepSeek V4 / reasoner 和 MiniMax M2.x 上可用。** 这些提供商根据其工具调用文档拒绝 `tool_choice`；绑定流程现在通过能力表自动跳过它。
- **`pip install .` 安装在以控制台脚本运行 CLI 时会读取项目 `.env`。** (#747)
- **报告端到端保存**——此前流式块会从 `complete_report.md` 中丢失。(#719, #736)
- **股票代码提示保留交易所后缀**（`.SH`、`.SZ`、`.SS`、`.HK`、`.T` 等），适用于 A 股、港股、东京及其他非美国流程。(#770)
- **Docker 权限错误**不再阻止首次运行写入 `~/.tradingagents/`。(#519, #627, #672, #771)
- **配置状态不再在多次运行之间泄漏**（当子字典被修改时）；`set_config` 的部分更新会保留同级默认值。(#788)
- **`max_recur_limit` 配置实际生效**——此前会读取但未转发给传播器。(#764)
- **缺少 API Key 的错误**会指出要设置的确切环境变量。(#680)
- **更安静的启动**——抑制了来自 langgraph-checkpoint 的嘈杂上游 `LangChainPendingDeprecationWarning`；待该包发布修复后将移除。

### 安全

- **每个文件系统路径位置（缓存、检查点数据库、结果）的股票代码路径穿越校验**，使恶意股票代码无法逃逸其预期目录。(#618)

## [0.2.4] — 2026-04-25

### 新增

- **结构化输出决策智能体。** 研究经理、Trader 和投资组合经理现在在主调用中使用 `llm.with_structured_output(Schema)` 并返回类型化的 Pydantic 实例。使用每个提供商原生的结构化输出模式（OpenAI / xAI 使用 `json_schema`，Gemini 使用 `response_schema`，Anthropic 使用 tool-use，OpenAI 兼容提供商使用 function-calling）。渲染辅助函数保留现有 markdown 形态，使记忆日志、CLI 显示和保存的报告保持不变。(#434)
- **LangGraph 检查点恢复**——通过 `--checkpoint` 选择性启用。每个节点后保存状态，使崩溃或中断的运行从最后一个成功步骤恢复。每个股票代码的 SQLite 数据库位于 `~/.tradingagents/cache/checkpoints/`。`--clear-checkpoints` 可重置它们。(#594)
- **持久化决策日志**，取代每个智能体的 BM25 记忆。决策在 `propagate()` 结束时自动存储；下一次同一股票代码的运行会用实际回报、相对 SPY 的 alpha 和一段反思来解析先前的待定条目。可通过 `TRADINGAGENTS_MEMORY_LOG_PATH` 覆盖路径。可选的 `memory_log_max_entries` 配置限制已解析条目；待定条目永远不会被修剪。(#578, #563, #564, #579)
- **DeepSeek、Qwen（阿里 DashScope）、GLM（智谱）和 Azure OpenAI** 提供商，以及动态 OpenRouter 模型选择。
- **Docker 支持**——多阶段构建，分离开发和运行时镜像。
- **`scripts/smoke_structured_output.py`**——针对任意提供商测试三个结构化输出智能体的诊断脚本，贡献者可用一条命令验证其配置。
- **5 档评级量表**（Buy / Overweight / Hold / Underweight / Sell），由研究经理、投资组合经理、信号处理器和记忆日志一致使用；Trader 保留 3 档（Buy / Hold / Sell），因为交易方向天然是三态的。
- **Pytest fixture**——延迟导入 LLM 客户端并提供占位 API Key，使测试套件无需凭据即可干净运行。(#588)

### 变更

- **`backend_url` 默认值现在为 `None`**，而不是 OpenAI URL。每个提供商客户端回退到其原生默认值。此前的默认值会将 OpenAI URL 泄漏到非 OpenAI 客户端（如 Gemini），给切换提供商但未覆盖 `backend_url` 的 Python 用户产生格式错误的请求 URL。CLI 流程不受影响。
- 所有文件 I/O 都传递显式的 `encoding="utf-8"`，因此 Windows 用户不再因 cp1252 默认值遇到 `UnicodeEncodeError`。(#543, #550, #576)
- 缓存和日志目录移至 `~/.tradingagents/`，以解决 Docker 权限问题。(#519)
- `SignalProcessor` 通过确定性启发式从投资组合经理渲染的 markdown 中读取评级——不额外调用 LLM。
- OpenAI 结构化输出调用默认使用 `method="function_calling"`，以避免 langchain-openai 的 Responses-API 解析路径发出的嘈杂 `PydanticSerializationUnexpectedValue` 警告。类型化结果相同，无警告。

### 修复

- 空记忆不再在智能体提示中触发捏造的过往经验；记忆日志重新设计使其在结构上不可能，因为只有投资组合经理会查阅记忆，且仅在存在条目时。(#572)
- 工具调用日志会处理每条块消息，而不仅是最后一条；记忆分数归一化可处理空分数数组。(#534, #531)

### 移除

- `FinancialSituationMemory`（每智能体 BM25 系统）和无效的 `reflect_and_remember()` 管道；由持久化决策日志取代。
- 硬编码的 Google 端点，该端点在 `langchain-google-genai` 改变 API 路径时导致 404。(#493, #496)

### 贡献者

感谢所有通过代码、设计和报告塑造此版本的人：

- [@claytonbrown](https://github.com/claytonbrown) — 检查点恢复 (#594)、测试 fixture (#588)、成本跟踪 (#582) 和结构化验证 (#583) 的设计反馈
- [@Bcardo](https://github.com/Bcardo) — 记忆日志重新设计 (#579)、空记忆幻觉报告 (#572)、编码修复提案 (#570)
- [@voidborne-d](https://github.com/voidborne-d) — 记忆持久化设计 (#564)、投资组合经理状态修复 (#503)
- [@mannubaveja007](https://github.com/mannubaveja007) — 结构化输出功能请求 (#434)
- [@kelder66](https://github.com/kelder66) — 仅 RAM 记忆问题 (#563)
- [@Gujiassh](https://github.com/Gujiassh) — 工具调用日志修复 (#534)、测试桩 PR (#533)
- [@iuyup](https://github.com/iuyup) — 记忆分数归一化修复 (#531)
- [@kaihg](https://github.com/kaihg) — Google base_url 修复 (#496)
- [@32ryh98yfe](https://github.com/32ryh98yfe) — Gemini 404 报告 (#493)
- [@uppb](https://github.com/uppb) — OpenRouter 动态模型选择 (#482)
- [@guoz14](https://github.com/guoz14) — OpenRouter 受限模型报告 (#337)
- [@samchenku](https://github.com/samchenku) — 指标名称规范化 (#490)
- [@JasonOA888](https://github.com/JasonOA888) — y_finance pandas 导入修复 (#488)
- [@tiffanychum](https://github.com/tiffanychum) — 过期导入清理 (#499)
- [@zaizou](https://github.com/zaizou) — Docker 权限问题 (#519)
- [@Stosman123](https://github.com/Stosman123), [@mauropuga](https://github.com/mauropuga), [@hotwind2015](https://github.com/hotwind2015) — Windows 编码缺陷报告 (#543, #550, #576)
- [@nnishad](https://github.com/nnishad), [@atharvajoshi01](https://github.com/atharvajoshi01) — 编码修复提案 (#568, #549)

## [0.2.3] — 2026-03-29

### 新增

- **多语言输出**，适用于分析师报告和最终决策，并提供 CLI 选择器。内部智能体辩论保持英文以保证推理质量。(#472)
- 默认目录中的 **GPT-5.4 系列模型**，具有深度/快速模型拆分。
- **统一模型目录**，作为 CLI 选项和提供商验证的单一事实来源。

### 变更

- `base_url` 会转发给 Google 和 Anthropic 客户端，使企业代理在各提供商间一致工作。(#427)
- 将 Google 的 `api_key` 参数标准化为统一的 `api_key` 形式。

### 修复

- 当 `curr_date` 位于获取窗口中间时，回测获取器不再泄漏前视数据。(#475)
- 来自 LLM 的无效指标名称会在工具边界被捕获，而不是使运行崩溃。(#429)
- yfinance 新闻获取器遵循与价格获取器相同的指数退避重试。(#445)

### 贡献者

- [@ahmedk20](https://github.com/ahmedk20) — 多语言输出 (#472)
- [@CadeYu](https://github.com/CadeYu) — 模型目录类型标注 (#464)
- [@javierdejesusda](https://github.com/javierdejesusda) — 统一 Google API Key 参数 (#453)
- [@voidborne-d](https://github.com/voidborne-d) — yfinance 新闻重试 (#445)
- [@kostakost2](https://github.com/kostakost2) — 前视偏差报告 (#475)
- [@lu-zhengda](https://github.com/lu-zhengda) — 代理/base_url 支持请求 (#427)
- [@VamsiKrishna2021](https://github.com/VamsiKrishna2021) — 无效指标崩溃报告 (#429)

## [0.2.2] — 2026-03-22

### 新增

- 为投资组合经理引入 **五档评级量表**（Buy / Overweight / Hold / Underweight / Sell）。
- 为 Claude 模型提供 **Anthropic effort 级别**支持。
- 为原生 OpenAI 模型提供 **OpenAI Responses API** 路径。

### 变更

- `risk_manager` 重命名为 `portfolio_manager`，以匹配 CLI 显示中展示的角色描述。
- 带交易所限定的股票代码（如 `7203.T`、`BRK.B`）在所有智能体提示和工具调用中保留。
- 尝试进程级 UTF-8 默认值以实现跨平台一致性（注意：此方法实际上未生效；在 v0.2.4 中替换为每次调用显式的 `encoding="utf-8"` 参数）。

### 修复

- yfinance 速率限制错误会以指数退避重试。(#426)
- 支持 HTTP 客户端 SSL 自定义，适用于需要自定义证书包的环境。(#379)
- 报告章节写入能优雅处理字符串列表内容。

### 贡献者

- [@CadeYu](https://github.com/CadeYu) — 带交易所限定的股票代码保留 (#413)
- [@yang1002378395-cmyk](https://github.com/yang1002378395-cmyk) — HTTP 客户端 SSL 自定义 (#379)

## [0.2.1] — 2026-03-15

### 安全

- 修补 `langchain-core` 漏洞（LangGrinch）。(#335)
- 移除受 CVE-2026-22218 影响的 `chainlit` 依赖。

### 新增

- `pyproject.toml` 构建系统配置；项目现在通过现代打包工具安装。

### 移除

- `setup.py`——依赖合并到 `pyproject.toml`。

### 修复

- 风险经理读取正确的基本面报告来源。(#341)
- 所有 `open()` 调用都接收显式的 UTF-8 编码（初始版本）。
- `get_indicators` 工具处理来自 LLM 的逗号分隔指标名称。(#368)
- `Propagation` 会初始化每个辩论状态字段，使风险辩论者不会看到缺失的键。
- 股票数据解析可容忍格式错误的 CSV 和 NaN 值。
- 条件辩论逻辑遵循配置的轮数。(#361)

### 贡献者

- [@RinZ27](https://github.com/RinZ27) — `langchain-core` 安全补丁 (#335)
- [@Ljx-007](https://github.com/Ljx-007) — 风险经理基本面报告修复 (#341)
- [@makk9](https://github.com/makk9) — 辩论轮数配置问题 (#361)

## [0.2.0] — 2026-02-04

这是自最初公开版本以来最大的版本。框架从单提供商转向多提供商架构，
并增加了多个可用于生产的环境。

### 新增

- **多提供商 LLM 支持**（OpenAI、Google、Anthropic、xAI、OpenRouter、Ollama），通过工厂模式实现，并带有提供商特定的 thinking 配置。
- **Alpha Vantage** 集成作为可配置的主要数据提供商，yfinance 作为社区稳定性回退。
- CLI 中的 **页脚统计**：通过 LangChain 回调实时跟踪 LLM 调用、工具调用和 token 使用量。
- **分析后报告保存**——当运行完成时，框架写入按章节的 markdown 文件（分析师报告、辩论记录、最终决策）。
- **公告面板**——从 `api.tauric.ai/v1/announcements` 获取更新，用于 CLI 欢迎界面。
- **工具回退**，使单个供应商中断不会停止流水线。

### 变更

- Risky / Safe 风险辩论者重命名为 **Aggressive / Conservative**，以与显示的智能体标签一致。
- 默认数据供应商切换，以在社区部署中平衡可靠性和配额。
- 更新 Ollama 和 OpenRouter 模型列表；明确默认端点。

### 修复

- 实时显示中的分析师状态跟踪和消息去重。
- 智能体循环中的无限循环防护；反思和日志记录加固。
- 各种数据供应商实现缺陷和工具签名不匹配。

### 贡献者

此版本是第一个有大量外部贡献的版本；2025 年末的许多社区 PR 也在此落地。

- [@luohy15](https://github.com/luohy15) — Alpha Vantage 数据供应商集成 (#235)
- [@EdwardoSunny](https://github.com/EdwardoSunny) — yfinance 获取优化 (#245)
- [@Mirza-Samad-Ahmed-Baig](https://github.com/Mirza-Samad-Ahmed-Baig) — 无限循环防护、反思和日志记录修复 (#89)
- [@ZeroAct](https://github.com/ZeroAct) — 保存结果路径支持 (#29)
- [@Zhongyi-Lu](https://github.com/Zhongyi-Lu) — `.env` gitignore (#49)
- [@csoboy](https://github.com/csoboy) — 本地 Ollama 设置 (#53)
- [@chauhang](https://github.com/chauhang) — 初始 Docker 支持尝试 (#47，后回滚；合并的 Docker 支持在 v0.2.4 发布)

## [0.1.1] — 2025-06-07

### 移除

- 曾与 v0.1.0 捆绑的静态站点资源；公开站点现已独立存在。

## [0.1.0] — 2025-06-05

### 新增

- TradingAgents 多智能体交易框架的 **首次公开版本**：市场 / 情绪 / 新闻 / 基本面分析师；看多和看空研究员；交易员；激进、保守和中立风险辩论者；投资组合经理。LangGraph 编排、yfinance 数据、每智能体 BM25 记忆、单提供商 OpenAI 集成、交互式 CLI。

[0.2.4]: https://github.com/TauricResearch/TradingAgents/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/TauricResearch/TradingAgents/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/TauricResearch/TradingAgents/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/TauricResearch/TradingAgents/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/TauricResearch/TradingAgents/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/TauricResearch/TradingAgents/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/TauricResearch/TradingAgents/releases/tag/v0.1.0
