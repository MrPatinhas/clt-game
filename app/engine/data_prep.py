import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
SCOUTS_DIR = DATA_DIR / "player_scouts"

# Empirical Era Conversion Factors (derived across 131,660 active appearances in 2014-2025)
RB_TO_DS_FACTOR = 1.286  # 2014-2019 RB (mean 1.088/g) -> 2020-2025 DS (mean 1.399/g)
DD_TO_DE_FACTOR = 2.160  # 2014-2020 DD (mean 1.503/g) -> 2022-2025 DE (mean 3.247/g)

# Universal 17 Scouts (PE, PS, PC, V excluded per PRD)
UNIVERSAL_SCOUTS = [
    "G", "A", "SG", "DP", "DE", "DS", "FT", "FD", "FF", "FS",
    "GC", "CV", "CA", "GS", "FC", "I", "PP"
]

BASE_WEIGHTS = {
    "G": 8.0, "A": 5.0, "SG": 5.0, "DP": 7.0, "DE": 1.3, "DS": 1.0,
    "FT": 3.0, "FD": 1.2, "FF": 0.8, "FS": 0.5,
    "GC": -3.0, "CV": -3.0, "CA": -1.0, "GS": -1.0, "FC": -0.3,
    "I": -0.1, "PP": -4.0
}

POS_CODE_MAP = {1: "GOL", 2: "LAT", 3: "ZAG", 4: "MEI", 5: "ATA", 6: "TEC"}
POS_NAME_MAP = {1: "Goleiro", 2: "Lateral", 3: "Zagueiro", 4: "Meia", 5: "Atacante", 6: "Técnico"}

# Required composition per 24-man Rooster (168 total players across 7 Roosters)
ROOSTER_QUOTAS = {
    1: 2,  # 2 GK (GOL)  -> 14 drafted from top 26 pool
    3: 4,  # 4 ZAG       -> 28 drafted from top 50 pool
    2: 4,  # 4 LAT       -> 28 drafted from top 50 pool
    4: 8,  # 8 MEI       -> 56 drafted from top 96 pool
    5: 5,  # 5 ATA       -> 35 drafted from top 64 pool
    6: 1,  # 1 TEC       -> 7 drafted from top 14 pool
}

#Expanded Legends Pool sizes (~300 top players) for per-game stochastic variety
POOL_CANDIDATE_SIZES = {
    1: 26,
    3: 50,
    2: 50,
    4: 96,
    5: 64,
    6: 14,
}

ROOSTER_THEMES = [
    {
        "rooster_id": "time_squad_a",
        "name": "Time Squad A",
        "tagline": "Relíquias da Cartola · Unidade Alpha",
        "accent_color": "#F9A03F",
        "secondary_color": "#2E2A27",
        "emblem": "🎩",
        "emblem_url": "/assets/emblems/squad_a.png"
    },
    {
        "rooster_id": "time_squad_b",
        "name": "Time Squad B",
        "tagline": "Pêndulo Imortal · Unidade Bravo",
        "accent_color": "#3A86C8",
        "secondary_color": "#2E2A27",
        "emblem": "⏳",
        "emblem_url": "/assets/emblems/squad_b.png"
    },
    {
        "rooster_id": "time_squad_c",
        "name": "Time Squad C",
        "tagline": "Bússola do Século · Unidade Charlie",
        "accent_color": "#F2C249",
        "secondary_color": "#2E2A27",
        "emblem": "🧭",
        "emblem_url": "/assets/emblems/squad_c.png"
    },
    {
        "rooster_id": "time_squad_d",
        "name": "Time Squad D",
        "tagline": "Ampulheta Dourada · Unidade Delta",
        "accent_color": "#E0533C",
        "secondary_color": "#2E2A27",
        "emblem": "⌛",
        "emblem_url": "/assets/emblems/squad_d.png"
    },
    {
        "rooster_id": "time_squad_e",
        "name": "Time Squad E",
        "tagline": "Engrenagem Real · Unidade Echo",
        "accent_color": "#F9A03F",
        "secondary_color": "#2E2A27",
        "emblem": "⚙️",
        "emblem_url": "/assets/emblems/squad_e.png"
    },
    {
        "rooster_id": "time_squad_f",
        "name": "Time Squad F",
        "tagline": "Vórtice de Cronos · Unidade Foxtrot",
        "accent_color": "#3A86C8",
        "secondary_color": "#2E2A27",
        "emblem": "🌀",
        "emblem_url": "/assets/emblems/squad_f.png"
    },
    {
        "rooster_id": "time_squad_g",
        "name": "Time Squad G",
        "tagline": "Oráculo Eterno · Unidade Golf",
        "accent_color": "#F2C249",
        "secondary_color": "#2E2A27",
        "emblem": "🕰️",
        "emblem_url": "/assets/emblems/squad_g.png"
    }
]


def build_normalized_scouts():
    print("1. Loading raw seasonal player_scouts (2014-2025)...")
    dfs = []
    for p in sorted(SCOUTS_DIR.glob("season=*")):
        df_s = pd.read_parquet(p / "data.parquet")
        dfs.append(df_s)
    df = pd.concat(dfs, ignore_index=True)

    for col in UNIVERSAL_SCOUTS + ["RB", "DD"]:
        if col not in df.columns:
            df[col] = 0.0
        else:
            df[col] = df[col].fillna(0.0).astype(float)

    print("2. Applying empirical era conversions: RB -> DS (x1.286) and DD -> DE (x2.160)...")
    rb_mask = (df["DS"] == 0.0) & (df["RB"] > 0.0)
    df.loc[rb_mask, "DS"] = (df.loc[rb_mask, "RB"] * RB_TO_DS_FACTOR).round(2)

    dd_mask = (df["DE"] == 0.0) & (df["DD"] > 0.0)
    df.loc[dd_mask, "DE"] = (df.loc[dd_mask, "DD"] * DD_TO_DE_FACTOR).round(2)

    scout_score = pd.Series(0.0, index=df.index)
    for s, w in BASE_WEIGHTS.items():
        scout_score += df[s] * w

    is_coach = df["position_id"] == 6
    df["base_norm_score"] = np.where(
        ~df["played"],
        0.0,
        np.where(is_coach, df["points"], scout_score)
    ).round(2)

    keep_cols = [
        "player_id", "season", "round", "team_id", "position_id",
        "played", "points", "base_norm_score", "price", "price_variation"
    ] + UNIVERSAL_SCOUTS

    df_norm = df[keep_cols].sort_values(["season", "round", "player_id"]).reset_index(drop=True)
    out_path = DATA_DIR / "normalized_scouts.parquet"
    df_norm.to_parquet(out_path, index=False)
    print(f"-> Saved {len(df_norm):,} normalized rows to {out_path}")
    return df_norm


def build_player_career_stats(df_norm: pd.DataFrame):
    print("\n3. Computing player modal positions, career metrics, and top-3 clubs...")
    players = pd.read_parquet(DATA_DIR / "players.parquet")
    teams = pd.read_parquet(DATA_DIR / "teams.parquet")
    team_lookup = teams.set_index("team_id").to_dict("index")

    active = df_norm[df_norm["played"]].copy()

    pos_counts = active.groupby(["player_id", "position_id"]).size().reset_index(name="cnt")
    pos_counts = pos_counts.sort_values(["player_id", "cnt", "position_id"], ascending=[True, False, True])
    modal_pos_map = pos_counts.drop_duplicates("player_id").set_index("player_id")["position_id"].to_dict()

    team_counts = active.groupby(["player_id", "team_id"]).size().reset_index(name="apps")
    team_counts = team_counts.sort_values(["player_id", "apps"], ascending=[True, False])
    top3_teams_df = team_counts.groupby("player_id").head(3)

    top_teams_map = {}
    for pid, grp in top3_teams_df.groupby("player_id"):
        t_list = []
        for _, r in grp.iterrows():
            tid = int(r["team_id"])
            t_info = team_lookup.get(tid, {})
            t_list.append({
                "team_id": tid,
                "team_name": t_info.get("team_name", f"Clube {tid}"),
                "abbreviation": t_info.get("abbreviation", "CLB"),
                "badge_url": t_info.get("badge_url", ""),
                "badge_small_url": t_info.get("badge_small_url", ""),
                "appearances": int(r["apps"])
            })
        top_teams_map[int(pid)] = t_list

    career_agg = active.groupby("player_id").agg(
        rounds_played=("played", "count"),
        seasons_played=("season", "nunique"),
        avg_score=("base_norm_score", "mean"),
        avg_raw_points=("points", "mean"),
        total_score=("base_norm_score", "sum"),
        total_goals=("G", "sum"),
        total_assists=("A", "sum"),
        total_ds=("DS", "sum"),
        total_de=("DE", "sum"),
        total_sg=("SG", "sum")
    ).reset_index()

    df_career = players.merge(career_agg, on="player_id", how="left")
    df_career["rounds_played"] = df_career["rounds_played"].fillna(0).astype(int)
    df_career["seasons_played"] = df_career["seasons_played"].fillna(0).astype(int)
    df_career["avg_score"] = df_career["avg_score"].fillna(0.0).round(2)
    df_career["avg_raw_points"] = df_career["avg_raw_points"].fillna(0.0).round(2)
    df_career["total_score"] = df_career["total_score"].fillna(0.0).round(2)

    df_career["mode_position_id"] = df_career["player_id"].map(modal_pos_map).fillna(df_career["position_id"]).astype(int)
    df_career["mode_position_code"] = df_career["mode_position_id"].map(POS_CODE_MAP).fillna("MEI")
    df_career["mode_position_name"] = df_career["mode_position_id"].map(POS_NAME_MAP).fillna("Meia")
    df_career["top_teams_json"] = df_career["player_id"].map(
        lambda pid: json.dumps(top_teams_map.get(int(pid), []), ensure_ascii=False)
    )

    career_path = DATA_DIR / "player_career_stats.parquet"
    df_career.to_parquet(career_path, index=False)
    print(f"-> Saved career stats for {len(df_career):,} players to {career_path}")
    return df_career


def generate_dynamic_roosters(df_career: pd.DataFrame = None, seed: int = None):
    """
    Dynamically generates 7 balanced 24-man Roosters (168 players total) by
    stochastically sampling without replacement from the Top ~300 Legends Pool
    and applying a randomized deficit-compensated snake draft.
    Every new game call produces a fresh set of 7 Roosters!
    """
    if df_career is None:
        df_career = pd.read_parquet(DATA_DIR / "player_career_stats.parquet")

    rng = np.random.default_rng(seed)
    rooster_buckets = {i: [] for i in range(7)}

    # Randomize initial Rooster priority order so Rooster 0 doesn't always pick first
    initial_tiebreaker = rng.random(7)

    for pos_id in [1, 3, 2, 4, 5, 6]:
        quota_per_rooster = ROOSTER_QUOTAS[pos_id]
        total_needed = quota_per_rooster * 7
        pool_size = POOL_CANDIDATE_SIZES[pos_id]

        # Filter to players with at least 45 active rounds so they have meaningful multi-season history
        elig = df_career[(df_career["mode_position_id"] == pos_id) & (df_career["rounds_played"] >= 45)].copy()
        if len(elig) < pool_size:
            elig = df_career[df_career["mode_position_id"] == pos_id].copy()

        r_min, r_max = elig["rounds_played"].min(), elig["rounds_played"].max()
        s_min, s_max = elig["avg_score"].min(), elig["avg_score"].max()
        elig["norm_r"] = (elig["rounds_played"] - r_min) / max(1.0, (r_max - r_min))
        elig["norm_s"] = (elig["avg_score"] - s_min) / max(0.01, (s_max - s_min))
        elig["rank_score"] = 0.60 * elig["norm_r"] + 0.40 * elig["norm_s"]

        # Take the top `pool_size` candidates for this position (~300 total across all positions)
        candidates = elig.sort_values(["rank_score", "rounds_played"], ascending=[False, False]).head(pool_size).copy()

        # Weighted stochastic sampling without replacement:
        # Higher rank_score has higher probability of appearing, but pool rotates every run!
        weights = np.power(np.clip(candidates["rank_score"].values, 0.15, 1.0), 1.6)
        probs = weights / weights.sum()
        sampled_indices = rng.choice(len(candidates), size=min(total_needed, len(candidates)), replace=False, p=probs)
        draft_pool = candidates.iloc[sampled_indices].copy()

        # Add slight random jitter to rank_score before tiering so tier boundaries also permute across runs
        draft_pool["draft_order_score"] = draft_pool["rank_score"] + rng.normal(0, 0.045, size=len(draft_pool))
        draft_pool = draft_pool.sort_values("draft_order_score", ascending=False).reset_index(drop=True)

        for tier_idx in range(quota_per_rooster):
            tier_slice = draft_pool.iloc[tier_idx * 7 : (tier_idx + 1) * 7].copy()
            # Sort Roosters by lowest accumulated strength + random tie-breaker so all 7 stay balanced
            rooster_order = sorted(
                range(7),
                key=lambda r_i: (
                    sum(p["avg_score"] for p in rooster_buckets[r_i]) * 1.5
                    + sum(p["rounds_played"] for p in rooster_buckets[r_i]) / 55.0
                    + rng.normal(0, 0.35)
                    + initial_tiebreaker[r_i] * 0.1
                )
            )
            tier_rows = tier_slice.sort_values(["avg_score", "rounds_played"], ascending=[False, False]).reset_index(drop=True)
            for idx_in_tier, rooster_num in enumerate(rooster_order):
                p_row = tier_rows.iloc[idx_in_tier]
                pid = int(p_row["player_id"])
                top_teams = json.loads(p_row["top_teams_json"]) if isinstance(p_row.get("top_teams_json"), str) else []
                rooster_buckets[rooster_num].append({
                    "player_id": pid,
                    "short_name": p_row["canonical_nickname"],
                    "full_name": p_row["canonical_name"],
                    "position_id": int(p_row["mode_position_id"]),
                    "position_code": p_row["mode_position_code"],
                    "position_name": p_row["mode_position_name"],
                    "avg_score": float(p_row["avg_score"]),
                    "rounds_played": int(p_row["rounds_played"]),
                    "seasons_played": int(p_row["seasons_played"]),
                    "first_season": int(p_row["first_season"]),
                    "last_season": int(p_row["last_season"]),
                    "photo_url": p_row["photo_url"],
                    "is_silhouette": bool(p_row["is_silhouette"]),
                    "top_teams": top_teams,
                    "rank_score": round(float(p_row["rank_score"]), 4)
                })

    roosters_out = []
    for i, theme in enumerate(ROOSTER_THEMES):
        squad = rooster_buckets[i]
        avg_s = round(float(np.mean([p["avg_score"] for p in squad])), 2)
        avg_r = round(float(np.mean([p["rounds_played"] for p in squad])), 1)
        total_r = int(np.sum([p["rounds_played"] for p in squad]))
        roosters_out.append({
            "index": i,
            "rooster_id": theme["rooster_id"],
            "name": theme["name"],
            "tagline": theme["tagline"],
            "emblem": theme["emblem"],
            "emblem_url": theme.get("emblem_url", ""),
            "accent_color": theme["accent_color"],
            "secondary_color": theme["secondary_color"],
            "summary": {
                "player_count": len(squad),
                "mean_player_avg_score": avg_s,
                "mean_rounds_played": avg_r,
                "total_historical_appearances": total_r
            },
            "players": squad
        })

    # Also save latest sample to roosters.json for inspection
    roosters_json_path = DATA_DIR / "roosters.json"
    with open(roosters_json_path, "w", encoding="utf-8") as f:
        json.dump(roosters_out, f, ensure_ascii=False, indent=2)

    return roosters_out


if __name__ == "__main__":
    if not (DATA_DIR / "normalized_scouts.parquet").exists():
        df_norm = build_normalized_scouts()
    else:
        df_norm = pd.read_parquet(DATA_DIR / "normalized_scouts.parquet")

    df_career = build_player_career_stats(df_norm)
    run1 = generate_dynamic_roosters(df_career)
    print(f"-> Rebuilt player_career_stats.parquet and roosters.json with local club logos and emblem_urls ({len(run1)} squads).")
