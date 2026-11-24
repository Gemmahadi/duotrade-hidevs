"""Lyzr agent wrappers — the agents' brains.

Each DuoTrade agent is a real Lyzr Studio agent (lyzr-adk). When
LYZR_API_KEY is set, the agent is created (or reused) in Studio and asked
to reason about the market signal / trade decision. When the key is absent
(offline test), the wrapper falls back to the deterministic local logic and
says so plainly — the demo never pretends a local computation is an LLM.
"""
import os

ANALYST_INSTRUCTIONS = (
    "You are DuoTrade Analyst, a crypto market analyst agent. "
    "You receive live price indicators (RSI-14, SMA-200, price) and explain "
    "the signal in one short paragraph: what the numbers say, what the "
    "risk is, and what you recommend to the Trader agent. Be concrete, "
    "no hype, no financial advice beyond the simulated demo."
)
TRADER_INSTRUCTIONS = (
    "You are DuoTrade Trader, a paper-trading agent. You receive the "
    "Analyst agent's signal and the current virtual portfolio. You decide "
    "whether to act on the signal, in one short paragraph: your decision, "
    "the position size, and the risk check. You only ever trade simulated "
    "money. Never claim a trade is real."
)


def _studio():
    key = os.environ.get("LYZR_API_KEY")
    if not key:
        return None
    from lyzr import Studio
    return Studio(api_key=key)


def _ask(instructions, prompt):
    """Ask a Lyzr agent; returns (text, mode). mode is 'lyzr' or 'local'."""
    studio = _studio()
    if studio is None:
        return None, "local"
    try:
        agent = studio.create_agent(
            name="DuoTrade",
            instructions=instructions,
            model="gpt-4o-mini",
        )
        resp = agent.run(prompt)
        text = getattr(resp, "response", None) or str(resp)
        return text, "lyzr"
    except TypeError:
        # Older SDK signature: retry with the minimal argument set.
        agent = studio.create_agent(instructions=instructions)
        resp = agent.run(prompt)
        text = getattr(resp, "response", None) or str(resp)
        return text, "lyzr"


def analyst_reason(signal):
    prompt = (f"Market snapshot for {signal['symbol']}: price "
              f"${signal['price_usd']}, RSI-14 {signal['rsi14']}, SMA-200 "
              f"${signal['sma200']}. Computed signal: {signal['signal']} "
              f"because {signal['reason']}. Explain this to the Trader.")
    text, mode = _ask(ANALYST_INSTRUCTIONS, prompt)
    if mode == "local":
        return (f"[local] {signal['symbol']}: {signal['signal']} — "
                f"{signal['reason']} (RSI {signal['rsi14']}, "
                f"SMA200 ${signal['sma200']})."), mode
    return text, mode


def trader_reason(signal, trade, portfolio_value):
    prompt = (f"Analyst signal for {signal['symbol']}: {signal['signal']} "
              f"at ${signal['price_usd']}. Trade executed: {trade['action']} "
              f"{trade.get('qty', '')} ({trade.get('note', '')}). Virtual "
              f"portfolio value now ${portfolio_value}. Justify the "
              f"decision in one paragraph.")
    text, mode = _ask(TRADER_INSTRUCTIONS, prompt)
    if mode == "local":
        return (f"[local] Trader {trade['action']} {signal['symbol']} "
                f"per signal {signal['signal']}; portfolio "
                f"${portfolio_value} (simulated)."), mode
    return text, mode
