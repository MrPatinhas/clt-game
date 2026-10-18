"""
CLT (Cartola Legends of Time) — Universal 17-Scout Scoring & Crazy Rules Engine
================================================================================
Implements the normalized 17-scout weight matrix across the Base Cartola rule and
all 8 Crazy Rules defined in the PRD.
"""

from typing import Dict, List, Any

UNIVERSAL_SCOUTS: List[str] = [
    "G", "A", "SG", "DP", "DE", "DS", "FT", "FD", "FF", "FS",
    "GC", "CV", "CA", "GS", "FC", "I", "PP"
]

SCOUT_LABELS: Dict[str, str] = {
    "G": "Gol",
    "A": "Assistência",
    "SG": "Saldo de Gols (Sem Sofrer)",
    "DP": "Defesa de Pênalti",
    "DE": "Defesa Difícil (Norm.)",
    "DS": "Desarme / Roubada (Norm.)",
    "FT": "Finalização na Trave",
    "FD": "Finalização Defendida",
    "FF": "Finalização para Fora",
    "FS": "Falta Sofrida",
    "GC": "Gol Contra",
    "CV": "Cartão Vermelho",
    "CA": "Cartão Amarelo",
    "GS": "Gol Sofrido (Goleiro)",
    "FC": "Falta Cometida",
    "I": "Impedimento",
    "PP": "Pênalti Perdido",
}

BASE_WEIGHTS: Dict[str, float] = {
    "G": 8.0, "A": 5.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.0,
    "FT": 3.0, "FD": 1.2, "FF": 0.8, "FS": 0.5,
    "GC": -3.0, "CV": -3.0, "CA": -1.0, "GS": -1.0, "FC": -0.3,
    "I": -0.1, "PP": -4.0
}

CRAZY_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "gabriel_jesus",
        "name": "Regra de Gabriel Jesus",
        "tagline": "Gol não vale nada. O que vale é marcar lateral e roubar bola!",
        "art_url": "/assets/rules/gabriel_jesus.png",
        "accent_color": "#F9A03F",
        "weights": {
            "G": 4.0, "A": 5.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 3.1,
            "FT": 3.5, "FD": 0.6, "FF": 0.4, "FS": 0.5,
            "GC": -6.0, "CV": -5.0, "CA": -2.0, "GS": -2.0, "FC": -0.5,
            "I": -0.5, "PP": -3.5
        },
        "key_changes": [
            "DS (Desarme) dispara para +3.1 pts (3.1x o valor base)",
            "G (Gol) cai pela metade (+4.0 pts)",
            "FD (+0.6) e FF (+0.4) reduzidos pela metade"
        ]
    },
    {
        "rule_id": "felipe_melo",
        "name": "Regra de Felipe Melo",
        "tagline": "Cartão é sinal de entrega e não punição. Toda falta sofrida é simulação!",
        "art_url": "/assets/rules/felipe_melo.png",
        "accent_color": "#E0533C",
        "weights": {
            "G": 8.0, "A": 5.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.3,
            "FT": 3.5, "FD": 1.2, "FF": 0.8, "FS": -0.5,
            "GC": -6.0, "CV": 5.0, "CA": 2.0, "GS": -2.0, "FC": 0.0,
            "I": -0.5, "PP": -3.5
        },
        "key_changes": [
            "CV (Cartão Vermelho) soma +5.0 pts!",
            "CA (Cartão Amarelo) soma +2.0 pts!",
            "FC (Falta Cometida) zerada (0.0) · FS (Falta Sofrida) pune (-0.5)"
        ]
    },
    {
        "rule_id": "futsal",
        "name": "Regra do Futsal",
        "tagline": "Toque curto! Assistência vale ouro, sem impedimento e falta pesa o triplo.",
        "art_url": "/assets/rules/futsal.png",
        "accent_color": "#3A86C8",
        "weights": {
            "G": 8.0, "A": 8.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.3,
            "FT": 3.5, "FD": 1.2, "FF": 0.8, "FS": 0.5,
            "GC": -6.0, "CV": -5.0, "CA": -2.0, "GS": -2.0, "FC": -1.5,
            "I": 0.0, "PP": -3.5
        },
        "key_changes": [
            "A (Assistência) sobe para +8.0 pts (igual a um Gol!)",
            "I (Impedimento) anulado (0.0 pts)",
            "FC (Falta Cometida) severa (-1.5 pts por falta)"
        ]
    },
    {
        "rule_id": "mano_menezes",
        "name": "Regra do Mano Menezes",
        "tagline": "Achei ofensivo, recua! Saldo de Gols (SG) vale o dobro.",
        "art_url": "/assets/rules/mano_menezes.png",
        "accent_color": "#3A86C8",
        "weights": {
            "G": 8.0, "A": 5.0, "SG": 10.0, "DP": 7.0, "DE": 1.3, "DS": 1.3,
            "FT": 3.5, "FD": 1.2, "FF": 0.8, "FS": 0.5,
            "GC": -6.0, "CV": -5.0, "CA": -2.0, "GS": -2.0, "FC": -0.5,
            "I": -0.5, "PP": -3.5
        },
        "key_changes": [
            "SG (Saldo de Gols para GOL/ZAG/LAT) vale +10.0 pts (Dobro!)",
            "DS (Desarme) bonificado (+1.3 pts)",
            "Defesas sólidas dominam a rodada"
        ]
    },
    {
        "rule_id": "vanderlei",
        "name": "Regra do Vanderlei",
        "tagline": "O que vale na vida são pontes! Defesa Difícil e DP valem ouro, GS pesa.",
        "art_url": "/assets/rules/vanderlei.png",
        "accent_color": "#F2C249",
        "weights": {
            "G": 8.0, "A": 5.0, "SG": 5.0, "DP": 14.0, "DE": 3.2, "DS": 1.3,
            "FT": 3.5, "FD": 2.0, "FF": 0.8, "FS": 0.5,
            "GC": -6.0, "CV": -5.0, "CA": -2.0, "GS": -4.0, "FC": -0.5,
            "I": -0.5, "PP": -3.5
        },
        "key_changes": [
            "DE (Defesa Difícil) salta para +3.2 pts · DP vale +14.0 pts!",
            "FD (Finalização Defendida) sobe para +2.0 pts",
            "GS (Gol Sofrido) pune pesadamente (-4.0 pts)"
        ]
    },
    {
        "rule_id": "garcom",
        "name": "Regra do Garçom",
        "tagline": "Mais vale aquele que compartilha (+10 A) do que aquele que comemora (+5 G)!",
        "art_url": "/assets/rules/garcom.png",
        "accent_color": "#F2C249",
        "weights": {
            "G": 5.0, "A": 10.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.3,
            "FT": 3.5, "FD": 1.2, "FF": 0.8, "FS": 0.5,
            "GC": -6.0, "CV": -5.0, "CA": -2.0, "GS": -2.0, "FC": -0.5,
            "I": -0.5, "PP": -3.5
        },
        "key_changes": [
            "A (Assistência) vale o dobro (+10.0 pts)!",
            "G (Gol) reduzido para +5.0 pts",
            "Meias criativos e laterais cruzadores viram reis"
        ]
    },
    {
        "rule_id": "buda",
        "name": "Regra do Buda",
        "tagline": "Seja positivo! Zero negatividades — todos os scouts negativos são zerados.",
        "art_url": "/assets/rules/buda.png",
        "accent_color": "#F9A03F",
        "weights": {
            "G": 8.0, "A": 5.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.3,
            "FT": 3.5, "FD": 1.2, "FF": 0.8, "FS": 0.5,
            "GC": 0.0, "CV": 0.0, "CA": 0.0, "GS": 0.0, "FC": 0.0,
            "I": 0.0, "PP": 0.0
        },
        "key_changes": [
            "GC, CV, CA, GS, FC, I e PP valem 0.0 (Ninguém perde pontos!)",
            "FT sobe para +3.5 pts e DS para +1.3 pts",
            "Paz interior total no gramado"
        ]
    },
    {
        "rule_id": "open_capitao",
        "name": "Regra Open Capitão",
        "tagline": "DOBRO DE TUDO POSITIVO E QUÁDRUPLO DAS PUNIÇÕES!",
        "art_url": "/assets/rules/open_capitao.png",
        "accent_color": "#E0533C",
        "weights": {
            "G": 16.0, "A": 10.0, "SG": 10.0, "DP": 14.0, "DE": 2.6, "DS": 2.6,
            "FT": 7.0, "FD": 2.4, "FF": 1.6, "FS": 1.0,
            "GC": -24.0, "CV": -20.0, "CA": -8.0, "GS": -8.0, "FC": -2.0,
            "I": -2.0, "PP": -14.0
        },
        "key_changes": [
            "Todos os scouts positivos valem 2x (Gol = +16.0, Assistência = +10.0)!",
            "Todos os scouts negativos punem 4x (CA = -8.0, CV = -20.0, GS = -8.0)!",
            "Alta voltagem: Capitão (2x) pode chegar a +32 pts por Gol ou -40 por CV!"
        ]
    }
]

RULES_BY_ID: Dict[str, Dict[str, Any]] = {r["rule_id"]: r for r in CRAZY_RULES}


def get_rule_with_comparison(rule_id: str) -> Dict[str, Any]:
    """Returns the Crazy Rule enriched with a 17-scout comparison against BASE_WEIGHTS."""
    rule = RULES_BY_ID.get(rule_id, CRAZY_RULES[0]).copy()
    comparison = []
    for s in UNIVERSAL_SCOUTS:
        base_w = BASE_WEIGHTS[s]
        curr_w = rule["weights"][s]
        diff = round(curr_w - base_w, 2)
        status = "same"
        if curr_w > base_w:
            status = "buff"
        elif curr_w < base_w:
            status = "nerf"
        comparison.append({
            "scout": s,
            "label": SCOUT_LABELS[s],
            "base_weight": base_w,
            "rule_weight": curr_w,
            "diff": diff,
            "status": status
        })
    rule["scout_comparison"] = comparison
    return rule


def evaluate_player_round_score(
    scout_row: Dict[str, Any] | None,
    position_id: int,
    rule_id: str,
    is_captain: bool = False
) -> Dict[str, Any]:
    """
    Computes a single player's score for a specific (season, round) under `rule_id`.
    - If `scout_row` is None or `played` is False: returns 0.0 (`zeroed=True`).
    - If `position_id == 6` (TEC): uses static historical `points` from the database.
    - Otherwise: sums the 17 universal scouts * rule weights.
    - Multiplies by 2.0 if `is_captain=True`.
    """
    if not scout_row or not bool(scout_row.get("played", False)):
        return {
            "played": False,
            "raw_score": 0.0,
            "final_score": 0.0,
            "is_captain": is_captain,
            "zeroed": True,
            "breakdown": []
        }

    rule = RULES_BY_ID.get(rule_id, CRAZY_RULES[0])
    weights = rule["weights"]

    if int(position_id) == 6:
        raw_pts = round(float(scout_row.get("points", 0.0)), 2)
        breakdown = [{
            "scout": "TEC",
            "label": "Pontuação Histórica do Técnico",
            "count": 1.0,
            "weight": raw_pts,
            "points": raw_pts
        }]
    else:
        raw_pts = 0.0
        breakdown = []
        for s in UNIVERSAL_SCOUTS:
            cnt = float(scout_row.get(s, 0.0))
            if abs(cnt) > 1e-6:
                w = float(weights[s])
                pts = round(cnt * w, 2)
                raw_pts += pts
                breakdown.append({
                    "scout": s,
                    "label": SCOUT_LABELS[s],
                    "count": round(cnt, 2),
                    "weight": w,
                    "points": pts
                })
        raw_pts = round(raw_pts, 2)

    final_pts = round(raw_pts * 2.0, 2) if is_captain else raw_pts
    zeroed = abs(raw_pts) < 1e-6

    return {
        "played": True,
        "raw_score": raw_pts,
        "final_score": final_pts,
        "is_captain": is_captain,
        "zeroed": zeroed,
        "breakdown": breakdown
    }
