# CLT (Cartola Legends of Time) — PRD, Architecture & Agent Worklog

**Project:** CLT (*Cartola Legends of Time*)  
**Genre:** Roguelike Historical Fantasy Football Strategy Game (Browser-Based)  
**Tech Stack:** Python (`FastAPI` + `pandas`/`pyarrow`) Backend + Modern HTML5/CSS3/Vanilla JS Frontend  
**Data Foundation:** 12 Seasons of Campeonato Brasileiro Série A (2014–2025) — `359,385` player-round records, `131,660` active appearances, `4,631` unique players, `4,560` matches, `39` clubs.  
**Status:** PRD Signed Off — Ready for Phase 1 Execution

---

## 1. Product Requirements Document (PRD) & Locked Design Decisions

### 1.1 Core Vision
**CLT (Cartola Legends of Time)** is a roguelike memory, deduction, and tactical adaptation game built on 12 seasons (`2014–2025`) of Campeonato Brasileiro Série A data. Each player commands a 24-man roster ("Rooster") of Brasileirão legends in a **Best-of-5 series** (first to 3 match wins; or Best-of-3 mode, first to 2 wins). Every match shifts to a different **(Season, Round)** chosen alternately by the two competitors. Players use memory, partial information reveals (*Bucket of the Souls*, *Highlights of Destiny*, *Half-Time 6v6 Sample*), substitutions, and one-off Power-Ups while adapting to *Crazy Rules* that warp scout weights.

### 1.2 Locked Architectural & Gameplay Decisions (Signed Off)
1. **Scout Normalization & Extinct Scouts (`PE`, `PS`, `PC`):**
   * **Excluded:** `PE` (*Passe Errado*), `PS` (*Pênalti Sofrido*), `PC` (*Pênalti Cometido*), and `V` (*Vitória do Técnico*) are excluded so that **all 12 seasons (2014–2025) share an identical 17-scout universal vector**.
   * **Era Conversion Factors (Empirical Dataset Ratios across 131,660 Active Appearances):**
     * **Tackles (`RB -> DS`):** In `2014–2019`, `DS = round(RB * 1.286, 2)` ($\mu_{\text{RB}} = 1.088 \to \mu_{\text{DS}} = 1.399$).
     * **Saves (`DD -> DE`):** In `2014–2020`, `DE = round(DD * 2.160, 2)` ($\mu_{\text{DD}} = 1.503 \to \mu_{\text{DE}} = 3.247$).
     * *(In 2021, where both `RB`/`DS` and `DD`/`DE` columns existed during the transition, we use `DS` if non-zero else `RB * 1.286`, and `DE` if non-zero else `DD * 2.160`).*
   * **UI Disclaimer:** Displayed in the rules/analytics view explaining that pre-2020 `RB` and pre-2021 `DD` were normalized to `DS` ($\times 1.286$) and `DE` ($\times 2.160$).
2. **Coach (`TEC`, `position_id = 6`) Scoring:**
   * Coaches use their **static historical Cartola points (`points` / `pontos_num`)** from the database for that `(Season, Round)`, unaffected by Crazy Rule scout multipliers (though still eligible for $2\times$ if selected as Captain, or restricted to outfield/GK if preferred).
3. **Stage 1 — The 7 Pre-Defined Roosters (`24 players` each = `168 players` total):**
   * Composition per Rooster: **`2 GK, 4 ZAG, 4 LAT, 8 MEI, 5 ATA, 1 TEC`**.
   * Players are assigned to their **modal position (`mode_pos`)** across their career active appearances.
   * Ranked within each position by a composite longevity + quality metric:
     $$\text{RankScore}_p = 0.60 \times \widehat{\text{RoundsPlayed}}_p + 0.40 \times \widehat{\text{AvgPoints}}_p$$
   * Partitioned across the 7 Roosters via a **Stratified Snake Draft** (`1..7, 7..1`) so all 7 Roosters have virtually identical expected appearances and average scores across eras, each with a themed "Galo / Rooster" identity.
   * When playing vs. AI, the AI picks from the remaining 6 Roosters and **must choose a different Rooster in subsequent series**.
4. **Stage 2 & Stage 3 — Parameters & *Bucket of the Souls*:**
   * **Alternating Parameter Choice:** In Game 1, Player A chooses **Round (`1–38`)** and Player B chooses **Year (`2014–2025`)**; roles alternate every game in the Best-of-5.
   * **Turn Order in Bucket of the Souls:** The **second parameter chooser** (the last one who chose a parameter) gets **first pick** from the 6-player Bucket of the Souls (1 guaranteed active player per position `GK, ZAG, LAT, MEI, ATA, TEC` in that `(Year, Round)` who is not currently in either player's Rooster).
   * **Information Hiding:** Bucket cards show **only** Player Name, Photo, Position, and the Club they defended in that specific `(Year, Round)`—no average scores or historical stats.
   * **Same-Position Swap & Roguelike Persistence:** Swapping drops a player of the **same position** from your Rooster and **permanently mutates your 24-man Rooster for the remainder of the Best-of-5 series** (or a player may Pass).
5. **Stage 4 — *Highlights of Destiny*:**
   * Displays the 10 fixtures of that `(Year, Round)` as 10 gray horizontal bars (2 columns $\times$ 5 rows).
   * Mandatory choice: **(A) Reveal 5 random matchups (Home vs. Away teams only)** OR **(B) Reveal 2 random matchups + final scores (`Home X x Y Away`)**.
6. **Stage 5 — *Crazy Rules* (17 Universal Scouts):**
   * One of the 8 Crazy Rules (or Base Rule if configured) is rolled, warping the 17 scout weights (`G, A, SG, DP, DE, DS, FT, FD, FF, FS, GC, CV, CA, GS, FC, I, PP`).
   * **Regra do Futsal (Updated for Universal Scouts):** *"Toque de bola curto e sem impedimento! Assistência vale ouro (+8.0), Impedimento zerado (0.0) e Falta Cometida pesa o triplo (-1.5)."*
7. **Stage 6 & Stage 7 — First Half, Half-Time & Power-Ups:**
   * **Valid Formations (11 on pitch + 1 TEC):** `4-4-2` (`2 ZAG, 2 LAT, 4 MEI, 2 ATA`), `4-3-3` (`2 ZAG, 2 LAT, 3 MEI, 3 ATA`), `4-5-1` (`2 ZAG, 2 LAT, 5 MEI, 1 ATA`), `3-4-3` (`3 ZAG, 0 LAT, 4 MEI, 3 ATA`), `3-5-2` (`3 ZAG, 0 LAT, 5 MEI, 2 ATA`).
   * **Captain ($2\times$):** Doubles the chosen player's score (positive or negative). If the Captain is substituted out at Half-Time, the $2\times$ armband can be reassigned to another on-field player.
   * **Half-Time 6v6 Sample:** Reveals the partial score sum of 6 randomly sampled starters from Team A vs. 6 randomly sampled starters from Team B.
   * **Half-Time Substitutions:** Up to **3 substitutions** from the bench (may shift between any of the 5 valid formations).
   * **Power-Up Inventory (1 of each per Best-of-5 series, max 1 played per Half-Time):**
     1. **`REVEAL ZEROED PLAYERS`:** Highlights in neon-blue any of your current starters who scored `0.0` (did not play or zeroed) in that round *before* you lock in your 3 Half-Time substitutions.
     2. **`COPYCAT`:** Pick 1 opponent starter and 1 of your starters; your chosen starter copies the opponent starter's final score.
     3. **`GRENAL`:** Randomly removes (red-cards / zeroes out) 3 outfield/GK starters from **each** team (`9 vs 9` chaos).
8. **Stage 8 — Match Conclusion & Analytical Report:**
   * Evaluates final scores on the pitch, awards the match win, and displays a full analytical report: every starter's score, expandable per-scout breakdown, Match MVP badge, and bench player scores.

---

## 2. Universal 17-Scout Weight Matrix (Base vs. 8 Crazy Rules)

With `RB -> DS` ($\times 1.286$) and `DD -> DE` ($\times 2.160$) normalized and `PE`/`PS`/`PC` excluded, here is the unified 17-scout weight table across the Base Rule and all 8 Crazy Rules:

| Rule Name | Description | `G` | `A` | `SG` | `DP` | `DE` | `DS` | `FT` | `FD` | `FF` | `FS` | `GC` | `CV` | `CA` | `GS` | `FC` | `I` | `PP` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Base Cartola (Normalized)** | Pontuação clássica normalizada (`DE` e `DS`) | `8.0` | `5.0` | `5.0` | `7.0` | `1.3` | `1.0` | `3.0` | `1.2` | `0.8` | `0.5` | `-3.0` | `-3.0` | `-1.0` | `-1.0` | `-0.3` | `-0.1` | `-4.0` |
| **1. Regra de Gabriel Jesus** | *Gol vale metade. O que vale é marcar lateral e desarmar!* | **`4.0`** | `5.0` | `5.0` | `7.0` | `1.3` | **`3.1`** | `3.5` | `0.6` | `0.4` | `0.5` | `-6.0` | `-5.0` | `-2.0` | `-2.0` | `-0.5` | `-0.5` | `-3.5` |
| **2. Regra de Felipe Melo** | *Cartão é sinal de entrega! Falta sofrida é simulação.* | `8.0` | `5.0` | `5.0` | `7.0` | `1.3` | `1.3` | `3.5` | `1.2` | `0.8` | **`-0.5`** | `-6.0` | **`+5.0`** | **`+2.0`** | `-2.0` | **`0.0`** | `-0.5` | `-3.5` |
| **3. Regra do Futsal** | *Toque curto! Assistência vale ouro, sem impedimento, falta pesa.* | `8.0` | **`8.0`** | `5.0` | `7.0` | `1.3` | `1.3` | `3.5` | `1.2` | `0.8` | `0.5` | `-6.0` | `-5.0` | `-2.0` | `-2.0` | **`-1.5`** | **`0.0`** | `-3.5` |
| **4. Regra do Mano Menezes** | *Achei ofensivo, recua! SG vale o dobro.* | `8.0` | `5.0` | **`10.0`** | `7.0` | `1.3` | `1.3` | `3.5` | `1.2` | `0.8` | `0.5` | `-6.0` | `-5.0` | `-2.0` | `-2.0` | `-0.5` | `-0.5` | `-3.5` |
| **5. Regra do Vanderlei** | *O que vale na vida são pontes! Defesa (DE/DP) vale ouro, GS pesa.* | `8.0` | `5.0` | `5.0` | **`14.0`** | **`3.2`** | `1.3` | `3.5` | **`2.0`** | `0.8` | `0.5` | `-6.0` | `-5.0` | `-2.0` | **`-4.0`** | `-0.5` | `-0.5` | `-3.5` |
| **6. Regra do Garçom** | *Mais vale aquele que compartilha (+10 A) que aquele que comemora (+5 G).* | **`5.0`** | **`10.0`** | `5.0` | `7.0` | `1.3` | `1.3` | `3.5` | `1.2` | `0.8` | `0.5` | `-6.0` | `-5.0` | `-2.0` | `-2.0` | `-0.5` | `-0.5` | `-3.5` |
| **7. Regra do Buda** | *Seja positivo! Zero negatividades (todos os scouts negativos = 0).* | `8.0` | `5.0` | `5.0` | `7.0` | `1.3` | `1.3` | `3.5` | `1.2` | `0.8` | `0.5` | **`0.0`** | **`0.0`** | **`0.0`** | **`0.0`** | **`0.0`** | **`0.0`** | **`0.0`** |
| **8. Regra Open Capitão** | *Dobro de tudo positivo e quádruplo das punições!* | **`16.0`** | **`10.0`** | **`10.0`** | **`14.0`** | **`2.6`** | **`2.6`** | **`7.0`** | **`2.4`** | **`1.6`** | **`1.0`** | **`-24.0`** | **`-20.0`** | **`-8.0`** | **`-8.0`** | **`-2.0`** | **`-2.0`** | **`-14.0`** |

*(Note: In the Crazy Rules above, the legacy `DD` weights `3.0 / 7.0 / 6.0` and `RB` weights `1.7 / 4.0 / 3.4` from the draft were divided by the empirical conversion factors `2.160` and `1.286` so that `DE_equiv * weight_DE` and `DS_equiv * weight_DS` yield the exact same point totals as the draft intended!)*

---

## 3. Project Directory Layout (`C:\Users\thiag\Documents\CLT\`)

```text
C:\Users\thiag\Documents\CLT\
├── data/
│   ├── teams.parquet                 # 39 clubs + badge_url (60x60) & badge_small_url (30x30)
│   ├── matches.parquet               # 4,560 fixtures (2014-2025)
│   ├── players.parquet               # 4,631 players + photo_url (220x220) & is_silhouette
│   ├── player_scouts/                # Partitioned season=2014..2025 raw fixture scouts
│   ├── normalized_scouts.parquet     # [Phase 1] Pre-computed 17-scout normalized table + base scores
│   └── roosters.json                 # [Phase 1] The 7 pre-defined 24-man balanced Roosters
├── pipeline/                         # Data engineering & QA scripts
├── app/
│   ├── main.py                       # [Phase 2] FastAPI server & REST endpoints
│   ├── engine/
│   │   ├── data_prep.py              # [Phase 1] Normalization & 7 Roosters generator
│   │   ├── rules.py                  # [Phase 2] 17-scout weights, Crazy Rules & score calculator
│   │   ├── game_state.py             # [Phase 2] 8-stage state machine, Bucket of Souls, Power-Ups
│   │   └── ai_agent.py               # [Phase 2] 3-tier AI opponent (Rookie, Veteran, Oracle)
│   └── static/
│       ├── index.html                # [Phase 3-5] Single-Page Game UI
│       ├── styles.css                # [Phase 3-5] 3D Carousel, Pitch, Neon Power-Up & Card styles
│       └── app.js                    # [Phase 3-5] Interactive Stage 1-8 controller
├── raw_idea.md                       # Original game design memo
└── IMPLEMENTATION_PLAN.md            # This master PRD & Agent Worklog
```

---

## 4. Iterative Implementation Worklog (Step-by-Step)

After each phase below, we will inspect the output/app together for your feedback before advancing:

- [x] **Phase 1 — Game Data Pre-Computation & Dynamic 7-Rooster Pool (`app/engine/data_prep.py`)**
  - [x] Build `data/normalized_scouts.parquet` applying `RB -> DS` ($\times 1.286$) and `DD -> DE` ($\times 2.160$), keeping the 17 universal scouts + static `TEC` points, and computing career normalized average scores (`359,385` rows).
  - [x] Compute each player's modal position (`mode_pos`), career active rounds, normalized average score, and top-3 clubs by appearances (with club abbreviations and `badge_small_url`) in `data/player_career_stats.parquet` (`4,631` players).
  - [x] Implement `generate_dynamic_roosters()` drawing stochastically without replacement from the **Top ~300 Legends Pool** (`26 GOL, 50 ZAG, 50 LAT, 96 MEI, 64 ATA, 14 TEC`) with randomized deficit-compensated snake drafting so every single run generates 7 fresh, balanced 24-man Roosters.
  - *Checkpoint 1:* Completed & verified.
- [x] **Phase 2 — Core Game Engine, Crazy Rules, Power-Ups & AI (`app/engine/` & `app/main.py`)**
  - [x] Implement `rules.py` (Base + 8 Crazy Rules evaluator, `TEC` static score lookup, Captain $2\times$ multiplier).
  - [x] Implement `game_state.py` (Best-of-5 / Best-of-3 series state, Stage 1–8 transitions, Bucket of Souls generator & persistent swap logic, Highlights of Destiny sampler, Half-Time 6v6 sampler, Formation validator, and Power-Ups: `REVEAL ZEROED`, `COPYCAT`, `GRENAL`).
  - [x] Implement `ai_agent.py` (Rookie/Veteran/Oracle difficulty tiers + non-repeating Rooster selection).
  - [x] Expose full game loop endpoints in `app/main.py` and run automated simulation smoke tests (`pipeline/qa_test_engine.py`).
  - *Checkpoint 2:* Verified across all 8 stages via `qa_test_engine.py`.
- [x] **Phase 3 — Stage 1 UI: "Time Squad A..G" (3D Carousel & Minimized Squad Drawers)**
  - [x] Build the 3D perspective Time Squad & Player Card carousel (keyboard arrow keys + click navigation) showing Player Photo/Silhouette, Short Name, Position, Top-3 Club Logos/Abbreviations, Avg Score, and Rounds Played.
  - [x] Build the persistent minimized Human & AI Time Squad drawers (clickable at any stage to inspect all 24 players) + live **"🎲 Sortear Novos Time Squads"** button.
  - *Checkpoint 3:* Completed & visually approved by Thiago at `http://127.0.0.1:8000`.
- [x] **Phase 3.5 — Visual Polish, Brand Palette, Custom Art & 3rd Table View (Sequential Task Log)**
  - [x] **Task 3.5.1 — Local Club Logos (`39/39` Série A teams) & Brand Logo Crop:**
    - Cropped the official **CLT Logo** from `assets/Gemini_Generated_Image_wpoozewpoozewpoo.jpg` into `assets/ui/clt_logo.png`.
    - Fetched and normalized all **39 club crests** locally into `assets/clubs/<ABBR>.png` at a uniform `64x64` transparent PNG resolution (`39/39` verified), and wired `/assets/` into `main.py` and `data_prep.py`.
  - [x] **Task 3.5.2 — Custom Time-Travel Artwork (`assets/emblems/`, `assets/powerups/`, `assets/rules/`):**
    - Generated 7 illustrated **Time Squad Emblems** (`squad_a.png` .. `squad_g.png`), 3 **Power-Up Art Cards** (`reveal_zeroed.png`, `copycat.png`, `grenal.png`), and 8 **Crazy Rule Illustrations** (`gabriel_jesus.png`, `felipe_melo.png`, `futsal.png`, `mano_menezes.png`, `vanderlei.png`, `garcom.png`, `buda.png`, `open_capitao.png`) matching the CLT steampunk/chrono-football aesthetic. (14 generated via `image-generator` before quota limit + 4 composite steampunk crests in `06_prepare_game_art_assets.py`).
  - [x] **Task 3.5.3 — Official CLT Color Palette & Time-Travel Theme (`styles.css` & `index.html`):**
    - Applied the 6-color brand palette (`#FDFBF7` Parchment Cream, `#F9A03F` Cartola Amber, `#E0533C` Vermilion, `#F2C249` Clockwork Gold, `#2E2A27` Espresso Ink, `#3A86C8` Chrono Sapphire) across the entire interface and replaced emoji emblems with the generated artwork.
  - [x] **Task 3.5.4 — 3rd Team Display Format: 24-Row Position-Grouped Tactical Table (`app.js` & `styles.css`):**
    - Added the **`📋 Tabela por Posição (24)`** view mode (and inside the consultation modal) displaying all 24 players in a structured table with styled position sub-header blocks (`GOLEIROS — 2`, `ZAGUEIROS — 4`, `LATERAIS — 4`, `MEIAS — 8`, `ATACANTES — 5`, `TÉCNICO — 1`).
  - [x] **Task 3.5.5 — Time-Travel Generation Animation ("Temporal Vortex" Reroll):**
    - Added the clockwork/time-rift animation (`#temporal-vortex-overlay` + `.shuffling` 3D card implode & deal) when generating new Time Squads.
- [x] **Phase 4 — Stages 2, 3, 4 & 5 UI (Parameters, Bucket of Souls, Highlights of Destiny, Crazy Rule)**
  - [x] Build Stage 2 alternating Year/Round selector (with 1-click turn-order toggle for testing 1st vs 2nd chooser).
  - [x] Build Stage 3 *Bucket of the Souls* 6-card draft (strictly hiding historical averages; enforcing same-position swap or Pass; persistent Time Squad mutation).
  - [x] Build Stage 4 *Highlights of Destiny* (2 columns $\times$ 5 gray bars; choice of 5 matchups vs. 2 matchups + scores).
  - [x] Build Stage 5 *Crazy Rule* reveal screen with custom artwork and 17-scout `BUFF` / `NERF` comparison matrix.
  - *Checkpoint 4:* Completed & reviewed.
- [x] **Phase 4.5 — Anti-Rigging Progression Locks, Persistent Telemetry Header & Compact Grid Cards**
  - [x] **Anti-Rigging Progression Locks (`game_state.py` & `app.js`):** Locked completed stages into strict Read-Only Consultation Mode (`🔒`) so players cannot return to Stage 3 (*Bucket of the Souls*) to make multiple swaps, nor click both Option A and Option B in Stage 4 (*Highlights of Destiny*) to double-dip match information. Added a prominent **"🔄 Resetar Partida / Nova Run"** button to cleanly restart the run from scratch.
  - [x] **Persistent Match Telemetry HUD (`#match-hud-bar`):** Added a sticky top telemetry ribbon displaying **Série Temporal**, **Temporada (`YYYY`)**, **Rodada (`#RR`)**, **Destiny Revelado**, and **Regra Maluca** at all times.
  - [x] **Compact 24-Card Grid View (`styles.css`):** Reduced card width (`minmax(156px, 1fr)`, 6–8 cards per row) and height (`222px`, `68px` portrait) in Grid mode and inside the Consultation Modal so all 24 athletes fit with minimal scrolling.
- [x] **Phase 5 — Stages 6, 7 & 8 UI, Coach Icons & Tutorial/Codex Tabs (`index.html`, `styles.css`, `app.js`)**
  - [x] Build Stage 6 Interactive Mini-Field with formation validation (`4-4-2`, `4-3-3`, `4-5-1`, `3-4-3`, `3-5-2`), red/green status indicator, 1-click Auto-Fill Best Averages, Captain ($2\times$) badge, and *KICK OFF* button.
  - [x] Build Stage 7 Half-Time screen (6v6 random sample scoreboard, up to 3 substitutions with formation shift, Captain reassignment if subbed, and Power-Up cards with neon-blue highlight for `REVEAL ZEROED`, starter dropdowns for `COPYCAT`, and `9v9` chaos banner for `GRENAL`).
  - [x] Build Stage 8 Match Conclusion analytical report (final scoreboard, Match MVP spotlight, side-by-side 12-starter tables with individual scout pills, expandable 12-bench scores, and Best-of-5 series progression / Champion celebration).
  - [x] Add custom cartoon **Human Coach (`assets/ui/human_coach.png`)** and **Robot Coach (`assets/ui/robot_coach.png`)** avatars next to the player and AI squad dock buttons, consultation modal headers, and match scoreboards.
  - [x] Build the **`📖 Como Jogar (Tutorial)`** tab (`#tutorial-modal`) with 6 custom cartoon stage illustrations (`assets/tutorial/stage_1_squads.png` .. `stage_7_8_climax.png`) and concrete numerical turn-by-turn examples.
  - [x] Build the **`📜 Regras, Power-Ups & Era`** Codex tab (`#codex-modal`) detailing the `2014–2025` time frame, mathematical scout normalization (`RB -> DS` $\times 1.286$, `DD -> DE` $\times 2.160$), all 3 Half-Time Power-Ups, and all 8 Crazy Rules.
  - *Checkpoint 5:* Full end-to-end gameplay complete and running at `http://127.0.0.1:8000`.

