import re
from pathlib import Path
import pandas as pd

DATA_DIR = Path(r"C:\Users\thiag\Documents\CLT\data")
SCOUTS_DIR = DATA_DIR / "player_scouts"

# 1. Fix 'played' column across all seasons to ensure 100% consistency
scout_cols_list = [
    "G", "A", "DS", "RB", "SG", "FS", "FF", "FD", "FT",
    "DE", "DD", "DP", "GS", "FC", "GC", "CA", "CV", "PC", "PS", "PP", "PE", "I", "V"
]

print("Standardizing 'played' flag across all seasons...")
for p in sorted(SCOUTS_DIR.glob("season=*")):
    parquet_file = p / "data.parquet"
    df = pd.read_parquet(parquet_file)
    active_scouts = [c for c in scout_cols_list if c in df.columns]
    
    # Universal active player definition: points != 0 OR any scout action recorded
    has_scout = (df[active_scouts].sum(axis=1) > 0)
    has_points = (df["points"] != 0.0)
    is_active = (has_points | has_scout)
    
    df["played"] = is_active.astype(bool)
    df.to_parquet(parquet_file, index=False)
    season_num = p.name.split("=")[1]
    print(f"Season {season_num}: {len(df):,} total rows | {is_active.sum():,} active pitch appearances")

# 2. Clean Global Player Dictionary Strings
print("\nSanitizing strings in PLAYERS.PARQUET...")
df_players = pd.read_parquet(DATA_DIR / "players.parquet")

def sanitize_string(text):
    if not isinstance(text, str):
        return ""
    # Remove control characters and non-printable bytes
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # Fix common mojibake
    cleaned = cleaned.replace("Ã¡", "á").replace("Ã©", "é").replace("Ã­", "í").replace("Ã³", "ó").replace("Ãº", "ú")
    cleaned = cleaned.replace("Ã£", "ã").replace("Ãµ", "õ").replace("Ã¢", "â").replace("Ãª", "ê").replace("Ã§", "ç")
    cleaned = cleaned.replace("Ã", "Á").replace("Ã", "É").replace("Ã", "Í").replace("Ã", "Ó").replace("Ã", "Ú")
    cleaned = cleaned.replace("Ã", "Ã").replace("Ã", "Õ").replace("Ã", "Â").replace("Ã", "Ê").replace("Ã", "Ç")
    return cleaned.strip()

df_players["canonical_name"] = df_players["canonical_name"].apply(sanitize_string)
df_players["canonical_nickname"] = df_players["canonical_nickname"].apply(sanitize_string)
df_players["slug"] = df_players["slug"].apply(sanitize_string)

# Clean aliases
def clean_alias_list(aliases):
    if not isinstance(aliases, (list, tuple, set)):
        return []
    cleaned_set = set()
    for a in aliases:
        c = sanitize_string(str(a))
        if len(c) > 1:
            cleaned_set.add(c)
    return sorted(list(cleaned_set))

df_players["known_aliases"] = df_players["known_aliases"].apply(clean_alias_list)

df_players.to_parquet(DATA_DIR / "players.parquet", index=False)
print(f"Successfully sanitized {len(df_players):,} players in PLAYERS.PARQUET")
