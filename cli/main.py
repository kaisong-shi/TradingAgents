import sys
from enum import StrEnum
from typing import Annotated

import typer
from rich.markup import escape

from cli.display import console
from cli.models import AnalystType, AssetType
from cli.prompts import filter_analysts_for_asset_type, parse_analysts
from cli.run import run_analysis
from tradingagents.backtest import iter_grid, run_backtest, summarize
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.llm_clients.openai_client import SIGNED_IN_PROVIDERS
from tradingagents.portfolio import load_portfolio

# prompt_toolkit's win32 output module is importable only on Windows (it asserts
# the platform at import time), so gate on the platform rather than catching the
# failure — that way a genuinely broken prompt_toolkit on Windows still surfaces
# instead of silently disabling the handler below. Off Windows this stays an
# empty tuple, which `except` accepts and never matches (#1138).
if sys.platform == "win32":  # pragma: no cover - platform dependent
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError

    _NO_CONSOLE_ERRORS: tuple[type[BaseException], ...] = (NoConsoleScreenBufferError,)
else:
    _NO_CONSOLE_ERRORS = ()

app = typer.Typer(
    name="TradingAgents",
    help="TradingAgents CLI：多智能体 LLM 金融交易框架",
    add_completion=True,  # Enable shell completion
)


@app.callback(invoke_without_command=True)
def analyze(
    ctx: typer.Context,
    checkpoint: bool | None = typer.Option(
        None,
        "--checkpoint/--no-checkpoint",
        help="启用/禁用断点续跑（每个节点后保存状态，使崩溃的运行可以继续）。"
        "省略时遵循 TRADINGAGENTS_CHECKPOINT_ENABLED。",
    ),
    clear_checkpoints: bool = typer.Option(
        False,
        "--clear-checkpoints",
        help="运行前删除所有已保存的断点（强制全新开始）。",
    ),
    portfolio: str = typer.Option(
        None,
        "--portfolio",
        help="包含当前持仓和现金的 JSON 文件，使交易员、风险与投资组合智能体"
        "按你的实际仓位进行决策。",
    ),
    ticker: str = typer.Option(None, "--ticker", help="要分析的股票代码，例如 NVDA 或 0700.HK；跳过提问"),
    date: str = typer.Option(None, "--date", help="分析日期，YYYY-MM-DD；跳过提问"),
    analysts: str = typer.Option(
        None, "--analysts", help="逗号分隔的分析师，例如 market,news；跳过提问"
    ),
    save: bool | None = typer.Option(
        None, "--save/--no-save", help="无需询问，将报告保存到 results_dir"
    ),
    show: bool | None = typer.Option(
        None, "--show/--no-show", help="无需询问，在结束时显示完整报告"
    ),
    html: bool | None = typer.Option(
        None, "--html/--no-html",
        help="无需询问，额外将报告保存为单个 HTML 页面 complete_report.html（默认：是）",
    ),
):
    """运行一次分析。直接执行 `tradingagents` 即是此命令。

    命令行参数可回答对应问题；若提供商、模型、深度和语言也通过
    TRADINGAGENTS_* 环境变量设置，则运行过程不会提问。
    """
    if ctx.invoked_subcommand is not None:
        return
    if clear_checkpoints:
        from tradingagents.graph.checkpointer import clear_all_checkpoints
        n = clear_all_checkpoints(DEFAULT_CONFIG["data_cache_dir"])
        console.print(f"[yellow]已清除 {n} 个断点。[/yellow]")
    portfolio_context = None
    if portfolio:
        try:
            portfolio_context = load_portfolio(portfolio)
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            raise typer.Exit(code=1) from None

    try:
        flags = {"ticker": ticker, "date": date, "analysts": analysts, "save": save, "show": show, "html": html}
        run_analysis(checkpoint=checkpoint, portfolio=portfolio_context, flags=flags)
    except _NO_CONSOLE_ERRORS:
        # A terminal with no console buffer cannot host the interactive prompts.
        # Emit one actionable line on stderr instead of a prompt_toolkit
        # traceback; plain text, since rich may not render here either (#1138).
        typer.echo(
            "错误：没有可用的 Windows 控制台。交互式 CLI 需要真实的控制台缓冲区 — "
            "请从 Windows Terminal、PowerShell 或 cmd.exe 运行，而不要使用管道或嵌入式终端。",
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def backtest(
    tickers: str = typer.Argument(..., help="逗号分隔的股票代码，例如 NVDA,AAPL"),
    start: str = typer.Option(..., "--start", help="首个分析日期，YYYY-MM-DD"),
    end: str = typer.Option(..., "--end", help="最后一个分析日期，YYYY-MM-DD"),
    every: int = typer.Option(7, "--every", help="分析日期之间的天数间隔"),
    analysts: str = typer.Option(
        None, "--analysts", help="逗号分隔要运行的分析师：market、sentiment、news、fundamentals；省略则运行该资产类型允许的全部"
    ),
    asset_type: str = typer.Option("stock", "--asset-type", help="stock 或 crypto"),
    portfolio: str = typer.Option(
        None, "--portfolio", help="包含持仓和现金的 JSON 文件，在网格中保持不变"
    ),
    run_id: str = typer.Option(
        None, "--run-id", help="继续之前的回测：跳过已完成的单元格并复用其日志"
    ),
):
    """在多个股票代码和日期的网格上为历史决策打分。"""

    try:
        dates = iter_grid(start, end, every)
        book = load_portfolio(portfolio) if portfolio else None
        kind = AssetType(asset_type.strip().lower())
        # The analysts are named and checked as for an analysis; without a
        # choice, every analyst the asset type allows runs.
        chosen = (parse_analysts(analysts, kind) if analysts
                  else filter_analysts_for_asset_type(list(AnalystType), kind))
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from None

    names = [t.strip() for t in tickers.split(",") if t.strip()]
    if not names:
        console.print("[red]没有可分析的 ticker；请用逗号分隔传入，例如 NVDA,AAPL[/red]")
        raise typer.Exit(code=1)

    def show_progress(done, total, ticker, date):
        console.print(f"[dim][{done}/{total}] {ticker} {date}[/dim]")

    kwargs = {"asset_type": kind.value, "portfolio": book, "run_id": run_id, "progress": show_progress,
              "selected_analysts": [a.value for a in chosen]}

    try:
        result = run_backtest(names, dates, DEFAULT_CONFIG, **kwargs)
    except Exception as exc:  # a missing key or an unknown analyst is a setup error
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from None
    console.print(summarize(result).render())
    console.print(f"\n运行了 {result.cells_run} 个单元格，跳过了 {result.skipped} 个。日志：{result.log_path}")
    console.print(f"继续或结算本次回测：--run-id {result.run_id}")
    for ticker, date, reason in result.failures:
        console.print(f"[yellow]失败：[/yellow] {ticker} {date}：{reason}")
    for ticker, reason in result.settlement_failures:
        console.print(f"[yellow]未结算：[/yellow] {ticker}：{reason}")


# The plans `login` and `logout` take: the providers signed in to, not keyed.
Plan = StrEnum("Plan", {name: name for name in SIGNED_IN_PROVIDERS})


@app.command()
def login(plan: Annotated[Plan, typer.Argument(help="用于登录的套餐")]):
    """使用你的 ChatGPT Plus 或 Pro 套餐登录（chatgpt 提供商）。"""
    from tradingagents.llm_clients import chatgpt_auth

    try:
        # One unwrapped line, so the sign-in address can be copied whole.
        email = chatgpt_auth.sign_in(
            say=lambda line: console.print(line, soft_wrap=True, markup=False, highlight=False))
    except chatgpt_auth.ChatGPTAuthError as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from None
    console.print(f"[green]已登录 ChatGPT，账号：{escape(email)}。[/green]")


@app.command()
def logout(plan: Annotated[Plan, typer.Argument(help="要退出登录的套餐")]):
    """退出你的 ChatGPT 套餐：撤销本机访问权限并清除登录信息。"""
    from tradingagents.llm_clients import chatgpt_auth

    outcome = chatgpt_auth.sign_out()
    if outcome == "revoked":
        console.print("已退出 ChatGPT。")
    elif outcome == "forgotten":
        console.print("[yellow]已在此设备退出，但无法连接 OpenAI 来撤销登录；"
                      "该登录在 OpenAI 侧仍有效，直到过期。[/yellow]")
    else:
        console.print("尚未登录 ChatGPT。")


if __name__ == "__main__":
    app()
