const DEFAULT_SILHOUETTE = "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/silhuetas/OUT/220x220.png";

const POSITION_BLOCKS = [
  { code: "GOL", title: "🧤 GOLEIROS (GOL)", subtitle: "Guardiões da Meta Temporal" },
  { code: "ZAG", title: "🛡️ ZAGUEIROS (ZAG)", subtitle: "Muralha Central & Jogo Aéreo" },
  { code: "LAT", title: "⚡ LATERAIS (LAT)", subtitle: "Alas de Desarme & Apoio Ofensivo" },
  { code: "MEI", title: "🎩 MEIO-CAMPISTAS (MEI)", subtitle: "Maestros, Garçons & Motores do Meio" },
  { code: "ATA", title: "🔥 ATACANTES (ATA)", subtitle: "Artilheiros & Finalizadores Letais" },
  { code: "TEC", title: "📋 COMANDANTE TÉCNICO (TEC)", subtitle: "Estrategista à Beira do Gramado" },
];

const FORMATION_QUOTAS = {
  "4-3-3": { GOL: 1, ZAG: 2, LAT: 2, MEI: 3, ATA: 3, TEC: 1 },
  "4-4-2": { GOL: 1, ZAG: 2, LAT: 2, MEI: 4, ATA: 2, TEC: 1 },
  "4-5-1": { GOL: 1, ZAG: 2, LAT: 2, MEI: 5, ATA: 1, TEC: 1 },
  "3-4-3": { GOL: 1, ZAG: 3, LAT: 0, MEI: 4, ATA: 3, TEC: 1 },
  "3-5-2": { GOL: 1, ZAG: 3, LAT: 0, MEI: 5, ATA: 2, TEC: 1 },
};

const ART_GALLERY_CATALOG = {
  emblems: [
    { title: "Time Squad A", desc: "Relíquias da Cartola · Unidade Alpha", src: "/assets/emblems/squad_a.png" },
    { title: "Time Squad B", desc: "Pêndulo Imortal · Unidade Bravo", src: "/assets/emblems/squad_b.png" },
    { title: "Time Squad C", desc: "Bússola do Século · Unidade Charlie", src: "/assets/emblems/squad_c.png" },
    { title: "Time Squad D", desc: "Ampulheta Dourada · Unidade Delta", src: "/assets/emblems/squad_d.png" },
    { title: "Time Squad E", desc: "Engrenagem Real · Unidade Echo", src: "/assets/emblems/squad_e.png" },
    { title: "Time Squad F", desc: "Vórtice de Cronos · Unidade Foxtrot", src: "/assets/emblems/squad_f.png" },
    { title: "Time Squad G", desc: "Oráculo Eterno · Unidade Golf", src: "/assets/emblems/squad_g.png" },
  ],
  powerups: [
    { title: "Reveal Zeroed Players", desc: "Raio-X Temporal: Revela quem zerou na rodada", src: "/assets/powerups/reveal_zeroed.png" },
    { title: "Copycat", desc: "Espelho de Cronos: Copia 1 titular adversário", src: "/assets/powerups/copycat.png" },
    { title: "Grenal", desc: "Caos Clássico: Expulsa 3 titulares de cada lado", src: "/assets/powerups/grenal.png" },
  ],
  rules: [
    { title: "Regra de Gabriel Jesus", desc: "Gol vale 4.0 · Desarme e Falta Sofrida brilham", src: "/assets/rules/gabriel_jesus.png" },
    { title: "Regra de Felipe Melo", desc: "Cartão é sinal de entrega (+2 CA / +5 CV)", src: "/assets/rules/felipe_melo.png" },
    { title: "Regra do Futsal", desc: "Assistência +8.0 · Sem Impedimentos (I = 0)", src: "/assets/rules/futsal.png" },
    { title: "Regra do Mano Menezes", desc: "Achei Ofensivo, Recua · SG vale o Dobro (+10)", src: "/assets/rules/mano_menezes.png" },
    { title: "Regra do Vanderlei", desc: "Pontes Imortais · Defesa Difícil e DP Dobrados", src: "/assets/rules/vanderlei.png" },
    { title: "Regra do Garçom", desc: "Compartilhar > Comemorar · A = +10.0, G = +5.0", src: "/assets/rules/garcom.png" },
    { title: "Regra do Buda", desc: "Zero Negatividades · Todos os scouts negativos = 0", src: "/assets/rules/buda.png" },
    { title: "Regra Open Capitão", desc: "Dobro dos Positivos · Quádruplo dos Negativos", src: "/assets/rules/open_capitao.png" },
  ],
  coaches_and_tutorial: [
    { title: "Treinador Humano", desc: "Avatar oficial do Comandante Humano", src: "/assets/ui/human_coach.png" },
    { title: "Oráculo Robô IA", desc: "Avatar oficial do Autômato Temporal IA", src: "/assets/ui/robot_coach.png" },
    { title: "Stage 1 · Cápsulas Temporais", desc: "Ilustração Cartoon dos 7 Time Squads", src: "/assets/tutorial/stage_1_squads.png" },
    { title: "Stage 2 · Coordenadas do Tempo", desc: "Ilustração Cartoon do Ano & Rodada", src: "/assets/tutorial/stage_2_coordinates.png" },
    { title: "Stage 3 · Bucket of the Souls", desc: "Ilustração Cartoon do Caldeirão de Almas", src: "/assets/tutorial/stage_3_bucket.png" },
    { title: "Stage 4 · Highlights of Destiny", desc: "Ilustração Cartoon das 10 Barras do Oráculo", src: "/assets/tutorial/stage_4_destiny.png" },
    { title: "Stage 5 & 6 · Regra & Campo", desc: "Ilustração Cartoon da Prancheta Tática", src: "/assets/tutorial/stage_5_6_pitch.png" },
    { title: "Stage 7 & 8 · Clímax & Troféu", desc: "Ilustração Cartoon do Intervalo & Apito Final", src: "/assets/tutorial/stage_7_8_climax.png" },
  ],
};

let appState = {
  run_id: 1,
  stage: 1,
  maxUnlockedStage: 1,
  roosters: [],
  activeRoosterIdx: 0,
  activePlayerIdx: 0,
  posFilter: "ALL",
  viewMode: "3d", // "3d" | "grid" | "table"
  modalRoosterIdx: null,
  modalViewMode: "cards",
  humanRoosterIdx: null,
  aiRoosterIdx: null,
  isAnimatingVortex: false,

  // Stage 2 UI state
  stage2ParamType: "round", // "round" | "season"
  stage2SelectedVal: 10,

  // Stage 3 UI state
  selectedBucketPlayerId: null,
  selectedDropPlayerId: null,

  // Stage 6 Lineup UI state
  stage6Formation: "4-3-3",
  stage6Starters: [],
  stage6CaptainId: null,

  // Stage 7 Half-Time UI state
  stage7Formation: "4-3-3",
  stage7Starters: [],
  stage7CaptainId: null,
  copycatOwnId: null,
  copycatOppId: null,

  // Engine sub-states
  match_number: 1,
  human_wins: 0,
  ai_wins: 0,
  target_wins: 3,
  powerups_remaining: { human: { reveal_zeroed: true, copycat: true, grenal: true } },
  match_history: [],
  stage2: {},
  stage3: {},
  stage4: {},
  stage5: {},
  stage6: {},
  stage7: {},
  stage8: {},
};

function autoBuildBestLineup(squad, formation) {
  const quotas = FORMATION_QUOTAS[formation] || FORMATION_QUOTAS["4-3-3"];
  const starters = [];
  Object.entries(quotas).forEach(([posCode, count]) => {
    if (count <= 0) return;
    const cands = squad
      .filter((p) => p.position_code === posCode)
      .sort((a, b) => b.avg_score - a.avg_score);
    cands.slice(0, count).forEach((p) => starters.push(p.player_id));
  });
  const bestCap = squad
    .filter((p) => starters.includes(p.player_id) && p.position_code !== "TEC")
    .sort((a, b) => b.avg_score - a.avg_score)[0];
  return {
    formation,
    starter_ids: starters,
    captain_id: bestCap ? bestCap.player_id : starters[0] || null,
  };
}

function syncFromServer(data) {
  const prevMatchNum = appState.match_number;
  appState.run_id = data.run_id || 1;
  appState.stage = data.stage || 1;

  if (data.match_number && data.match_number !== prevMatchNum) {
    // New match in the series: reset maxUnlockedStage to current stage (Stage 2)
    appState.maxUnlockedStage = appState.stage;
    appState.stage6Starters = [];
    appState.stage7Starters = [];
  } else {
    appState.maxUnlockedStage = Math.max(appState.maxUnlockedStage, appState.stage);
  }

  if (appState.stage === 1 && data.human_rooster_index === null) {
    appState.maxUnlockedStage = 1;
    appState.stage6Starters = [];
    appState.stage7Starters = [];
  }

  appState.roosters = data.roosters || [];
  appState.humanRoosterIdx = data.human_rooster_index;
  appState.aiRoosterIdx = data.ai_rooster_index;
  appState.match_number = data.match_number || 1;
  appState.human_wins = data.human_wins || 0;
  appState.ai_wins = data.ai_wins || 0;
  appState.target_wins = data.target_wins || 3;
  appState.powerups_remaining = data.powerups_remaining || {
    human: { reveal_zeroed: true, copycat: true, grenal: true },
  };
  appState.match_history = data.match_history || [];
  appState.stage2 = data.stage2 || {};
  appState.stage3 = data.stage3 || {};
  appState.stage4 = data.stage4 || {};
  appState.stage5 = data.stage5 || {};
  appState.stage6 = data.stage6 || {};
  appState.stage7 = data.stage7 || {};
  appState.stage8 = data.stage8 || {};

  if (appState.stage2 && appState.stage2.human_param_type) {
    appState.stage2ParamType = appState.stage2.human_param_type;
    if (appState.stage2ParamType === "season" && (appState.stage2SelectedVal < 2014 || appState.stage2SelectedVal > 2025)) {
      appState.stage2SelectedVal = 2019;
    } else if (appState.stage2ParamType === "round" && (appState.stage2SelectedVal < 1 || appState.stage2SelectedVal > 38)) {
      appState.stage2SelectedVal = 10;
    }
  }

  // Initialize & sanitize Stage 6 draft lineup against the current 24-man squad
  if (appState.humanRoosterIdx !== null && appState.roosters[appState.humanRoosterIdx]) {
    const hSquad = appState.roosters[appState.humanRoosterIdx].players;
    const validIds = new Set(hSquad.map((p) => p.player_id));

    if (appState.stage6 && appState.stage6.human_lineup) {
      appState.stage6Formation = appState.stage6.human_lineup.formation;
      appState.stage6Starters = appState.stage6.human_lineup.starter_ids.filter((id) => validIds.has(id));
      appState.stage6CaptainId = appState.stage6.human_lineup.captain_id;
    } else {
      // Strip any orphan player IDs dropped during Stage 3 (Bucket of the Souls)
      appState.stage6Starters = Array.from(new Set(appState.stage6Starters)).filter((id) => validIds.has(id));
      // Only auto-build best lineup when Stage 3 is completed or when entering Stage 6
      if (!appState.stage6Starters.length && (appState.stage >= 6 || (appState.stage3 && appState.stage3.completed))) {
        const auto = autoBuildBestLineup(hSquad, appState.stage6Formation || "4-3-3");
        appState.stage6Formation = auto.formation;
        appState.stage6Starters = auto.starter_ids;
        appState.stage6CaptainId = auto.captain_id;
      }
    }

    // Initialize Stage 7 halftime lineup from Stage 6 if not yet populated
    if (appState.stage7 && appState.stage7.final_human_lineup) {
      appState.stage7Formation = appState.stage7.final_human_lineup.formation;
      appState.stage7Starters = appState.stage7.final_human_lineup.starter_ids.filter((id) => validIds.has(id));
      appState.stage7CaptainId = appState.stage7.final_human_lineup.captain_id;
    } else if (appState.stage6 && appState.stage6.human_lineup && !appState.stage7Starters.length) {
      appState.stage7Formation = appState.stage6.human_lineup.formation;
      appState.stage7Starters = appState.stage6.human_lineup.starter_ids.filter((id) => validIds.has(id));
      appState.stage7CaptainId = appState.stage6.human_lineup.captain_id;
    } else {
      appState.stage7Starters = Array.from(new Set(appState.stage7Starters)).filter((id) => validIds.has(id));
    }
  }
}

function circularOffset(index, activeIndex, total) {
  let diff = (index - activeIndex) % total;
  if (diff < 0) diff += total;
  if (diff > total / 2) diff -= total;
  return diff;
}

function getFilteredPlayers() {
  const rooster = appState.roosters[appState.activeRoosterIdx];
  if (!rooster) return [];
  if (appState.posFilter === "ALL") return rooster.players;
  return rooster.players.filter((p) => p.position_code === appState.posFilter);
}

function getClubLogoUrl(teamObj) {
  if (!teamObj) return "";
  if (teamObj.abbreviation) {
    return `/assets/clubs/${teamObj.abbreviation}.png`;
  }
  return teamObj.badge_small_url || teamObj.badge_url || "";
}

function createAthleteCardHTML(p, extraClass = "", dataIdx = null) {
  const clubsHTML = (p.top_teams || [])
    .slice(0, 3)
    .map((t) => {
      const badgeImg = getClubLogoUrl(t);
      return `
        <span class="club-pill" title="${t.team_name} (${t.appearances} jogos na Série A)">
          ${badgeImg ? `<img src="${badgeImg}" alt="${t.abbreviation}" onerror="this.style.display='none'" />` : ""}
          <span class="club-abbr">${t.abbreviation}</span>
        </span>
      `;
    })
    .join("");

  const idxAttr = dataIdx !== null ? `data-idx="${dataIdx}"` : "";
  const bucketBadge = p.recruited_from_bucket
    ? `<span style="background:#3A86C8;color:#FDFBF7;font-size:0.62rem;padding:2px 6px;border-radius:4px;font-weight:800;">👻 BUCKET</span>`
    : `<span class="era-span-tag">⏳ ${p.first_season}–${p.last_season}</span>`;

  return `
    <div class="athlete-card ${extraClass}" ${idxAttr}>
      <div class="athlete-card-header">
        <span class="pos-badge pos-${p.position_code}">${p.position_code}</span>
        ${bucketBadge}
      </div>

      <div class="athlete-portrait-box">
        <img
          src="${p.photo_url || DEFAULT_SILHOUETTE}"
          alt="${p.short_name}"
          loading="lazy"
          onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';"
        />
      </div>

      <div class="athlete-identity">
        <div class="athlete-short-name" title="${p.full_name}">${p.short_name}</div>
        <div class="athlete-pos-label">${p.position_name}</div>
      </div>

      <div class="athlete-teams-strip">
        ${clubsHTML || '<span class="club-abbr">—</span>'}
      </div>

      <div class="athlete-metrics-row">
        <div class="metric-box">
          <span class="metric-label">Média Histórica</span>
          <span class="metric-value">${p.avg_score.toFixed(2)} pts</span>
        </div>
        <div class="metric-box">
          <span class="metric-label">Rodadas Jogadas</span>
          <span class="metric-value rounds">${p.rounds_played} rod</span>
        </div>
      </div>
    </div>
  `;
}

function createPositionGroupedTableHTML(players) {
  let rowCounter = 1;
  const blocksHTML = POSITION_BLOCKS.map((block) => {
    const groupPlayers = players.filter((p) => p.position_code === block.code);
    if (!groupPlayers.length) return "";

    const meanScore =
      groupPlayers.reduce((acc, p) => acc + p.avg_score, 0) / groupPlayers.length;
    const sumRounds = groupPlayers.reduce((acc, p) => acc + p.rounds_played, 0);

    const subHeaderRow = `
      <tr class="pos-subheader-row pos-sub-${block.code}">
        <td colspan="6">
          <div class="pos-subheader-flex">
            <span>${block.title} · <small style="font-weight:500;opacity:0.85;">${block.subtitle}</small></span>
            <span class="pos-subheader-meta">
              ${groupPlayers.length} ${groupPlayers.length === 1 ? "Atleta" : "Atletas"} · Média do Setor: ${meanScore.toFixed(2)} pts · ${sumRounds} jogos acumulados
            </span>
          </div>
        </td>
      </tr>
    `;

    const rows = groupPlayers
      .map((p) => {
        const clubsCell = (p.top_teams || [])
          .slice(0, 3)
          .map((t) => {
            const logoUrl = getClubLogoUrl(t);
            return `
              <span class="table-club-badge" title="${t.team_name}: ${t.appearances} jogos">
                <img src="${logoUrl}" alt="${t.abbreviation}" onerror="this.style.display='none'" />
                <span class="club-abbr">${t.abbreviation}</span>
                <span class="table-club-games">(${t.appearances}j)</span>
              </span>
            `;
          })
          .join("");

        const pct = Math.min(100, Math.max(12, (p.avg_score / 8.5) * 100));
        const currentIdx = rowCounter++;

        return `
          <tr class="tactical-row">
            <td style="width:84px;">
              <span style="font-family:'JetBrains Mono',monospace;color:var(--text-dim);font-size:0.75rem;margin-right:6px;">#${String(currentIdx).padStart(2, "0")}</span>
              <span class="pos-badge pos-${p.position_code}">${p.position_code}</span>
            </td>
            <td>
              <div class="table-athlete-cell">
                <img
                  src="${p.photo_url || DEFAULT_SILHOUETTE}"
                  alt="${p.short_name}"
                  class="table-avatar"
                  loading="lazy"
                  onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';"
                />
                <div class="table-athlete-names">
                  <span class="table-short-name">${p.short_name} ${p.recruited_from_bucket ? '<span style="color:var(--text-sapphire);font-size:0.7rem;">(👻 Bucket)</span>' : ""}</span>
                  <span class="table-full-name">${p.full_name}</span>
                </div>
              </div>
            </td>
            <td style="width:135px;">
              <span class="era-span-tag">⏳ ${p.first_season}–${p.last_season}</span>
            </td>
            <td>
              <div class="table-clubs-cell">
                ${clubsCell || "—"}
              </div>
            </td>
            <td style="width:190px;">
              <div class="table-score-wrap">
                <span class="table-score-val">${p.avg_score.toFixed(2)} pts</span>
                <div class="table-score-bar-bg">
                  <div class="table-score-bar-fill" style="width:${pct.toFixed(0)}%;"></div>
                </div>
              </div>
            </td>
            <td style="width:130px;text-align:right;">
              <span class="table-rounds-val">${p.rounds_played} rodadas</span>
            </td>
          </tr>
        `;
      })
      .join("");

    return subHeaderRow + rows;
  }).join("");

  return `
    <table class="tactical-table">
      <thead>
        <tr>
          <th># / Pos</th>
          <th>Atleta Histórico</th>
          <th>Linha do Tempo</th>
          <th>Clubes Mais Defendidos (Série A)</th>
          <th>Média Normalizada</th>
          <th style="text-align:right;">Experiência</th>
        </tr>
      </thead>
      <tbody>
        ${blocksHTML}
      </tbody>
    </table>
  `;
}

// ============================================================================
// STAGE STEPPER NAVIGATION & PERSISTENT MATCH TELEMETRY HUD
// ============================================================================
function isStageLocked(step) {
  if (step === 1) return appState.humanRoosterIdx !== null;
  if (step === 2) return Boolean(appState.stage2 && appState.stage2.completed);
  if (step === 3) return Boolean(appState.stage3 && appState.stage3.completed);
  if (step === 4) return Boolean(appState.stage4 && appState.stage4.completed);
  if (step === 5) return Boolean(appState.stage5 && appState.stage5.locked);
  if (step === 6) return Boolean(appState.stage6 && appState.stage6.completed);
  if (step === 7) return Boolean(appState.stage7 && appState.stage7.completed);
  if (step === 8) return Boolean(appState.stage8 && appState.stage8.human_total !== undefined);
  return false;
}

function renderStepper() {
  const buttons = document.querySelectorAll("#stage-stepper .stepper-item");
  const baseLabels = {
    1: "Time Squads",
    2: "Ano & Rodada",
    3: "Bucket of Souls",
    4: "Highlights of Destiny",
    5: "Regra Maluca",
    6: "Escalação & Campo",
    7: "Intervalo & Power-Ups",
    8: "Placar & Relatório",
  };

  buttons.forEach((btn) => {
    const step = parseInt(btn.getAttribute("data-step"), 10);
    const isUnlocked = step <= appState.maxUnlockedStage;
    const lockedDone = isStageLocked(step);
    btn.disabled = !isUnlocked;
    btn.classList.toggle("active", step === appState.stage);
    btn.classList.toggle("completed", lockedDone);

    const labelEl = btn.querySelector(".stepper-label");
    if (labelEl && baseLabels[step]) {
      labelEl.textContent = lockedDone ? `🔒 ${baseLabels[step]}` : baseLabels[step];
    }
  });

  for (let s = 1; s <= 8; s++) {
    const el = document.getElementById(`stage-view-${s}`);
    if (el) {
      el.classList.toggle("hidden", s !== appState.stage);
    }
  }
}

function renderMatchHud() {
  const hudBar = document.getElementById("match-hud-bar");
  if (!hudBar) return;

  if (appState.humanRoosterIdx === null) {
    hudBar.classList.add("hidden");
    return;
  }

  hudBar.classList.remove("hidden");

  const s2 = appState.stage2 || {};
  const s4 = appState.stage4 || {};
  const s5 = appState.stage5 || {};

  // Series
  const seriesEl = document.getElementById("hud-series-val");
  if (seriesEl) {
    seriesEl.textContent = `Partida #${appState.match_number} · Você ${appState.human_wins} x ${appState.ai_wins} IA`;
  }

  // Year (Season)
  const yearBox = document.getElementById("hud-year-box");
  const yearVal = document.getElementById("hud-year-val");
  if (yearVal && yearBox) {
    if (s2.season) {
      yearVal.textContent = `${s2.season}`;
      yearBox.classList.add("locked-highlight");
    } else {
      yearVal.textContent = "A definir (Stage 2)";
      yearBox.classList.remove("locked-highlight");
    }
  }

  // Round
  const roundBox = document.getElementById("hud-round-box");
  const roundVal = document.getElementById("hud-round-val");
  if (roundVal && roundBox) {
    if (s2.round) {
      roundVal.textContent = `Rodada #${String(s2.round).padStart(2, "0")}`;
      roundBox.classList.add("locked-highlight");
    } else {
      roundVal.textContent = "A definir (Stage 2)";
      roundBox.classList.remove("locked-highlight");
    }
  }

  // Destiny Highlights
  const destBox = document.getElementById("hud-destiny-box");
  const destVal = document.getElementById("hud-destiny-val");
  if (destVal && destBox) {
    if (s4.completed) {
      destVal.textContent = s4.choice_mode === "2_scores" ? "🔒 2 Placares Exatos" : "🔒 5 Confrontos";
      destBox.classList.add("locked-highlight");
    } else {
      destVal.textContent = "Pendente (Stage 4)";
      destBox.classList.remove("locked-highlight");
    }
  }

  // Crazy Rule
  const ruleBox = document.getElementById("hud-rule-box");
  const ruleVal = document.getElementById("hud-rule-val");
  if (ruleVal && ruleBox) {
    if (s5.active_rule && s5.active_rule.name) {
      ruleVal.textContent = s5.active_rule.name;
      ruleBox.classList.add("locked-highlight");
    } else {
      ruleVal.textContent = "Oculta (Stage 5)";
      ruleBox.classList.remove("locked-highlight");
    }
  }
}

// ============================================================================
// STAGE 1 RENDERERS
// ============================================================================
function renderRoosterCarousel() {
  const track = document.getElementById("rooster-carousel-track");
  const counter = document.getElementById("rooster-counter");
  const total = appState.roosters.length;
  if (!total || !track) return;

  counter.textContent = `${appState.activeRoosterIdx + 1} / ${total}`;
  const stage1Locked = appState.humanRoosterIdx !== null;

  track.innerHTML = appState.roosters
    .map((r, i) => {
      const offset = circularOffset(i, appState.activeRoosterIdx, total);
      const absOff = Math.abs(offset);

      const translateX = offset * 288;
      const translateZ = -absOff * 115;
      const rotateY = offset * -24;
      const scale = offset === 0 ? 1.04 : Math.max(0.72, 0.92 - absOff * 0.08);
      const opacity = absOff > 2 ? 0 : offset === 0 ? 1 : Math.max(0.35, 0.85 - (absOff - 1) * 0.32);
      const zIndex = 20 - absOff;
      const pointerEvents = absOff > 2 ? "none" : "auto";

      const isActive = offset === 0;
      const borderStyle = isActive
        ? `border-color: ${r.accent_color}; box-shadow: 0 18px 45px rgba(0,0,0,0.75), 0 0 28px ${r.accent_color}55;`
        : "";

      const isHumanPicked = appState.humanRoosterIdx === i;
      const isAiPicked = appState.aiRoosterIdx === i;
      let btnLabel = "Escolher Time Squad";
      let btnExtraStyle = "";
      if (isHumanPicked) {
        btnLabel = "🔒 Seu Time Squad (Voltar à Partida →)";
      } else if (isAiPicked) {
        btnLabel = "🤖 Time Squad da IA";
        btnExtraStyle = "opacity:0.75;background:#2E2A27;";
      } else if (stage1Locked) {
        btnLabel = "🔒 Elenco Já Travado";
        btnExtraStyle = "opacity:0.5;cursor:not-allowed;background:#2E2A27;";
      }

      const emblemSrc = r.emblem_url || `/assets/emblems/squad_${String.fromCharCode(97 + i)}.png`;

      return `
        <div
          class="rooster-card-3d ${isActive ? "active" : ""}"
          data-ridx="${i}"
          style="
            transform: translateX(${translateX}px) translateZ(${translateZ}px) rotateY(${rotateY}deg) scale(${scale});
            opacity: ${opacity};
            z-index: ${zIndex};
            pointer-events: ${pointerEvents};
            ${borderStyle}
          "
        >
          <div class="rooster-card-top">
            <div class="rooster-emblem-box" style="border-color: ${r.accent_color}">
              <img src="${emblemSrc}" alt="${r.name}" class="rooster-emblem-img" />
            </div>
            <div class="rooster-title-block">
              <h3>${r.name}</h3>
              <p>${r.tagline}</p>
            </div>
          </div>

          <div class="rooster-stats-row">
            <div class="r-stat">
              <span class="r-stat-label">Média Elenco</span>
              <span class="r-stat-val" style="color: ${r.accent_color}">${r.summary.mean_player_avg_score.toFixed(2)} pts</span>
            </div>
            <div class="r-stat">
              <span class="r-stat-label">Média Jogos</span>
              <span class="r-stat-val">${r.summary.mean_rounds_played.toFixed(0)} rod</span>
            </div>
            <div class="r-stat">
              <span class="r-stat-label">Total Aparições</span>
              <span class="r-stat-val">${r.summary.total_historical_appearances.toLocaleString("pt-BR")}</span>
            </div>
          </div>

          <div class="rooster-card-footer">
            <span class="rooster-quota-text">2 GOL · 4 ZAG · 4 LAT · 8 MEI · 5 ATA · 1 TEC</span>
            <button class="btn-select-rooster" style="${btnExtraStyle}" data-select-ridx="${i}">${btnLabel}</button>
          </div>
        </div>
      `;
    })
    .join("");

  track.querySelectorAll(".rooster-card-3d").forEach((card) => {
    card.addEventListener("click", (e) => {
      const selectBtn = e.target.closest("[data-select-ridx]");
      if (selectBtn) {
        e.stopPropagation();
        const idx = parseInt(selectBtn.getAttribute("data-select-ridx"), 10);
        if (stage1Locked) {
          appState.stage = appState.maxUnlockedStage;
          renderAll();
          return;
        }
        selectRooster(idx);
        return;
      }
      const idx = parseInt(card.getAttribute("data-ridx"), 10);
      if (idx !== appState.activeRoosterIdx) {
        appState.activeRoosterIdx = idx;
        appState.activePlayerIdx = 0;
        renderAll();
      }
    });
  });
}

function renderPlayerShowcase() {
  const rooster = appState.roosters[appState.activeRoosterIdx];
  if (!rooster) return;

  const emblemSrc = rooster.emblem_url || `/assets/emblems/squad_${String.fromCharCode(97 + appState.activeRoosterIdx)}.png`;
  const miniEmblem = document.getElementById("active-rooster-emblem-mini");
  if (miniEmblem) miniEmblem.src = emblemSrc;

  const titleEl = document.getElementById("active-rooster-title");
  if (titleEl) titleEl.textContent = `${rooster.name} — ${rooster.tagline}`;

  const players = getFilteredPlayers();
  const total = players.length;
  if (appState.activePlayerIdx >= total) {
    appState.activePlayerIdx = 0;
  }

  const wrapper3D = document.getElementById("player-3d-wrapper");
  const wrapperGrid = document.getElementById("player-grid-wrapper");
  const wrapperTable = document.getElementById("player-table-wrapper");
  if (!wrapper3D) return;

  wrapper3D.classList.add("hidden");
  wrapperGrid.classList.add("hidden");
  wrapperTable.classList.add("hidden");

  if (appState.viewMode === "3d") {
    wrapper3D.classList.remove("hidden");

    const track = document.getElementById("player-carousel-track");
    const counter = document.getElementById("player-counter");
    counter.textContent =
      total > 0
        ? `Carta ${appState.activePlayerIdx + 1} de ${total} (${players[appState.activePlayerIdx].short_name})`
        : "0 Cartas";

    track.innerHTML = players
      .map((p, i) => {
        const offset = circularOffset(i, appState.activePlayerIdx, total);
        const absOff = Math.abs(offset);

        const visible = absOff <= 3;
        const translateX = offset * 215;
        const translateZ = -absOff * 95;
        const rotateY = offset * -26;
        const scale = offset === 0 ? 1.04 : Math.max(0.68, 0.91 - absOff * 0.07);
        const opacity = !visible ? 0 : offset === 0 ? 1 : Math.max(0.25, 0.88 - absOff * 0.22);
        const zIndex = 30 - absOff;

        const html = createAthleteCardHTML(p, offset === 0 ? "active-card" : "", i);
        return html.replace(
          'class="athlete-card',
          `style="transform: translateX(${translateX}px) translateZ(${translateZ}px) rotateY(${rotateY}deg) scale(${scale}); opacity: ${opacity}; z-index: ${zIndex}; pointer-events: ${visible ? "auto" : "none"};" class="athlete-card`
        );
      })
      .join("");

    track.querySelectorAll(".athlete-card").forEach((card) => {
      card.addEventListener("click", () => {
        const idx = parseInt(card.getAttribute("data-idx"), 10);
        if (!isNaN(idx)) {
          appState.activePlayerIdx = idx;
          renderPlayerShowcase();
        }
      });
    });
  } else if (appState.viewMode === "grid") {
    wrapperGrid.classList.remove("hidden");
    wrapperGrid.innerHTML = players.map((p) => createAthleteCardHTML(p)).join("");
  } else if (appState.viewMode === "table") {
    wrapperTable.classList.remove("hidden");
    wrapperTable.innerHTML = createPositionGroupedTableHTML(players);
  }
}

// ============================================================================
// STAGE 2: SEASON (2014-2025) & ROUND (1-38) PARAMETERS
// ============================================================================
function renderStage2() {
  const container = document.getElementById("stage2-container");
  if (!container || appState.humanRoosterIdx === null) return;

  const s2 = appState.stage2 || {};
  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const aRooster = appState.roosters[appState.aiRoosterIdx];

  // ANTI-RIGGING LOCK: If Stage 2 is already completed, show Read-Only Locked View
  if (s2.completed) {
    container.innerHTML = `
      <div class="locked-stage-banner">
        <div>
          <strong>🔒 ETAPA 2 SELADA (ANTI-RIGGING):</strong> As coordenadas temporais desta partida já foram cravadas e não podem ser alteradas.
        </div>
        <button id="btn-s2-back-active" class="btn-chrono" style="padding:7px 14px;font-size:0.8rem;">
          ➡️ Voltar para Etapa Atual (Stage ${appState.maxUnlockedStage})
        </button>
      </div>

      <div class="stage2-top-banner">
        <div>
          <span class="stage-pill">COORDENADAS OFICIAIS DA PARTIDA #${appState.match_number}</span>
          <h3 style="font-family:'Cinzel',serif;font-size:1.45rem;color:var(--text-gold);margin-top:6px;">
            ⏳ Temporada ${s2.season} &nbsp;·&nbsp; 🧭 Rodada #${String(s2.round).padStart(2, "0")}
          </h3>
        </div>
        <div style="font-size:0.95rem;font-weight:800;">
          ${hRooster.name} <span style="color:var(--text-amber);">VS</span> ${aRooster.name}
        </div>
      </div>

      <div class="ai-log-banner">${s2.ai_log || ""}</div>
    `;

    document.getElementById("btn-s2-back-active").addEventListener("click", () => {
      appState.stage = appState.maxUnlockedStage;
      renderAll();
    });
    return;
  }

  const humanIsFirst = s2.first_chooser === "human";

  const turnText = humanIsFirst
    ? "Você escolhe o 1º parâmetro temporal · 🤖 A IA escolherá o 2º parâmetro e abrirá o Bucket of the Souls!"
    : "🤖 A IA escolheu o 1º parâmetro temporal · ✨ Você escolhe o 2º parâmetro e terá a 1ª escolha no Bucket of the Souls!";

  const nextOrderTarget = humanIsFirst ? "ai" : "human";

  let selectorHTML = "";
  const mode = humanIsFirst ? appState.stage2ParamType : s2.human_param_type;

  if (mode === "season") {
    const seasons = Array.from({ length: 12 }, (_, i) => 2014 + i);
    selectorHTML = `
      <h3 style="font-family:'Cinzel',serif;color:var(--text-gold);margin-bottom:12px;">
        ⏳ Escolha a Temporada Histórica (2014–2025) ${s2.round ? `para a Rodada #${s2.round}` : ""}
      </h3>
      <div class="season-grid">
        ${seasons
          .map(
            (y) => `
          <button class="season-dial-btn ${appState.stage2SelectedVal === y ? "selected" : ""}" data-s2-val="${y}">
            <span class="season-year">${y}</span>
            <span class="season-era-sub">Série A · 38 Rod</span>
          </button>
        `
          )
          .join("")}
      </div>
    `;
  } else {
    const rounds = Array.from({ length: 38 }, (_, i) => i + 1);
    selectorHTML = `
      <h3 style="font-family:'Cinzel',serif;color:var(--text-gold);margin-bottom:12px;">
        🧭 Escolha a Rodada do Campeonato (1–38) ${s2.season ? `da Temporada ${s2.season}` : ""}
      </h3>
      <div class="round-grid">
        ${rounds
          .map(
            (r) => `
          <button class="round-dial-btn ${appState.stage2SelectedVal === r ? "selected" : ""}" data-s2-val="${r}">
            #${String(r).padStart(2, "0")}
          </button>
        `
          )
          .join("")}
      </div>
    `;
  }

  container.innerHTML = `
    <div class="stage2-top-banner">
      <div>
        <div style="font-size:0.75rem;color:var(--text-gold);font-family:'JetBrains Mono',monospace;">
          PARTIDA #${appState.match_number} · SÉRIE: VOCÊ ${appState.human_wins} x ${appState.ai_wins} IA (ALVO: ${appState.target_wins} VITÓRIAS)
        </div>
        <div style="font-size:1.05rem;font-weight:800;margin-top:4px;">
          ${hRooster.name} <span style="color:var(--text-amber);">VS</span> ${aRooster.name}
        </div>
      </div>

      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <span class="turn-order-pill">${turnText}</span>
        <button id="btn-s2-swap-order" class="btn-gallery" style="font-size:0.76rem;padding:7px 12px;">
          🔄 Inverter Ordem (Testar ${humanIsFirst ? "IA 1º" : "Humano 1º"})
        </button>
      </div>
    </div>

    <div class="ai-log-banner">${s2.ai_log || ""}</div>

    ${
      humanIsFirst
        ? `
      <div class="param-mode-tabs">
        <button class="mode-btn ${appState.stage2ParamType === "round" ? "active" : ""}" id="btn-s2-mode-round">
          🧭 Escolher Rodada (1–38) e deixar Ano para a IA
        </button>
        <button class="mode-btn ${appState.stage2ParamType === "season" ? "active" : ""}" id="btn-s2-mode-season">
          ⏳ Escolher Ano (2014–2025) e deixar Rodada para a IA
        </button>
      </div>
    `
        : ""
    }

    ${selectorHTML}

    <div style="display:flex;justify-content:flex-end;margin-top:12px;">
      <button id="btn-s2-confirm" class="btn-chrono" style="font-size:0.95rem;padding:12px 24px;">
        ⚡ Cravar Coordenada (${mode === "season" ? `Temporada ${appState.stage2SelectedVal}` : `Rodada #${appState.stage2SelectedVal}`}) & Ir ao Bucket of the Souls →
      </button>
    </div>
  `;

  const swapBtn = document.getElementById("btn-s2-swap-order");
  if (swapBtn) {
    swapBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage2/swap-order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ first_chooser: nextOrderTarget }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const btnRound = document.getElementById("btn-s2-mode-round");
  const btnSeason = document.getElementById("btn-s2-mode-season");
  if (btnRound && btnSeason) {
    btnRound.addEventListener("click", () => {
      appState.stage2ParamType = "round";
      appState.stage2SelectedVal = 10;
      renderStage2();
    });
    btnSeason.addEventListener("click", () => {
      appState.stage2ParamType = "season";
      appState.stage2SelectedVal = 2019;
      renderStage2();
    });
  }

  container.querySelectorAll("[data-s2-val]").forEach((btn) => {
    btn.addEventListener("click", () => {
      appState.stage2SelectedVal = parseInt(btn.getAttribute("data-s2-val"), 10);
      renderStage2();
    });
  });

  document.getElementById("btn-s2-confirm").addEventListener("click", async () => {
    const res = await fetch("/api/stage2/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        param_type: mode,
        value: appState.stage2SelectedVal,
      }),
    });
    const data = await res.json();
    appState.selectedBucketPlayerId = null;
    appState.selectedDropPlayerId = null;
    syncFromServer(data);
    renderAll();
  });
}

// ============================================================================
// STAGE 3: BUCKET OF THE SOULS (6 ACTIVE PLAYERS, STRICTLY 1 SWAP MAX)
// ============================================================================
function renderStage3() {
  const container = document.getElementById("stage3-container");
  if (!container || !appState.stage3 || !appState.stage3.bucket_cards) return;

  const s3 = appState.stage3;
  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const cards = s3.bucket_cards || [];
  const isLocked = Boolean(s3.completed);

  const selectedCard = !isLocked
    ? cards.find((c) => c.player_id === appState.selectedBucketPlayerId && !c.picked_by)
    : null;
  const samePosCandidates = selectedCard
    ? hRooster.players.filter((p) => p.position_code === selectedCard.position_code)
    : [];

  if (selectedCard && !samePosCandidates.some((p) => p.player_id === appState.selectedDropPlayerId)) {
    appState.selectedDropPlayerId = samePosCandidates[0] ? samePosCandidates[0].player_id : null;
  }

  const aiBanner = s3.ai_decision
    ? `<div class="ai-log-banner">🤖 <strong>Movimento da IA no Bucket:</strong> ${s3.ai_decision.reason}</div>`
    : `<div class="ai-log-banner">✨ <strong>Você tem a 1ª escolha no Bucket of the Souls!</strong> A IA fará a escolha dela logo após a sua decisão.</div>`;

  const humanBanner =
    isLocked && s3.human_decision
      ? `<div class="locked-stage-banner">
           <div>
             <strong>🔒 DECISÃO SELADA NO BUCKET (ANTI-RIGGING):</strong> ${s3.human_decision.reason}
           </div>
           <button id="btn-s3-back-active" class="btn-chrono" style="padding:7px 14px;font-size:0.8rem;">
             ➡️ Ir para Etapa Atual (Stage ${appState.maxUnlockedStage})
           </button>
         </div>`
      : "";

  const cardsHTML = cards
    .map((c) => {
      const isTaken = Boolean(c.picked_by) || isLocked;
      const isSelected = !isLocked && appState.selectedBucketPlayerId === c.player_id;
      const clubLogo = getClubLogoUrl(c.round_team);
      const statusBadge =
        c.picked_by === "ai"
          ? `<div style="background:#E0533C;color:#FDFBF7;font-size:0.7rem;font-weight:800;padding:4px 8px;border-radius:6px;">🤖 RECRUTADO PELA IA</div>`
          : c.picked_by === "human"
          ? `<div style="background:#10B981;color:#FDFBF7;font-size:0.7rem;font-weight:800;padding:4px 8px;border-radius:6px;">✅ NO SEU ELENCO</div>`
          : isLocked
          ? `<div class="mystery-stat-pill" style="opacity:0.65;">🔒 Bucket Encerrado</div>`
          : `<div class="mystery-stat-pill">🔒 Média & Jogos Ocultos</div>`;

      return `
        <div
          class="bucket-soul-card ${isTaken ? "taken" : ""} ${isSelected ? "selected-soul" : ""}"
          data-bucket-pid="${c.player_id}"
        >
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span class="pos-badge pos-${c.position_code}">${c.position_code}</span>
            <span class="era-span-tag">✅ Atuou em ${s3.season}/R${s3.round}</span>
          </div>

          <div class="athlete-portrait-box" style="height:110px;">
            <img
              src="${c.photo_url || DEFAULT_SILHOUETTE}"
              alt="${c.short_name}"
              style="width:100px;height:100px;object-fit:contain;"
              onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';"
            />
          </div>

          <div>
            <div class="athlete-short-name">${c.short_name}</div>
            <div class="athlete-pos-label">${c.position_name}</div>
          </div>

          <div class="bucket-round-club-box" title="Clube defendido na Rodada #${s3.round} de ${s3.season}">
            ${clubLogo ? `<img src="${clubLogo}" alt="${c.round_team.abbreviation}" />` : ""}
            <div style="text-align:left;">
              <div style="font-size:0.62rem;color:var(--text-muted);text-transform:uppercase;">Clube na Rodada</div>
              <div style="font-size:0.82rem;font-weight:800;color:var(--text-light);">${c.round_team.team_name} (${c.round_team.abbreviation})</div>
            </div>
          </div>

          ${statusBadge}
        </div>
      `;
    })
    .join("");

  let swapDrawerHTML = "";
  if (selectedCard && !isLocked) {
    swapDrawerHTML = `
      <div class="swap-drawer">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
          <div>
            <span class="stage-pill">TROCA ÚNICA DE MESMA POSIÇÃO (${selectedCard.position_code})</span>
            <h4 style="font-family:'Cinzel',serif;font-size:1.1rem;color:var(--text-light);">
              Escolha qual ${selectedCard.position_code} do seu Time Squad será liberado para a entrada de <span style="color:var(--text-amber);">${selectedCard.short_name}</span>:
            </h4>
          </div>
        </div>

        <div class="swap-candidates-grid">
          ${samePosCandidates
            .map((p) => {
              const isDropSel = appState.selectedDropPlayerId === p.player_id;
              return `
                <div class="swap-cand-item ${isDropSel ? "selected-drop" : ""}" data-drop-pid="${p.player_id}">
                  <img src="${p.photo_url || DEFAULT_SILHOUETTE}" class="table-avatar" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
                  <div style="text-align:left;">
                    <div style="font-weight:800;color:var(--text-light);font-size:0.9rem;">${p.short_name}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--text-gold);">
                      Média: ${p.avg_score.toFixed(2)} · ${p.rounds_played}j (${p.first_season}–${p.last_season})
                    </div>
                  </div>
                </div>
              `;
            })
            .join("")}
        </div>

        <div style="display:flex;justify-content:flex-end;gap:12px;">
          <button id="btn-s3-confirm-swap" class="btn-chrono" style="padding:11px 22px;">
            🔄 Confirmar Única Troca (${selectedCard.short_name} IN) & Avançar →
          </button>
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    ${humanBanner}

    <div class="stage2-top-banner">
      <div>
        <span class="stage-pill">COORDENADA TEMPORAL CRAVADA</span>
        <h3 style="font-family:'Cinzel',serif;font-size:1.3rem;color:var(--text-light);">
          ⏳ Temporada ${s3.season} · Rodada #${s3.round} do Brasileirão Série A
        </h3>
      </div>
      ${
        !isLocked
          ? `<button id="btn-s3-pass" class="btn-gallery" style="padding:10px 18px;font-size:0.88rem;">
               ⏭️ Passar a Vez (Manter 24 Atletas Intactos) →
             </button>`
          : `<span class="hud-lock-indicator">🔒 1 Decisão por Partida</span>`
      }
    </div>

    ${aiBanner}

    ${
      !isLocked
        ? `<p style="font-size:0.86rem;color:var(--text-muted);">
             💡 <strong>Regra Oficial:</strong> Você tem direito a <strong>no máximo 1 troca</strong> da mesma posição por partida (ou pode passar a vez). Após confirmar, o Bucket é trancado!
           </p>`
        : ""
    }

    <div class="bucket-grid">${cardsHTML}</div>

    ${swapDrawerHTML}
  `;

  const backActiveBtn = document.getElementById("btn-s3-back-active");
  if (backActiveBtn) {
    backActiveBtn.addEventListener("click", () => {
      appState.stage = appState.maxUnlockedStage;
      renderAll();
    });
  }

  if (isLocked) return;

  container.querySelectorAll("[data-bucket-pid]").forEach((el) => {
    el.addEventListener("click", () => {
      const pid = parseInt(el.getAttribute("data-bucket-pid"), 10);
      const card = cards.find((c) => c.player_id === pid);
      if (!card || card.picked_by) return;
      appState.selectedBucketPlayerId = pid;
      renderStage3();
    });
  });

  container.querySelectorAll("[data-drop-pid]").forEach((el) => {
    el.addEventListener("click", () => {
      appState.selectedDropPlayerId = parseInt(el.getAttribute("data-drop-pid"), 10);
      renderStage3();
    });
  });

  const passBtn = document.getElementById("btn-s3-pass");
  if (passBtn) {
    passBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage3/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "pass" }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const swapBtn = document.getElementById("btn-s3-confirm-swap");
  if (swapBtn) {
    swapBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage3/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "swap",
          bucket_player_id: appState.selectedBucketPlayerId,
          dropped_player_id: appState.selectedDropPlayerId,
        }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }
}

// ============================================================================
// STAGE 4: HIGHLIGHTS OF DESTINY (STRICTLY OPTION A OR OPTION B — NO DOUBLE DIP)
// ============================================================================
function renderStage4() {
  const container = document.getElementById("stage4-container");
  if (!container || !appState.stage4) return;

  const s4 = appState.stage4;
  const s3 = appState.stage3 || {};
  const slots = s4.slots || [];
  const isLocked = Boolean(s4.completed);

  const summaryLogs = [];
  if (s3.human_decision) summaryLogs.push(`👤 ${s3.human_decision.reason}`);
  if (s3.ai_decision) summaryLogs.push(`🤖 ${s3.ai_decision.reason}`);

  const lockBannerHTML = isLocked
    ? `<div class="locked-stage-banner">
         <div>
           <strong>🔒 REVELAÇÃO DO ORÁCULO SELADA (ANTI-RIGGING):</strong> Você escolheu <strong>${
             s4.choice_mode === "2_scores"
               ? "OPÇÃO B (2 Confrontos + Placar Exato)"
               : "OPÇÃO A (5 Confrontos Sem Placar)"
           }</strong>. Os demais jogos permanecem ocultos!
         </div>
         <button id="btn-s4-proceed-top" class="btn-chrono" style="padding:8px 16px;font-size:0.82rem;">
           ⚡ Ir para Stage 5 (Regra Maluca) →
         </button>
       </div>`
    : "";

  const barsHTML = slots
    .map((slot, idx) => {
      if (!slot.revealed) {
        return `
          <div class="destiny-bar unrevealed">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;">CONFRONTO #${String(idx + 1).padStart(2, "0")}</span>
            <span style="font-family:'Cinzel',serif;font-weight:800;letter-spacing:0.12em;">🔒 OCULTO NAS BRUMAS DO TEMPO</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;">? x ?</span>
          </div>
        `;
      }

      const hLogo = getClubLogoUrl(slot.home_team);
      const aLogo = getClubLogoUrl(slot.away_team);
      const scoreText = slot.show_score
        ? `${slot.home_score} × ${slot.away_score}`
        : `VS`;

      return `
        <div class="destiny-bar revealed">
          <div class="destiny-team-side home">
            <img src="${hLogo}" alt="${slot.home_team.abbreviation}" />
            <span>${slot.home_team.team_name}</span>
          </div>
          <span class="destiny-score-pill">${scoreText}</span>
          <div class="destiny-team-side away">
            <span>${slot.away_team.team_name}</span>
            <img src="${aLogo}" alt="${slot.away_team.abbreviation}" />
          </div>
        </div>
      `;
    })
    .join("");

  container.innerHTML = `
    ${lockBannerHTML}

    ${
      summaryLogs.length
        ? `<div class="ai-log-banner">${summaryLogs.join(" &nbsp;|&nbsp; ")}</div>`
        : ""
    }

    <div class="destiny-choices-row">
      <button
        class="destiny-choice-btn ${s4.choice_mode === "5_matches" ? "active-choice" : ""}"
        id="btn-s4-5matches"
        ${isLocked ? "disabled" : ""}
      >
        <div style="font-family:'Cinzel',serif;font-size:1.08rem;font-weight:900;color:var(--text-gold);margin-bottom:4px;">
          ${s4.choice_mode === "5_matches" ? "✅ " : isLocked ? "🔒 " : "🔍 "}OPÇÃO A: Revelar 5 Confrontos (Sem Placar)
        </div>
        <div style="font-size:0.82rem;color:var(--text-muted);">
          Descubra <strong>5 jogos (Mandante vs Visitante)</strong> da Rodada #${s4.round} de ${s4.season} para identificar quais clubes atuaram em casa.
        </div>
      </button>

      <button
        class="destiny-choice-btn ${s4.choice_mode === "2_scores" ? "active-choice" : ""}"
        id="btn-s4-2scores"
        ${isLocked ? "disabled" : ""}
      >
        <div style="font-family:'Cinzel',serif;font-size:1.08rem;font-weight:900;color:var(--text-amber);margin-bottom:4px;">
          ${s4.choice_mode === "2_scores" ? "✅ " : isLocked ? "🔒 " : "🎯 "}OPÇÃO B: Revelar 2 Confrontos + Placar Exato
        </div>
        <div style="font-size:0.82rem;color:var(--text-muted);">
          Descubra <strong>2 jogos com o placar final exato</strong> para caçar goleadas (G/A) ou defesas que garantiram Saldo de Gol (SG)!
        </div>
      </button>
    </div>

    <div class="destiny-bars-grid">
      ${barsHTML}
    </div>
  `;

  const topProceed = document.getElementById("btn-s4-proceed-top");
  if (topProceed) {
    topProceed.addEventListener("click", () => {
      appState.stage = 5;
      renderAll();
    });
  }

  if (isLocked) {
    appendStage4ProceedButton();
    return;
  }

  document.getElementById("btn-s4-5matches").addEventListener("click", async () => {
    const res = await fetch("/api/stage4/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ choice_mode: "5_matches" }),
    });
    const data = await res.json();
    syncFromServer(data);
    appState.stage = 4;
    renderAll();
  });

  document.getElementById("btn-s4-2scores").addEventListener("click", async () => {
    const res = await fetch("/api/stage4/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ choice_mode: "2_scores" }),
    });
    const data = await res.json();
    syncFromServer(data);
    appState.stage = 4;
    renderAll();
  });
}

function appendStage4ProceedButton() {
  const container = document.getElementById("stage4-container");
  if (!container || document.getElementById("btn-s4-proceed-s5")) return;
  const div = document.createElement("div");
  div.style.cssText = "display:flex;justify-content:flex-end;margin-top:10px;";
  div.innerHTML = `
    <button id="btn-s4-proceed-s5" class="btn-chrono" style="font-size:0.96rem;padding:12px 24px;">
      ⚡ Avançar para Stage 5 (Revelar Regra Maluca da Partida) →
    </button>
  `;
  container.appendChild(div);
  document.getElementById("btn-s4-proceed-s5").addEventListener("click", () => {
    appState.stage = 5;
    renderAll();
  });
}

// ============================================================================
// STAGE 5: CRAZY RULES REVEAL & 17-SCOUT WEIGHT MATRIX
// ============================================================================
function renderStage5() {
  const container = document.getElementById("stage5-container");
  if (!container || !appState.stage5 || !appState.stage5.active_rule) return;

  const rule = appState.stage5.active_rule;
  const allRules = appState.stage5.all_rules_summary || [];
  const isLocked = Boolean(appState.stage5.locked);

  const rulePills = !isLocked
    ? allRules
        .map(
          (r) => `
          <button
            class="mode-btn ${r.rule_id === rule.rule_id ? "active" : ""}"
            data-force-rule="${r.rule_id}"
            style="border:1px solid rgba(242,194,73,0.3);"
          >
            ${r.name}
          </button>
        `
        )
        .join("")
    : "";

  const scoutCards = (rule.scout_comparison || [])
    .map((sc) => {
      const badge =
        sc.status === "buff"
          ? `<span style="color:var(--text-emerald);font-weight:800;font-size:0.74rem;">▲ BUFF</span>`
          : sc.status === "nerf"
          ? `<span style="color:var(--text-vermilion);font-weight:800;font-size:0.74rem;">▼ NERF</span>`
          : `<span style="color:var(--text-dim);font-size:0.72rem;">= BASE</span>`;

      return `
        <div class="scout-delta-card ${sc.status}">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-family:'JetBrains Mono',monospace;font-weight:900;font-size:1rem;color:var(--text-gold);">${sc.scout}</span>
            ${badge}
          </div>
          <div style="font-size:0.73rem;color:var(--text-muted);margin:3px 0 6px;">${sc.label}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.86rem;color:var(--text-light);">
            <span style="opacity:0.6;text-decoration:line-through;margin-right:6px;">${sc.base_weight > 0 ? `+${sc.base_weight}` : sc.base_weight}</span>
            <strong>${sc.rule_weight > 0 ? `+${sc.rule_weight}` : sc.rule_weight} pts</strong>
          </div>
        </div>
      `;
    })
    .join("");

  container.innerHTML = `
    ${
      isLocked
        ? `<div class="locked-stage-banner">
             <div><strong>🔒 REGRA MALUCA SELADA:</strong> ${rule.name} está oficialmente ativa para a escalação desta partida.</div>
             <button id="btn-s5-back-active" class="btn-chrono" style="padding:7px 14px;font-size:0.8rem;">
               ➡️ Voltar ao Gramado (Stage 6)
             </button>
           </div>`
        : `<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:16px;">
             <div style="display:flex;gap:6px;flex-wrap:wrap;">${rulePills}</div>
             <button id="btn-s5-random" class="btn-gallery" style="padding:8px 14px;">
               🎲 Sortear Outra Regra (Modo Teste)
             </button>
           </div>`
    }

    <div class="crazy-rule-hero">
      <img src="${rule.art_url}" alt="${rule.name}" class="crazy-rule-art" />
      <div>
        <span class="stage-pill">REGRA ATIVA NA PARTIDA #${appState.match_number}</span>
        <h3 style="font-family:'Cinzel',serif;font-size:1.75rem;color:var(--text-gold);margin:6px 0;">${rule.name}</h3>
        <p style="font-size:1.02rem;color:var(--text-light);font-style:italic;margin-bottom:14px;">"${rule.tagline}"</p>

        <div style="background:rgba(249,160,63,0.12);border-left:4px solid var(--text-amber);padding:12px 16px;border-radius:10px;">
          <div style="font-size:0.75rem;font-weight:800;color:var(--text-gold);text-transform:uppercase;margin-bottom:6px;">
            ⚡ Impactos Táticos Principais:
          </div>
          <ul style="padding-left:18px;font-size:0.88rem;color:var(--text-light);line-height:1.6;">
            ${(rule.key_changes || []).map((k) => `<li>${k}</li>`).join("")}
          </ul>
        </div>
      </div>
    </div>

    <h4 style="font-family:'Cinzel',serif;color:var(--text-gold);font-size:1.05rem;">
      📊 Matriz Universal dos 17 Scouts (Cartola Base vs ${rule.name})
    </h4>
    <div class="scout-matrix-grid">
      ${scoutCards}
    </div>

    ${
      !isLocked
        ? `<div style="display:flex;justify-content:flex-end;margin-top:22px;">
             <button id="btn-s5-proceed" class="btn-chrono" style="font-size:0.98rem;padding:12px 26px;">
               🔒 Selar Regra & Avançar para Stage 6 (Escalação no Gramado) →
             </button>
           </div>`
        : ""
    }
  `;

  const backBtn = document.getElementById("btn-s5-back-active");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      appState.stage = appState.maxUnlockedStage;
      renderAll();
    });
  }

  if (isLocked) return;

  container.querySelectorAll("[data-force-rule]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const ruleId = btn.getAttribute("data-force-rule");
      const res = await fetch("/api/stage5/reroll", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rule_id: ruleId }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  });

  const randBtn = document.getElementById("btn-s5-random");
  if (randBtn) {
    randBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage5/reroll", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const procBtn = document.getElementById("btn-s5-proceed");
  if (procBtn) {
    procBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage5/proceed", { method: "POST" });
      syncFromServer(await res.json());
      renderAll();
    });
  }
}

// ============================================================================
// SHARED TACTICAL PITCH & SQUAD BUILDER HELPERS (STAGE 6 & STAGE 7)
// ============================================================================
let _lineupToastTimer = null;

function showLineupDiagnosticToast(message, isValid = false) {
  let toast = document.getElementById("lineup-diagnostic-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "lineup-diagnostic-toast";
    document.body.appendChild(toast);
  }
  toast.className = `lineup-diagnostic-toast ${isValid ? "toast-ok" : "toast-error"}`;
  toast.style.opacity = "1";
  toast.style.display = "flex";
  toast.innerHTML = `
    <div style="display:flex;align-items:center;gap:10px;">
      <span style="font-size:1.15rem;">${isValid ? "✅" : "⚠️"}</span>
      <span>${message}</span>
    </div>
    <button id="btn-close-diag-toast" style="background:transparent;border:none;color:#FDFBF7;font-weight:900;cursor:pointer;font-size:0.95rem;">✕</button>
  `;
  const closeBtn = document.getElementById("btn-close-diag-toast");
  if (closeBtn) {
    closeBtn.onclick = () => {
      toast.style.display = "none";
    };
  }
  if (_lineupToastTimer) clearTimeout(_lineupToastTimer);
  _lineupToastTimer = setTimeout(() => {
    if (toast) toast.style.display = "none";
  }, 5500);
}

function sanitizeLineupState(squad, starterIds, captainId) {
  const validSquadIds = new Set((squad || []).map((p) => p.player_id));
  const cleanStarters = Array.from(new Set(starterIds || [])).filter((id) => validSquadIds.has(id));
  let cleanCap = captainId && cleanStarters.includes(captainId) ? captainId : null;
  if (!cleanCap && cleanStarters.length > 0) {
    const nonTec = squad.find((p) => cleanStarters.includes(p.player_id) && p.position_code !== "TEC");
    cleanCap = nonTec ? nonTec.player_id : cleanStarters[0];
  }
  return { starterIds: cleanStarters, captainId: cleanCap };
}

function evaluateLineupStatus(squad, formation, starterIds, captainId) {
  const quotas = FORMATION_QUOTAS[formation] || FORMATION_QUOTAS["4-3-3"];
  const squadById = {};
  squad.forEach((p) => {
    squadById[p.player_id] = p;
  });

  // Always count only valid unique IDs belonging to the current 24-man squad
  const cleanStarters = Array.from(new Set(starterIds || [])).filter((id) => squadById[id] !== undefined);

  const counts = { GOL: 0, ZAG: 0, LAT: 0, MEI: 0, ATA: 0, TEC: 0 };
  cleanStarters.forEach((pid) => {
    const p = squadById[pid];
    if (p && counts[p.position_code] !== undefined) {
      counts[p.position_code] += 1;
    }
  });

  const missingMessages = [];
  const diagPills = [];

  Object.entries(quotas).forEach(([pos, req]) => {
    const cur = counts[pos] || 0;
    if (req === 0 && cur === 0) {
      return;
    }
    if (cur < req) {
      const diff = req - cur;
      const msg = `${ diff === 1 ? "Falta" : "Faltam" } ${diff} ${pos} (${cur}/${req})`;
      missingMessages.push(msg);
      diagPills.push(`<span class="diag-pos-pill missing">❌ ${pos}: ${cur}/${req} · ${msg}</span>`);
    } else if (cur > req) {
      const diff = cur - req;
      const msg = `Excesso de ${diff} ${pos} (${cur}/${req})`;
      missingMessages.push(msg);
      diagPills.push(`<span class="diag-pos-pill excess">⚠️ ${pos}: ${cur}/${req} · Remova ${diff} ${pos}</span>`);
    } else {
      diagPills.push(`<span class="diag-pos-pill ok">✅ ${pos}: ${cur}/${req}</span>`);
    }
  });

  const hasValidCap = cleanStarters.includes(captainId);
  const capPlayer = hasValidCap ? squadById[captainId] : null;
  if (!hasValidCap) {
    missingMessages.push("Falta definir o Capitão (© 2x)");
    diagPills.push(`<span class="diag-pos-pill missing">❌ CAP © 2x: Pendente</span>`);
  } else {
    diagPills.push(`<span class="diag-pos-pill ok">✅ CAP © 2x: ${capPlayer ? capPlayer.short_name : "OK"}</span>`);
  }

  const isValid = missingMessages.length === 0 && cleanStarters.length === 12;
  const diagPillsHTML = `<div class="diag-pos-pills-row">${diagPills.join("")}</div>`;
  const reasonList = missingMessages.length > 0 ? missingMessages.join(" · ") : `Total escalado: ${cleanStarters.length}/12`;

  return {
    isValid,
    counts,
    quotas,
    hasValidCap,
    missingMessages,
    diagPillsHTML,
    toastMessage: isValid
      ? `Formação ${formation} completa (11 Titulares + TEC + Capitão © 2x)! Pronto para o Kick-Off!`
      : `Formação ${formation} incompleta — ${reasonList}`,
    summaryText: isValid
      ? `🟢 ESCALAÇÃO VÁLIDA (${formation}): 11 Titulares + 1 Técnico + Capitão (${capPlayer ? capPlayer.short_name : "2x"}) prontos!`
      : `🔴 ESCALAÇÃO INCOMPLETA (${formation}): ${reasonList}`,
  };
}

function buildInteractivePitchHTML(squad, formation, starterIds, captainId, options = {}) {
  const quotas = FORMATION_QUOTAS[formation] || FORMATION_QUOTAS["4-3-3"];
  const zeroedSet = new Set(options.zeroedIds || []);
  const expelledSet = new Set(options.expelledIds || []);
  const squadById = {};
  squad.forEach((p) => {
    squadById[p.player_id] = p;
  });

  const startersByPos = { GOL: [], ZAG: [], LAT: [], MEI: [], ATA: [], TEC: [] };
  starterIds.forEach((pid) => {
    const p = squadById[pid];
    if (p && startersByPos[p.position_code]) {
      startersByPos[p.position_code].push(p);
    }
  });

  const renderSlotToken = (posCode, slotIdx) => {
    const p = startersByPos[posCode][slotIdx];
    if (!p) {
      return `
        <div class="pitch-token empty-slot">
          <span class="pos-badge pos-${posCode}" style="font-size:0.58rem;padding:2px 5px;">${posCode}</span>
          <span style="font-size:0.62rem;margin-top:4px;color:#FF8A80;font-weight:800;">Falta ${posCode}</span>
        </div>
      `;
    }
    const isCap = p.player_id === captainId;
    const isZero = zeroedSet.has(p.player_id);
    const isExp = expelledSet.has(p.player_id);
    const extraCls = [
      isCap ? "is-captain" : "",
      isZero ? "zeroed-neon-glow" : "",
      isExp ? "grenal-expelled-glow" : "",
    ]
      .filter(Boolean)
      .join(" ");

    return `
      <div class="pitch-token ${extraCls}" data-pitch-pid="${p.player_id}" title="Clique para tornar Capitão (2x) ou remover">
        ${isCap ? `<span class="captain-armband-badge">© 2x</span>` : ""}
        ${isZero ? `<div style="font-size:0.55rem;background:#00E5FF;color:#000;font-weight:900;border-radius:4px;margin-bottom:2px;">⚡ ZEROU!</div>` : ""}
        ${isExp ? `<div style="font-size:0.55rem;background:#E0533C;color:#FFF;font-weight:900;border-radius:4px;margin-bottom:2px;">🟥 EXPULSO</div>` : ""}
        <img src="${p.photo_url || DEFAULT_SILHOUETTE}" class="pitch-token-avatar" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
        <div class="pitch-token-name">${p.short_name}</div>
        <div class="pitch-token-sub">${posCode} · ${p.avg_score.toFixed(1)}</div>
      </div>
    `;
  };

  const ataRow = Array.from({ length: quotas.ATA }, (_, i) => renderSlotToken("ATA", i)).join("");
  const meiRow = Array.from({ length: quotas.MEI }, (_, i) => renderSlotToken("MEI", i)).join("");

  // Defense row combines LAT (left/right flanks) + ZAG (center)
  const defTokens = [];
  if (quotas.LAT >= 1) defTokens.push(renderSlotToken("LAT", 0));
  for (let z = 0; z < quotas.ZAG; z++) {
    defTokens.push(renderSlotToken("ZAG", z));
  }
  if (quotas.LAT >= 2) defTokens.push(renderSlotToken("LAT", 1));

  const golRow = `${renderSlotToken("GOL", 0)} <div style="margin-left:18px;">${renderSlotToken("TEC", 0)}</div>`;

  return `
    <div class="tactical-pitch-board">
      <div style="text-align:center;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:rgba(253,251,247,0.75);z-index:2;">
        ⬆️ ATAQUE · FORMAÇÃO ${formation} (Clique em um titular no gramado para dar a faixa © 2x)
      </div>
      <div class="pitch-row">${ataRow}</div>
      <div class="pitch-row">${meiRow}</div>
      <div class="pitch-row">${defTokens.join("")}</div>
      <div class="pitch-row">${golRow}</div>
    </div>
  `;
}

function buildSquadSelectorListHTML(squad, formation, starterIds, captainId, options = {}) {
  const quotas = FORMATION_QUOTAS[formation] || FORMATION_QUOTAS["4-3-3"];
  const starterSet = new Set(starterIds);
  const zeroedSet = new Set(options.zeroedIds || []);
  const expelledSet = new Set(options.expelledIds || []);
  const isReadOnly = Boolean(options.readOnly);

  return POSITION_BLOCKS.map((block) => {
    const req = quotas[block.code] || 0;
    const posPlayers = squad.filter((p) => p.position_code === block.code);
    const curSelected = posPlayers.filter((p) => starterSet.has(p.player_id)).length;
    const statusBadge =
      curSelected === req
        ? `<span style="color:var(--text-emerald);font-weight:900;">✅ ${curSelected} / ${req}</span>`
        : curSelected < req
        ? `<span style="color:var(--text-vermilion);font-weight:900;">❌ ${curSelected} / ${req} (Falta ${req - curSelected} ${block.code})</span>`
        : `<span style="color:var(--text-amber);font-weight:900;">⚠️ ${curSelected} / ${req} (Excesso +${curSelected - req})</span>`;

    const rowsHTML = posPlayers
      .map((p) => {
        const isStarter = starterSet.has(p.player_id);
        const isCap = p.player_id === captainId;
        const isZero = zeroedSet.has(p.player_id);
        const isExp = expelledSet.has(p.player_id);
        const clubsMini = (p.top_teams || [])
          .slice(0, 2)
          .map((t) => `<img src="${getClubLogoUrl(t)}" style="width:15px;height:15px;vertical-align:middle;" title="${t.team_name}" /> ${t.abbreviation}`)
          .join(" · ");

        return `
          <div class="lineup-player-row ${isStarter ? "selected-starter" : ""} ${isZero ? "zeroed-alert" : ""}">
            <div style="display:flex;align-items:center;gap:8px;min-width:0;">
              <img src="${p.photo_url || DEFAULT_SILHOUETTE}" class="table-avatar" style="width:34px;height:34px;" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
              <div style="min-width:0;">
                <div style="font-weight:800;font-size:0.84rem;color:var(--text-light);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                  ${p.short_name}
                  ${p.recruited_from_bucket ? `<span style="color:var(--text-sapphire);font-size:0.65rem;">(👻 Bucket)</span>` : ""}
                  ${isZero ? `<span style="background:#00E5FF;color:#000;font-size:0.62rem;padding:1px 5px;border-radius:4px;font-weight:900;">⚡ ZEROU NA RODADA</span>` : ""}
                  ${isExp ? `<span style="background:#E0533C;color:#FFF;font-size:0.62rem;padding:1px 5px;border-radius:4px;font-weight:900;">🟥 EXPULSO (GRENAL)</span>` : ""}
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.67rem;color:var(--text-muted);">
                  Média: <strong style="color:var(--text-gold);">${p.avg_score.toFixed(2)}</strong> · ${p.rounds_played}j · ${clubsMini}
                </div>
              </div>
            </div>

            ${
              !isReadOnly
                ? `<div style="display:flex;align-items:center;gap:5px;flex-shrink:0;">
                     ${
                       isStarter
                         ? `<button class="btn-cap-toggle ${isCap ? "active-cap" : ""}" data-cap-pid="${p.player_id}" title="Definir como Capitão (Pontuação Dobrada 2x)">
                              © 2x
                            </button>`
                         : ""
                     }
                     <button class="btn-lineup-toggle ${isStarter ? "active-starter" : ""}" data-toggle-pid="${p.player_id}">
                       ${isStarter ? "✅ Titular" : "+ Escalar"}
                     </button>
                   </div>`
                : `<span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:800;color:${isStarter ? "var(--text-emerald)" : "var(--text-dim)"};">
                     ${isStarter ? (isCap ? "✅ TITULAR (© 2x)" : "✅ TITULAR") : "Reserva"}
                   </span>`
            }
          </div>
        `;
      })
      .join("");

    return `
      <div class="lineup-pos-group-header">
        <span>${block.title}</span>
        <span>${statusBadge}</span>
      </div>
      ${rowsHTML}
    `;
  }).join("");
}

function togglePlayerInLineup(squad, formation, starterIds, captainId, clickedPid) {
  const quotas = FORMATION_QUOTAS[formation] || FORMATION_QUOTAS["4-3-3"];
  const sanitized = sanitizeLineupState(squad, starterIds, captainId);
  const player = squad.find((p) => p.player_id === clickedPid);
  if (!player) return sanitized;

  const posCode = player.position_code;
  const maxForPos = quotas[posCode] || 0;
  let nextStarters = [...sanitized.starterIds];
  let nextCap = sanitized.captainId;

  if (nextStarters.includes(clickedPid)) {
    nextStarters = nextStarters.filter((id) => id !== clickedPid);
    if (nextCap === clickedPid) {
      nextCap = nextStarters[0] || null;
    }
  } else {
    if (maxForPos === 0) {
      showLineupDiagnosticToast(
        `A formação ${formation} não utiliza atletas da posição ${posCode} (0/${maxForPos})! Mude para 4-3-3, 4-4-2 ou 4-5-1 para escalar Laterais.`,
        false
      );
      return sanitized;
    }
    const samePosStarters = nextStarters.filter((id) => {
      const sp = squad.find((x) => x.player_id === id);
      return sp && sp.position_code === posCode;
    });
    if (samePosStarters.length >= maxForPos) {
      // Automatically swap out the first selected player of that position to make toggling effortless
      const removedId = samePosStarters[0];
      nextStarters = nextStarters.filter((id) => id !== removedId);
      if (nextCap === removedId) {
        nextCap = clickedPid;
      }
    }
    nextStarters.push(clickedPid);
    if (!nextCap) nextCap = clickedPid;
  }

  return sanitizeLineupState(squad, nextStarters, nextCap);
}

// ============================================================================
// STAGE 6: TACTICAL FORMATION, INTERACTIVE PITCH & CAPTAIN (2x)
// ============================================================================
function renderStage6() {
  const container = document.getElementById("stage6-container");
  if (!container || appState.humanRoosterIdx === null) return;

  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const squad = hRooster.players;
  const s6 = appState.stage6 || {};
  const isLocked = Boolean(s6.completed);

  // Sanitize Stage 6 starters in-place so dropped Bucket players never linger as ghost IDs
  const cleanS6 = sanitizeLineupState(squad, appState.stage6Starters, appState.stage6CaptainId);
  appState.stage6Starters = cleanS6.starterIds;
  appState.stage6CaptainId = cleanS6.captainId;

  const status = evaluateLineupStatus(
    squad,
    appState.stage6Formation,
    appState.stage6Starters,
    appState.stage6CaptainId
  );

  const formationBtnsHTML = Object.keys(FORMATION_QUOTAS)
    .map(
      (fmt) => `
      <button
        class="mode-btn ${appState.stage6Formation === fmt ? "active" : ""}"
        data-s6-fmt="${fmt}"
        ${isLocked ? "disabled" : ""}
      >
        📐 ${fmt}
      </button>
    `
    )
    .join("");

  container.innerHTML = `
    ${
      isLocked
        ? `<div class="locked-stage-banner">
             <div><strong>🔒 ESCALAÇÃO TITULAR CONFIRMADA (ANTI-RIGGING):</strong> Seus 12 titulares do 1º tempo já entraram em campo!</div>
             <button id="btn-s6-back-active" class="btn-chrono" style="padding:7px 14px;font-size:0.8rem;">
               ➡️ Ir para Etapa Atual (Stage ${appState.maxUnlockedStage})
             </button>
           </div>`
        : ""
    }

    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:var(--text-gold);font-weight:800;">ESQUEMA TÁTICO:</span>
        <div class="view-mode-toggle">${formationBtnsHTML}</div>
      </div>

      ${
        !isLocked
          ? `<div style="display:flex;gap:8px;flex-wrap:wrap;">
               <button id="btn-s6-autofill" class="btn-gallery" style="padding:7px 13px;font-size:0.78rem;">
                 ⚡ Auto-Escalar Melhores Médias (${appState.stage6Formation})
               </button>
               <button id="btn-s6-clear" class="btn-gallery" style="padding:7px 13px;font-size:0.78rem;border-color:#E0533C;">
                 🧹 Limpar Campo
               </button>
             </div>`
          : ""
      }
    </div>

    <div class="status-indicator-bar ${status.isValid ? "valid" : "invalid"}">
      <div style="flex:1;">
        <div>${status.summaryText}</div>
        ${status.diagPillsHTML}
      </div>
      ${
        !isLocked
          ? `<button id="btn-s6-kickoff" class="btn-chrono" style="${!status.isValid ? "opacity:0.75;border-color:#E0533C;" : ""}">
               ${status.isValid ? "⚽ KICK-OFF! Iniciar Partida & Ir para o Intervalo (Stage 7) →" : "⚠️ Verificar Pendências da Escalação"}
             </button>`
          : ""
      }
    </div>

    <div class="pitch-workspace">
      ${buildInteractivePitchHTML(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId)}
      <div class="squad-selector-pane">
        ${buildSquadSelectorListHTML(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId, {
          readOnly: isLocked,
        })}
      </div>
    </div>
  `;

  const backBtn = document.getElementById("btn-s6-back-active");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      appState.stage = appState.maxUnlockedStage;
      renderAll();
    });
  }

  if (isLocked) return;

  container.querySelectorAll("[data-s6-fmt]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fmt = btn.getAttribute("data-s6-fmt");
      const auto = autoBuildBestLineup(squad, fmt);
      appState.stage6Formation = auto.formation;
      appState.stage6Starters = auto.starter_ids;
      appState.stage6CaptainId = auto.captain_id;
      renderStage6();
      const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  document.getElementById("btn-s6-autofill").addEventListener("click", () => {
    const auto = autoBuildBestLineup(squad, appState.stage6Formation);
    appState.stage6Starters = auto.starter_ids;
    appState.stage6CaptainId = auto.captain_id;
    renderStage6();
    const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
    showLineupDiagnosticToast(st.toastMessage, st.isValid);
  });

  document.getElementById("btn-s6-clear").addEventListener("click", () => {
    appState.stage6Starters = [];
    appState.stage6CaptainId = null;
    renderStage6();
    const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
    showLineupDiagnosticToast(st.toastMessage, st.isValid);
  });

  container.querySelectorAll("[data-toggle-pid]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pid = parseInt(btn.getAttribute("data-toggle-pid"), 10);
      const res = togglePlayerInLineup(
        squad,
        appState.stage6Formation,
        appState.stage6Starters,
        appState.stage6CaptainId,
        pid
      );
      appState.stage6Starters = res.starterIds;
      appState.stage6CaptainId = res.captainId;
      renderStage6();
      const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  container.querySelectorAll("[data-cap-pid]").forEach((btn) => {
    btn.addEventListener("click", () => {
      appState.stage6CaptainId = parseInt(btn.getAttribute("data-cap-pid"), 10);
      renderStage6();
      const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  container.querySelectorAll("[data-pitch-pid]").forEach((tok) => {
    tok.addEventListener("click", () => {
      const pid = parseInt(tok.getAttribute("data-pitch-pid"), 10);
      if (appState.stage6CaptainId !== pid) {
        appState.stage6CaptainId = pid;
      } else {
        appState.stage6Starters = appState.stage6Starters.filter((id) => id !== pid);
        appState.stage6CaptainId = appState.stage6Starters[0] || null;
      }
      renderStage6();
      const st = evaluateLineupStatus(squad, appState.stage6Formation, appState.stage6Starters, appState.stage6CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  const kickoffBtn = document.getElementById("btn-s6-kickoff");
  if (kickoffBtn) {
    kickoffBtn.addEventListener("click", async () => {
      if (!status.isValid) {
        showLineupDiagnosticToast(status.toastMessage, false);
        return;
      }
      const res = await fetch("/api/stage6/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          formation: appState.stage6Formation,
          starter_ids: appState.stage6Starters,
          captain_id: appState.stage6CaptainId,
        }),
      });
      const data = await res.json();
      if (data.error) {
        showLineupDiagnosticToast(data.error, false);
        return;
      }
      appState.stage7Formation = appState.stage6Formation;
      appState.stage7Starters = [...appState.stage6Starters];
      appState.stage7CaptainId = appState.stage6CaptainId;
      syncFromServer(data);
      renderAll();
    });
  }
}

// ============================================================================
// STAGE 7: HALF-TIME 6v6 SAMPLE, 3 SUBSTITUTIONS & POWER-UPS
// ============================================================================
function renderStage7() {
  const container = document.getElementById("stage7-container");
  if (!container || appState.humanRoosterIdx === null) return;

  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const aRooster = appState.roosters[appState.aiRoosterIdx];
  const squad = hRooster.players;
  const s6 = appState.stage6 || {};
  const s7 = appState.stage7 || {};
  const isLocked = Boolean(s7.completed);

  const cleanS7 = sanitizeLineupState(squad, appState.stage7Starters, appState.stage7CaptainId);
  appState.stage7Starters = cleanS7.starterIds;
  appState.stage7CaptainId = cleanS7.captainId;

  const initialStarters = (s6.human_lineup && s6.human_lineup.starter_ids) || [];
  const subsMade = appState.stage7Starters.filter((id) => !initialStarters.includes(id)).length;
  const status = evaluateLineupStatus(
    squad,
    appState.stage7Formation,
    appState.stage7Starters,
    appState.stage7CaptainId
  );
  const subsValid = subsMade <= 3;
  const canConfirmHalftime = status.isValid && subsValid;

  const sample = s7.halftime_sample || { human_sample_score: 0, ai_sample_score: 0, sample_size: 6 };
  const remPowerups = (appState.powerups_remaining && appState.powerups_remaining.human) || {};
  const usedThisMatch = s7.powerup_used;

  const aiPreview = s7.ai_starters_preview || [];
  if (!appState.copycatOwnId && appState.stage7Starters.length) {
    appState.copycatOwnId = appState.stage7Starters[0];
  }
  if (!appState.copycatOppId && aiPreview.length) {
    appState.copycatOppId = aiPreview[0].player_id;
  }

  const zeroedIds = s7.zeroed_starter_ids || [];
  const grenalObj = s7.grenal_removed || {};
  const expelledIds = grenalObj.human_removed_ids || [];

  // Power-Up Feedback Banner
  let powerupEffectBanner = "";
  if (usedThisMatch === "reveal_zeroed") {
    powerupEffectBanner = `
      <div class="ai-log-banner" style="border-left-color:var(--text-cyan);background:rgba(0,229,255,0.14);">
        ⚡ <strong>RAIO-X TEMPORAL ATIVADO (Reveal Zeroed Players):</strong>
        ${
          zeroedIds.length > 0
            ? `Foram detectados <strong>${zeroedIds.length} titulares zerados</strong> (destacados em <span style="color:var(--text-cyan);font-weight:800;">AZUL NEON</span> no gramado e na lista)! Aproveite suas 3 substituições para trocá-los!`
            : `Boa notícia! <strong>Nenhum dos seus 12 titulares zerou</strong> nesta rodada!`
        }
      </div>
    `;
  } else if (usedThisMatch === "copycat" && s7.copycat_info) {
    powerupEffectBanner = `
      <div class="ai-log-banner" style="border-left-color:var(--text-gold);">
        🪞 <strong>ESPELHO DE CRONOS ATIVADO (Copycat):</strong> Seu titular <strong>${s7.copycat_info.own_short_name}</strong> copiará a pontuação base do titular adversário <strong>${s7.copycat_info.opponent_short_name}</strong> no cálculo final!
      </div>
    `;
  } else if (usedThisMatch === "grenal" && s7.grenal_removed) {
    powerupEffectBanner = `
      <div class="ai-log-banner" style="border-left-color:#E0533C;background:rgba(224,83,60,0.18);">
        🟥 <strong>CAOS GRENAL ATIVADO (3 Expulsos de Cada Lado):</strong><br/>
        • <strong>Seus 3 Titulares Expulsos (0.00 pts):</strong> ${(grenalObj.human_removed_names || []).join(", ")}<br/>
        • <strong>3 Titulares da IA Expulsos (0.00 pts):</strong> ${(grenalObj.ai_removed_names || []).join(", ")}
      </div>
    `;
  }

  const ownOptionsHTML = appState.stage7Starters
    .map((pid) => {
      const p = squad.find((x) => x.player_id === pid);
      if (!p) return "";
      return `<option value="${pid}" ${appState.copycatOwnId === pid ? "selected" : ""}>${p.short_name} (${p.position_code})</option>`;
    })
    .join("");

  const oppOptionsHTML = aiPreview
    .map(
      (ap) =>
        `<option value="${ap.player_id}" ${appState.copycatOppId === ap.player_id ? "selected" : ""}>${ap.short_name} (${ap.position_code} · Méd ${ap.avg_score.toFixed(1)})</option>`
    )
    .join("");

  const formationBtnsHTML = Object.keys(FORMATION_QUOTAS)
    .map(
      (fmt) => `
      <button
        class="mode-btn ${appState.stage7Formation === fmt ? "active" : ""}"
        data-s7-fmt="${fmt}"
        ${isLocked ? "disabled" : ""}
      >
        📐 ${fmt}
      </button>
    `
    )
    .join("");

  container.innerHTML = `
    ${
      isLocked
        ? `<div class="locked-stage-banner">
             <div><strong>🔒 INTERVALO ENCERRADO:</strong> As decisões de intervalo já foram seladas.</div>
             <button id="btn-s7-back-active" class="btn-chrono" style="padding:7px 14px;font-size:0.8rem;">
               ➡️ Ir para o Placar Final (Stage 8)
             </button>
           </div>`
        : ""
    }

    <!-- 1. HALF-TIME 6v6 RANDOM SAMPLE SCOREBOARD -->
    <div class="halftime-scoreboard">
      <div style="display:flex;align-items:center;gap:12px;">
        <img src="/assets/ui/human_coach.png" class="dock-coach-avatar" style="width:52px;height:52px;" />
        <div>
          <div style="font-size:0.7rem;color:var(--text-gold);font-family:'JetBrains Mono',monospace;font-weight:800;">🧑‍💼 SEU TIME (AMOSTRA 6/12 TITULARES)</div>
          <div style="font-weight:800;font-size:1.05rem;">${hRooster.name}</div>
        </div>
      </div>

      <div style="text-align:center;">
        <span class="stage-pill">⏱️ PLACAR PARCIAL DO INTERVALO (AMOSTRA ALEATÓRIA 6v6)</span>
        <div style="display:flex;align-items:center;justify-content:center;gap:18px;margin-top:4px;">
          <span class="halftime-score-num">${sample.human_sample_score.toFixed(2)}</span>
          <span class="vs-medallion" style="width:36px;height:36px;font-size:0.75rem;">VS</span>
          <span class="halftime-score-num" style="color:var(--text-sapphire);">${sample.ai_sample_score.toFixed(2)}</span>
        </div>
      </div>

      <div style="display:flex;align-items:center;gap:12px;">
        <div style="text-align:right;">
          <div style="font-size:0.7rem;color:var(--text-sapphire);font-family:'JetBrains Mono',monospace;font-weight:800;">🤖 ORÁCULO IA (AMOSTRA 6/12 TITULARES)</div>
          <div style="font-weight:800;font-size:1.05rem;">${aRooster.name}</div>
          <button id="btn-s7-peek-ai-scoreboard" class="btn-peek-ai-lineup" style="margin-top:6px;">
            🔍 Ver 12 Titulares & Campo da IA
          </button>
        </div>
        <img src="/assets/ui/robot_coach.png" class="dock-coach-avatar" style="width:52px;height:52px;" />
      </div>
    </div>

    <!-- 2. POWER-UPS ARSENAL (MAX 1 PER MATCH, NON-REPEATING IN SERIES) -->
    <h4 style="font-family:'Cinzel',serif;color:var(--text-gold);margin-bottom:10px;">
      ⚡ Arsenal de Power-Ups de Intervalo (Máx. 1 por Partida · Uso Único na Série)
    </h4>

    <div class="powerups-grid">
      <!-- Reveal Zeroed -->
      <div class="powerup-card ${usedThisMatch === "reveal_zeroed" ? "used-this-match" : !remPowerups.reveal_zeroed ? "exhausted" : ""}">
        <img src="/assets/powerups/reveal_zeroed.png" class="powerup-art-thumb" alt="Reveal Zeroed" />
        <div style="flex:1;">
          <div style="font-weight:800;color:var(--text-gold);font-size:0.92rem;">🔍 Reveal Zeroed Players</div>
          <p style="font-size:0.74rem;color:var(--text-muted);margin:3px 0 8px;">
            Destaca em <strong>azul neon</strong> quem zerou entre seus 12 titulares para você substituí-los!
          </p>
          <button
            class="btn-chrono"
            id="btn-pu-zeroed"
            style="padding:6px 12px;font-size:0.74rem;"
            ${usedThisMatch || !remPowerups.reveal_zeroed || isLocked ? "disabled style='opacity:0.45;cursor:not-allowed;padding:6px 12px;font-size:0.74rem;'" : ""}
          >
            ${usedThisMatch === "reveal_zeroed" ? "✅ Ativado Agora" : !remPowerups.reveal_zeroed ? "🔒 Já Usado na Série" : "⚡ Acionar Raio-X"}
          </button>
        </div>
      </div>

      <!-- Copycat -->
      <div class="powerup-card ${usedThisMatch === "copycat" ? "used-this-match" : !remPowerups.copycat ? "exhausted" : ""}">
        <img src="/assets/powerups/copycat.png" class="powerup-art-thumb" alt="Copycat" />
        <div style="flex:1;">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;">
            <div style="font-weight:800;color:var(--text-gold);font-size:0.92rem;">🪞 Copycat (Espelho)</div>
            <button id="btn-s7-peek-ai-copycat" class="btn-peek-ai-lineup" style="padding:3px 8px;font-size:0.68rem;">
              🔍 Espiar Titulares IA
            </button>
          </div>
          <p style="font-size:0.72rem;color:var(--text-muted);margin:2px 0 6px;">
            1 titular seu copia a pontuação base de 1 titular da IA:
          </p>
          <div style="display:flex;flex-direction:column;gap:4px;margin-bottom:6px;">
            <select id="sel-copycat-own" style="background:var(--bg-input);color:var(--text-light);border:1px solid var(--border-brass);border-radius:5px;padding:3px;font-size:0.7rem;" ${usedThisMatch || !remPowerups.copycat || isLocked ? "disabled" : ""}>
              ${ownOptionsHTML}
            </select>
            <select id="sel-copycat-opp" style="background:var(--bg-input);color:var(--text-sapphire);border:1px solid #3A86C8;border-radius:5px;padding:3px;font-size:0.7rem;font-weight:700;" ${usedThisMatch || !remPowerups.copycat || isLocked ? "disabled" : ""}>
              ${oppOptionsHTML}
            </select>
          </div>
          <button
            class="btn-chrono"
            id="btn-pu-copycat"
            style="padding:6px 12px;font-size:0.74rem;"
            ${usedThisMatch || !remPowerups.copycat || isLocked ? "disabled style='opacity:0.45;cursor:not-allowed;padding:6px 12px;font-size:0.74rem;'" : ""}
          >
            ${usedThisMatch === "copycat" ? "✅ Ativado Agora" : !remPowerups.copycat ? "🔒 Já Usado na Série" : "🪞 Copiar Pontuação"}
          </button>
        </div>
      </div>

      <!-- Grenal -->
      <div class="powerup-card ${usedThisMatch === "grenal" ? "used-this-match" : !remPowerups.grenal ? "exhausted" : ""}">
        <img src="/assets/powerups/grenal.png" class="powerup-art-thumb" alt="Grenal" />
        <div style="flex:1;">
          <div style="font-weight:800;color:var(--text-vermilion);font-size:0.92rem;">🟥 Grenal (Caos Clássico)</div>
          <p style="font-size:0.74rem;color:var(--text-muted);margin:3px 0 8px;">
            Expulsa <strong>3 titulares aleatórios de cada time</strong> (pontuam 0.00)! Ideal se você estiver atrás no placar!
          </p>
          <button
            class="btn-chrono"
            id="btn-pu-grenal"
            style="padding:6px 12px;font-size:0.74rem;"
            ${usedThisMatch || !remPowerups.grenal || isLocked ? "disabled style='opacity:0.45;cursor:not-allowed;padding:6px 12px;font-size:0.74rem;'" : ""}
          >
            ${usedThisMatch === "grenal" ? "✅ Ativado Agora" : !remPowerups.grenal ? "🔒 Já Usado na Série" : "🟥 Provocar Grenal"}
          </button>
        </div>
      </div>
    </div>

    ${powerupEffectBanner}

    <!-- 3. HALF-TIME SUBSTITUTIONS (UP TO 3 SUBS + FORMATION CHANGE) -->
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin:16px 0 12px;">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--text-gold);font-weight:800;">
          🔄 SUBSTITUIÇÕES NO INTERVALO: <span style="color:${subsValid ? "var(--text-emerald)" : "var(--text-vermilion)"};">${subsMade} / 3 USADAS</span>
        </span>
        <div class="view-mode-toggle">${formationBtnsHTML}</div>
      </div>

      ${
        !isLocked
          ? `<button id="btn-s7-reset-subs" class="btn-gallery" style="padding:6px 12px;font-size:0.76rem;">
               ↩️ Restaurar Titulares do 1º Tempo (0 Trocas)
             </button>`
          : ""
      }
    </div>

    <div class="status-indicator-bar ${canConfirmHalftime ? "valid" : "invalid"}">
      <div style="flex:1;">
        <div>
          ${
            !subsValid
              ? `🔴 LIMITE DE SUBSTITUIÇÕES EXCEDIDO (${subsMade}/3)! Você só pode trocar até 3 atletas em relação ao 1º tempo.`
              : status.summaryText
          }
        </div>
        ${status.diagPillsHTML}
      </div>
      ${
        !isLocked
          ? `<button id="btn-s7-confirm" class="btn-chrono" style="${!canConfirmHalftime ? "opacity:0.75;border-color:#E0533C;" : ""}">
               ${canConfirmHalftime ? "🔥 Iniciar 2º Tempo & Revelar Súmula Final (Stage 8) →" : "⚠️ Verificar Pendências da Escalação"}
             </button>`
          : ""
      }
    </div>

    <div class="pitch-workspace">
      ${buildInteractivePitchHTML(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId, {
        zeroedIds,
        expelledIds,
      })}
      <div class="squad-selector-pane">
        ${buildSquadSelectorListHTML(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId, {
          zeroedIds,
          expelledIds,
          readOnly: isLocked,
        })}
      </div>
    </div>
  `;

  const backBtn = document.getElementById("btn-s7-back-active");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      appState.stage = appState.maxUnlockedStage;
      renderAll();
    });
  }

  const openAiLineupPeek = () => {
    if (appState.aiRoosterIdx !== null) {
      openRoosterModal(
        appState.aiRoosterIdx,
        "🤖 ESCALAÇÃO TITULAR DA IA NO GRAMADO (12 TITULARES & RESERVAS)",
        false,
        "lineup"
      );
    }
  };
  const btnPeekScoreboard = document.getElementById("btn-s7-peek-ai-scoreboard");
  if (btnPeekScoreboard) btnPeekScoreboard.addEventListener("click", openAiLineupPeek);
  const btnPeekCopycat = document.getElementById("btn-s7-peek-ai-copycat");
  if (btnPeekCopycat) btnPeekCopycat.addEventListener("click", openAiLineupPeek);

  if (isLocked) return;

  // Power-Up Handlers
  const btnZeroed = document.getElementById("btn-pu-zeroed");
  if (btnZeroed) {
    btnZeroed.addEventListener("click", async () => {
      const res = await fetch("/api/stage7/powerup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ powerup_id: "reveal_zeroed" }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const selOwn = document.getElementById("sel-copycat-own");
  const selOpp = document.getElementById("sel-copycat-opp");
  if (selOwn) {
    selOwn.addEventListener("change", () => {
      appState.copycatOwnId = parseInt(selOwn.value, 10);
    });
  }
  if (selOpp) {
    selOpp.addEventListener("change", () => {
      appState.copycatOppId = parseInt(selOpp.value, 10);
    });
  }

  const btnCopycat = document.getElementById("btn-pu-copycat");
  if (btnCopycat) {
    btnCopycat.addEventListener("click", async () => {
      const res = await fetch("/api/stage7/powerup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          powerup_id: "copycat",
          target_own_id: appState.copycatOwnId,
          target_opponent_id: appState.copycatOppId,
        }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const btnGrenal = document.getElementById("btn-pu-grenal");
  if (btnGrenal) {
    btnGrenal.addEventListener("click", async () => {
      const res = await fetch("/api/stage7/powerup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ powerup_id: "grenal" }),
      });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  // Formation & Substitution Handlers
  container.querySelectorAll("[data-s7-fmt]").forEach((btn) => {
    btn.addEventListener("click", () => {
      appState.stage7Formation = btn.getAttribute("data-s7-fmt");
      renderStage7();
      const st = evaluateLineupStatus(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  const resetSubsBtn = document.getElementById("btn-s7-reset-subs");
  if (resetSubsBtn) {
    resetSubsBtn.addEventListener("click", () => {
      appState.stage7Formation = s6.human_lineup.formation;
      appState.stage7Starters = [...s6.human_lineup.starter_ids];
      appState.stage7CaptainId = s6.human_lineup.captain_id;
      renderStage7();
      const st = evaluateLineupStatus(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  }

  container.querySelectorAll("[data-toggle-pid]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pid = parseInt(btn.getAttribute("data-toggle-pid"), 10);
      const res = togglePlayerInLineup(
        squad,
        appState.stage7Formation,
        appState.stage7Starters,
        appState.stage7CaptainId,
        pid
      );
      appState.stage7Starters = res.starterIds;
      appState.stage7CaptainId = res.captainId;
      renderStage7();
      const st = evaluateLineupStatus(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  container.querySelectorAll("[data-cap-pid]").forEach((btn) => {
    btn.addEventListener("click", () => {
      appState.stage7CaptainId = parseInt(btn.getAttribute("data-cap-pid"), 10);
      renderStage7();
      const st = evaluateLineupStatus(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  container.querySelectorAll("[data-pitch-pid]").forEach((tok) => {
    tok.addEventListener("click", () => {
      const pid = parseInt(tok.getAttribute("data-pitch-pid"), 10);
      if (appState.stage7CaptainId !== pid) {
        appState.stage7CaptainId = pid;
      } else {
        appState.stage7Starters = appState.stage7Starters.filter((id) => id !== pid);
        appState.stage7CaptainId = appState.stage7Starters[0] || null;
      }
      renderStage7();
      const st = evaluateLineupStatus(squad, appState.stage7Formation, appState.stage7Starters, appState.stage7CaptainId);
      showLineupDiagnosticToast(st.toastMessage, st.isValid);
    });
  });

  const confirmBtn = document.getElementById("btn-s7-confirm");
  if (confirmBtn) {
    confirmBtn.addEventListener("click", async () => {
      if (!subsValid) {
        showLineupDiagnosticToast(`Limite de 3 substituições excedido (${subsMade}/3)! Desfaça ${subsMade - 3} troca(s).`, false);
        return;
      }
      if (!status.isValid) {
        showLineupDiagnosticToast(status.toastMessage, false);
        return;
      }
      const res = await fetch("/api/stage7/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          formation: appState.stage7Formation,
          final_starter_ids: appState.stage7Starters,
          captain_id: appState.stage7CaptainId,
        }),
      });
      const data = await res.json();
      if (data.error) {
        showLineupDiagnosticToast(data.error, false);
        return;
      }
      await playClimaxRevealAnimation(data, sample);
      syncFromServer(data);
      renderAll();
    });
  }
}

// ============================================================================
// STAGE 8: FINAL MATCH REPORT, MVP, SCOUT BREAKDOWN & SERIES PROGRESSION
// ============================================================================
function renderScoutBreakdownPills(ev) {
  if (!ev) return "";
  if (ev.grenal_expelled) {
    return `<span class="scout-pill-tag neg-scout">🟥 EXPULSO NO GRENAL (0.00 pts)</span>`;
  }
  if (ev.copied_from) {
    return `<span class="scout-pill-tag pos-scout">🪞 COPYCAT de ${ev.copied_from} (Base: ${ev.raw_score.toFixed(2)})</span>`;
  }
  if (!ev.played) {
    return `<span class="scout-pill-tag">🔒 Não atuou na rodada (0.00)</span>`;
  }
  const bd = ev.breakdown || [];
  if (!bd.length) {
    return `<span class="scout-pill-tag">Atuou · Sem scouts (TEC / 0.0)</span>`;
  }
  return bd
    .map((b) => {
      const cls = b.points >= 0 ? "pos-scout" : "neg-scout";
      const sign = b.points >= 0 ? "+" : "";
      return `<span class="scout-pill-tag ${cls}" title="${b.label}: ${b.count}x (${sign}${b.points} pts)">${b.scout}:${b.count} (${sign}${b.points})</span>`;
    })
    .join("");
}

function renderReportTeamColumn(title, coachImg, rooster, reportData, totalScore, formation) {
  const starters = (reportData && reportData.starters) || [];
  const bench = (reportData && reportData.bench) || [];

  const renderRows = (list) =>
    list
      .map((item) => {
        const ev = item.eval || { final_score: 0, raw_score: 0 };
        const rTeam = item.round_team;
        const clubBadge = rTeam
          ? `<span class="club-pill" style="margin-left:6px;"><img src="${getClubLogoUrl(rTeam)}" style="width:14px;height:14px;" /> <span class="club-abbr">${rTeam.abbreviation}</span></span>`
          : `<span style="font-size:0.65rem;color:var(--text-dim);margin-left:6px;">(Sem Jogo)</span>`;

        return `
          <div class="report-player-row">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;flex:1;">
              <span class="pos-badge pos-${item.position_code}" style="min-width:42px;text-align:center;">${item.position_code}</span>
              <img src="${item.photo_url || DEFAULT_SILHOUETTE}" class="table-avatar" style="width:36px;height:36px;" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
              <div style="min-width:0;flex:1;">
                <div style="font-weight:800;font-size:0.88rem;color:var(--text-light);">
                  ${item.short_name}
                  ${item.is_captain ? `<span style="background:#F2C249;color:#1E1B18;font-size:0.64rem;padding:1px 6px;border-radius:999px;font-weight:900;margin-left:4px;">© 2x CAPITÃO</span>` : ""}
                  ${clubBadge}
                </div>
                <div style="margin-top:3px;">
                  ${renderScoutBreakdownPills(ev)}
                </div>
              </div>
            </div>
            <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-weight:900;font-size:0.98rem;color:${ev.final_score > 0 ? "var(--text-emerald)" : ev.final_score < 0 ? "var(--text-vermilion)" : "var(--text-muted)"};min-width:74px;">
              ${ev.final_score.toFixed(2)} pts
            </div>
          </div>
        `;
      })
      .join("");

  const benchSum = bench.reduce((acc, x) => acc + (x.eval ? x.eval.final_score : 0), 0);

  return `
    <div class="report-team-box">
      <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;margin-bottom:10px;border-bottom:2px solid rgba(242,194,73,0.3);">
        <div style="display:flex;align-items:center;gap:10px;">
          <img src="${coachImg}" class="dock-coach-avatar" />
          <div>
            <div style="font-size:0.68rem;color:var(--text-gold);font-family:'JetBrains Mono',monospace;font-weight:800;">${title} · ESQUEMA ${formation || "4-3-3"}</div>
            <h4 style="font-family:'Cinzel',serif;font-size:1.1rem;color:var(--text-light);">${rooster.name}</h4>
          </div>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:1.35rem;font-weight:900;color:var(--text-gold);">
          ${totalScore.toFixed(2)} pts
        </div>
      </div>

      <div style="font-family:'Cinzel',serif;font-size:0.8rem;color:var(--text-gold);font-weight:800;margin-bottom:6px;">
        ⚽ 12 TITULARES ESCALADOS:
      </div>
      ${renderRows(starters)}

      <details style="margin-top:14px;background:var(--bg-subtle);padding:10px;border-radius:10px;border:1px solid var(--border-brass);">
        <summary style="cursor:pointer;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--text-amber);font-weight:800;">
          🪑 Ver Pontuação dos 12 Reservas no Banco (Soma do Banco: ${benchSum.toFixed(2)} pts)
        </summary>
        <div style="margin-top:8px;">
          ${renderRows(bench)}
        </div>
      </details>
    </div>
  `;
}

function renderStage8() {
  const container = document.getElementById("stage8-container");
  if (!container || !appState.stage8 || appState.stage8.human_total === undefined) return;

  const s8 = appState.stage8;
  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const aRooster = appState.roosters[appState.aiRoosterIdx];
  const humanWon = s8.winner === "human";
  const mvp = s8.mvp;

  let nextActionHTML = "";
  if (s8.series_over) {
    const humanChamp = s8.series_winner === "human";
    nextActionHTML = `
      <div class="post-selection-banner" style="margin-bottom:20px;border-width:3px;">
        <span class="stage-pill">${humanChamp ? "🏆 GLÓRIA ETERNA NAS LINHAS DO TEMPO" : "🤖 SUPREMACIA DO ORÁCULO TEMPORAL"}</span>
        <h2 style="font-family:'Cinzel',serif;font-size:2rem;color:var(--text-gold);margin:8px 0;">
          ${humanChamp ? "🎉 PARABÉNS! VOCÊ VENCEU A SÉRIE TEMPORAL!" : "🤖 O ORÁCULO IA VENCEU A SÉRIE TEMPORAL!"}
        </h2>
        <p style="font-size:0.95rem;color:var(--text-light);margin-bottom:14px;">
          Placar Final da Série: <strong>Você ${appState.human_wins} x ${appState.ai_wins} IA</strong>
        </p>
        <button id="btn-s8-new-run" class="btn-chrono" style="font-size:1rem;padding:12px 28px;">
          🔄 Iniciar Nova Série Temporal (Sortear 7 Novos Time Squads)
        </button>
      </div>
    `;
  } else {
    nextActionHTML = `
      <div style="display:flex;justify-content:center;margin-bottom:22px;">
        <button id="btn-s8-next-match" class="btn-chrono" style="font-size:1.05rem;padding:14px 32px;">
          ⏭️ Avançar para a Partida #${s8.match_number + 1} da Série (Série Atual: Você ${appState.human_wins} x ${appState.ai_wins} IA) →
        </button>
      </div>
    `;
  }

  const mvpHTML = mvp
    ? `
      <div class="mvp-spotlight-card">
        <div style="display:flex;align-items:center;gap:14px;">
          <img src="${mvp.photo_url || DEFAULT_SILHOUETTE}" class="table-avatar" style="width:58px;height:58px;border:2px solid var(--clt-gold);" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
          <div>
            <span class="stage-pill">⭐ CRAQUE DA PARTIDA (MVP TEMPORAL)</span>
            <h3 style="font-family:'Cinzel',serif;font-size:1.3rem;color:var(--text-light);">
              ${mvp.short_name} (${mvp.position_code}) ${mvp.is_captain ? "© 2x" : ""}
            </h3>
            <div style="margin-top:4px;">${renderScoutBreakdownPills(mvp.eval)}</div>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;font-weight:700;">Pontuação Final MVP</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.85rem;font-weight:900;color:var(--text-gold);">
            ${mvp.eval.final_score.toFixed(2)} pts
          </div>
        </div>
      </div>
    `
    : "";

  container.innerHTML = `
    <div class="final-match-banner">
      <span class="stage-pill">PARTIDA #${s8.match_number} ENCERRADA · TEMPORADA ${s8.season} · RODADA #${s8.round} · ${s8.rule_name}</span>
      <h2 style="font-family:'Cinzel',serif;font-size:1.85rem;color:${humanWon ? "var(--text-emerald)" : "var(--text-amber)"};margin:8px 0;">
        ${humanWon ? "🏆 VITÓRIA DO SEU TIME SQUAD!" : "🤖 VITÓRIA DO TIME SQUAD DA IA!"}
      </h2>

      <div style="display:flex;justify-content:center;align-items:center;gap:28px;margin:14px 0;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:10px;">
          <img src="/assets/ui/human_coach.png" class="dock-coach-avatar" style="width:48px;height:48px;" />
          <div style="text-align:left;">
            <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;">🧑‍💼 VOCÊ (${hRooster.name})</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:2.1rem;font-weight:900;color:var(--text-gold);">
              ${s8.human_total.toFixed(2)} pts
            </div>
          </div>
        </div>

        <span class="vs-medallion">VS</span>

        <div style="display:flex;align-items:center;gap:10px;">
          <div style="text-align:right;">
            <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;">🤖 ORÁCULO IA (${aRooster.name})</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:2.1rem;font-weight:900;color:var(--text-sapphire);">
              ${s8.ai_total.toFixed(2)} pts
            </div>
          </div>
          <img src="/assets/ui/robot_coach.png" class="dock-coach-avatar" style="width:48px;height:48px;" />
        </div>
      </div>

      <div style="font-family:'JetBrains Mono',monospace;font-size:0.88rem;color:var(--text-light);">
        Placar da Série (Melhor de ${appState.target_wins === 3 ? "5" : "3"}): <strong>Você ${appState.human_wins} x ${appState.ai_wins} IA</strong>
      </div>
    </div>

    ${nextActionHTML}

    ${mvpHTML}

    <div class="report-columns">
      ${renderReportTeamColumn("🧑‍💼 SEU TIME TITULAR", "/assets/ui/human_coach.png", hRooster, s8.human_report, s8.human_total, s8.human_formation)}
      ${renderReportTeamColumn("🤖 TIME TITULAR DA IA", "/assets/ui/robot_coach.png", aRooster, s8.ai_report, s8.ai_total, s8.ai_formation)}
    </div>
  `;

  const nextMatchBtn = document.getElementById("btn-s8-next-match");
  if (nextMatchBtn) {
    nextMatchBtn.addEventListener("click", async () => {
      const res = await fetch("/api/stage8/next-match", { method: "POST" });
      syncFromServer(await res.json());
      renderAll();
    });
  }

  const newRunBtn = document.getElementById("btn-s8-new-run");
  if (newRunBtn) {
    newRunBtn.addEventListener("click", () => {
      rerollNewRun();
    });
  }
}

// ============================================================================
// SECOND-HALF CLIMAX & ROLLING SCOREBOARD REVEAL ANIMATION (STAGE 7 -> STAGE 8)
// ============================================================================
async function playClimaxRevealAnimation(finalData, sample) {
  const overlay = document.getElementById("climax-reveal-overlay");
  const card = document.getElementById("climax-reveal-card");
  if (!overlay || !card || !finalData || !finalData.stage8) return;

  const s8 = finalData.stage8;
  const hRooster = appState.roosters[appState.humanRoosterIdx] || { name: "Seu Time Squad" };
  const aRooster = appState.roosters[appState.aiRoosterIdx] || { name: "Time Squad IA" };
  const startH = sample && sample.human_sample_score !== undefined ? sample.human_sample_score : 0;
  const startA = sample && sample.ai_sample_score !== undefined ? sample.ai_sample_score : 0;
  const endH = s8.human_total !== undefined ? s8.human_total : 0;
  const endA = s8.ai_total !== undefined ? s8.ai_total : 0;
  const humanWon = s8.winner === "human";
  const mvp = s8.mvp;

  card.innerHTML = `
    <div class="climax-gears-bg"></div>
    <div style="position:relative;z-index:2;">
      <span class="stage-pill" id="climax-phase-pill">⏱️ 46' BOLA ROLANDO NO 2º TEMPO · APURAÇÃO TEMPORAL</span>
      <h2 style="font-family:'Cinzel',serif;font-size:1.75rem;color:#F2C249;margin:8px 0 4px;" id="climax-headline">
        Calculando os 17 Scouts Universais (${s8.season} · Rodada #${s8.round})...
      </h2>
      <div style="font-size:0.86rem;color:#D5CBBF;margin-bottom:10px;">
        🎩 Regra Ativa: <strong style="color:#F9A03F;">${s8.rule_name || "Cartola"}</strong>
      </div>

      <div class="climax-duel-row">
        <div class="climax-team-col">
          <img src="/assets/ui/human_coach.png" class="climax-coach-badge" alt="Você" />
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#F2C249;font-weight:800;">🧑‍💼 VOCÊ</div>
          <div style="font-family:'Cinzel',serif;font-weight:900;font-size:1.05rem;color:#FDFBF7;">${hRooster.name}</div>
          <div class="climax-rolling-score" id="climax-score-human">${startH.toFixed(2)}</div>
        </div>

        <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
          <div class="vs-medallion" style="width:54px;height:54px;font-size:1.05rem;">VS</div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#D5CBBF;" id="climax-clock-tag">45' → 90'</span>
        </div>

        <div class="climax-team-col">
          <img src="/assets/ui/robot_coach.png" class="climax-coach-badge" alt="IA" />
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#7CC0F5;font-weight:800;">🤖 ORÁCULO IA</div>
          <div style="font-family:'Cinzel',serif;font-weight:900;font-size:1.05rem;color:#FDFBF7;">${aRooster.name}</div>
          <div class="climax-rolling-score ai-side" id="climax-score-ai">${startA.toFixed(2)}</div>
        </div>
      </div>

      <div id="climax-verdict-box" style="min-height:84px;display:flex;flex-direction:column;align-items:center;justify-content:center;">
        <div id="climax-verdict-stamp" class="climax-verdict-stamp" style="background:${
          humanWon ? "linear-gradient(135deg,#10B981,#047857)" : "linear-gradient(135deg,#E0533C,#991B1B)"
        };color:#FDFBF7;border:2px solid #F2C249;">
          ${humanWon ? "🏆 VITÓRIA DO SEU TIME SQUAD!" : "🤖 VITÓRIA DO TIME SQUAD DA IA!"}
        </div>
        ${
          mvp
            ? `<div id="climax-mvp-line" style="opacity:0;transition:opacity 0.4s ease;margin-top:8px;font-size:0.86rem;color:#F2C249;font-family:'JetBrains Mono',monospace;">
                 ⭐ Craque da Partida (MVP): <strong>${mvp.short_name} (${mvp.position_code})</strong> — ${mvp.eval.final_score.toFixed(2)} pts
               </div>`
            : ""
        }
      </div>

      <div style="margin-top:12px;">
        <button id="btn-skip-climax" class="btn-gallery" style="padding:7px 18px;font-size:0.78rem;">
          📊 Abrir Súmula Completa Agora →
        </button>
      </div>
    </div>
  `;

  overlay.classList.remove("hidden");

  return new Promise((resolve) => {
    let finished = false;
    const finishAnim = () => {
      if (finished) return;
      finished = true;
      overlay.classList.add("hidden");
      resolve();
    };

    const skipBtn = document.getElementById("btn-skip-climax");
    if (skipBtn) skipBtn.addEventListener("click", finishAnim);

    const hScoreEl = document.getElementById("climax-score-human");
    const aScoreEl = document.getElementById("climax-score-ai");
    const clockEl = document.getElementById("climax-clock-tag");
    const pillEl = document.getElementById("climax-phase-pill");
    const headEl = document.getElementById("climax-headline");
    const stampEl = document.getElementById("climax-verdict-stamp");
    const mvpEl = document.getElementById("climax-mvp-line");

    const durationMs = 2000;
    const t0 = performance.now();

    function stepFrame(now) {
      if (finished) return;
      const elapsed = now - t0;
      const progress = Math.min(1, elapsed / durationMs);
      // Cubic ease-out
      const eased = 1 - Math.pow(1 - progress, 3);

      const curH = startH + (endH - startH) * eased;
      const curA = startA + (endA - startA) * eased;
      const curMin = Math.min(90, Math.floor(45 + 45 * progress));

      if (hScoreEl) hScoreEl.textContent = curH.toFixed(2);
      if (aScoreEl) aScoreEl.textContent = curA.toFixed(2);
      if (clockEl) clockEl.textContent = `⏱️ ${curMin}' DO 2º TEMPO`;

      if (progress > 0.45 && progress < 0.95 && pillEl) {
        pillEl.textContent = "🔥 RETA FINAL DO 2º TEMPO · APLICANDO MULTIPLICADORES E CAPITÃO (2x)";
      }

      if (progress < 1) {
        requestAnimationFrame(stepFrame);
      } else {
        if (clockEl) clockEl.textContent = "🎺 90+4' FIM DE JOGO!";
        if (pillEl) pillEl.textContent = "🎺 APITO FINAL · PLACAR OFICIAL DA PARTIDA #" + s8.match_number;
        if (headEl) headEl.textContent = `${hRooster.name} ${endH.toFixed(2)} × ${endA.toFixed(2)} ${aRooster.name}`;
        if (stampEl) stampEl.classList.add("revealed");
        if (mvpEl) mvpEl.style.opacity = "1";
        setTimeout(finishAnim, 1350);
      }
    }

    requestAnimationFrame(stepFrame);
  });
}

// ============================================================================
// MINIMIZED DOCK & MODALS (ROOSTER, TUTORIAL, CODEX, ART GALLERY)
// ============================================================================
function renderMinimizedDock() {
  const dock = document.getElementById("minimized-dock");
  if (appState.humanRoosterIdx === null || appState.aiRoosterIdx === null) {
    dock.classList.add("hidden");
    return;
  }

  const hRooster = appState.roosters[appState.humanRoosterIdx];
  const aRooster = appState.roosters[appState.aiRoosterIdx];
  if (!hRooster || !aRooster) return;

  const hEmblem = hRooster.emblem_url || `/assets/emblems/squad_${String.fromCharCode(97 + appState.humanRoosterIdx)}.png`;
  const aEmblem = aRooster.emblem_url || `/assets/emblems/squad_${String.fromCharCode(97 + appState.aiRoosterIdx)}.png`;

  dock.classList.remove("hidden");

  document.getElementById("dock-human-name").innerHTML = `<img src="${hEmblem}" class="dock-emblem-mini" style="vertical-align:middle;margin-right:6px;" /> ${hRooster.name}`;
  document.getElementById("dock-ai-name").innerHTML = `<img src="${aEmblem}" class="dock-emblem-mini" style="vertical-align:middle;margin-right:6px;" /> ${aRooster.name}`;
  document.getElementById("dock-stage-indicator").textContent = `⏳ STAGE ${appState.stage} · SÉRIE ${appState.human_wins} x ${appState.ai_wins}`;
}

function buildModalActiveLineupHTML(rooster, isHuman) {
  const s6 = appState.stage6 || {};
  const s7 = appState.stage7 || {};
  const lineupObj = isHuman
    ? (s7.final_human_lineup || s6.human_lineup || {
        formation: appState.stage6Formation,
        starter_ids: appState.stage6Starters,
        captain_id: appState.stage6CaptainId,
      })
    : s6.ai_lineup;

  if (!lineupObj || !lineupObj.starter_ids || !lineupObj.starter_ids.length) {
    return `
      <div style="padding:28px;text-align:center;">
        <p style="font-size:0.95rem;">A escalação titular de 12 jogadores deste esquadrão ainda não foi definida nesta partida.</p>
      </div>
    `;
  }

  const formation = lineupObj.formation || "4-3-3";
  const starterIds = lineupObj.starter_ids || [];
  const captainId = lineupObj.captain_id;
  const starterSet = new Set(starterIds);
  const grenalObj = s7.grenal_removed || {};
  const expelledIds = isHuman ? grenalObj.human_removed_ids || [] : grenalObj.ai_removed_ids || [];
  const expelledSet = new Set(expelledIds);

  const canPickCopycatTarget =
    !isHuman &&
    appState.stage === 7 &&
    !s7.completed &&
    !s7.powerup_used &&
    appState.powerups_remaining &&
    appState.powerups_remaining.human &&
    appState.powerups_remaining.human.copycat;

  const listHTML = POSITION_BLOCKS.map((block) => {
    const posPlayers = rooster.players.filter((p) => p.position_code === block.code);
    const curSelected = posPlayers.filter((p) => starterSet.has(p.player_id)).length;

    const rows = posPlayers
      .map((p) => {
        const isStarter = starterSet.has(p.player_id);
        const isCap = p.player_id === captainId;
        const isExp = expelledSet.has(p.player_id);
        const clubsMini = (p.top_teams || [])
          .slice(0, 3)
          .map((t) => `<img src="${getClubLogoUrl(t)}" style="width:15px;height:15px;vertical-align:middle;" title="${t.team_name}" /> ${t.abbreviation}`)
          .join(" · ");

        return `
          <div class="lineup-player-row ${isStarter ? "selected-starter" : ""}">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
              <img src="${p.photo_url || DEFAULT_SILHOUETTE}" class="table-avatar" style="width:36px;height:36px;" onerror="this.onerror=null;this.src='${DEFAULT_SILHOUETTE}';" />
              <div style="min-width:0;">
                <div style="font-weight:800;font-size:0.86rem;color:var(--text-light);">
                  ${p.short_name}
                  ${isCap ? `<span style="background:#F2C249;color:#1E1B18;font-size:0.62rem;padding:1px 6px;border-radius:999px;font-weight:900;margin-left:4px;">© 2x CAPITÃO</span>` : ""}
                  ${isExp ? `<span style="background:#E0533C;color:#FFF;font-size:0.62rem;padding:1px 5px;border-radius:4px;font-weight:900;margin-left:4px;">🟥 EXPULSO (GRENAL)</span>` : ""}
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--text-muted);">
                  Média: <strong style="color:var(--text-gold);">${p.avg_score.toFixed(2)}</strong> · ${p.rounds_played}j (${p.first_season}–${p.last_season}) · ${clubsMini}
                </div>
              </div>
            </div>

            <div style="display:flex;align-items:center;gap:6px;flex-shrink:0;">
              ${
                isStarter && canPickCopycatTarget && p.position_code !== "TEC"
                  ? `<button class="btn-peek-ai-lineup" data-pick-copycat-opp="${p.player_id}" style="padding:4px 9px;font-size:0.68rem;">
                       🪞 Alvo Copycat
                     </button>`
                  : ""
              }
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:800;color:${isStarter ? "var(--text-emerald)" : "var(--text-dim)"};">
                ${isStarter ? "✅ TITULAR" : "🪑 Reserva"}
              </span>
            </div>
          </div>
        `;
      })
      .join("");

    return `
      <div class="lineup-pos-group-header">
        <span>${block.title}</span>
        <span>Escalados: ${curSelected}</span>
      </div>
      ${rows}
    `;
  }).join("");

  return `
    <div class="ai-log-banner" style="margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
      <div>
        <strong>${isHuman ? "🧑‍💼 SUA ESCALAÇÃO TITULAR" : "🤖 ESCALAÇÃO TITULAR DO ORÁCULO IA"} (ESQUEMA ${formation}):</strong>
        Confira os <strong>12 titulares em campo</strong> (incluindo o Capitão <strong>© 2x</strong>) e os 12 reservas.
        ${canPickCopycatTarget ? `Você pode clicar em <strong>"🪞 Alvo Copycat"</strong> em qualquer titular da IA para selecioná-lo direto no espelho!` : ""}
      </div>
    </div>
    <div class="pitch-workspace">
      ${buildInteractivePitchHTML(rooster.players, formation, starterIds, captainId, {
        expelledIds,
      })}
      <div class="squad-selector-pane">
        ${listHTML}
      </div>
    </div>
  `;
}

function renderModalContent() {
  const rooster = appState.roosters[appState.modalRoosterIdx];
  if (!rooster) return;
  const isHuman = appState.modalRoosterIdx === appState.humanRoosterIdx;
  const container = document.getElementById("modal-rooster-content");

  const btnLineup = document.getElementById("modal-btn-lineup");
  const btnCards = document.getElementById("modal-btn-cards");
  const btnTable = document.getElementById("modal-btn-table");

  const hasAiLineup = appState.stage6 && appState.stage6.ai_lineup && appState.stage6.ai_lineup.starter_ids;
  const hasHumanLineup =
    (appState.stage6 && appState.stage6.human_lineup) || (appState.stage6Starters && appState.stage6Starters.length > 0);
  const canShowLineupTab = appState.stage >= 6 && (isHuman ? hasHumanLineup : hasAiLineup);

  if (btnLineup) {
    btnLineup.classList.toggle("hidden", !canShowLineupTab);
    btnLineup.classList.toggle("active", appState.modalViewMode === "lineup");
  }
  if (btnCards) btnCards.classList.toggle("active", appState.modalViewMode === "cards");
  if (btnTable) btnTable.classList.toggle("active", appState.modalViewMode === "table");

  if (appState.modalViewMode === "lineup" && canShowLineupTab) {
    container.innerHTML = buildModalActiveLineupHTML(rooster, isHuman);
    container.querySelectorAll("[data-pick-copycat-opp]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const oppPid = parseInt(btn.getAttribute("data-pick-copycat-opp"), 10);
        const oppPlayer = rooster.players.find((x) => x.player_id === oppPid);
        appState.copycatOppId = oppPid;
        document.getElementById("rooster-modal").classList.add("hidden");
        renderStage7();
        showLineupDiagnosticToast(
          `🪞 ${oppPlayer ? oppPlayer.short_name : "Titular IA"} selecionado como alvo do Copycat! Clique em "🪞 Copiar Pontuação" para ativar.`,
          true
        );
      });
    });
  } else if (appState.modalViewMode === "cards") {
    container.innerHTML = `<div class="modal-rooster-grid">${rooster.players.map((p) => createAthleteCardHTML(p)).join("")}</div>`;
  } else {
    container.innerHTML = createPositionGroupedTableHTML(rooster.players);
  }
}

function openRoosterModal(roosterIdx, roleTitle, isHuman = true, defaultMode = null) {
  const rooster = appState.roosters[roosterIdx];
  if (!rooster) return;

  appState.modalRoosterIdx = roosterIdx;
  if (defaultMode) {
    appState.modalViewMode = defaultMode;
  } else if (!isHuman && appState.stage >= 7 && appState.stage6 && appState.stage6.ai_lineup) {
    // In Stage 7/8, opening the AI modal defaults to showing the AI's 12 starters & pitch!
    appState.modalViewMode = "lineup";
  } else if (appState.modalViewMode === "lineup" && appState.stage < 6) {
    appState.modalViewMode = "cards";
  }

  const emblemSrc = rooster.emblem_url || `/assets/emblems/squad_${String.fromCharCode(97 + roosterIdx)}.png`;
  const coachAvatarEl = document.getElementById("modal-coach-avatar");
  if (coachAvatarEl) {
    coachAvatarEl.src = isHuman ? "/assets/ui/human_coach.png" : "/assets/ui/robot_coach.png";
    coachAvatarEl.style.display = "inline-block";
  }
  document.getElementById("modal-rooster-emblem").src = emblemSrc;
  document.getElementById("modal-owner-badge").textContent = roleTitle;
  document.getElementById("modal-rooster-name").textContent = `${rooster.name} — ${rooster.tagline}`;
  renderModalContent();
  document.getElementById("rooster-modal").classList.remove("hidden");
}

function openTutorialModal() {
  const body = document.getElementById("tutorial-modal-body");
  const steps = [
    {
      stage: "STAGE 1 · CONVOCAÇÃO TEMPORAL DOS TIME SQUADS",
      title: "1. Escolha sua Cápsula Temporal de 24 Lendas (Início da Série)",
      img: "/assets/tutorial/stage_1_squads.png",
      desc: "No início de uma Série (Melhor de 5 ou Melhor de 3), a máquina do tempo sorteia 7 Time Squads inéditos (A até G) a partir das ~300 maiores lendas do Brasileirão (2014–2025). Cada elenco possui exatamente 2 GOL, 4 ZAG, 4 LAT, 8 MEI, 5 ATA e 1 TEC.",
      example:
        "🎯 Exemplo de Turno: Você analisa os 7 esquadrões usando a Grade Compacta ou a Tabela por Posição e escolhe o Time Squad A (forte em atacantes de 2019–2021). O Oráculo Robô IA escolhe o Time Squad D. Ambos os elencos ficam minimizados nas abas inferiores (com os ícones do Treinador Humano 🧑‍💼 e do Robô IA 🤖) para consulta rápida a qualquer momento!",
    },
    {
      stage: "STAGE 2 · COORDENADAS DA MÁQUINA DO TEMPO (ANO & RODADA)",
      title: "2. Um Escolhe o Ano (2014–2025), o Outro Escolhe a Rodada (1–38)",
      img: "/assets/tutorial/stage_2_coordinates.png",
      desc: "Toda partida viaja para uma rodada real da história do Brasileirão! Quem faz a 1ª escolha decide se quer cravar o Ano ou a Rodada; o adversário crava o parâmetro restante. Regra de Ouro do Equilíbrio: Quem faz a 2ª escolha no Stage 2 ganha o direito de escolher 1º no Bucket of the Souls (Stage 3)!",
      example:
        "🎯 Exemplo de Turno: Vendo que seus principais craques brilharam em 2019, você crava a Temporada 2019. Em resposta, a IA analisa os atletas dela e crava a Rodada #15 de 2019. As coordenadas (⏳ 2019 · 🧭 Rodada #15) ficam fixadas no topo da tela durante toda a partida!",
    },
    {
      stage: "STAGE 3 · BUCKET OF THE SOULS (RECRUTAMENTO CEGO)",
      title: "3. 6 Almas que Entraram em Campo na Rodada (Troca Permanente)",
      img: "/assets/tutorial/stage_3_bucket.png",
      desc: "O caldeirão temporal revela 6 jogadores (1 de cada posição: GOL, ZAG, LAT, MEI, ATA, TEC) que comprovadamente entraram em campo naquela exata rodada histórica! Porém, a média de carreira deles fica oculta. Você pode fazer no máximo 1 troca pela mesma posição (ou passar a vez).",
      example:
        "🎯 Exemplo de Turno: Seus 2 goleiros atuais jogaram apenas entre 2014 e 2017 (logo, não atuaram em 2019!). No Bucket of the Souls aparece Fernando Prass (GOL · Palmeiras em 2019/R15). Você troca seu goleiro inativo por Fernando Prass! Essa mutação é permanente para o restante da série!",
    },
    {
      stage: "STAGE 4 · HIGHLIGHTS OF DESTINY (VISÃO DO ORÁCULO)",
      title: "4. 5 Confrontos (Mandante vs Visitante) OU 2 Placares Exatos",
      img: "/assets/tutorial/stage_4_destiny.png",
      desc: "Os 10 jogos da rodada aparecem ocultos em barras misteriosas. Você tem direito a 1 única revelação estratégica: Opção A revela 5 confrontos (sem placar, ótimo para saber quem jogou em casa) OU Opção B revela 2 confrontos com o placar exato (ótimo para caçar goleadas ou Saldo de Gol - SG)!",
      example:
        "🎯 Exemplo de Turno: Você escolhe a Opção B (2 Placares Exatos) e descobre que na Rodada #15 de 2019 o Grêmio venceu por 3 x 0! Você imediatamente sabe que os defensores do Grêmio garantiram SG (+5.0 pts) e que o ataque tricolor marcou 3 gols!",
    },
    {
      stage: "STAGE 5 & STAGE 6 · REGRA MALUCA & PRANCHETA TÁTICA NO GRAMADO",
      title: "5. A Regra Maluca Distorce os Scouts & Você Escala 11 + 1 TEC + Capitão (2x)",
      img: "/assets/tutorial/stage_5_6_pitch.png",
      desc: "No Stage 5, o jogo sorteia 1 das 8 Regras Malucas que alteram os pesos dos 17 scouts universais. Em seguida, no Stage 6, você escolhe sua formação (4-3-3, 4-4-2, 4-5-1, 3-4-3 ou 3-5-2), escala seus 12 titulares e entrega a braçadeira de Capitão (© 2x) antes do Kick-Off!",
      example:
        "🎯 Exemplo de Turno: A Regra do Garçom é sorteada (Assistência passa a valer +10.0 pts!). Você muda seu esquema para 4-5-1 para povoar o meio-campo com meias criativos como Arrascaeta e Everton Ribeiro, e coloca a faixa de Capitão (2x) em Dudu!",
    },
    {
      stage: "STAGE 7 & STAGE 8 · INTERVALO 6v6, POWER-UPS & SÚMULA FINAL",
      title: "6. Placar Parcial 6v6, Power-Ups de Intervalo, 3 Substituições & Troféu",
      img: "/assets/tutorial/stage_7_8_climax.png",
      desc: "No Intervalo (Stage 7), você vê uma amostra parcial 6v6 do placar, pode acionar 1 Power-Up (Reveal Zeroed, Copycat ou Grenal — cada um só pode ser usado 1 vez em toda a série!) e fazer até 3 substituições. No Stage 8, todos os scouts são revelados, o MVP é coroado e o vencedor soma 1 ponto na Série!",
      example:
        "🎯 Exemplo de Turno: No intervalo você está perdendo a amostra 6v6 por 18.4 a 24.0. Você ativa o Power-Up 'Reveal Zeroed Players', descobre 2 titulares brilhando em azul neon (zerados!), substitui ambos por reservas que atuaram em 2019 e vira o jogo no 2º tempo para 68.5 x 61.2!",
    },
  ];

  body.innerHTML = `
    <div class="codex-era-banner">
      <h4 style="font-family:'Cinzel',serif;color:var(--text-gold);font-size:1.15rem;margin-bottom:6px;">
        🧭 Bem-vindo ao Cartola Legends of Time (CLT) — O Roguelike Estratégico do Brasileirão!
      </h4>
      <p style="font-size:0.88rem;color:var(--text-light);">
        Em <strong>CLT</strong>, você (🧑‍💼 <strong>Comandante Humano</strong>) enfrenta o 🤖 <strong>Oráculo Robô IA</strong> em uma série <strong>Melhor de 5</strong> (ou Melhor de 3).
        O segredo da vitória não é apenas ter craques famosos, mas <strong>cruzar a janela histórica de cada atleta (ex: 2016–2021) com o Ano, a Rodada, os Confrontos revelados e a Regra Maluca da partida</strong>!
      </p>
    </div>

    <div class="tutorial-steps-grid">
      ${steps
        .map(
          (s) => `
        <div class="tutorial-step-card">
          <img src="${s.img}" alt="${s.title}" class="tutorial-cartoon-img" />
          <div>
            <span class="stage-pill">${s.stage}</span>
            <h4 style="font-family:'Cinzel',serif;font-size:1.22rem;color:var(--text-gold);margin:4px 0 8px;">${s.title}</h4>
            <p style="font-size:0.88rem;color:var(--text-muted);line-height:1.55;">${s.desc}</p>
            <div class="example-turn-box">${s.example}</div>
          </div>
        </div>
      `
        )
        .join("")}
    </div>
  `;

  document.getElementById("tutorial-modal").classList.remove("hidden");
}

function openCodexModal() {
  const body = document.getElementById("codex-modal-body");

  const powerupDetails = [
    {
      name: "🔍 Reveal Zeroed Players (Raio-X Temporal)",
      src: "/assets/powerups/reveal_zeroed.png",
      badge: "Informação Pura · Sem Risco",
      desc: "Escaneia imediatamente os seus 12 titulares escalados no 1º tempo e destaca em AZUL NEON todos aqueles que pontuaram 0.00 (ou não entraram em campo naquela rodada histórica). Combina perfeitamente com as suas 3 substituições de intervalo!",
    },
    {
      name: "🪞 Copycat (Espelho de Cronos)",
      src: "/assets/powerups/copycat.png",
      badge: "Espelhamento Tático · Alvo Direto",
      desc: "Permite escolher 1 titular do seu time e 1 titular da escalação da IA. No apito final (Stage 8), o seu jogador substitui a própria pontuação base pela pontuação base do jogador adversário escolhido (e se o seu jogador for o seu Capitão © 2x, ele dobra a nota copiada!).",
    },
    {
      name: "🟥 Grenal (Caos Clássico — 6 Expulsões)",
      src: "/assets/powerups/grenal.png",
      badge: "Alto Risco · Virada de Mesa",
      desc: "Instaura o caos total no gramado: sorteia e expulsa 3 titulares de linha do seu time e 3 titulares de linha da IA! Os 6 jogadores expulsos têm sua pontuação final cravada em 0.00 pts. Ideal quando sua amostra 6v6 no intervalo está muito atrás da IA!",
    },
  ];

  const ruleDetails = [
    {
      name: "Regra de Gabriel Jesus",
      src: "/assets/rules/gabriel_jesus.png",
      tagline: "Gol não é tão importante; o negócio é ajudar a equipe!",
      changes: "Gol cai pela metade (G: +8.0 → +4.0) · Desarme sobe 67% (DS: +1.2 → +2.0) · Falta Sofrida triplica (FS: +0.5 → +1.5).",
      tip: "Valorize volantes caça-bolas e pontas que sofrem muitas faltas!",
    },
    {
      name: "Regra de Felipe Melo",
      src: "/assets/rules/felipe_melo.png",
      tagline: "Cartão é sinal de entrega em campo!",
      changes: "Cartão Amarelo vira bônus (CA: -1.0 → +2.0) · Cartão Vermelho vira festa (CV: -3.0 → +5.0) · Falta Cometida bonifica (FC: -0.3 → +0.5) · Gol contra-atacado cai (G: +8.0 → +6.0).",
      tip: "Zagueiros e volantes brucutus tornam-se minas de ouro!",
    },
    {
      name: "Regra do Futsal",
      src: "/assets/rules/futsal.png",
      tagline: "Quadra curta, passe rápido e sem bandeirinha!",
      changes: "Assistência sobe 60% (A: +5.0 → +8.0) · Impedimento é zerado (I: -0.1 → 0.0) · Finalizações ganham bônus (FD: +1.2 → +1.8 / FF: +0.8 → +1.2).",
      tip: "Escale atacantes finalizadores e meias de último passe!",
    },
    {
      name: "Regra do Mano Menezes",
      src: "/assets/rules/mano_menezes.png",
      tagline: "Achei ofensivo, recua o time!",
      changes: "Saldo de Gols dobra de valor (SG: +5.0 → +10.0) · Desarme sobe 50% (DS: +1.2 → +1.8) · Gol cai (G: +8.0 → +5.0).",
      tip: "Formações com 4 ou 5 defensores (4-4-2 / 4-5-1) de clubes que não sofreram gols dominam a rodada!",
    },
    {
      name: "Regra do Vanderlei",
      src: "/assets/rules/vanderlei.png",
      tagline: "Milagres sob as traves valem ouro!",
      changes: "Defesa de Goleiro dobra (DE: +1.0 → +2.0) · Defesa de Pênalti dobra (DP: +7.0 → +14.0) · Gol Sofrido penaliza menos (GS: -1.0 → -0.5).",
      tip: "Colocar a braçadeira de Capitão (© 2x) em um grande goleiro pode render mais de 30 pontos!",
    },
    {
      name: "Regra do Garçom",
      src: "/assets/rules/garcom.png",
      tagline: "Mais vale aquele que compartilha do que aquele que comemora!",
      changes: "Assistência dobra de valor (A: +5.0 → +10.0) · Gol cai (G: +8.0 → +5.0).",
      tip: "Meias armadores (camisas 10) e laterais ofensivos superam centroavantes!",
    },
    {
      name: "Regra do Buda",
      src: "/assets/rules/buda.png",
      tagline: "Zero negatividades no plano espiritual do futebol!",
      changes: "TODOS os 7 scouts negativos são anulados para 0.0 (GC, CV, CA, GS, PP, FC e I = 0.0).",
      tip: "Goleiros que sofreram muitos gols mas fizeram defesas (DE) e atacantes que perderam pênalti não perdem nenhum ponto!",
    },
    {
      name: "Regra Open Capitão",
      src: "/assets/rules/open_capitao.png",
      tagline: "Sobrecarga Temporal: Dobro de glória, quádruplo de dor!",
      changes: "Todos os scouts positivos valem o DOBRO (2x: G=+16, A=+10, SG=+10, DP=+14) · Todos os scouts negativos valem o QUÁDRUPLO (4x: CV=-12, GC=-12, CA=-4, GS=-4).",
      tip: "Partida de altíssima volatilidade! Evite defensores de times que sofreram gols (GS = -4.0 cada)!",
    },
  ];

  body.innerHTML = `
    <!-- SECTION 1: THE 2014-2025 TIME FRAME & NORMALIZATION -->
    <div class="codex-era-banner">
      <span class="stage-pill">⏳ A JANELA TEMPORAL OFICIAL · 12 TEMPORADAS (2014–2025)</span>
      <h4 style="font-family:'Cinzel',serif;color:var(--text-gold);font-size:1.3rem;margin:6px 0 10px;">
        Por que 2014–2025 e como funciona a Normalização Histórica dos Scouts?
      </h4>
      <p style="font-size:0.88rem;color:var(--text-light);margin-bottom:10px;">
        O banco de dados do <strong>Cartola Legends of Time</strong> abrange <strong>12 edições completas do Brasileirão Série A (2014 a 2025)</strong>,
        totalizando <strong>454 rodadas históricas</strong>, <strong>39 clubes</strong> e <strong>359.385 participações de atletas</strong>.
        Para que lendas de 2015 (como Jadson ou Elias) possam enfrentar craques de 2024 (como Estêvão ou Hulk) em total igualdade matemática, o motor aplica <strong>3 regras de engenharia temporal</strong>:
      </p>
      <ul style="padding-left:20px;font-size:0.85rem;color:var(--text-muted);line-height:1.7;">
        <li>
          <strong>1. Unificação dos 17 Scouts Universais:</strong> Scouts efêmeros que existiram em apenas algumas edições (como <em>Passe Incompleto - PI</em>, <em>Passe Certo - PC</em> e <em>Vitória de Técnico - V</em>) foram removidos do cálculo de atletas de linha, mantendo os <strong>17 scouts universais</strong> presentes de 2014 a 2025 (mais a nota estática oficial dos Técnicos).
        </li>
        <li>
          <strong>2. Calibração de Roubadas de Bola → Desarmes (2014–2019 vs 2020–2025):</strong> Até 2019 o Cartola contabilizava <code>RB</code> (Roubadas de Bola); em 2020 mudou o critério para <code>DS</code> (Desarmes), elevando o volume médio em <strong>+28,6%</strong>. Por isso, toda <code>RB</code> de 2014–2019 recebe o fator exato de equivalência <strong><code>DS = RB × 1.286</code></strong>.
        </li>
        <li>
          <strong>3. Calibração de Defesa Difícil → Defesa de Goleiro (2014–2021 vs 2022–2025):</strong> Em 2022 o scout <code>DD</code> foi substituído por <code>DE</code> (Defesa simples), aumentando a frequência em <strong>2,16x</strong>. Assim, toda <code>DD</code> de 2014–2021 é convertida por <strong><code>DE = DD × 2.160</code></strong>.
        </li>
      </ul>
    </div>

    <!-- SECTION 2: THE 3 POWER-UPS -->
    <h4 class="art-section-title">⚡ Os 3 Power-Ups de Intervalo (Stage 7 · 1 por Partida, Sem Repetir na Série)</h4>
    <div class="codex-cards-grid">
      ${powerupDetails
        .map(
          (p) => `
        <div class="codex-item-card">
          <img src="${p.src}" alt="${p.name}" />
          <div>
            <span class="stage-pill" style="margin-bottom:4px;">${p.badge}</span>
            <h5 style="font-family:'Cinzel',serif;font-size:1.02rem;color:var(--text-gold);margin-bottom:4px;">${p.name}</h5>
            <p style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;">${p.desc}</p>
          </div>
        </div>
      `
        )
        .join("")}
    </div>

    <!-- SECTION 3: THE 8 CRAZY RULES -->
    <h4 class="art-section-title">🎩 As 8 Regras Malucas do Vórtice Temporal (Stage 5)</h4>
    <div class="codex-cards-grid">
      ${ruleDetails
        .map(
          (r) => `
        <div class="codex-item-card">
          <img src="${r.src}" alt="${r.name}" />
          <div>
            <h5 style="font-family:'Cinzel',serif;font-size:1.04rem;color:var(--text-gold);">${r.name}</h5>
            <div style="font-size:0.76rem;color:var(--text-amber);font-style:italic;margin-bottom:5px;font-weight:700;">"${r.tagline}"</div>
            <p style="font-size:0.78rem;color:var(--text-light);line-height:1.45;margin-bottom:5px;"><strong>Pesos Alterados:</strong> ${r.changes}</p>
            <p style="font-size:0.75rem;color:var(--text-emerald);font-weight:700;">💡 <strong>Dica Tática:</strong> ${r.tip}</p>
          </div>
        </div>
      `
        )
        .join("")}
    </div>
  `;

  document.getElementById("codex-modal").classList.remove("hidden");
}

function openArtGalleryModal() {
  const body = document.getElementById("art-gallery-body");
  const renderCards = (items) =>
    items
      .map(
        (item) => `
      <div class="art-card">
        <img src="${item.src}" alt="${item.title}" loading="lazy" />
        <h4>${item.title}</h4>
        <p>${item.desc}</p>
      </div>
    `
      )
      .join("");

  body.innerHTML = `
    <h4 class="art-section-title">🛡️ 7 Emblemas Oficiais dos Time Squads (assets/emblems/)</h4>
    <div class="art-grid">${renderCards(ART_GALLERY_CATALOG.emblems)}</div>

    <h4 class="art-section-title">⚡ 3 Cartas de Power-Ups de Intervalo (assets/powerups/)</h4>
    <div class="art-grid">${renderCards(ART_GALLERY_CATALOG.powerups)}</div>

    <h4 class="art-section-title">🎩 8 Ilustrações das Regras Malucas (assets/rules/)</h4>
    <div class="art-grid">${renderCards(ART_GALLERY_CATALOG.rules)}</div>

    <h4 class="art-section-title">🧑‍💼🤖 Avatares dos Treinadores & 6 Ilustrações Cartoon do Tutorial (assets/ui/ & assets/tutorial/)</h4>
    <div class="art-grid">${renderCards(ART_GALLERY_CATALOG.coaches_and_tutorial)}</div>
  `;

  document.getElementById("art-gallery-modal").classList.remove("hidden");
}

function renderAll() {
  document.getElementById("run-badge").textContent = `Linha #${appState.run_id}`;
  renderStepper();
  renderMatchHud();
  if (appState.stage === 1) {
    renderRoosterCarousel();
    renderPlayerShowcase();
  } else if (appState.stage === 2) {
    renderStage2();
  } else if (appState.stage === 3) {
    renderStage3();
  } else if (appState.stage === 4) {
    renderStage4();
  } else if (appState.stage === 5) {
    renderStage5();
  } else if (appState.stage === 6) {
    renderStage6();
  } else if (appState.stage === 7) {
    renderStage7();
  } else if (appState.stage === 8) {
    renderStage8();
  }
  renderMinimizedDock();
}

async function fetchInitialState() {
  const res = await fetch("/api/state");
  syncFromServer(await res.json());
  renderAll();
}

async function rerollNewRun() {
  if (appState.isAnimatingVortex) return;
  appState.stage = 1;
  appState.maxUnlockedStage = 1;
  appState.stage6Starters = [];
  appState.stage7Starters = [];
  renderStepper();
  appState.isAnimatingVortex = true;

  const overlay = document.getElementById("temporal-vortex-overlay");
  const statusText = document.getElementById("vortex-status-text");
  const track = document.getElementById("rooster-carousel-track");

  track.classList.add("shuffling");
  overlay.classList.remove("hidden");
  statusText.textContent = "Abrindo Fenda Temporal 2014–2025 · Embaralhando ~300 Lendas...";

  const fetchPromise = fetch("/api/new-run", { method: "POST" }).then((r) => r.json());

  await new Promise((r) => setTimeout(r, 480));
  statusText.textContent = "Equilibrando 7 Cápsulas Temporais (24 Atletas por Time Squad)...";

  const [data] = await Promise.all([fetchPromise, new Promise((r) => setTimeout(r, 520))]);

  appState.activeRoosterIdx = 0;
  appState.activePlayerIdx = 0;
  syncFromServer(data);
  renderAll();

  requestAnimationFrame(() => {
    setTimeout(() => {
      track.classList.remove("shuffling");
      overlay.classList.add("hidden");
      appState.isAnimatingVortex = false;
    }, 80);
  });
}

async function selectRooster(idx) {
  const aiDiff = document.getElementById("ai-difficulty").value;
  const seriesMode = document.getElementById("series-mode").value;
  const res = await fetch("/api/select-rooster", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      rooster_index: idx,
      ai_difficulty: aiDiff,
      series_mode: seriesMode,
    }),
  });
  const data = await res.json();
  appState.activeRoosterIdx = idx;
  syncFromServer(data);
  renderAll();
}

function setViewMode(mode) {
  appState.viewMode = mode;
  document.getElementById("btn-view-3d").classList.toggle("active", mode === "3d");
  document.getElementById("btn-view-grid").classList.toggle("active", mode === "grid");
  document.getElementById("btn-view-table").classList.toggle("active", mode === "table");
  renderPlayerShowcase();
}

document.addEventListener("DOMContentLoaded", () => {
  fetchInitialState();

  document.getElementById("btn-reroll-run").addEventListener("click", rerollNewRun);
  const hudResetBtn = document.getElementById("btn-hud-reset-run");
  if (hudResetBtn) {
    hudResetBtn.addEventListener("click", rerollNewRun);
  }
  document.getElementById("btn-open-tutorial-tab").addEventListener("click", openTutorialModal);
  document.getElementById("btn-open-codex-tab").addEventListener("click", openCodexModal);
  document.getElementById("btn-open-art-gallery").addEventListener("click", openArtGalleryModal);

  // Stage Stepper Navigation Click
  document.querySelectorAll("#stage-stepper .stepper-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetStep = parseInt(btn.getAttribute("data-step"), 10);
      if (targetStep <= appState.maxUnlockedStage) {
        appState.stage = targetStep;
        renderAll();
      }
    });
  });

  document.getElementById("rooster-prev").addEventListener("click", () => {
    const n = appState.roosters.length;
    if (!n) return;
    appState.activeRoosterIdx = (appState.activeRoosterIdx - 1 + n) % n;
    appState.activePlayerIdx = 0;
    renderAll();
  });

  document.getElementById("rooster-next").addEventListener("click", () => {
    const n = appState.roosters.length;
    if (!n) return;
    appState.activeRoosterIdx = (appState.activeRoosterIdx + 1) % n;
    appState.activePlayerIdx = 0;
    renderAll();
  });

  document.getElementById("player-prev").addEventListener("click", () => {
    const players = getFilteredPlayers();
    if (!players.length) return;
    appState.activePlayerIdx = (appState.activePlayerIdx - 1 + players.length) % players.length;
    renderPlayerShowcase();
  });

  document.getElementById("player-next").addEventListener("click", () => {
    const players = getFilteredPlayers();
    if (!players.length) return;
    appState.activePlayerIdx = (appState.activePlayerIdx + 1) % players.length;
    renderPlayerShowcase();
  });

  // Mobile Touch Swipe Navigation for Carousels
  function setupTouchSwipe(elId, onLeft, onRight) {
    const el = document.getElementById(elId);
    if (!el) return;
    let startX = 0;
    let startY = 0;
    el.addEventListener("touchstart", (e) => {
      if (e.touches.length === 1) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      }
    }, { passive: true });
    el.addEventListener("touchend", (e) => {
      if (e.changedTouches.length === 1) {
        const dx = e.changedTouches[0].clientX - startX;
        const dy = e.changedTouches[0].clientY - startY;
        if (Math.abs(dx) > 36 && Math.abs(dx) > Math.abs(dy)) {
          if (dx < 0) onLeft();
          else onRight();
        }
      }
    }, { passive: true });
  }

  setupTouchSwipe("rooster-stage-3d", 
    () => document.getElementById("rooster-next")?.click(), 
    () => document.getElementById("rooster-prev")?.click()
  );
  setupTouchSwipe("player-stage-3d", 
    () => document.getElementById("player-next")?.click(), 
    () => document.getElementById("player-prev")?.click()
  );

  window.addEventListener("keydown", (e) => {
    if (appState.stage === 1) {
      if (e.key === "ArrowRight") {
        const players = getFilteredPlayers();
        if (!players.length) return;
        appState.activePlayerIdx = (appState.activePlayerIdx + 1) % players.length;
        renderPlayerShowcase();
      } else if (e.key === "ArrowLeft") {
        const players = getFilteredPlayers();
        if (!players.length) return;
        appState.activePlayerIdx = (appState.activePlayerIdx - 1 + players.length) % players.length;
        renderPlayerShowcase();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        const n = appState.roosters.length;
        if (!n) return;
        appState.activeRoosterIdx = (appState.activeRoosterIdx - 1 + n) % n;
        appState.activePlayerIdx = 0;
        renderAll();
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        const n = appState.roosters.length;
        if (!n) return;
        appState.activeRoosterIdx = (appState.activeRoosterIdx + 1) % n;
        appState.activePlayerIdx = 0;
        renderAll();
      }
    }
    if (e.key === "Escape") {
      document.getElementById("rooster-modal").classList.add("hidden");
      document.getElementById("tutorial-modal").classList.add("hidden");
      document.getElementById("codex-modal").classList.add("hidden");
      document.getElementById("art-gallery-modal").classList.add("hidden");
    }
  });

  document.querySelectorAll(".pos-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".pos-tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      appState.posFilter = btn.getAttribute("data-pos");
      appState.activePlayerIdx = 0;
      renderPlayerShowcase();
    });
  });

  document.getElementById("btn-view-3d").addEventListener("click", () => setViewMode("3d"));
  document.getElementById("btn-view-grid").addEventListener("click", () => setViewMode("grid"));
  document.getElementById("btn-view-table").addEventListener("click", () => setViewMode("table"));

  // Theme Toggle (Dark Mode vs Light Cream Mode)
  const themeBtn = document.getElementById("btn-theme-toggle");
  const applyTheme = (isLight) => {
    document.body.classList.toggle("light-mode", isLight);
    if (themeBtn) {
      themeBtn.innerHTML = isLight ? "🌙 Modo Escuro" : "☀️ Modo Claro";
    }
    try {
      localStorage.setItem("clt_theme_mode", isLight ? "light" : "dark");
    } catch (_) {}
  };

  try {
    const savedTheme = localStorage.getItem("clt_theme_mode");
    if (savedTheme === "light") {
      applyTheme(true);
    }
  } catch (_) {}

  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const nextLight = !document.body.classList.contains("light-mode");
      applyTheme(nextLight);
    });
  }

  const modalBtnLineup = document.getElementById("modal-btn-lineup");
  if (modalBtnLineup) {
    modalBtnLineup.addEventListener("click", () => {
      appState.modalViewMode = "lineup";
      renderModalContent();
    });
  }

  document.getElementById("modal-btn-cards").addEventListener("click", () => {
    appState.modalViewMode = "cards";
    renderModalContent();
  });

  document.getElementById("modal-btn-table").addEventListener("click", () => {
    appState.modalViewMode = "table";
    renderModalContent();
  });

  document.getElementById("dock-human-btn").addEventListener("click", () => {
    if (appState.humanRoosterIdx !== null) {
      openRoosterModal(appState.humanRoosterIdx, "🧑‍💼 SEU TIME SQUAD · CONSULTA DE ELENCO (24 ATLETAS)", true);
    }
  });

  document.getElementById("dock-ai-btn").addEventListener("click", () => {
    if (appState.aiRoosterIdx !== null) {
      openRoosterModal(appState.aiRoosterIdx, "🤖 TIME SQUAD DA IA · ESCALAÇÃO & ELENCO (24 ATLETAS)", false);
    }
  });

  document.getElementById("modal-close-btn").addEventListener("click", () => {
    document.getElementById("rooster-modal").classList.add("hidden");
  });

  document.getElementById("rooster-modal").addEventListener("click", (e) => {
    if (e.target.id === "rooster-modal") {
      document.getElementById("rooster-modal").classList.add("hidden");
    }
  });

  document.getElementById("tutorial-modal-close-btn").addEventListener("click", () => {
    document.getElementById("tutorial-modal").classList.add("hidden");
  });

  document.getElementById("tutorial-modal").addEventListener("click", (e) => {
    if (e.target.id === "tutorial-modal") {
      document.getElementById("tutorial-modal").classList.add("hidden");
    }
  });

  document.getElementById("codex-modal-close-btn").addEventListener("click", () => {
    document.getElementById("codex-modal").classList.add("hidden");
  });

  document.getElementById("codex-modal").addEventListener("click", (e) => {
    if (e.target.id === "codex-modal") {
      document.getElementById("codex-modal").classList.add("hidden");
    }
  });

  document.getElementById("art-modal-close-btn").addEventListener("click", () => {
    document.getElementById("art-gallery-modal").classList.add("hidden");
  });

  document.getElementById("art-gallery-modal").addEventListener("click", (e) => {
    if (e.target.id === "art-gallery-modal") {
      document.getElementById("art-gallery-modal").classList.add("hidden");
    }
  });
});

