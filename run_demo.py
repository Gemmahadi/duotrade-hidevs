"""DuoTrade demo run — Analyst -> Band room -> Trader -> dashboard.

One run: live CoinGecko prices, RSI/SMA signals, Lyzr reasoning (or local
fallback, labelled), Band room handoff (or local transcript mirror),
simulated paper trades, static HTML dashboard.

Usage:  python3 run_demo.py
Env:    LYZR_API_KEY, BAND_ANALYST_API_KEY, BAND_TRADER_API_KEY, BAND_ROOM_ID
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from analyst import analyze, COINS  # noqa: E402
from band_client import post  # noqa: E402
from lyzr_agents import analyst_reason, trader_reason  # noqa: E402
from trader import execute, portfolio, portfolio_value  # noqa: E402

ROOT = os.path.dirname(__file__)
DATA = os.path.join(ROOT, "data")

# Load .env (keys live there, never in code or git). The dashboard and
# run_demo both read the same file.
_ENV = os.path.join(ROOT, ".env")
if os.path.exists(_ENV):
    for _line in open(_ENV):
        _line = _line.strip()
        if _line and "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k, _v)

ANALYST_HANDLE = "gemmahadi/duotrade-analyst"
TRADER_HANDLE = "gemmahadi/duotrade-trader"


def dashboard(signals, trades, value, lyzr_mode, band_mode):
    rows = "".join(
        f"<tr><td>{s['symbol']}</td><td>${s['price_usd']}</td>"
        f"<td>{s['rsi14']}</td><td>${s['sma200']}</td>"
        f"<td><b>{s['signal']}</b></td><td>{s['reason']}</td></tr>"
        for s in signals
    )
    trows = "".join(
        f"<tr><td>{t['time']}</td><td>{t['symbol']}</td>"
        f"<td>{t['signal']}</td><td><b>{t['action']}</b></td>"
        f"<td>{t.get('qty', '')}</td><td>{t.get('note', '')}</td></tr>"
        for t in trades[-10:]
    )
    transcript = ""
    tp = os.path.join(DATA, "band_transcript.md")
    if os.path.exists(tp):
        with open(tp) as f:
            transcript = f.read()[-4000:]
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>DuoTrade — Agent-to-Agent Paper Trading</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:2em auto;
padding:0 1em}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px
solid #ccc;padding:.4em;text-align:left}}pre{{background:#f4f4f4;padding:1em;
white-space:pre-wrap}}</style></head><body>
<h1>DuoTrade — Analyst 🤝 Trader</h1>
<p><b>Track:</b> Finance — Analyze &amp; Trade (HiDevs Diwali Festiverse).
<b>Agents:</b> Lyzr Studio (reasoning) + Band room (coordination) +
Finch-style skills. <b>Money:</b> SIMULATED only, $10,000 virtual.</p>
<p><b>Live data:</b> CoinGecko free API, 1h closes, 14d. <b>Rule:</b>
RSI(14)&lt;30 + price&gt;SMA200 → BUY; RSI&gt;70 → SELL.
<b>Lyzr mode:</b> {lyzr_mode}. <b>Band mode:</b> {band_mode}.</p>
<p><b>Portfolio value:</b> ${value} (cash ${portfolio()['cash']},
positions {portfolio()['positions']})</p>
<h2>Signals</h2><table><tr><th>Coin</th><th>Price</th><th>RSI-14</th>
<th>SMA-200</th><th>Signal</th><th>Reason</th></tr>{rows}</table>
<h2>Recent trades</h2><table><tr><th>Time (UTC)</th><th>Coin</th>
<th>Signal</th><th>Action</th><th>Qty</th><th>Note</th></tr>{trows}</table>
<h2>Band room transcript</h2><pre>{transcript}</pre>
<p><small>Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')} UTC.
DuoTrade by GEMMA WORKS — hackathon demo, not financial advice.</small></p>
</body></html>"""
    with open(os.path.join(ROOT, "dashboard.html"), "w") as f:
        f.write(html)


def main():
    room = os.environ.get("BAND_ROOM_ID")
    a_key = os.environ.get("BAND_ANALYST_API_KEY")
    t_key = os.environ.get("BAND_TRADER_API_KEY")
    signals, trades = [], []
    lyzr_mode, band_mode = "local", "local-transcript"
    for sym in COINS:
        try:
            sig = analyze(sym)
        except Exception as e:  # noqa: BLE001
            sig = {"symbol": sym, "error": str(e)}
            signals.append(sig)
            continue
        signals.append(sig)
        reason, lyzr_mode = analyst_reason(sig)
        if lyzr_mode == "lyzr":
            lyzr_mode = "lyzr"
        r = post("DuoTrade Analyst", a_key, room,
                 f"@{TRADER_HANDLE} {sig['symbol']} signal "
                 f"{sig['signal']} at ${sig['price_usd']}: {reason}",
                 mention_id=os.environ.get("BAND_TRADER_AGENT_ID"),
                 mention_handle=TRADER_HANDLE)
        band_mode = r["mode"]
        trade = execute(sig)
        trades.append(trade)
        treason, _ = trader_reason(sig, trade,
                                  portfolio_value(
                                      {s["symbol"]: s.get("price_usd", 0)
                                       for s in signals}))
        post("DuoTrade Trader", t_key, room,
             f"@{ANALYST_HANDLE} {sig['symbol']}: {treason}",
             mention_id=os.environ.get("BAND_ANALYST_AGENT_ID"),
             mention_handle=ANALYST_HANDLE)
    value = portfolio_value({s["symbol"]: s.get("price_usd", 0)
                             for s in signals})
    dashboard(signals, trades, value, lyzr_mode, band_mode)
    print(json.dumps({"signals": signals, "trades": trades,
                      "portfolio_value": value, "lyzr": lyzr_mode,
                      "band": band_mode}, indent=2))


if __name__ == "__main__":
    main()
