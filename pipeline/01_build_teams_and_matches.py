import json
import urllib.request
import unicodedata
import pandas as pd
from pathlib import Path

DATA_DIR = Path(r"C:\Users\thiag\Documents\CLT\data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

CANONICAL_CLUBS = {
    262: {"name": "Flamengo", "abbr": "FLA", "slug": "flamengo"},
    263: {"name": "Botafogo", "abbr": "BOT", "slug": "botafogo"},
    264: {"name": "Corinthians", "abbr": "COR", "slug": "corinthians"},
    265: {"name": "Bahia", "abbr": "BAH", "slug": "bahia"},
    266: {"name": "Fluminense", "abbr": "FLU", "slug": "fluminense"},
    267: {"name": "Vasco da Gama", "abbr": "VAS", "slug": "vasco-da-gama"},
    268: {"name": "Portuguesa", "abbr": "POR", "slug": "portuguesa"},
    275: {"name": "Palmeiras", "abbr": "PAL", "slug": "palmeiras"},
    276: {"name": "São Paulo", "abbr": "SAO", "slug": "sao-paulo"},
    277: {"name": "Santos", "abbr": "SAN", "slug": "santos"},
    280: {"name": "Red Bull Bragantino", "abbr": "RBB", "slug": "red-bull-bragantino"},
    282: {"name": "Atlético-MG", "abbr": "CAM", "slug": "atletico-mg"},
    283: {"name": "Cruzeiro", "abbr": "CRU", "slug": "cruzeiro"},
    284: {"name": "Grêmio", "abbr": "GRE", "slug": "gremio"},
    285: {"name": "Internacional", "abbr": "INT", "slug": "internacional"},
    286: {"name": "Juventude", "abbr": "JUV", "slug": "juventude"},
    287: {"name": "Vitória", "abbr": "VIT", "slug": "vitoria"},
    288: {"name": "Criciúma", "abbr": "CRI", "slug": "criciuma"},
    289: {"name": "Paraná", "abbr": "PAR", "slug": "parana"},
    290: {"name": "Goiás", "abbr": "GOI", "slug": "goias"},
    292: {"name": "Sport", "abbr": "SPT", "slug": "sport"},
    293: {"name": "Athletico-PR", "abbr": "CAP", "slug": "athletico-pr"},
    294: {"name": "Coritiba", "abbr": "CFC", "slug": "coritiba"},
    303: {"name": "Ponte Preta", "abbr": "PON", "slug": "ponte-preta"},
    314: {"name": "Avaí", "abbr": "AVA", "slug": "avai"},
    315: {"name": "Chapecoense", "abbr": "CHA", "slug": "chapecoense"},
    316: {"name": "Figueirense", "abbr": "FIG", "slug": "figueirense"},
    317: {"name": "Joinville", "abbr": "JOI", "slug": "joinville"},
    327: {"name": "América-MG", "abbr": "AME", "slug": "america-mg"},
    341: {"name": "CSA", "abbr": "CSA", "slug": "csa"},
    344: {"name": "Santa Cruz", "abbr": "STA", "slug": "santa-cruz"},
    354: {"name": "Ceará", "abbr": "CEA", "slug": "ceara"},
    356: {"name": "Fortaleza", "abbr": "FOR", "slug": "fortaleza"},
    373: {"name": "Atlético-GO", "abbr": "ACG", "slug": "atletico-go"},
    1371: {"name": "Cuiabá", "abbr": "CUI", "slug": "cuiaba"},
    2132: {"name": "Amazonas", "abbr": "AMA", "slug": "amazonas"},
    2137: {"name": "Novorizontino", "abbr": "NOV", "slug": "novorizontino"},
    2140: {"name": "Remo", "abbr": "REM", "slug": "remo"},
    2305: {"name": "Mirassol", "abbr": "MIR", "slug": "mirassol"},
}

def clean_team_str(s):
    if not isinstance(s, str):
        return ""
    try:
        if "Ã" in s or "Â" in s:
            s = s.encode("latin-1").decode("utf-8")
    except Exception:
        pass
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.replace("-", " ").strip().lower()
    return " ".join(s.split())

NAME_LOOKUP = {
    "flamengo": 262, "fla": 262,
    "botafogo": 263, "botafogo rj": 263, "bot": 263,
    "corinthians": 264, "cor": 264,
    "bahia": 265, "bah": 265,
    "fluminense": 266, "flu": 266,
    "vasco": 267, "vasco da gama": 267, "vas": 267,
    "portuguesa": 268, "por": 268,
    "palmeiras": 275, "pal": 275,
    "sao paulo": 276, "sao": 276,
    "santos": 277, "san": 277,
    "bragantino": 280, "red bull bragantino": 280, "rbb": 280,
    "atletico mg": 282, "cam": 282,
    "cruzeiro": 283, "cru": 283,
    "gremio": 284, "gre": 284,
    "internacional": 285, "int": 285,
    "juventude": 286, "juv": 286,
    "vitoria": 287, "vit": 287,
    "criciuma": 288, "cri": 288,
    "parana": 289, "par": 289,
    "goias": 290, "goi": 290,
    "sport": 292, "spt": 292, "spo": 292,
    "athletico pr": 293, "atletico pr": 293, "cap": 293,
    "coritiba": 294, "cfc": 294,
    "ponte preta": 303, "pon": 303,
    "avai": 314, "ava": 314,
    "chapecoense": 315, "cha": 315,
    "figueirense": 316, "fig": 316,
    "joinville": 317, "joi": 317,
    "america mg": 327, "ame": 327,
    "csa": 341,
    "santa cruz": 344, "sta": 344, "stc": 344,
    "ceara": 354, "cea": 354,
    "fortaleza": 356, "for": 356,
    "atletico go": 373, "acg": 373,
    "cuiaba": 1371, "cui": 1371,
    "amazonas": 2132, "ama": 2132,
    "novorizontino": 2137, "nov": 2137,
    "remo": 2140, "rem": 2140,
    "mirassol": 2305, "mir": 2305,
}

def get_team_id(team_str):
    cleaned = clean_team_str(team_str)
    return NAME_LOOKUP.get(cleaned, None)

def fetch_cartola_escudos():
    print("Fetching live club escudos from Cartola FC API...")
    url = "https://api.cartola.globo.com/clubes"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"Warning: could not fetch live Cartola API escudos ({e}), using CDN fallback format.")
        return {}

def build_teams():
    print("Building TEAMS.PARQUET with official badge URLs...")
    api_clubes = fetch_cartola_escudos()

    records = []
    for cid, info in sorted(CANONICAL_CLUBS.items()):
        badge_60 = None
        badge_30 = None

        # 1. Match from live Cartola API if available
        str_id = str(cid)
        if str_id in api_clubes:
            escudos = api_clubes[str_id].get("escudos", {})
            badge_60 = escudos.get("60x60")
            badge_30 = escudos.get("30x30")
        else:
            # Match by abbreviation or name in API
            for _, c_info in api_clubes.items():
                if c_info.get("abreviacao", "").upper() == info["abbr"].upper():
                    escudos = c_info.get("escudos", {})
                    badge_60 = escudos.get("60x60")
                    badge_30 = escudos.get("30x30")
                    break

        # 2. Fallback to Globo CDN pattern
        if not badge_60:
            badge_60 = f"https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/{info['abbr']}/60x60.png"
            badge_30 = f"https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/{info['abbr']}/30x30.png"

        records.append({
            "team_id": int(cid),
            "team_name": info["name"],
            "abbreviation": info["abbr"],
            "slug": info["slug"],
            "badge_url": badge_60,
            "badge_small_url": badge_30
        })

    df_teams = pd.DataFrame(records)
    teams_path = DATA_DIR / "teams.parquet"
    df_teams.to_parquet(teams_path, index=False)
    print(f"-> Successfully saved {len(df_teams)} canonical clubs with badge URLs to {teams_path}")
    return df_teams

def build_matches():
    print("\nBuilding MATCHES.PARQUET (All 12 seasons: 2014-2025)...")
    url = "https://raw.githubusercontent.com/williamorim/brasileirao/master/data-raw/csv/matches.csv"
    df_raw = pd.read_csv(url)

    df = df_raw[(df_raw["season"] >= 2014) & (df_raw["season"] <= 2025)].copy().reset_index(drop=True)
    df["round"] = (df.groupby("season").cumcount() // 10) + 1

    def parse_scores(score_str):
        if not isinstance(score_str, str) or "x" not in score_str.lower():
            return None, None
        parts = score_str.lower().split("x")
        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            return None, None

    scores = df["score"].apply(parse_scores)
    df["home_score"] = [s[0] for s in scores]
    df["away_score"] = [s[1] for s in scores]

    df["home_team_id"] = df["home"].apply(get_team_id).astype("int64")
    df["away_team_id"] = df["away"].apply(get_team_id).astype("int64")

    id_to_name = {cid: info["name"] for cid, info in CANONICAL_CLUBS.items()}
    df["home_team"] = df["home_team_id"].map(id_to_name).fillna(df["home"])
    df["away_team"] = df["away_team_id"].map(id_to_name).fillna(df["away"])

    df_matches = df[[
        "id_match", "season", "round", "date",
        "home_team_id", "away_team_id", "home_team", "away_team",
        "home_score", "away_score"
    ]].rename(columns={"id_match": "match_id"})

    matches_path = DATA_DIR / "matches.parquet"
    df_matches.to_parquet(matches_path, index=False)
    print(f"-> Successfully saved {len(df_matches)} matches across 12 seasons to {matches_path}")
    print(f"-> Null home_team_id: {df_matches['home_team_id'].isna().sum()} | Null away_team_id: {df_matches['away_team_id'].isna().sum()}")
    return df_matches

if __name__ == "__main__":
    build_teams()
    build_matches()
