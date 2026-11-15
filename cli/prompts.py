import datetime
import os
import subprocess
import sys
from pathlib import Path

import questionary
import typer
from dotenv import find_dotenv, set_key
from rich.markup import escape

from cli.display import console
from cli.models import AnalystType, AssetType
from tradingagents.dataflows.symbols import safe_ticker_component
from tradingagents.llm_clients.api_key_env import get_api_key_env
from tradingagents.llm_clients.model_catalog import get_model_options
from tradingagents.llm_clients.openai_client import OPENAI_COMPATIBLE_PROVIDERS, SIGNED_IN_PROVIDERS

TICKER_INPUT_EXAMPLES = "SPY, 0700.HK, BTC-USD"

ANALYST_CHOICES = [
    ("市场分析师", AnalystType.MARKET),
    ("情绪分析师", AnalystType.SOCIAL),
    ("新闻分析师", AnalystType.NEWS),
    ("基本面分析师", AnalystType.FUNDAMENTALS),
]

CRYPTO_SUFFIXES = ("-USD", "-USDT", "-USDC", "-BTC", "-ETH")


# The style of every selection menu.
_MENU_STYLE = questionary.Style([
    ("selected", "fg:magenta noinherit"),
    ("highlighted", "fg:magenta noinherit"),
    ("pointer", "fg:magenta noinherit"),
])


def is_valid_ticker_input(value: str) -> bool:
    """Whether a ticker entry names a symbol the run can use.

    The symbol it resolves to (``XAUUSD+`` -> ``GC=F``) must pass the data
    layer's own check, so the prompt refuses exactly what the run would.
    Empty input is allowed (it defaults to SPY downstream).
    """
    if not value.strip():
        return True
    try:
        safe_ticker_component(normalize_ticker_symbol(value))
    except ValueError:
        return False
    return True


def get_ticker() -> str:
    """Prompt the user to enter a ticker symbol, preserving exchange suffixes.

    Uses questionary.text (not typer.prompt, which strips trailing dot-suffixes
    like ``000404.SH`` on some shells) and validates the symbol charset so an
    obvious typo is caught before the run starts.
    """
    ticker = questionary.text(
        f"请输入股票代码（例如 {TICKER_INPUT_EXAMPLES}）：",
        validate=lambda x: (
            is_valid_ticker_input(x)
            or "请输入有效的股票代码，例如 AAPL、000404.SZ、0700.HK、GC=F。"
        ),
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if ticker is None:
        console.print("\n[red]未提供股票代码，正在退出...[/red]")
        exit(1)

    return normalize_ticker_symbol(ticker) if ticker.strip() else "SPY"


def parse_ticker(value: str) -> str:
    """A ticker given on the command line, canonical; empty or malformed is refused."""
    if not value.strip() or not is_valid_ticker_input(value):
        raise ValueError(f"不是有效的股票代码：{value!r}（例如 {TICKER_INPUT_EXAMPLES}）")
    return normalize_ticker_symbol(value)


def parse_analysis_date(value: str) -> str:
    """An analysis date as YYYY-MM-DD, today or earlier."""
    try:
        day = datetime.datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"不是有效日期：{value!r}；请使用 YYYY-MM-DD") from None
    if day > datetime.date.today():
        raise ValueError(f"{value} 是未来日期")
    return day.isoformat()


def parse_analysts(value: str, asset_type: AssetType) -> list[AnalystType]:
    """Comma-separated analyst names, in the canonical order, checked against the asset."""
    # "sentiment" is the name users see; the analyst's key is "social".
    names = [{"sentiment": "social"}.get(n, n) for n in (n.strip().lower() for n in value.split(",")) if n]
    if not names:
        raise ValueError("请至少指定一位分析师")
    known = {a.value: a for a in AnalystType}
    unknown = [n for n in names if n not in known]
    if unknown:
        choices = ", ".join("sentiment" if name == "social" else name for name in known)
        raise ValueError(f"未知分析师：{', '.join(unknown)}；请从 {choices} 中选择")
    available = filter_analysts_for_asset_type(list(known.values()), asset_type)
    unavailable = [n for n in names if known[n] not in available]
    if unavailable:
        raise ValueError(f"{', '.join(unavailable)} 不适用于资产类型 {asset_type.value}")
    return [a for a in available if a.value in names]


def normalize_ticker_symbol(ticker: str) -> str:
    """Resolve user input to its canonical Yahoo symbol (single source of truth).

    Delegates to the data layer's ``normalize_symbol`` so the symbol the CLI
    passes through the pipeline is exactly the one the data path will price
    (e.g. ``BTCUSD`` -> ``BTC-USD``, ``XAUUSD`` -> ``GC=F``). Falls back to the
    plain upper-case if the data layer is unavailable.
    """
    try:
        from tradingagents.dataflows.symbols import normalize_symbol

        return normalize_symbol(ticker)
    except Exception:
        return ticker.strip().upper()


def detect_asset_type(ticker: str) -> AssetType:
    """Classify on the canonical symbol so e.g. BTCUSD and BTC-USDT both read as
    crypto (#981/#982), matching what the data path will actually fetch."""
    canonical = normalize_ticker_symbol(ticker)
    if canonical.endswith(CRYPTO_SUFFIXES):
        return AssetType.CRYPTO
    return AssetType.STOCK


def filter_analysts_for_asset_type(
    analysts: list[AnalystType], asset_type: AssetType
) -> list[AnalystType]:
    if asset_type != AssetType.CRYPTO:
        return analysts
    return [
        analyst
        for analyst in analysts
        if analyst != AnalystType.FUNDAMENTALS
    ]


def _mode_label(mode: str) -> str:
    """The Chinese label for a model tier: quick -> 快速, deep -> 深度."""
    return {"quick": "快速", "deep": "深度"}.get(mode.lower(), mode)


def _matching_choice(options, default):
    """The option value equal to ``default``, or None to leave the menu as is."""
    return next((value for _, value in options if value == default), None)


def select_analysts(asset_type: AssetType = AssetType.STOCK, default=None) -> list[AnalystType]:
    """Select analysts using an interactive checkbox.

    ``default`` pre-checks the previous run's analysts; the prompt still shows.
    """
    available_analysts = filter_analysts_for_asset_type(
        [value for _, value in ANALYST_CHOICES],
        asset_type,
    )
    choices = questionary.checkbox(
        "选择你的 [分析师团队]：",
        choices=[
            questionary.Choice(display, value=value, checked=value.value in (default or []))
            for display, value in ANALYST_CHOICES
            if value in available_analysts
        ],
        instruction="\n- 按空格键选择/取消选择分析师\n- 按 'a' 全选/取消全选\n- 完成后按回车",
        validate=lambda x: len(x) > 0 or "必须至少选择一位分析师。",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        console.print("\n[red]未选择分析师，正在退出...[/red]")
        exit(1)

    return choices


def select_research_depth(default=None) -> int:
    """Select research depth using an interactive selection."""

    DEPTH_OPTIONS = [
        ("浅度 - 快速研究，辩论与策略讨论轮次较少", 1),
        ("中等 - 折中方案，适度的辩论与策略讨论", 3),
        ("深度 - 全面研究，深入的辩论与策略讨论", 5),
    ]

    choice = questionary.select(
        "选择你的 [研究深度]：",
        choices=[
            questionary.Choice(display, value=value) for display, value in DEPTH_OPTIONS
        ],
        default=_matching_choice(DEPTH_OPTIONS, default),
        instruction="\n- 使用方向键导航\n- 按回车键选择",
        style=questionary.Style(
            [
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]未选择研究深度，正在退出...[/red]")
        exit(1)

    return choice


# Mainstream OpenRouter chat-LLM provider namespaces. We surface the newest
# models from these rather than the universal-newest, which is dominated by
# niche/experimental releases. These are the general-purpose chat providers;
# more enterprise/specialised namespaces (nvidia, cohere, amazon, ...) tend to
# ship research/safety variants as their newest, so they're left out of the
# shortlist. Provider names are stable (unlike model IDs), so this rarely needs
# touching; anything not here is still reachable via Custom ID.
_OPENROUTER_MAINSTREAM = {
    "openai", "anthropic", "google", "deepseek", "qwen", "mistralai",
    "meta-llama", "x-ai", "z-ai", "minimax", "moonshotai",
}


def _fetch_openrouter_models() -> list[tuple[str, str]]:
    """Fetch available models from the OpenRouter API."""
    import requests
    try:
        resp = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        resp.raise_for_status()
        models = resp.json().get("data", [])
        # Newest first so the top-N shown really is the latest available — the
        # API currently returns this order, but sort explicitly so the prompt's
        # "latest available" label holds regardless of response ordering.
        models.sort(key=lambda m: m.get("created") or 0, reverse=True)
        return [(m.get("name") or m["id"], m["id"]) for m in models]
    except Exception as e:
        console.print(f"\n[yellow]无法获取 OpenRouter 模型：{e}[/yellow]")
        return []


def select_chatgpt_model(mode: str, default=None) -> str:
    """Select one of the ChatGPT plan's models, or enter a model ID."""
    from tradingagents.llm_clients import chatgpt_auth
    try:
        models = chatgpt_auth.list_models()
    except Exception as e:
        console.print(f"\n[yellow]无法列出你的 ChatGPT 套餐模型：{escape(str(e))}[/yellow]")
        models = []
    return _select_listed_model(f"选择你的 [{_mode_label(mode)}思考] ChatGPT 套餐模型：",
                                models, default, _prompt_custom_model_id)


def _select_listed_model(title: str, models, default, custom) -> str:
    """Select from ``models`` ((name, model ID) pairs, listed live) or enter one with ``custom``."""
    choices = [questionary.Choice(name, value=mid) for name, mid in models]
    choices.append(questionary.Choice("自定义模型 ID", value="custom"))
    choice = questionary.select(
        title,
        choices=choices,
        default=default if any(c.value == default for c in choices) else None,
        instruction="\n- 使用方向键导航\n- 按回车键选择",
        style=_MENU_STYLE,
    ).ask()
    if choice is None:
        console.print("\n[red]未选择模型，正在退出...[/red]")
        exit(1)
    return custom() if choice == "custom" else choice


def _require_text(message: str, hint: str) -> str:
    """Prompt for a required value; exit cleanly if the user cancels.

    ``questionary.text(...).ask()`` returns None on Ctrl-C/Esc; mirror the
    exit-on-cancel behavior of the other required selections so a cancelled
    prompt never returns an empty model/deployment that would fail downstream.
    """
    response = questionary.text(
        message,
        validate=lambda x: len(x.strip()) > 0 or hint,
    ).ask()
    if response is None:
        console.print("\n[red]已取消，正在退出...[/red]")
        exit(1)
    return response.strip()


def select_openrouter_model(mode: str, default=None) -> str:
    """Select an OpenRouter model from the newest available, or enter a custom ID.

    ``mode`` ("quick"/"deep") labels the prompt so the two consecutive
    OpenRouter selections are distinguishable, like the other providers (#1000).
    """
    models = _fetch_openrouter_models()  # newest first
    # Prefer the newest from mainstream providers so the shortlist isn't crowded
    # out by niche/experimental releases; fall back to all if none match.
    mainstream = [
        (name, mid) for name, mid in models
        if not mid.startswith("~")  # skip variant/alias duplicate routes
        and mid.split("/", 1)[0] in _OPENROUTER_MAINSTREAM
    ]
    top = (mainstream or models)[:5]
    return _select_listed_model(
        f"选择你的 [{_mode_label(mode)}思考] OpenRouter 模型（最新可用）：", top, default,
        lambda: _require_text("输入 OpenRouter 模型 ID（例如 google/gemma-4-26b-a4b-it）：",
                              "请输入模型 ID。"))


# Providers whose models are listed live, with the menu that offers them.
LISTED_LIVE = {"openrouter": select_openrouter_model, "chatgpt": select_chatgpt_model}


def _prompt_custom_model_id() -> str:
    """Prompt user to type a custom model ID."""
    return _require_text("输入模型 ID：", "请输入模型 ID。")


def _select_model(provider: str, mode: str, default=None) -> str:
    """Select a model for the given provider and mode (quick/deep)."""
    listed = LISTED_LIVE.get(provider.lower())
    if listed is not None:
        return listed(mode, default)

    if provider.lower() == "azure":
        return _require_text(
            f"输入 Azure 部署名称（{mode}-thinking）：",
            "请输入部署名称。",
        )

    choice = questionary.select(
        f"选择你的 [{_mode_label(mode)}思考 LLM 引擎]：",
        choices=[
            questionary.Choice(display, value=value)
            for display, value in get_model_options(provider, mode)
        ],
        default=_matching_choice(get_model_options(provider, mode), default),
        instruction="\n- 使用方向键导航\n- 按回车键选择",
        style=_MENU_STYLE,
    ).ask()

    if choice is None:
        console.print(f"\n[red]未选择 {mode} 思考 LLM 引擎，正在退出...[/red]")
        exit(1)

    if choice == "custom":
        return _prompt_custom_model_id()

    return choice


def select_shallow_thinking_agent(provider, default=None) -> str:
    """Select shallow thinking llm engine using an interactive selection."""
    return _select_model(provider, "quick", default)


def select_deep_thinking_agent(provider, default=None) -> str:
    """Select deep thinking llm engine using an interactive selection."""
    return _select_model(provider, "deep", default)


def _llm_provider_table() -> list[tuple[str, str, str | None]]:
    """(display_name, provider_key, base_url) for every supported provider.

    Shared by the interactive picker and by env-driven configuration so an
    env-set provider resolves to the same default endpoint the menu uses.
    Ollama users can point at a remote ollama-serve via OLLAMA_BASE_URL
    (convention from the broader Ollama ecosystem); falls back to the
    localhost default when unset.
    """
    ollama_url = os.environ.get("OLLAMA_BASE_URL") or "http://localhost:11434/v1"
    return [
        ("OpenAI", "openai", "https://api.openai.com/v1"),
        ("Google", "google", None),
        ("Anthropic", "anthropic", "https://api.anthropic.com/"),
        ("ChatGPT（Plus 或 Pro 套餐）", "chatgpt", "https://api.openai.com/v1"),
        ("xAI", "xai", "https://api.x.ai/v1"),
        ("DeepSeek", "deepseek", "https://api.deepseek.com"),
        ("Qwen", "qwen", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        # Z.AI international, the platform ZHIPU_API_KEY belongs to; the CN
        # platform is the separate glm-cn key, chosen in the region prompt.
        ("GLM", "glm", "https://api.z.ai/api/paas/v4/"),
        ("MiniMax", "minimax", "https://api.minimax.io/v1"),
        ("OpenRouter", "openrouter", "https://openrouter.ai/api/v1"),
        ("Mistral", "mistral", "https://api.mistral.ai/v1"),
        ("Kimi (Moonshot)", "kimi", "https://api.moonshot.ai/v1"),
        ("Groq", "groq", "https://api.groq.com/openai/v1"),
        ("NVIDIA NIM", "nvidia", "https://integrate.api.nvidia.com/v1"),
        ("Azure OpenAI", "azure", None),
        ("Amazon Bedrock", "bedrock", None),
        ("Ollama", "ollama", ollama_url),
        ("OpenAI 兼容（vLLM、LM Studio、llama.cpp、自定义中转）", "openai_compatible", None),
    ]


def provider_default_url(provider_key: str) -> str | None:
    """Return the default backend URL for a provider key, or None if unknown."""
    key = provider_key.lower()
    for _, pk, url in _llm_provider_table():
        if pk == key:
            return url
    return None


def resolve_backend_url(
    provider: str, menu_url: str | None = None, env_url: str | None = None
) -> str | None:
    """Resolve the backend URL with the correct precedence.

    An explicit env override (``env_url``, from ``TRADINGAGENTS_LLM_BACKEND_URL``
    via ``DEFAULT_CONFIG['backend_url']``) is honored regardless of how the
    provider was chosen — interactively or from the environment (#978).
    Otherwise the menu/region URL, then the provider's default.
    """
    return env_url or menu_url or provider_default_url(provider)


def prompt_openai_compatible_url(default=None) -> str:
    """Prompt for a custom OpenAI-compatible endpoint base URL."""
    url = questionary.text(
        "输入 OpenAI 兼容的 base URL "
        "（例如 vLLM 用 http://localhost:8000/v1，LM Studio 用 http://localhost:1234/v1）：",
        default=default or "",
        validate=lambda x: x.strip().startswith(("http://", "https://"))
        or "请输入以 http:// 或 https:// 开头的 URL",
    ).ask()
    if not url:
        console.print("\n[red]未提供端点 URL，正在退出...[/red]")
        exit(1)
    return url.strip()


# The menu entry that groups the providers used through a personal plan.
_SUBSCRIPTION = ("subscription", None)


def select_llm_provider(default=None) -> tuple[str, str | None]:
    """Select the LLM provider and its API endpoint."""
    PROVIDERS = _llm_provider_table()
    # A region-specific key (qwen-cn) is chosen in a later prompt; the menu
    # lists the base provider.
    base = (default or "").split("-cn")[0]
    choices = []
    for display, provider_key, url in PROVIDERS:
        if provider_key in SIGNED_IN_PROVIDERS:
            continue
        choices.append(questionary.Choice(display, value=(provider_key, url)))
        if provider_key == "anthropic":
            choices.append(questionary.Choice("订阅（使用你的 ChatGPT 套餐）", value=_SUBSCRIPTION))
    preselected = _SUBSCRIPTION if base in SIGNED_IN_PROVIDERS else next(
        ((key, url) for _, key, url in PROVIDERS if key == base), None
    )

    choice = questionary.select(
        "选择你的 LLM 提供商：",
        choices=choices,
        default=preselected,
        instruction="\n- 使用方向键导航\n- 按回车键选择",
        style=_MENU_STYLE,
    ).ask()

    if choice is None:
        console.print("\n[red]未选择 LLM 提供商，正在退出...[/red]")
        exit(1)

    if choice == _SUBSCRIPTION:
        choice = questionary.select(
            "选择你的订阅：",
            choices=[questionary.Choice(display, value=(key, url))
                     for display, key, url in PROVIDERS if key in SIGNED_IN_PROVIDERS],
            style=_MENU_STYLE,
        ).ask()
        if choice is None:
            console.print("\n[red]未选择订阅，正在退出...[/red]")
            exit(1)

    provider, url = choice
    return provider, url


def ask_openai_reasoning_effort() -> str:
    """Ask for OpenAI reasoning effort level."""
    choices = [
        questionary.Choice("中等（默认）", "medium"),
        questionary.Choice("高（更全面）", "high"),
        questionary.Choice("低（更快）", "low"),
    ]
    return questionary.select(
        "选择推理强度：",
        choices=choices,
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
            ("pointer", "fg:cyan noinherit"),
        ]),
    ).ask()


def ask_anthropic_effort() -> str | None:
    """Ask for Anthropic effort level.

    Controls token usage and response thoroughness on Claude 4.5 / 4.6 / 4.7
    models. The API also accepts "max"; we expose low/medium/high as the
    common selection range.
    """
    return questionary.select(
        "选择力度等级：",
        choices=[
        questionary.Choice("高（推荐）", "high"),
        questionary.Choice("中等（平衡）", "medium"),
        questionary.Choice("低（更快、更便宜）", "low"),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
            ("pointer", "fg:cyan noinherit"),
        ]),
    ).ask()


def ask_gemini_thinking_config() -> str | None:
    """Ask for Gemini thinking configuration.

    Returns thinking_level: "high" or "minimal".
    Client maps to appropriate API param based on model series.
    """
    return questionary.select(
        "选择思考模式：",
        choices=[
        questionary.Choice("启用思考（推荐）", "high"),
        questionary.Choice("最小/禁用思考", "minimal"),
        ],
        style=questionary.Style([
            ("selected", "fg:green noinherit"),
            ("highlighted", "fg:green noinherit"),
            ("pointer", "fg:green noinherit"),
        ]),
    ).ask()


def ask_glm_region() -> tuple[str, str]:
    """Ask which GLM platform (Z.AI international vs BigModel China) to use.

    Zhipu serves the same GLM models under two brands with separate
    accounts; keys aren't interchangeable. Returns (provider_key, backend_url).
    """
    return questionary.select(
        "选择 GLM 平台：",
        choices=[
            questionary.Choice(
                "Z.AI — api.z.ai（国际版，使用 ZHIPU_API_KEY）",
                value=("glm", "https://api.z.ai/api/paas/v4/"),
            ),
            questionary.Choice(
                "BigModel — open.bigmodel.cn（中国版，使用 ZHIPU_CN_API_KEY）",
                value=("glm-cn", "https://open.bigmodel.cn/api/paas/v4/"),
            ),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
            ("pointer", "fg:cyan noinherit"),
        ]),
    ).ask()


def ask_qwen_region() -> tuple[str, str]:
    """Ask which Qwen region (international vs China) to use.

    Alibaba DashScope exposes two endpoints with separate accounts —
    a key from one region does NOT authenticate against the other
    (fixes #758). Returns (provider_key, backend_url).
    """
    return questionary.select(
        "选择 Qwen 区域：",
        choices=[
            questionary.Choice(
                "国际版 — dashscope-intl.aliyuncs.com（使用 DASHSCOPE_API_KEY）",
                value=("qwen", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
            ),
            questionary.Choice(
                "中国版 — dashscope.aliyuncs.com（使用 DASHSCOPE_CN_API_KEY）",
                value=("qwen-cn", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            ),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
            ("pointer", "fg:cyan noinherit"),
        ]),
    ).ask()


def ask_minimax_region() -> tuple[str, str]:
    """Ask which MiniMax region (global vs China) to use.

    MiniMax exposes two endpoints with separate accounts — a key from
    one region does NOT authenticate against the other. Returns
    (provider_key, backend_url).
    """
    return questionary.select(
        "选择 MiniMax 区域：",
        choices=[
            questionary.Choice(
                "全球版 — api.minimax.io（使用 MINIMAX_API_KEY）",
                value=("minimax", "https://api.minimax.io/v1"),
            ),
            questionary.Choice(
                "中国版 — api.minimaxi.com（使用 MINIMAX_CN_API_KEY）",
                value=("minimax-cn", "https://api.minimaxi.com/v1"),
            ),
        ],
        style=questionary.Style([
            ("selected", "fg:cyan noinherit"),
            ("highlighted", "fg:cyan noinherit"),
            ("pointer", "fg:cyan noinherit"),
        ]),
    ).ask()


def confirm_ollama_endpoint(url: str) -> None:
    """Show the resolved Ollama endpoint after provider selection.

    Surfaces three things the user benefits from seeing before model
    selection: which URL we'll actually hit, where it came from
    (`OLLAMA_BASE_URL` vs default), and a soft warning if the URL is
    missing the scheme/port that ollama-serve expects. The warning is
    advisory only — we don't reject malformed input, since the user may
    be doing something deliberately unusual (e.g. a reverse-proxy path).
    """
    from_env = os.environ.get("OLLAMA_BASE_URL")
    origin = "（来自 OLLAMA_BASE_URL）" if from_env and from_env == url else ""
    console.print(f"[green]✓ 正在使用 Ollama：{url}{origin}[/green]")

    if not url.startswith(("http://", "https://")):
        console.print(
            f"[yellow]注意：{url!r} 缺少协议前缀。"
            f"Ollama-serve 通常期望形如 "
            f"http://<host>:11434/v1 的 URL。[/yellow]"
        )
    elif ":11434" not in url and "://localhost" not in url and "://127.0.0.1" not in url:
        # Soft hint when the port differs from the ollama-serve default
        # and the host isn't local (where users sometimes proxy on :80).
        console.print(
            f"[yellow]注意：{url!r} 未包含端口 11434。"
            f"请确认你的远程 ollama-serve 正在上述端口上监听。[/yellow]"
        )


def ensure_signed_in(provider: str) -> None:
    """Make sure a plan provider's sign-in works before the run, offering to sign in now.

    Signing in runs as its own process (``tradingagents login chatgpt``), so its
    read of a pasted address ends with it and never takes a later answer."""
    if provider.lower() not in SIGNED_IN_PROVIDERS:
        return
    from tradingagents.llm_clients import chatgpt_auth  # the one signed-in provider

    try:
        chatgpt_auth.access_token()
    except chatgpt_auth.ChatGPTUnreachable as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from None
    except chatgpt_auth.ChatGPTAuthError as exc:
        if not sys.stdin.isatty():
            console.print(f"[red]{escape(str(exc))}[/red]")
            raise typer.Exit(code=1) from None
        console.print(f"\n[yellow]{escape(str(exc))}[/yellow]")
        # -P keeps a cli/ package in the working directory from shadowing ours.
        login = [sys.executable, "-P", "-m", "cli.main", "login", "chatgpt"]
        if subprocess.run(login).returncode != 0:
            raise typer.Exit(code=1) from None
    console.print(f"[green]✓ 正在使用你的 ChatGPT 套餐：[/green] {escape(chatgpt_auth.signed_in_as() or '')}")


def ensure_api_key(provider: str) -> str | None:
    """Make sure the API key for `provider` is available in the environment.

    If the env var is already set, returns its value untouched. Otherwise
    interactively prompts the user, persists the value to the project's
    .env file via python-dotenv's set_key (creating .env if needed), and
    exports it into os.environ so the current process picks it up.

    Returns None for providers that do not require a key (e.g. ollama)
    and for providers not found in the canonical mapping.
    """
    env_var = get_api_key_env(provider)
    if env_var is None:
        return None  # ollama / unknown — no key check possible

    # Key-optional providers (generic OpenAI-compatible / local servers) read the
    # key when present but must never force an interactive prompt.
    spec = OPENAI_COMPATIBLE_PROVIDERS.get(provider.lower())
    if spec is not None and spec.key_optional:
        return os.environ.get(env_var)

    existing = os.environ.get(env_var)
    if existing:
        return existing

    if not sys.stdin.isatty():
        console.print(f"[red]{env_var} 未设置，且没有终端可用于询问。[/red]")
        raise typer.Exit(code=1)

    console.print(
        f"\n[yellow]你的环境中未设置 {env_var}。[/yellow]"
    )
    key = questionary.password(
        f"粘贴你的 {env_var}（将保存到 .env）：",
        style=questionary.Style([
            ("text", "fg:cyan"),
            ("highlighted", "noinherit"),
        ]),
    ).ask()
    if not key:
        console.print(
            f"[red]已跳过。在设置 {env_var} 之前，API 调用将会失败。[/red]"
        )
        return None

    env_path = find_dotenv(usecwd=True) or str(Path.cwd() / ".env")
    # The file holds credentials, so make it owner-only before writing: create
    # it 0600 when absent, and tighten an existing one (set_key keeps the mode).
    if not os.path.exists(env_path):
        os.close(os.open(env_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600))
    os.chmod(env_path, 0o600)
    set_key(env_path, env_var, key)
    os.environ[env_var] = key
    console.print(f"[green]已将 {env_var} 保存到 {env_path}[/green]")
    return key


def ask_output_language(default=None) -> str:
    """Ask for report output language.

    ``default`` is offered only when it is one of the listed languages: a custom
    one entered last time is free text, which the menu cannot preselect.
    """
    choices = [
        questionary.Choice("英语（默认）", "English"),
        questionary.Choice("中文", "Chinese"),
        questionary.Choice("日语（日本語）", "Japanese"),
        questionary.Choice("韩语（한국어）", "Korean"),
        questionary.Choice("印地语（हिन्दी）", "Hindi"),
        questionary.Choice("西班牙语（Español）", "Spanish"),
        questionary.Choice("葡萄牙语（Português）", "Portuguese"),
        questionary.Choice("法语（Français）", "French"),
        questionary.Choice("德语（Deutsch）", "German"),
        questionary.Choice("阿拉伯语（العربية）", "Arabic"),
        questionary.Choice("俄语（Русский）", "Russian"),
        questionary.Choice("自定义语言", "custom"),
    ]
    choice = questionary.select(
        "选择输出语言：",
        choices=choices,
        default=_matching_choice([(c.title, c.value) for c in choices], default),
        style=questionary.Style([
            ("selected", "fg:yellow noinherit"),
            ("highlighted", "fg:yellow noinherit"),
            ("pointer", "fg:yellow noinherit"),
        ]),
    ).ask()

    # Output language has a sensible default, so a cancel falls back to English
    # rather than exiting the run (unlike the required model/provider prompts).
    if choice is None:
        return "English"
    if choice == "custom":
        return (questionary.text(
            "输入语言名称（例如土耳其语、越南语、泰语、印尼语）：",
            validate=lambda x: len(x.strip()) > 0 or "请输入语言名称。",
        ).ask() or "").strip() or "English"

    return choice
