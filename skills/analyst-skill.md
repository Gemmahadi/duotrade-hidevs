# Skill: duo-analyst v1.0.0 (Finch-style versioned skill)
# Used by: DuoTrade Analyst agent (Lyzr). Defines what the agent can do,
# its inputs/outputs, and its limits. Versioned so the Trader can rely on
# a stable contract — the same idea as a Finch skill package, shipped in
# this repo (a live Finch marketplace listing needs a wallet + review
# cycle that does not fit a 10-hour hackathon window; see README).

name: duo-analyst
version: 1.0.0
owner: GEMMA WORKS
description: >
  Fetch live crypto prices (CoinGecko free API, no key), compute RSI(14)
  and SMA(200) on 1h closes, and emit a structured trade signal
  (BUY / SELL / HOLD) with a one-line reason.
inputs:
  - symbol: ETH | BTC
  - timeframe: 1h closes, 14 days (CoinGecko market_chart)
outputs:
  - price_usd, rsi14, sma200, signal, reason (JSON)
rules:
  - BUY only when RSI(14) < 30 AND price > SMA200 (backtested rule).
  - SELL only when RSI(14) > 70.
  - Otherwise HOLD. Never invent a signal when data is missing.
  - Never claim the signal is financial advice.
limits:
  - CoinGecko free rate limit; one fetch per coin per run.
  - Binance klines are geo-blocked in the demo VM, so CoinGecko is the source.
