import sys
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\Users\thiag\Documents\CLT\data")

teams = pd.read_parquet(D / "teams.parquet")
matches = pd.read_parquet(D / "matches.parquet")
players = pd.read_parquet(D / "players.parquet")
scouts = pd.concat(
    [pd.read_parquet(p / "data.parquet") for p in sorted((D / "player_scouts").glob("season=*"))],
    ignore_index=True,
)

print("=== MATCHES ===")
print("null home_team_id:", matches["home_team_id"].isna().sum(), "/", len(matches))
print("null away_team_id:", matches["away_team_id"].isna().sum())
print("null scores:", matches["home_score"].isna().sum())
print("sample unmapped home names:", matches.loc[matches["home_team_id"].isna(), "home_team"].unique()[:10].tolist())
per_round = matches.groupby(["season", "round"]).size()
print("rounds with != 10 matches:", (per_round != 10).sum())
dup_team_round = pd.concat([
    matches[["season", "round", "home_team_id"]].rename(columns={"home_team_id": "t"}),
    matches[["season", "round", "away_team_id"]].rename(columns={"away_team_id": "t"}),
]).dropna().duplicated().sum()
print("team appearing twice in same (season, round):", dup_team_round)

print("\n=== TEAMS ===")
print("duplicate team_name:", teams[teams["team_name"].duplicated(keep=False)][["team_id", "team_name"]].values.tolist())
scout_teams = set(scouts["team_id"].unique())
missing = sorted(scout_teams - set(teams["team_id"]))
print("team_ids in scouts but NOT in teams.parquet:", missing)
print("scout rows with team_id == 0:", int((scouts["team_id"] == 0).sum()))
print("team_id==0 by season:", scouts[scouts["team_id"] == 0].groupby("season").size().to_dict())

print("\n=== PLAYERS (FK) ===")
orphans = set(scouts["player_id"]) - set(players["player_id"])
print("player_ids in scouts:", scouts["player_id"].nunique(), "| in players.parquet:", len(players))
print("orphan player_ids (scouts without dictionary entry):", len(orphans))
orph_active = scouts[scouts["player_id"].isin(orphans) & scouts["played"]]
print("active appearances belonging to orphans:", len(orph_active))
moj = players["canonical_name"].str.contains("Ã|Â|�", regex=True, na=False).sum()
print("canonical_name with mojibake markers (Ã/Â/�):", int(moj))
print("sample:", players.loc[players["canonical_name"].str.contains("Ã|Â|�", regex=True, na=False), "canonical_name"].head(5).tolist())

print("\n=== SCOUTS ===")
print("duplicate (player_id, season, round):", int(scouts.duplicated(["player_id", "season", "round"]).sum()))
print("rounds per season:", scouts.groupby("season")["round"].agg(["min", "max"]).to_dict("index"))
print("active rows of position 6 (Técnico):", int(((scouts["position_id"] == 6) & scouts["played"]).sum()))

# round-alignment hint: share of round-1 rows with non-zero points per season
r1 = scouts[scouts["round"] == 1].groupby("season")["points"].apply(lambda s: (s != 0).mean()).round(2)
print("share of round-1 rows with non-zero points (0.0 => file may be pre-round snapshot):", r1.to_dict())
