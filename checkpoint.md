# CLT (Cartola Legends of Time) — Progress Checkpoint & State Memo
**Last Updated:** October 2026  
**Current Phase:** Transitioning from Local Development (Phase 5 Complete) to Public Feedback Deployment (Phase 6)  
**Active Local Server:** `http://127.0.0.1:8000` (Daemon task running)

---

## 1. Completed Milestones Summary
- **Data Engineering & Scout Normalization:** 12 seasons (2014–2025) normalized to a 17-scout universal vector (`RB -> DS` x1.286, `DD -> DE` x2.160; `PE`, `PS`, `PC` excluded).
- **Core 8-Stage Game State Machine:** Best-of-5 / Best-of-3 series against Rookie/Veteran/Oracle AI coaches.
- **Visuals & Art Assets:** 39 local club badges, 7 illustrated Time Squad emblems, 3 Power-Up cards, 8 Crazy Rule illustrations, 2 Coach Avatars (Human & Robot), and 6 cartoon stage tutorial diagrams.
- **UI Engine & Anti-Rigging:**
  - 3D Squad Carousel + 24-Row Tactical Position Table (`📋 Tabela por Posição`).
  - Stage Progression Locks (`🔒`) preventing parameter rigging or double-dipping.
  - Persistent Match Telemetry HUD.
  - Mini-field tactical formation validator (4-4-2, 4-3-3, 4-5-1, 3-4-3, 3-5-2) with Captain 2x assignment.
  - Halftime Power-Up deck (`REVEAL ZEROED`, `COPYCAT`, `GRENAL`) and substitutions.
  - Complete tutorial modal (`📖 Como Jogar`) & rules codex (`📜 Regras & Power-Ups`).
  - High-contrast Light Mode (`Modo Claro`) with semantic theme tokens.

---

## 2. Key Codebase Findings for Deployment
- **Total Footprint:** Entire repository (data, assets, scripts) is ~30 MB.
- **Python Dependencies:** Standard library + `pandas`, `pyarrow`, `numpy`.
- **Identified Deployment Bottlenecks:**
  1. *Hardcoded Windows Root Paths:* `ROOT_DIR = Path(r"C:\Users\thiag\Documents\CLT")` in `main.py` and `game_state.py`. Needs conversion to dynamic relative paths (`Path(__file__).resolve().parent...`).
  2. *Single-Tenant Global State:* `ENGINE = CLTGameEngine(STORE)` is a singleton in `main.py`. In a public multi-user environment, all visitors share the same game state unless isolated via session tokens/cookies.
  3. *Static Asset Serving:* Handled via custom Python `BaseHTTPRequestHandler`. For public production, either retain Python HTTP server with threaded sessions or wrap with a production-grade ASGI/WSGI server (e.g. Uvicorn/Starlette or Gunicorn) or containerize.

---

## 3. Deployment Packaging & Multi-Tenancy (Phase 6 Progress)
- [x] **Step 6.1 — Relative Path Portability:** Replaced Windows hardcoded paths with dynamic `Path(__file__).resolve().parent...` in [main.py](file:///C:/Users/thiag/Documents/CLT/app/main.py), [game_state.py](file:///C:/Users/thiag/Documents/CLT/app/engine/game_state.py), and [data_prep.py](file:///C:/Users/thiag/Documents/CLT/app/engine/data_prep.py).
- [x] **Step 6.2 — Multi-Tenant Session Isolation:** Implemented thread-safe `SessionManager` in [main.py](file:///C:/Users/thiag/Documents/CLT/app/main.py) with `clt_session_id` cookies, dynamic `$PORT` binding (`0.0.0.0`), and background TTL cleaner. Verified 100% isolated games via [qa_verify_sessions.py](file:///C:/Users/thiag/Documents/CLT/pipeline/qa_verify_sessions.py).
- [x] **Step 6.3 — Production Packaging:** Created [requirements.txt](file:///C:/Users/thiag/Documents/CLT/requirements.txt), [.gitignore](file:///C:/Users/thiag/Documents/CLT/.gitignore), [Dockerfile](file:///C:/Users/thiag/Documents/CLT/Dockerfile), [railway.json](file:///C:/Users/thiag/Documents/CLT/railway.json), and [Procfile](file:///C:/Users/thiag/Documents/CLT/Procfile).
- [x] **Step 6.4 — GitHub Repository Pushed:** Published initial release `75e78fe` to [github.com/MrPatinhas/clt-game](https://github.com/MrPatinhas/clt-game).
- [ ] **Step 6.5 — Railway Deployment & Public Domain:** Connect GitHub repo to Railway.app and verify public HTTPS URL.
