"""
CLT (Cartola Legends of Time) — 3-Tier AI Opponent Engine
=========================================================
Implements decision-making for:
  - "rookie"  (Estagiário do Tempo): Uses career averages + high noise.
  - "veteran" (Cartoleiro Pro): Uses season-specific activity & season averages.
  - "oracle"  (Oráculo Temporal): Uses noisy round score lookahead.
"""

import random
from typing import Dict, List, Any, Optional, Tuple
try:
    from engine.rules import evaluate_player_round_score
except ImportError:
    from app.engine.rules import evaluate_player_round_score

VALID_FORMATIONS: Dict[str, Dict[str, int]] = {
    "4-4-2": {"GOL": 1, "ZAG": 2, "LAT": 2, "MEI": 4, "ATA": 2, "TEC": 1},
    "4-3-3": {"GOL": 1, "ZAG": 2, "LAT": 2, "MEI": 3, "ATA": 3, "TEC": 1},
    "4-5-1": {"GOL": 1, "ZAG": 2, "LAT": 2, "MEI": 5, "ATA": 1, "TEC": 1},
    "3-4-3": {"GOL": 1, "ZAG": 3, "LAT": 0, "MEI": 4, "ATA": 3, "TEC": 1},
    "3-5-2": {"GOL": 1, "ZAG": 3, "LAT": 0, "MEI": 5, "ATA": 2, "TEC": 1},
}


def ai_choose_season(
    ai_squad: List[Dict[str, Any]],
    chosen_round: Optional[int],
    difficulty: str,
    round_lookup: Dict[Tuple[int, int], Dict[int, Dict[str, Any]]]
) -> Tuple[int, str]:
    """AI selects a Season (2014..2025) and returns (season, reasoning_text)."""
    seasons = list(range(2014, 2026))
    if difficulty == "rookie":
        y = random.choice(seasons)
        return y, f"IA (Estagiário) girou a roleta temporal e cravou a temporada {y}!"

    if difficulty == "veteran":
        # Score each season by how many AI squad players were active in that era
        scored = []
        for y in seasons:
            era_matches = sum(1 for p in ai_squad if p["first_season"] <= y <= p["last_season"])
            if chosen_round is not None:
                rmap = round_lookup.get((y, chosen_round), {})
                active_cnt = sum(1 for p in ai_squad if rmap.get(p["player_id"], {}).get("played", False))
                score = era_matches * 0.6 + active_cnt * 1.4 + random.uniform(-1.5, 1.5)
            else:
                score = era_matches + random.uniform(-1.5, 1.5)
            scored.append((score, y))
        scored.sort(reverse=True)
        best_y = scored[0][1]
        return best_y, f"IA (Cartoleiro Pro) analisou a janela de carreira do elenco e escolheu o ano {best_y}!"

    # Oracle
    scored = []
    for y in seasons:
        r_check = chosen_round if chosen_round is not None else random.randint(1, 38)
        rmap = round_lookup.get((y, r_check), {})
        pts = sum(
            float(rmap.get(p["player_id"], {}).get("base_norm_score", 0.0))
            for p in ai_squad
            if rmap.get(p["player_id"], {}).get("played", False)
        )
        scored.append((pts + random.gauss(0, 12.0), y))
    scored.sort(reverse=True)
    best_y = scored[0][1]
    return best_y, f"IA (Oráculo Temporal) consultou os astros da Série A e decretou a temporada {best_y}!"


def ai_choose_round(
    ai_squad: List[Dict[str, Any]],
    chosen_season: Optional[int],
    difficulty: str,
    round_lookup: Dict[Tuple[int, int], Dict[int, Dict[str, Any]]]
) -> Tuple[int, str]:
    """AI selects a Round (1..38) and returns (round_num, reasoning_text)."""
    rounds = list(range(1, 39))
    if difficulty == "rookie" or chosen_season is None:
        r = random.choice(rounds)
        return r, f"IA sorteou a Rodada #{r} no calendário histórico!"

    scored = []
    for r in rounds:
        rmap = round_lookup.get((chosen_season, r), {})
        active_cnt = sum(1 for p in ai_squad if rmap.get(p["player_id"], {}).get("played", False))
        pts = sum(
            float(rmap.get(p["player_id"], {}).get("base_norm_score", 0.0))
            for p in ai_squad
            if rmap.get(p["player_id"], {}).get("played", False)
        )
        if difficulty == "veteran":
            val = active_cnt * 2.5 + random.uniform(-3.0, 3.0)
        else:
            val = pts + random.gauss(0, 10.0)
        scored.append((val, r))
    scored.sort(reverse=True)
    best_r = scored[0][1]
    return best_r, f"IA escolheu a Rodada #{best_r} buscando máxima sinergia histórica!"


def ai_bucket_decision(
    ai_squad: List[Dict[str, Any]],
    available_bucket: List[Dict[str, Any]],
    season: int,
    round_num: int,
    difficulty: str,
    round_lookup: Dict[Tuple[int, int], Dict[int, Dict[str, Any]]]
) -> Dict[str, Any]:
    """
    Decides whether the AI swaps a player from `available_bucket` into `ai_squad`
    (replacing a same-position player) or passes.
    """
    if not available_bucket:
        return {"action": "pass", "reason": "Bucket vazio."}

    if difficulty == "rookie" and random.random() < 0.30:
        return {"action": "pass", "reason": "IA (Estagiário) preferiu confiar no próprio elenco e passou a vez."}

    rmap = round_lookup.get((season, round_num), {})

    best_gain = 0.5  # minimum threshold to justify a swap
    best_choice = None

    for b_card in available_bucket:
        pos_code = b_card["position_code"]
        same_pos_squad = [p for p in ai_squad if p["position_code"] == pos_code]
        if not same_pos_squad:
            continue

        # Find the weakest AI player at this position for this (season, round)
        def eval_squad_member(p: Dict[str, Any]) -> float:
            rec = rmap.get(p["player_id"])
            played_now = bool(rec and rec.get("played", False))
            in_era = p["first_season"] <= season <= p["last_season"]
            if difficulty == "rookie":
                return p["avg_score"] + random.uniform(-1.5, 1.5)
            elif difficulty == "veteran":
                return (4.0 if in_era else 0.0) + (3.0 if played_now else 0.0) + p["avg_score"] * 0.5
            else:
                real_pts = float(rec.get("base_norm_score", 0.0)) if played_now else 0.0
                return real_pts + random.gauss(0, 1.8)

        same_pos_squad_sorted = sorted(same_pos_squad, key=eval_squad_member)
        weakest_p = same_pos_squad_sorted[0]
        weakest_val = eval_squad_member(weakest_p)

        # Evaluate bucket card (Note: Bucket cards are guaranteed to have played=True in (season, round)!)
        b_rec = rmap.get(b_card["player_id"], {})
        if difficulty == "rookie":
            b_val = 5.2 + random.uniform(-1.0, 2.0)
        elif difficulty == "veteran":
            b_val = 7.8 + random.uniform(-0.8, 1.2)
        else:
            b_val = float(b_rec.get("base_norm_score", 5.0)) + random.gauss(0, 1.5)

        gain = b_val - weakest_val
        if gain > best_gain:
            best_gain = gain
            best_choice = (b_card, weakest_p)

    if not best_choice:
        return {
            "action": "pass",
            "reason": "IA avaliou o Bucket of the Souls e decidiu manter seu Time Squad intacto."
        }

    b_in, p_out = best_choice
    return {
        "action": "swap",
        "bucket_player_id": b_in["player_id"],
        "dropped_player_id": p_out["player_id"],
        "bucket_player": b_in,
        "dropped_player": p_out,
        "reason": f"IA recrutou {b_in['short_name']} ({b_in['position_code']} · {b_in['round_team']['abbreviation']}) e liberou {p_out['short_name']}!"
    }


def ai_build_lineup(
    ai_squad: List[Dict[str, Any]],
    season: int,
    round_num: int,
    rule_id: str,
    difficulty: str,
    round_lookup: Dict[Tuple[int, int], Dict[int, Dict[str, Any]]]
) -> Dict[str, Any]:
    """Selects optimal formation, 12 starters (11 outfield/GK + 1 TEC), and Captain for the AI."""
    rmap = round_lookup.get((season, round_num), {})

    scored_players: Dict[int, float] = {}
    for p in ai_squad:
        pid = p["player_id"]
        rec = rmap.get(pid)
        if difficulty == "rookie":
            est = p["avg_score"] + random.gauss(0, 1.8)
        elif difficulty == "veteran":
            in_era = 2.5 if (p["first_season"] <= season <= p["last_season"]) else -2.0
            played_bonus = 3.5 if (rec and rec.get("played", False)) else 0.0
            est = p["avg_score"] + in_era + played_bonus + random.gauss(0, 1.4)
        else:
            eval_res = evaluate_player_round_score(rec, p["position_id"], rule_id, is_captain=False)
            est = eval_res["raw_score"] + random.gauss(0, 2.0)
        scored_players[pid] = est

    best_form_name = "4-3-3"
    best_total = -9999.0
    best_starters: List[int] = []

    for form_name, quotas in VALID_FORMATIONS.items():
        chosen_ids = []
        form_sum = 0.0
        for pos_code, count in quotas.items():
            if count == 0:
                continue
            cands = sorted(
                [p for p in ai_squad if p["position_code"] == pos_code],
                key=lambda x: scored_players[x["player_id"]],
                reverse=True
            )[:count]
            chosen_ids.extend([c["player_id"] for c in cands])
            form_sum += sum(scored_players[c["player_id"]] for c in cands)
        if form_sum > best_total:
            best_total = form_sum
            best_form_name = form_name
            best_starters = chosen_ids

    # Choose Captain among non-TEC starters with highest estimated score
    non_tec_starters = [
        pid for pid in best_starters
        if next((p["position_code"] for p in ai_squad if p["player_id"] == pid), "") != "TEC"
    ]
    captain_id = max(non_tec_starters, key=lambda pid: scored_players.get(pid, 0.0)) if non_tec_starters else best_starters[0]

    return {
        "formation": best_form_name,
        "starter_ids": best_starters,
        "captain_id": captain_id
    }
