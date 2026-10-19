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

## 3. Deployment Packaging & Multi-Tenancy (Phase 6 Complete)
- [x] **Step 6.1 — Relative Path Portability:** Replaced Windows hardcoded paths with dynamic `Path(__file__).resolve().parent...` in [main.py](file:///C:/Users/thiag/Documents/CLT/app/main.py), [game_state.py](file:///C:/Users/thiag/Documents/CLT/app/engine/game_state.py), and [data_prep.py](file:///C:/Users/thiag/Documents/CLT/app/engine/data_prep.py).
- [x] **Step 6.2 — Multi-Tenant Session Isolation:** Implemented thread-safe `SessionManager` in [main.py](file:///C:/Users/thiag/Documents/CLT/app/main.py) with `clt_session_id` cookies, dynamic `$PORT` binding (`0.0.0.0`), and background TTL cleaner. Verified 100% isolated games via [qa_verify_sessions.py](file:///C:/Users/thiag/Documents/CLT/pipeline/qa_verify_sessions.py).
- [x] **Step 6.3 — Production Packaging:** Created [requirements.txt](file:///C:/Users/thiag/Documents/CLT/requirements.txt), [.gitignore](file:///C:/Users/thiag/Documents/CLT/.gitignore), [Dockerfile](file:///C:/Users/thiag/Documents/CLT/Dockerfile), [railway.json](file:///C:/Users/thiag/Documents/CLT/railway.json), and [Procfile](file:///C:/Users/thiag/Documents/CLT/Procfile).
- [x] **Step 6.4 — GitHub Repository Pushed:** Published release to [github.com/MrPatinhas/clt-game](https://github.com/MrPatinhas/clt-game).
- [x] **Step 6.5 — Railway Deployment & Public HTTPS:** Live at Railway with zero downtime CI/CD.

---

## 4. Phase 7: Mobile Responsiveness & Dual-World Architecture (Complete)
- [x] **Physical Safety Backup:** Full clone preserved at `C:\Users\thiag\Documents\clt-desktop`.
- [x] **Frozen Desktop Git Tag:** Tag `v1.0-desktop-gold` pushed to GitHub.
- [x] **Zero Desktop Regression Guarantee:** All mobile overrides are scoped within `@media (max-width: 768px)` and `@media (max-width: 480px)`. Screens $> 768\text{px}$ remain 100% untouched down to the exact pixel.
- [x] **Mobile Ergonomics (CSS):**
  - Compact stacked header and scrollable telemetry HUD.
  - Numbered stage stepper with inactive label collapse on small screens.
  - Responsive 3D carousel scaling (`clamp` & `min` width) with touch-friendly arrows.
  - Tactical mini-pitch auto-scaling with docked bench.
  - Bottom-sheet pattern for consultation and tutorial modals.
- [x] **Touch Gestures (JS):** Native touch-swipe navigation on mobile for 3D carousels in [app.js](file:///C:/Users/thiag/Documents/CLT/app/static/app.js).

---

## 5. Phase 7.1: Mobile Ergonomic Polish & Substitution QoL (Complete)
- [x] **Compact Mobile Font Scale:** Applied uniform root scaling (`html { font-size: 14px; }` on $\le 768\text{px}$, `13px` on $\le 480\text{px}$) with tighter container padding, eliminating overflows and minimizing scrolling.
- [x] **Scroll-Anchored Lineup & Substitutions:** Created `withScrollPreserved(".bench-players-drawer", ...)` in [app.js](file:///C:/Users/thiag/Documents/CLT/app/static/app.js) so clicking starters, bench players, or captain in Stage 6 and Stage 7 keeps the roster drawer and page scroll perfectly anchored.
- [x] **Mobile Default View Mode (GRADE):** Set `appState.viewMode = window.innerWidth <= 768 ? "grid" : "3d"` so mobile visitors immediately see the 2-column Grade (Grid) layout while desktop continues defaulting to the 3D Carousel.

---

## 6. Phase 8: Viral WhatsApp Share Pop-up & Match Flow Polish (Complete)
- [x] **Default Series Mode to Best of 3 (MD3):** Configured `series_mode="bo3"` and `target_wins=2` by default across [game_state.py](file:///C:/Users/thiag/Documents/CLT/app/engine/game_state.py), [main.py](file:///C:/Users/thiag/Documents/CLT/app/main.py), and [index.html](file:///C:/Users/thiag/Documents/CLT/app/static/index.html) for faster, punchier mobile sessions.
- [x] **Default Theme to Light Cream Mode:** Set `body.light-mode` as default in [index.html](file:///C:/Users/thiag/Documents/CLT/app/static/index.html) and [app.js](file:///C:/Users/thiag/Documents/CLT/app/static/app.js), with user preference persistence via `localStorage`.
- [x] **Sofascore-Style End-of-Series Share Pop-up (`#share-run-modal`):**
  - **Centered CLT Logo:** Top-center brand crest with golden clockwork frame.
  - **Match Score Timeline:** Sofascore-inspired match-by-match rows detailing Season, Round, Active Rule, scores, and winner highlight.
  - **Human MVP Spotlight:** Highlights top-scoring human athlete with score, photo, and badge.
  - **1-Tap WhatsApp Clipboard Copy:** Generates formatted WhatsApp scorecard with emojis, match-by-match breakdown, human MVP, and direct link to `https://clt-cartologia.up.railway.app/`.
  - **Native Clipboard API + Fallback:** Resilient clipboard copying for iOS Safari, Chrome Android, and desktop browsers with visual feedback toast.
- [x] **Railway Memory & Boot Optimization (CLTDataStore):**
  - Replaced eager conversion of 359,385 Parquet rows into hundreds of thousands of Python dicts (`to_dict('records')` which consumed ~545 MB of RAM and triggered Linux container freeze/OOM on Railway) with `ScoutsBySeasonRound`.
  - Memory consumption plummeted from **545 MB to 86 MB** (~84% reduction), boot time reduced to **0.6 seconds**, and unbuffered log output enabled (`flush=True`).

---

## 7. Phase 9: Modal Layout & Ergonomic Controls Overhaul (Complete)
- [x] **Sofascore Share Modal Layout & Sticky WhatsApp Button:**
  - Diagnosed root cause of `bugs/missing_copy_button_font_wrong_size.png`: modal window lacked viewport height constraints (`max-height: 88vh; display: flex; flex-direction: column; overflow: hidden;`), pushing the copy button beyond the viewport on smaller displays.
  - Implemented pinned `.share-modal-footer` with sticky bottom positioning and styled `.share-modal-body` with `flex: 1; overflow-y: auto;` so content scrolls cleanly on any screen height.
  - Structured `.timeline-match-row` into a 3-column CSS Grid (`130px 1fr 88px`) preventing awkward word-wrapping (`Time ... 15.40`).
  - Calibrated font sizes across badge, headline, and score elements.
- [x] **Persistent Dock Primary Call-To-Action (`#dock-primary-cta`):**
  - Converted center of the persistent bottom dock into an intelligent, high-visibility CTA button (`#dock-primary-cta`).
  - Automatically adapts icon, text, and click delegation to the active stage:
    - Stage 1: `⚙️ Escolher Squad Selecionado`
    - Stage 2: `⚡ Cravar Coordenadas (Rodada #X / Temporada Y)`
    - Stage 3: `⚔️ Confirmar Troca` / `⏭️ Passar no Bucket`
    - Stage 4: `📜 Regras Malucas (Stage 5)`
    - Stage 5: `🔒 Selar Regra & Escalar (Stage 6)`
    - Stage 6: `⚡ Iniciar 1º Tempo` (or `📋 Escalar 11`) / `⏸️ Ir ao Intervalo`
    - Stage 7: `🔥 Iniciar 2º Tempo` / `🏆 Ver Placar Final`
    - Stage 8: `📱 Compartilhar no WhatsApp` / `⏭️ Próxima Partida`
  - Fully responsive across desktop, tablet, and mobile.
- [x] **Stage 2 Interactive Clockwork Rolling Tape Picker:**
  - Replaced the 38 static square buttons with an interactive horizontal rolling dial stripe.
  - Features `◀` and `▶` steppers, active round card display with round context (`1º Turno (Ida)` vs `2º Turno (Volta)`, `🔥 Reta Final Decisiva`), and smooth auto-centering on selection.
- [x] **Header Cluster Organization:**
  - Reorganized `#app-header` into two distinct labeled clusters:
    - **⚙️ Game Settings:** Oráculo IA, Série (MD3 default), Modo Claro toggle, Nova Série.
    - **📖 Help Section:** Como Jogar, Regras & Power-Ups, Acervo (26).

---

## 8. Phase 10: Temporal Draft Mode (Upcoming Scope)
- [ ] **Dual Stage 1 Entry Point:** Toggle between "Definied Time Squads" (current 7 pre-built squads) and "Temporal Draft".
- [ ] **Positional Draft Grid:** Human coach selects athletes position-by-position (GOL, ZAG, LAT, MEI, ATA, TEC) from the normalized player pool using the mobile-friendly Grade (Grid) layout.
- [ ] **AI Counter-Draft / Squad Allocation:** AI engine draws its squad from the pre-generated time squads while excluding any athlete already drafted by the human coach.
- [ ] **Local Verification Commitment:** Full end-to-end local testing on `http://127.0.0.1:8000` before staging and pushing to Railway production.


