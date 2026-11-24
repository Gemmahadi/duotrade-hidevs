# HiDevs Diwali Festiverse — GATE CHECK (24 Nov 2026, Adi: GAS 13:28 "bodo amat anggap aja belom tentu menang")

- Hackathon: Diwali Festiverse: The Agent-to-Agent Hackathon (India Edition)
- Devpost: https://theagent-to-agent-hackathon.devpost.com/ (104 participants)
- Deadline: 24 Nov 2026 22:00 IST = 23:30 WIB (TONIGHT). Top 10 announced 25 Nov 22:00 IST. Finale 28 Nov Bengaluru (top 10 only, live demo).
- Prizes: $700 cash total (BAND best use $250, Lyzr best use $250 cash + $250 credit, Agent37 best use $200 cash + $1500 credits, AdaL Pro subs) + $500 pro credits.
- Eligibility: 16-80, all countries, free, solo OK. AI is the point.
- Mandatory: build/integrate agents using sponsor platforms Lyzr, AdaL, Finch, Band (Devpost judging: "Lyzr, AdaL, Finch, Band, or Agent37" — integration quality is a judged criterion).
- Submit on Devpost; register on HiDevs platform (hidevs.xyz).
- Track chosen: Finance — Analyze & Trade. Project: "DuoTrade" — Analyst Agent (Lyzr) + Trader Agent (Lyzr), coordinated in a Band room (@mentions + handoff), Finch-style versioned skill files per agent, AdaL stretch.
- Strategy: live crypto prices (CoinGecko free, no key) + RSI(14)/SMA200 signal (backtested rule) -> simulated paper trades ($10k virtual, NO real money) -> dashboard. Demo = recorded run + Band room log.
- Sponsor status (researched 24 Nov 13:30):
  - Lyzr: pip install lyzr-adk, Studio.create_agent, free key at studio.lyzr.ai (Google/GitHub/email). REST API also available.
  - Band: docs.band.ai Agent API (REST+WS), band-sdk pip (py>=3.11). Sign in, create remote agent, per-agent UUID+API key. Hacker guide has 2-agent room quickstart.
  - **Band: DONE + LIVE 24 Nov 13:48** — akun Gemma Hadi, 2 agen (Analyst 4715b3b3…, Trader 509295f3…), room `4d23d8a0-0ff7-439a-b3a0-245a372af895`, kunci di `.env`. **Pertukaran pesan terverifikasi dua arah** (Analyst→Trader + Trader→Analyst, masing-masing terlihat di view penerima). Pelajaran API: `POST /chats` body `{"chat":{}}` (task_id wajib UUID yang sudah ada — jangan isi); kirim pesan body `{"message":{"content":...,"mentions":[{"id","handle"}]}}`, mentions WAJIB ≥1; python `requests` stall di app.band.ai — pakai urllib (band_client.py sudah urllib).
  - Finch (finchtech.ai): Agent Market — publish hosted agent/skill needs Provider workspace + public Invoke/Health URLs + HMAC + contract test + review. TOO HEAVY for 10h. Plan: Finch-style versioned SKILL.md files in repo, documented honestly; no live marketplace listing.
  - AdaL: adal_agent_sdk (pip from GitHub) + adal CLI + browser OAuth. Stretch goal (Builder agent) if time permits.
