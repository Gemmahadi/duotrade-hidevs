# DuoTrade — Agent-to-Agent Paper Trading

**HiDevs Diwali Festiverse (India Edition) — Track: Finance, Analyze & Trade.**
Two AI agents that collaborate: the **Analyst** researches live crypto
markets and the **Trader** acts on its signals. Simulated money only.

## How the agents collaborate

1. **Analyst Agent** (Lyzr Studio) — fetches live prices (CoinGecko free
   API), computes RSI(14) + SMA(200), emits a structured signal
   (BUY / SELL / HOLD) with a reason. Skill: `skills/analyst-skill.md`.
2. **Band room** — the Analyst posts its signal to a shared Band room,
   mentioning `@DuoTrade Trader`. Band is the coordination layer: rooms,
   mentions, and a replayable log.
3. **Trader Agent** (Lyzr Studio) — reads the handoff, checks the virtual
   portfolio, executes a **simulated** paper trade ($10,000 virtual, 10%
   allocation per BUY, full exit on SELL), and reports back to the room.
   Skill: `skills/trader-skill.md`.
4. **Dashboard** — `dashboard.html` (regenerated every run) shows signals,
   trades, portfolio value, and the Band room transcript.

## The signal (backtested, honest)

Rule: **RSI(14) < 30 AND price > SMA(200) → BUY; RSI(14) > 70 → SELL.**
Backtested 17 Nov 2026 on ETH/BTC 4h (RSI<30 + price>SMA200: win rate
57–86%, expectancy +0.15 to +1.93%/trade). The demo uses 1h closes from
CoinGecko because Binance klines are geo-blocked in the demo VM — same
rule shape, timeframe stated everywhere. This is a hackathon demo, not
financial advice.

## Sponsor integrations

- **Lyzr** — both agents are real Lyzr Studio agents (`lyzr-adk`,
  `src/lyzr_agents.py`). Free key from studio.lyzr.ai.
- **Band** — room coordination via the Band Agent API + `band-sdk`
  (`src/band_client.py`). Each agent has its own UUID + API key.
- **Finch** — each agent's capability is a versioned skill file
  (`skills/*.md`), the Finch skill-package idea shipped in-repo. A live
  Finch marketplace listing needs a Provider wallet + contract test +
  review cycle that does not fit a 10-hour hackathon window; that is
  documented here instead of faked.
- **AdaL** — stretch goal (Builder agent via `adal_agent_sdk`); not in v1.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env   # fill LYZR_API_KEY, BAND_* keys, BAND_ROOM_ID
python3 run_demo.py    # works without keys too: local fallback, labelled
```

Without keys the pipeline still runs end-to-end (local signal math +
local room transcript in `data/band_transcript.md`), and every such
output is labelled `[local]` so a local computation is never passed off
as an LLM call.

## Files

- `run_demo.py` — orchestrator (Analyst → Band → Trader → dashboard)
- `src/analyst.py` — CoinGecko + RSI/SMA signal
- `src/trader.py` — paper portfolio + trade log
- `src/band_client.py` — Band room posts (+ local transcript fallback)
- `src/lyzr_agents.py` — Lyzr Studio agent wrappers (+ local fallback)
- `skills/` — versioned Finch-style skill contracts
- `data/` — portfolio.json, trades.json, band_transcript.md (generated)
- `dashboard.html` — generated dashboard (after a run)

Built by GEMMA WORKS (Gemma Hadi) for the Diwali Festiverse, 24 Nov 2026.
