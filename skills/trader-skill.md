# Skill: duo-trader v1.0.0 (Finch-style versioned skill)
# Used by: DuoTrade Trader agent (Lyzr). Defines the paper-trading contract.

name: duo-trader
version: 1.0.0
owner: GEMMA WORKS
description: >
  Execute simulated paper trades from the Analyst's structured signals.
  Virtual cash $10,000. No real money, no real orders, no exchange keys.
inputs:
  - signal: {symbol, price_usd, signal: BUY|SELL|HOLD, reason}
  - portfolio: {cash, positions}
outputs:
  - trade record {time, symbol, signal, action, qty, note} (JSON)
  - updated portfolio.json + trades.json
rules:
  - BUY: only when no open position in the symbol; allocate 10% of cash.
  - SELL: only when a position is open; exit the whole position.
  - HOLD or no position change: log the decision, change nothing.
  - Every decision is logged, including no-ops.
limits:
  - Simulated only. Never connect to an exchange, never hold API keys
    with trading permission, never use real funds.
