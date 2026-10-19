"""
CLT (Cartola Legends of Time) — 8-Stage Game State Machine & In-Memory Data Store
=================================================================================
Manages the full lifecycle of a Best-of-5 / Best-of-3 series across Stages 1 to 8.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd

try:
    from engine.data_prep import generate_dynamic_roosters, POS_CODE_MAP, POS_NAME_MAP
    from engine.rules import (
        CRAZY_RULES,
        UNIVERSAL_SCOUTS,
        get_rule_with_comparison,
        evaluate_player_round_score,
    )
    from engine.ai_agent import (
        VALID_FORMATIONS,
        ai_choose_season,
        ai_choose_round,
        ai_bucket_decision,
        ai_build_lineup,
    )
except ImportError:
    from app.engine.data_prep import generate_dynamic_roosters, POS_CODE_MAP, POS_NAME_MAP
    from app.engine.rules import (
        CRAZY_RULES,
        UNIVERSAL_SCOUTS,
        get_rule_with_comparison,
        evaluate_player_round_score,
    )
    from app.engine.ai_agent import (
        VALID_FORMATIONS,
        ai_choose_season,
        ai_choose_round,
        ai_bucket_decision,
        ai_build_lineup,
    )

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_SILHOUETTE = "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/silhuetas/OUT/220x220.png"


class CLTDataStore:
    """Fast in-memory lookup tables for all 12 seasons (2014-2025)."""

    def __init__(self):
        print("Initializing CLTDataStore (teams, matches, career stats, normalized scouts)...")
        self.df_teams = pd.read_parquet(DATA_DIR / "teams.parquet")
        self.df_matches = pd.read_parquet(DATA_DIR / "matches.parquet")
        self.df_career = pd.read_parquet(DATA_DIR / "player_career_stats.parquet")
        self.df_scouts = pd.read_parquet(DATA_DIR / "normalized_scouts.parquet")

        # 1. Teams lookup
        self.teams_by_id: Dict[int, Dict[str, Any]] = {}
        for _, r in self.df_teams.iterrows():
            tid = int(r["team_id"])
            abbr = str(r["abbreviation"])
            self.teams_by_id[tid] = {
                "team_id": tid,
                "team_name": str(r["team_name"]),
                "abbreviation": abbr,
                "badge_url": f"/assets/clubs/{abbr}.png",
                "badge_small_url": f"/assets/clubs/{abbr}.png",
            }

        # 2. Career players lookup (for Bucket of the Souls permanent roster swaps)
        self.players_by_id: Dict[int, Dict[str, Any]] = {}
        for _, p_row in self.df_career.iterrows():
            pid = int(p_row["player_id"])
            top_teams = (
                json.loads(p_row["top_teams_json"])
                if isinstance(p_row.get("top_teams_json"), str)
                else []
            )
            self.players_by_id[pid] = {
                "player_id": pid,
                "short_name": str(p_row["canonical_nickname"]),
                "full_name": str(p_row["canonical_name"]),
                "position_id": int(p_row["mode_position_id"]),
                "position_code": str(p_row["mode_position_code"]),
                "position_name": str(p_row["mode_position_name"]),
                "avg_score": round(float(p_row["avg_score"]), 2),
                "rounds_played": int(p_row["rounds_played"]),
                "seasons_played": int(p_row["seasons_played"]),
                "first_season": int(p_row["first_season"]),
                "last_season": int(p_row["last_season"]),
                "photo_url": str(p_row["photo_url"] or DEFAULT_SILHOUETTE),
                "is_silhouette": bool(p_row["is_silhouette"]),
                "top_teams": top_teams,
            }

        # 3. Matches by (season, round)
        self.matches_by_sr: Dict[Tuple[int, int], List[Dict[str, Any]]] = {}
        for (s, r), grp in self.df_matches.groupby(["season", "round"]):
            m_list = []
            for idx, m in enumerate(grp.to_dict("records")):
                ht = self.teams_by_id.get(int(m["home_team_id"]), {})
                at = self.teams_by_id.get(int(m["away_team_id"]), {})
                m_list.append({
                    "slot_index": idx,
                    "match_id": int(m["match_id"]),
                    "home_team": ht,
                    "away_team": at,
                    "home_score": int(m["home_score"]) if pd.notna(m["home_score"]) else 0,
                    "away_score": int(m["away_score"]) if pd.notna(m["away_score"]) else 0,
                })
            self.matches_by_sr[(int(s), int(r))] = m_list

        # 4. Scouts by (season, round) -> {player_id: dict}
        self.scouts_by_sr: Dict[Tuple[int, int], Dict[int, Dict[str, Any]]] = {}
        cols = ["season", "round", "player_id", "team_id", "position_id", "played", "points", "base_norm_score"] + UNIVERSAL_SCOUTS
        records = self.df_scouts[cols].to_dict("records")
        for rec in records:
            key = (int(rec["season"]), int(rec["round"]))
            if key not in self.scouts_by_sr:
                self.scouts_by_sr[key] = {}
            self.scouts_by_sr[key][int(rec["player_id"])] = rec

        print(f"-> CLTDataStore ready: {len(self.scouts_by_sr)} (season, round) slices indexed.")


class CLTGameEngine:
    """Stateful game manager for the 8-stage CLT loop."""

    def __init__(self, store: CLTDataStore):
        self.store = store
        self.previous_ai_rooster_ids: List[str] = []
        self.run_id = 0
        self.state: Dict[str, Any] = {}
        self.start_new_run()

    def _recalc_rooster_summary(self, rooster: Dict[str, Any]):
        squad = rooster["players"]
        rooster["summary"] = {
            "player_count": len(squad),
            "mean_player_avg_score": round(float(np.mean([p["avg_score"] for p in squad])), 2),
            "mean_rounds_played": round(float(np.mean([p["rounds_played"] for p in squad])), 1),
            "total_historical_appearances": int(np.sum([p["rounds_played"] for p in squad])),
        }

    def start_new_run(self) -> Dict[str, Any]:
        self.run_id += 1
        roosters = generate_dynamic_roosters(self.store.df_career)
        self.state = {
            "run_id": self.run_id,
            "stage": 1,
            "series_mode": "bo3",
            "target_wins": 2,
            "ai_difficulty": "veteran",
            "match_number": 1,
            "human_wins": 0,
            "ai_wins": 0,
            "match_history": [],
            "roosters": roosters,
            "human_rooster_index": None,
            "ai_rooster_index": None,
            "powerups_remaining": {
                "human": {"reveal_zeroed": True, "copycat": True, "grenal": True},
                "ai": {"reveal_zeroed": True, "copycat": True, "grenal": True},
            },
            "stage2": {},
            "stage3": {},
            "stage4": {},
            "stage5": {},
            "stage6": {},
            "stage7": {},
            "stage8": {},
        }
        return self.state

    # =========================================================================
    # STAGE 1 -> STAGE 2: SELECT TIME SQUAD & INITIALIZE PARAMETERS
    # =========================================================================
    def select_rooster(self, rooster_index: int, ai_difficulty: str = "veteran", series_mode: str = "bo3") -> Dict[str, Any]:
        if self.state.get("human_rooster_index") is not None:
            raise ValueError("Seu Time Squad já está travado nesta série! Clique em 'Resetar Série' para iniciar uma nova run.")
        roosters = self.state["roosters"]
        r_idx = max(0, min(len(roosters) - 1, int(rooster_index)))
        self.state["human_rooster_index"] = r_idx
        self.state["ai_difficulty"] = ai_difficulty
        self.state["series_mode"] = series_mode
        self.state["target_wins"] = 2 if series_mode == "bo3" else 3

        avail = [i for i in range(len(roosters)) if i != r_idx]
        non_rep = [
            i for i in avail
            if roosters[i]["rooster_id"] not in self.previous_ai_rooster_ids[-2:]
        ]
        pool = non_rep if non_rep else avail
        ai_idx = random.choice(pool)
        self.state["ai_rooster_index"] = ai_idx
        self.previous_ai_rooster_ids.append(roosters[ai_idx]["rooster_id"])

        self.prepare_stage_2()
        return self.state

    def prepare_stage_2(self, first_chooser: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepares Stage 2 (Season & Round selection).
        Alternates who picks first based on `match_number` unless explicitly overridden.
        """
        if self.state.get("stage2", {}).get("completed", False):
            raise ValueError("As coordenadas temporais desta partida já foram travadas!")
        self.state["stage"] = 2
        m_num = self.state["match_number"]
        if first_chooser is None:
            first_chooser = "human" if (m_num % 2 == 1) else "ai"

        ai_squad = self.state["roosters"][self.state["ai_rooster_index"]]["players"]
        diff = self.state["ai_difficulty"]

        if first_chooser == "human":
            self.state["stage2"] = {
                "first_chooser": "human",
                "second_chooser": "ai",
                "bucket_first_picker": "ai",
                "human_param_type": "round",
                "season": None,
                "round": None,
                "ai_log": "Aguardando sua escolha do 1º parâmetro temporal...",
                "completed": False,
            }
        else:
            ai_locks_round = (m_num % 4 == 2)
            if ai_locks_round:
                r_val, ai_msg = ai_choose_round(ai_squad, None, diff, self.store.scouts_by_sr)
                self.state["stage2"] = {
                    "first_chooser": "ai",
                    "second_chooser": "human",
                    "bucket_first_picker": "human",
                    "human_param_type": "season",
                    "season": None,
                    "round": r_val,
                    "ai_log": f"🤖 IA escolheu o 1º parâmetro: Rodada #{r_val}! ({ai_msg}) Agora você escolhe o Ano (2014–2025) e terá a 1ª escolha no Bucket of the Souls!",
                    "completed": False,
                }
            else:
                y_val, ai_msg = ai_choose_season(ai_squad, None, diff, self.store.scouts_by_sr)
                self.state["stage2"] = {
                    "first_chooser": "ai",
                    "second_chooser": "human",
                    "bucket_first_picker": "human",
                    "human_param_type": "round",
                    "season": y_val,
                    "round": None,
                    "ai_log": f"🤖 IA escolheu o 1º parâmetro: Temporada {y_val}! ({ai_msg}) Agora você escolhe a Rodada (1–38) e terá a 1ª escolha no Bucket of the Souls!",
                    "completed": False,
                }
        return self.state

    def submit_stage_2_parameter(self, param_type: str, value: int) -> Dict[str, Any]:
        """Locks the Human's parameter (season or round), triggers AI if AI is 2nd, and advances to Stage 3."""
        s2 = self.state["stage2"]
        if s2.get("completed", False):
            raise ValueError("As coordenadas temporais desta partida já foram travadas!")
        ai_squad = self.state["roosters"][self.state["ai_rooster_index"]]["players"]
        diff = self.state["ai_difficulty"]

        if s2["first_chooser"] == "human":
            if param_type == "round":
                r_val = max(1, min(38, int(value)))
                y_val, ai_msg = ai_choose_season(ai_squad, r_val, diff, self.store.scouts_by_sr)
                s2["round"] = r_val
                s2["season"] = y_val
                s2["ai_log"] = f"Você cravou a Rodada #{r_val}. Em resposta, {ai_msg}"
            else:
                y_val = max(2014, min(2025, int(value)))
                r_val, ai_msg = ai_choose_round(ai_squad, y_val, diff, self.store.scouts_by_sr)
                s2["season"] = y_val
                s2["round"] = r_val
                s2["ai_log"] = f"Você cravou a Temporada {y_val}. Em resposta, {ai_msg}"
        else:
            if s2["season"] is None:
                s2["season"] = max(2014, min(2025, int(value)))
            else:
                s2["round"] = max(1, min(38, int(value)))

        s2["completed"] = True
        self.prepare_stage_3()
        return self.state

    # =========================================================================
    # STAGE 3: BUCKET OF THE SOULS (6 ACTIVE PLAYERS, 1 PER POSITION, NO STATS)
    # =========================================================================
    def prepare_stage_3(self) -> Dict[str, Any]:
        self.state["stage"] = 3
        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        first_picker = self.state["stage2"]["bucket_first_picker"]

        h_squad = self.state["roosters"][self.state["human_rooster_index"]]["players"]
        a_squad = self.state["roosters"][self.state["ai_rooster_index"]]["players"]
        excluded_ids = {p["player_id"] for p in h_squad} | {p["player_id"] for p in a_squad}

        rmap = self.store.scouts_by_sr.get((season, round_num), {})

        bucket_cards = []
        for pos_id in [1, 3, 2, 4, 5, 6]:
            pos_code = POS_CODE_MAP[pos_id]
            active_cands = [
                rec for pid, rec in rmap.items()
                if bool(rec.get("played", False))
                and pid not in excluded_ids
                and pid in self.store.players_by_id
                and self.store.players_by_id[pid]["position_id"] == pos_id
            ]
            if not active_cands:
                active_cands = [
                    rec for pid, rec in rmap.items()
                    if bool(rec.get("played", False))
                    and pid not in excluded_ids
                    and int(rec.get("position_id", 0)) == pos_id
                    and pid in self.store.players_by_id
                ]

            if active_cands:
                chosen_rec = random.choice(active_cands)
                pid = int(chosen_rec["player_id"])
                p_info = self.store.players_by_id[pid]
                tid = int(chosen_rec["team_id"])
                team_info = self.store.teams_by_id.get(tid, {
                    "team_id": tid,
                    "team_name": "Clube",
                    "abbreviation": "CLB",
                    "badge_url": "",
                })
                excluded_ids.add(pid)
                bucket_cards.append({
                    "player_id": pid,
                    "short_name": p_info["short_name"],
                    "full_name": p_info["full_name"],
                    "photo_url": p_info["photo_url"],
                    "position_id": pos_id,
                    "position_code": pos_code,
                    "position_name": POS_NAME_MAP[pos_id],
                    "round_team": team_info,
                    "picked_by": None,
                })

        s3 = {
            "season": season,
            "round": round_num,
            "first_picker": first_picker,
            "bucket_cards": bucket_cards,
            "ai_decision": None,
            "human_decision": None,
            "completed": False,
        }

        if first_picker == "ai":
            self._execute_ai_bucket_turn(s3)

        self.state["stage3"] = s3
        return self.state

    def _execute_ai_bucket_turn(self, s3: Dict[str, Any]):
        avail = [c for c in s3["bucket_cards"] if c["picked_by"] is None]
        ai_rooster = self.state["roosters"][self.state["ai_rooster_index"]]
        decision = ai_bucket_decision(
            ai_rooster["players"],
            avail,
            s3["season"],
            s3["round"],
            self.state["ai_difficulty"],
            self.store.scouts_by_sr,
        )
        if decision["action"] == "swap":
            b_id = decision["bucket_player_id"]
            drop_id = decision["dropped_player_id"]
            for c in s3["bucket_cards"]:
                if c["player_id"] == b_id:
                    c["picked_by"] = "ai"
                    break
            new_player_full = self.store.players_by_id[b_id].copy()
            new_player_full["recruited_from_bucket"] = True
            ai_rooster["players"] = [
                new_player_full if p["player_id"] == drop_id else p
                for p in ai_rooster["players"]
            ]
            self._recalc_rooster_summary(ai_rooster)
        s3["ai_decision"] = decision

    def submit_stage_3_bucket(self, action: str, bucket_player_id: Optional[int] = None, dropped_player_id: Optional[int] = None) -> Dict[str, Any]:
        """Executes Human's Bucket choice ('swap' or 'pass') strictly once per match."""
        s3 = self.state["stage3"]
        if s3.get("completed", False):
            raise ValueError("Sua decisão no Bucket of the Souls já foi selada nesta partida! Não é permitido fazer múltiplas trocas.")

        h_rooster = self.state["roosters"][self.state["human_rooster_index"]]

        if action == "swap" and bucket_player_id is not None and dropped_player_id is not None:
            b_id = int(bucket_player_id)
            d_id = int(dropped_player_id)
            b_card = next((c for c in s3["bucket_cards"] if c["player_id"] == b_id and c["picked_by"] is None), None)
            d_player = next((p for p in h_rooster["players"] if p["player_id"] == d_id), None)

            if not b_card or not d_player:
                raise ValueError("Jogador inválido para troca no Bucket of the Souls.")
            if b_card["position_code"] != d_player["position_code"]:
                raise ValueError("A troca no Bucket of the Souls exige atletas da MESMA posição!")

            b_card["picked_by"] = "human"
            new_player_full = self.store.players_by_id[b_id].copy()
            new_player_full["recruited_from_bucket"] = True
            h_rooster["players"] = [
                new_player_full if p["player_id"] == d_id else p
                for p in h_rooster["players"]
            ]
            self._recalc_rooster_summary(h_rooster)
            s3["human_decision"] = {
                "action": "swap",
                "bucket_player": b_card,
                "dropped_player": d_player,
                "reason": f"Você recrutou {b_card['short_name']} ({b_card['position_code']}) e liberou {d_player['short_name']} permanentemente!"
            }
        else:
            s3["human_decision"] = {
                "action": "pass",
                "reason": "Você passou a vez e manteve os 24 atletas do seu Time Squad."
            }

        if s3["first_picker"] == "human" and s3["ai_decision"] is None:
            self._execute_ai_bucket_turn(s3)

        s3["completed"] = True
        self.prepare_stage_4()
        return self.state

    # =========================================================================
    # STAGE 4: HIGHLIGHTS OF DESTINY (10 GRAY BARS -> 5 MATCHUPS OR 2 SCORES)
    # =========================================================================
    def prepare_stage_4(self) -> Dict[str, Any]:
        self.state["stage"] = 4
        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        fixtures = self.store.matches_by_sr.get((season, round_num), [])

        masked_slots = [
            {
                "slot_index": i,
                "revealed": False,
                "show_score": False,
                "home_team": None,
                "away_team": None,
                "home_score": None,
                "away_score": None,
            }
            for i in range(len(fixtures))
        ]
        self.state["stage4"] = {
            "season": season,
            "round": round_num,
            "choice_mode": None,
            "slots": masked_slots,
            "completed": False,
        }
        return self.state

    def submit_stage_4_highlights(self, choice_mode: str) -> Dict[str, Any]:
        """Reveals either 5 random matchups (no scores) or 2 random matchups with full scores — strictly once per match!"""
        s4 = self.state["stage4"]
        if s4.get("completed", False):
            raise ValueError("Os Highlights of Destiny já foram revelados nesta partida! Apenas 1 escolha (Opção A ou Opção B) é permitida.")

        season = s4["season"]
        round_num = s4["round"]
        fixtures = self.store.matches_by_sr.get((season, round_num), [])
        n_total = len(fixtures)

        if choice_mode == "2_scores":
            k = min(2, n_total)
            show_score = True
        else:
            choice_mode = "5_matches"
            k = min(5, n_total)
            show_score = False

        chosen_indices = set(random.sample(range(n_total), k)) if n_total > 0 else set()
        slots = []
        for i, m in enumerate(fixtures):
            if i in chosen_indices:
                slots.append({
                    "slot_index": i,
                    "revealed": True,
                    "show_score": show_score,
                    "home_team": m["home_team"],
                    "away_team": m["away_team"],
                    "home_score": m["home_score"] if show_score else None,
                    "away_score": m["away_score"] if show_score else None,
                })
            else:
                slots.append({
                    "slot_index": i,
                    "revealed": False,
                    "show_score": False,
                    "home_team": None,
                    "away_team": None,
                    "home_score": None,
                    "away_score": None,
                })

        s4["choice_mode"] = choice_mode
        s4["slots"] = slots
        s4["completed"] = True

        # Pre-generate Stage 5 Crazy Rule, and keep self.state["stage"] = 5
        self.prepare_stage_5()
        return self.state

    # =========================================================================
    # STAGE 5: CRAZY RULES REVEAL
    # =========================================================================
    def prepare_stage_5(self, force_rule_id: Optional[str] = None) -> Dict[str, Any]:
        if self.state.get("stage5", {}).get("locked", False):
            raise ValueError("A Regra Maluca já foi selada para a escalação desta partida!")
        self.state["stage"] = 5
        if force_rule_id:
            chosen = get_rule_with_comparison(force_rule_id)
        else:
            raw_rule = random.choice(CRAZY_RULES)
            chosen = get_rule_with_comparison(raw_rule["rule_id"])

        self.state["stage5"] = {
            "active_rule": chosen,
            "all_rules_summary": [
                {
                    "rule_id": r["rule_id"],
                    "name": r["name"],
                    "tagline": r["tagline"],
                    "art_url": r["art_url"],
                    "accent_color": r["accent_color"],
                }
                for r in CRAZY_RULES
            ],
            "completed": True,
            "locked": False,
        }
        return self.state

    # =========================================================================
    # STAGE 6, 7 & 8: LINEUP, HALF-TIME 6v6, POWER-UPS & FINAL REPORT
    # =========================================================================
    def prepare_stage_6(self) -> Dict[str, Any]:
        if "stage5" in self.state and self.state["stage5"]:
            self.state["stage5"]["locked"] = True
        self.state["stage"] = 6
        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        rule_id = self.state["stage5"]["active_rule"]["rule_id"]
        ai_squad = self.state["roosters"][self.state["ai_rooster_index"]]["players"]

        ai_lineup = ai_build_lineup(
            ai_squad,
            season,
            round_num,
            rule_id,
            self.state["ai_difficulty"],
            self.store.scouts_by_sr,
        )
        self.state["stage6"] = {
            "valid_formations": VALID_FORMATIONS,
            "human_lineup": None,
            "ai_lineup": ai_lineup,
            "completed": False,
        }
        return self.state

    def validate_lineup(self, squad: List[Dict[str, Any]], formation: str, starter_ids: List[int], captain_id: int) -> Tuple[bool, str]:
        if formation not in VALID_FORMATIONS:
            return False, f"Formação inválida: {formation}."
        quotas = VALID_FORMATIONS[formation]
        if len(starter_ids) != 12 or len(set(starter_ids)) != 12:
            return False, "A escalação deve conter exatamente 12 titulares únicos (11 em campo + 1 Técnico)."
        squad_by_id = {p["player_id"]: p for p in squad}
        counts = {"GOL": 0, "ZAG": 0, "LAT": 0, "MEI": 0, "ATA": 0, "TEC": 0}
        for pid in starter_ids:
            if pid not in squad_by_id:
                return False, f"Atleta {pid} não pertence ao seu Time Squad."
            counts[squad_by_id[pid]["position_code"]] += 1
        for pos_code, req in quotas.items():
            if counts.get(pos_code, 0) != req:
                return False, f"Formação {formation} exige {req} {pos_code}, mas foram selecionados {counts.get(pos_code, 0)}."
        if captain_id not in starter_ids:
            return False, "O Capitão (2x) deve estar entre os titulares escalados."
        return True, "Escalação válida! Pronto para o Kick-Off."

    def submit_stage_6_lineup(self, formation: str, starter_ids: List[int], captain_id: int) -> Dict[str, Any]:
        if self.state.get("stage6", {}).get("completed", False):
            raise ValueError("A escalação titular (Stage 6) já foi confirmada e o 1º tempo já começou!")
        h_squad = self.state["roosters"][self.state["human_rooster_index"]]["players"]
        ok, msg = self.validate_lineup(h_squad, formation, starter_ids, captain_id)
        if not ok:
            raise ValueError(msg)

        self.state["stage6"]["human_lineup"] = {
            "formation": formation,
            "starter_ids": [int(x) for x in starter_ids],
            "captain_id": int(captain_id),
        }
        self.state["stage6"]["completed"] = True
        self.prepare_stage_7()
        return self.state

    def prepare_stage_7(self) -> Dict[str, Any]:
        """Computes the Half-Time 6v6 random sample score and initializes Stage 7."""
        self.state["stage"] = 7
        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        rule_id = self.state["stage5"]["active_rule"]["rule_id"]
        rmap = self.store.scouts_by_sr.get((season, round_num), {})

        h_squad_map = {p["player_id"]: p for p in self.state["roosters"][self.state["human_rooster_index"]]["players"]}
        a_squad_map = {p["player_id"]: p for p in self.state["roosters"][self.state["ai_rooster_index"]]["players"]}

        h_starters = self.state["stage6"]["human_lineup"]["starter_ids"]
        h_cap = self.state["stage6"]["human_lineup"]["captain_id"]
        a_starters = self.state["stage6"]["ai_lineup"]["starter_ids"]
        a_cap = self.state["stage6"]["ai_lineup"]["captain_id"]

        h_sample_ids = random.sample(h_starters, min(6, len(h_starters)))
        a_sample_ids = random.sample(a_starters, min(6, len(a_starters)))

        h_sample_score = round(sum(
            evaluate_player_round_score(rmap.get(pid), h_squad_map[pid]["position_id"], rule_id, pid == h_cap)["final_score"]
            for pid in h_sample_ids
        ), 2)
        a_sample_score = round(sum(
            evaluate_player_round_score(rmap.get(pid), a_squad_map[pid]["position_id"], rule_id, pid == a_cap)["final_score"]
            for pid in a_sample_ids
        ), 2)

        ai_starters_preview = [
            {
                "player_id": pid,
                "short_name": a_squad_map[pid]["short_name"],
                "position_code": a_squad_map[pid]["position_code"],
                "photo_url": a_squad_map[pid]["photo_url"],
                "avg_score": a_squad_map[pid]["avg_score"],
                "is_captain": pid == a_cap,
            }
            for pid in a_starters
            if pid in a_squad_map
        ]

        self.state["stage7"] = {
            "halftime_sample": {
                "human_sample_score": h_sample_score,
                "ai_sample_score": a_sample_score,
                "sample_size": 6,
            },
            "ai_starters_preview": ai_starters_preview,
            "powerup_used": None,
            "zeroed_starter_ids": [],
            "copycat_info": None,
            "grenal_removed": None,
            "completed": False,
        }
        return self.state

    def use_stage_7_powerup(self, powerup_id: str, target_opponent_id: Optional[int] = None, target_own_id: Optional[int] = None) -> Dict[str, Any]:
        s7 = self.state["stage7"]
        if s7.get("completed", False):
            raise ValueError("O intervalo já foi encerrado!")
        if s7["powerup_used"] is not None:
            raise ValueError("Apenas 1 Power-Up pode ser utilizado por intervalo!")
        rem = self.state["powerups_remaining"]["human"]
        if not rem.get(powerup_id, False):
            raise ValueError(f"Power-Up '{powerup_id}' já foi utilizado nesta série!")

        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        rule_id = self.state["stage5"]["active_rule"]["rule_id"]
        rmap = self.store.scouts_by_sr.get((season, round_num), {})

        h_squad_map = {p["player_id"]: p for p in self.state["roosters"][self.state["human_rooster_index"]]["players"]}
        a_squad_map = {p["player_id"]: p for p in self.state["roosters"][self.state["ai_rooster_index"]]["players"]}
        h_starters = self.state["stage6"]["human_lineup"]["starter_ids"]
        a_starters = self.state["stage6"]["ai_lineup"]["starter_ids"]

        rem[powerup_id] = False
        s7["powerup_used"] = powerup_id

        if powerup_id == "reveal_zeroed":
            zeroed = []
            for pid in h_starters:
                ev = evaluate_player_round_score(rmap.get(pid), h_squad_map[pid]["position_id"], rule_id, False)
                if ev["zeroed"]:
                    zeroed.append(pid)
            s7["zeroed_starter_ids"] = zeroed

        elif powerup_id == "copycat":
            own_id = int(target_own_id) if target_own_id else h_starters[0]
            opp_id = int(target_opponent_id) if target_opponent_id else a_starters[0]
            s7["copycat_info"] = {
                "own_player_id": own_id,
                "own_short_name": h_squad_map.get(own_id, {}).get("short_name", "Titular"),
                "opponent_player_id": opp_id,
                "opponent_short_name": a_squad_map.get(opp_id, {}).get("short_name", "Adversário"),
            }

        elif powerup_id == "grenal":
            h_elig = [pid for pid in h_starters if h_squad_map[pid]["position_code"] != "TEC"]
            a_elig = [pid for pid in a_starters if a_squad_map[pid]["position_code"] != "TEC"]
            h_rem = random.sample(h_elig, min(3, len(h_elig)))
            a_rem = random.sample(a_elig, min(3, len(a_elig)))
            s7["grenal_removed"] = {
                "human_removed_ids": h_rem,
                "ai_removed_ids": a_rem,
                "human_removed_names": [f"{h_squad_map[p]['short_name']} ({h_squad_map[p]['position_code']})" for p in h_rem],
                "ai_removed_names": [f"{a_squad_map[p]['short_name']} ({a_squad_map[p]['position_code']})" for p in a_rem],
            }

        return self.state

    def submit_stage_7_halftime(self, formation: str, final_starter_ids: List[int], captain_id: int) -> Dict[str, Any]:
        """Validates up to 3 substitutions at Half-Time and advances to Stage 8 Match Conclusion."""
        if self.state.get("stage7", {}).get("completed", False):
            raise ValueError("As alterações de intervalo já foram submetidas nesta partida!")
        h_squad = self.state["roosters"][self.state["human_rooster_index"]]["players"]
        ok, msg = self.validate_lineup(h_squad, formation, final_starter_ids, captain_id)
        if not ok:
            raise ValueError(msg)

        initial_set = set(self.state["stage6"]["human_lineup"]["starter_ids"])
        final_set = set(int(x) for x in final_starter_ids)
        subs_count = len(final_set - initial_set)
        if subs_count > 3:
            raise ValueError(f"Limite máximo de 3 substituições no intervalo excedido ({subs_count} trocas feitas).")

        self.state["stage7"]["final_human_lineup"] = {
            "formation": formation,
            "starter_ids": [int(x) for x in final_starter_ids],
            "captain_id": int(captain_id),
            "subs_made": subs_count,
        }
        self.state["stage7"]["completed"] = True
        self.evaluate_stage_8()
        return self.state

    def evaluate_stage_8(self) -> Dict[str, Any]:
        """Computes final match scores, MVP, scout breakdown, bench scores, and updates series tally."""
        self.state["stage"] = 8
        season = int(self.state["stage2"]["season"])
        round_num = int(self.state["stage2"]["round"])
        rule_id = self.state["stage5"]["active_rule"]["rule_id"]
        rmap = self.store.scouts_by_sr.get((season, round_num), {})

        h_rooster = self.state["roosters"][self.state["human_rooster_index"]]
        a_rooster = self.state["roosters"][self.state["ai_rooster_index"]]

        h_lineup = self.state["stage7"].get("final_human_lineup") or self.state["stage6"]["human_lineup"]
        a_lineup = self.state["stage6"]["ai_lineup"]

        grenal = self.state["stage7"].get("grenal_removed") or {}
        h_red = set(grenal.get("human_removed_ids", []))
        a_red = set(grenal.get("ai_removed_ids", []))
        copycat = self.state["stage7"].get("copycat_info")

        def build_team_report(squad: List[Dict[str, Any]], starter_ids: List[int], cap_id: int, red_ids: set) -> Dict[str, Any]:
            starters_out = []
            bench_out = []
            starter_set = set(starter_ids)
            for p in squad:
                pid = p["player_id"]
                is_starter = pid in starter_set
                is_cap = is_starter and (pid == cap_id)
                ev = evaluate_player_round_score(rmap.get(pid), p["position_id"], rule_id, is_cap)
                if is_starter and pid in red_ids:
                    ev["final_score"] = 0.0
                    ev["grenal_expelled"] = True
                else:
                    ev["grenal_expelled"] = False

                rec = rmap.get(pid)
                round_team = self.store.teams_by_id.get(int(rec["team_id"])) if (rec and int(rec.get("team_id", 0)) in self.store.teams_by_id) else None
                item = {
                    **p,
                    "is_starter": is_starter,
                    "is_captain": is_cap,
                    "round_team": round_team,
                    "eval": ev,
                }
                if is_starter:
                    starters_out.append(item)
                else:
                    bench_out.append(item)
            return {"starters": starters_out, "bench": bench_out}

        a_rep = build_team_report(a_rooster["players"], a_lineup["starter_ids"], a_lineup["captain_id"], a_red)
        h_rep = build_team_report(h_rooster["players"], h_lineup["starter_ids"], h_lineup["captain_id"], h_red)

        # Apply Copycat if used
        if copycat:
            opp_id = copycat["opponent_player_id"]
            own_id = copycat["own_player_id"]
            opp_item = next((x for x in a_rep["starters"] if x["player_id"] == opp_id), None)
            own_item = next((x for x in h_rep["starters"] if x["player_id"] == own_id), None)
            if opp_item and own_item and not own_item["eval"].get("grenal_expelled"):
                copied_raw = opp_item["eval"]["raw_score"]
                mult = 2.0 if own_item["is_captain"] else 1.0
                own_item["eval"]["raw_score"] = copied_raw
                own_item["eval"]["final_score"] = round(copied_raw * mult, 2)
                own_item["eval"]["copied_from"] = opp_item["short_name"]

        h_total = round(sum(x["eval"]["final_score"] for x in h_rep["starters"]), 2)
        a_total = round(sum(x["eval"]["final_score"] for x in a_rep["starters"]), 2)

        all_starters = h_rep["starters"] + a_rep["starters"]
        mvp = max(all_starters, key=lambda x: x["eval"]["final_score"]) if all_starters else None

        if h_total >= a_total:
            winner = "human"
            self.state["human_wins"] += 1
        else:
            winner = "ai"
            self.state["ai_wins"] += 1

        series_over = (self.state["human_wins"] >= self.state["target_wins"]) or (self.state["ai_wins"] >= self.state["target_wins"])

        report = {
            "match_number": self.state["match_number"],
            "season": season,
            "round": round_num,
            "rule_name": self.state["stage5"]["active_rule"]["name"],
            "human_formation": h_lineup["formation"],
            "ai_formation": a_lineup["formation"],
            "human_total": h_total,
            "ai_total": a_total,
            "winner": winner,
            "mvp": mvp,
            "human_report": h_rep,
            "ai_report": a_rep,
            "series_over": series_over,
            "series_winner": ("human" if self.state["human_wins"] >= self.state["target_wins"] else "ai") if series_over else None,
        }
        self.state["stage8"] = report
        self.state["match_history"].append({
            "match_number": self.state["match_number"],
            "season": season,
            "round": round_num,
            "rule_name": self.state["stage5"]["active_rule"]["name"],
            "human_total": h_total,
            "ai_total": a_total,
            "winner": winner,
            "mvp": mvp,
        })
        return self.state

    def advance_to_next_match(self) -> Dict[str, Any]:
        """Advances the series to the next match (Stage 2) keeping persistent Bucket of Souls roster mutations."""
        prev_first = self.state.get("stage2", {}).get("first_chooser", "human")
        next_first = "ai" if prev_first == "human" else "human"
        self.state["match_number"] += 1
        self.state["stage2"] = {}
        self.state["stage3"] = {}
        self.state["stage4"] = {}
        self.state["stage5"] = {}
        self.state["stage6"] = {}
        self.state["stage7"] = {}
        self.state["stage8"] = {}
        self.prepare_stage_2(first_chooser=next_first)
        return self.state
