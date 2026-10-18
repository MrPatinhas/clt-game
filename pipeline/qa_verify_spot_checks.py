import sys
from pathlib import Path
import pandas as pd

# Set utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = Path(r"C:\Users\thiag\Documents\CLT\data")

# 1. Teams
df_teams = pd.read_parquet(DATA_DIR / "teams.parquet")
print("=== 1. TEAMS TABLE (teams.parquet) ===")
print(f"Total teams: {len(df_teams)}")
print(df_teams.head(5).to_string())

# 2. Matches
df_matches = pd.read_parquet(DATA_DIR / "matches.parquet")
print("\n=== 2. MATCHES TABLE (matches.parquet) ===")
print(f"Total matches: {len(df_matches)} across seasons {df_matches['season'].min()} - {df_matches['season'].max()}")
print("Matches per season:", df_matches["season"].value_counts().sort_index().to_dict())

# 3. Players
df_players = pd.read_parquet(DATA_DIR / "players.parquet")
print("\n=== 3. GLOBAL PLAYER DICTIONARY (players.parquet) ===")
print(f"Total unique players: {len(df_players):,}")
print("Position breakdown:")
print(df_players["position_name"].value_counts().to_dict())
sample_cols = ["player_id", "canonical_name", "canonical_nickname", "position_name", "first_season", "last_season"]
print(df_players[sample_cols].head(8).to_string())

# 4. Player Scouts Summary
print("\n=== 4. PLAYER SCOUTS BY SEASON (player_scouts/) ===")
scouts_dir = DATA_DIR / "player_scouts"
seasons = sorted([int(p.name.split("=")[1]) for p in scouts_dir.glob("season=*")])
total_rows = 0
total_active = 0
for s in seasons:
    df_s = pd.read_parquet(scouts_dir / f"season={s}" / "data.parquet")
    rows = len(df_s)
    active = int(df_s["played"].sum())
    total_rows += rows
    total_active += active
    scouts_in_season = [c for c in ["G", "A", "DS", "RB", "DE", "DD", "PE"] if c in df_s.columns]
    print(f"Season {s}: {rows:>6,} rows | {active:>5,} active matches | scouts: {scouts_in_season}")

print(f"\nTOTAL ALL SEASONS: {total_rows:,} records ({total_active:,} active pitch appearances)")

# 5. Spot check: Fábio (ID: 37656) career in CLT database
print("\n=== 5. SPOT CHECK: FÁBIO (ID: 37656) ===")
fabio_meta = df_players[df_players["player_id"] == 37656]
print("Player Dictionary Record:")
print(fabio_meta.to_string())

fabio_seasons = []
for s in seasons:
    df_s = pd.read_parquet(scouts_dir / f"season={s}" / "data.parquet")
    f_s = df_s[(df_s["player_id"] == 37656) & (df_s["played"] == True)]
    if len(f_s) > 0:
        saves_col = "DE" if "DE" in f_s.columns else ("DD" if "DD" in f_s.columns else None)
        total_saves = f_s[saves_col].sum() if saves_col else 0
        total_pts = f_s["points"].sum()
        fabio_seasons.append({
            "season": s,
            "team_id": f_s["team_id"].iloc[0],
            "matches_played": len(f_s),
            "total_points": round(total_pts, 1),
            "saves_metric": saves_col,
            "total_saves": int(total_saves)
        })
print("\nFábio Career Breakdown across CLT Dataset:")
print(pd.DataFrame(fabio_seasons).to_string())

# 6. Spot check: Hulk (ID: 39148) career in CLT database
print("\n=== 6. SPOT CHECK: HULK (ID: 39148) ===")
hulk_meta = df_players[df_players["player_id"] == 39148]
print("Player Dictionary Record:")
print(hulk_meta.to_string())

hulk_seasons = []
for s in seasons:
    df_s = pd.read_parquet(scouts_dir / f"season={s}" / "data.parquet")
    h_s = df_s[(df_s["player_id"] == 39148) & (df_s["played"] == True)]
    if len(h_s) > 0:
        g = h_s["G"].sum() if "G" in h_s.columns else 0
        a = h_s["A"].sum() if "A" in h_s.columns else 0
        pts = h_s["points"].sum()
        hulk_seasons.append({
            "season": s,
            "team_id": h_s["team_id"].iloc[0],
            "matches_played": len(h_s),
            "total_points": round(pts, 1),
            "goals": int(g),
            "assists": int(a)
        })
print("\nHulk Career Breakdown across CLT Dataset:")
print(pd.DataFrame(hulk_seasons).to_string())
