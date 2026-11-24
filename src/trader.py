"""DuoTrade Trader — simulated paper trading. NO real money, NO real orders.

Virtual cash $10,000. BUY allocates 10% of current cash to the asset;
SELL exits the whole position. Every trade is logged to data/trades.json
and the portfolio to data/portfolio.json.
"""
import json
import os
from datetime import datetime, timezone

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
START_CASH = 10_000.0
ALLOC = 0.10


def _load(name, default):
    p = os.path.join(DATA, name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return default


def _save(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w") as f:
        json.dump(obj, f, indent=2)


def portfolio():
    return _load("portfolio.json", {"cash": START_CASH, "positions": {}})


def execute(signal):
    """signal: dict from analyst.analyze(). Returns a trade record."""
    pf = portfolio()
    sym = signal["symbol"]
    price = signal["price_usd"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rec = {"time": now, "symbol": sym, "signal": signal["signal"],
           "price": price, "action": "NONE", "note": signal.get("reason", "")}
    pos = pf["positions"].get(sym, 0.0)
    if signal["signal"] == "BUY" and pos == 0.0 and pf["cash"] > 100:
        spend = round(pf["cash"] * ALLOC, 2)
        qty = round(spend / price, 6)
        pf["cash"] = round(pf["cash"] - spend, 2)
        pf["positions"][sym] = qty
        rec.update(action="BUY", qty=qty, spend_usd=spend)
    elif signal["signal"] == "SELL" and pos > 0.0:
        proceeds = round(pos * price, 2)
        pf["cash"] = round(pf["cash"] + proceeds, 2)
        pf["positions"][sym] = 0.0
        rec.update(action="SELL", qty=pos, proceeds_usd=proceeds)
    else:
        rec["note"] += " | trader: no position change"
    _save("portfolio.json", pf)
    trades = _load("trades.json", [])
    trades.append(rec)
    _save("trades.json", trades)
    return rec


def portfolio_value(prices):
    pf = portfolio()
    total = pf["cash"]
    for sym, qty in pf["positions"].items():
        total += qty * prices.get(sym, 0.0)
    return round(total, 2)
