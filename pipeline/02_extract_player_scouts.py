import os
import sys
import json
import unicodedata
import urllib.request
import re
from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path(r"C:\Users\thiag\Documents\CLT\data")
SCOUTS_DIR = DATA_DIR / "player_scouts"
SCOUTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_RAW = "https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/01_raw"

POSITION_MAP = {
    1: "Goleiro",
    2: "Lateral",
    3: "Zagueiro",
    4: "Meia",
    5: "Atacante",
    6: "Técnico"
}

ALL_POSSIBLE_SCOUTS = [
    "G", "A", "DS", "RB", "SG", "FS", "FF", "FD", "FT",
    "DE", "DD", "DP", "GS", "FC", "GC", "CA", "CV", "PC", "PS", "PP", "PE", "I", "V"
]

CLUB_NAME_TO_ID = {
    "flamengo": 262, "fla": 262,
    "botafogo": 263, "bot": 263,
    "corinthians": 264,
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
    "goias": 290, "goi": 290,
    "sport": 292, "spt": 292, "spo": 292,
    "athletico pr": 293, "atletico pr": 293, "cap": 293,
    "coritiba": 294, "cfc": 294,
    "ponte preta": 303, "pon": 303,
    "parana": 289, "par": 289,
    "avai": 314, "ava": 314,
    "chapecoense": 315, "cha": 315,
    "figueirense": 316, "fig": 316,
    "joinville": 317, "joi": 317,
    "america mg": 327, "ame": 327,
    "csa": 341,
    "santa cruz": 344, "sta": 344,
    "ceara": 354, "cea": 354,
    "fortaleza": 356, "for": 356,
    "atletico go": 373, "acg": 373,
    "cuiaba": 1371, "cui": 1371,
    "mirassol": 2305, "mir": 2305,
}

def clean_text(s):
    if not isinstance(s, str) or not s:
        return ""
    s = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", s)
    for _ in range(2):
        if "Ã" in s or "Â" in s:
            try:
                s = s.encode("latin-1").decode("utf-8")
            except Exception:
                break
    return s.strip()

def clean_club_key(s):
    if not isinstance(s, str) or not s:
        return ""
    s = clean_text(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.replace("-", " ").replace(".", " ").strip().lower()
    return " ".join(s.split())

def resolve_team_ids(df, id_col, team_col, full_club_col=None, fallback_pid_to_club=None):
    """Resolves numeric or string club identifiers to canonical integer team_ids."""
    num_tid = pd.to_numeric(df[team_col], errors="coerce").fillna(0).astype(int)
    if (num_tid == 0).any():
        # Try mapping string club names/abbreviations
        if full_club_col and full_club_col in df.columns:
            full_mapped = df[full_club_col].apply(lambda x: CLUB_NAME_TO_ID.get(clean_club_key(x), 0))
            abbr_mapped = df[team_col].apply(
                lambda x: CLUB_NAME_TO_ID.get(clean_club_key(x), 0)
                if str(x).strip().upper() not in ["ATL", "COR"] else 0
            )
            str_tid = np.where(abbr_mapped != 0, abbr_mapped, full_mapped)
            num_tid = np.where(num_tid != 0, num_tid, str_tid)
        else:
            str_tid = df[team_col].apply(lambda x: CLUB_NAME_TO_ID.get(clean_club_key(x), 0))
            num_tid = np.where(num_tid != 0, num_tid, str_tid)

    s_tid = pd.Series(num_tid, index=df.index)
    if fallback_pid_to_club:
        mask0 = s_tid == 0
        s_tid.loc[mask0] = df.loc[mask0, id_col].map(fallback_pid_to_club).fillna(0).astype(int)

    # Replace sentinel 0 or 1 ('Sem Clube') via per-player seasonal ffill/bfill
    tmp = pd.DataFrame({"pid": df[id_col].values, "tid": s_tid.values}, index=df.index)
    tmp["tid"] = tmp.groupby("pid")["tid"].transform(
        lambda s: s.replace({0: np.nan, 1: np.nan}).ffill().bfill()
    ).fillna(0).astype(int)
    return tmp["tid"]

def normalize_position(val):
    if pd.isna(val):
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        pass
    val_str = str(val).lower().strip()
    mapping = {
        "gol": 1, "goleiro": 1, "1": 1,
        "lat": 2, "lateral": 2, "2": 2,
        "zag": 3, "zagueiro": 3, "3": 3,
        "mei": 4, "meia": 4, "4": 4,
        "ata": 5, "atacante": 5, "5": 5,
        "tec": 6, "tecnico": 6, "técnico": 6, "6": 6
    }
    return mapping.get(val_str, 0)

def difference_scouts(df, id_col, round_col, scout_cols):
    """Computes round delta for cumulative seasons."""
    for c in scout_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    df = df.sort_values([id_col, round_col]).reset_index(drop=True)
    deltas = df.groupby(id_col)[scout_cols].diff()
    deltas = deltas.fillna(df[scout_cols])
    deltas = deltas.clip(lower=0.0)
    df[scout_cols] = deltas
    return df

def process_legacy_season(year: int, is_cumulative: bool):
    print(f"\nProcessing Season {year} (Legacy format, is_cumulative={is_cumulative})...")
    url = f"{BASE_RAW}/{year}/{year}_scouts_raw.csv"
    df = pd.read_csv(url, encoding="latin-1", low_memory=False)

    player_meta = []
    pid_to_club = {}

    if year in [2014, 2015, 2016]:
        id_col = "AtletaID"
        round_col = "Rodada"
        team_col = "ClubeID"
        pts_col = "Pontos"
        price_col = "Preco"
        var_col = "PrecoVariacao"
        full_club_col = None

        jog_url = f"{BASE_RAW}/{year}/{year}_jogadores.csv"
        df_jog = pd.read_csv(jog_url, encoding="latin-1")
        id_to_pos = {int(r["ID"]): normalize_position(r.get("PosicaoID")) for _, r in df_jog.iterrows()}
        pid_to_club = {int(r["ID"]): int(r["ClubeID"]) for _, r in df_jog.dropna(subset=["ID", "ClubeID"]).iterrows()}

        for _, row in df_jog.iterrows():
            pos_id = normalize_position(row.get("PosicaoID", 0))
            player_meta.append({
                "player_id": int(row["ID"]),
                "name": clean_text(str(row.get("Nome", ""))),
                "nickname": clean_text(str(row.get("Apelido", ""))),
                "slug": "",
                "position_id": pos_id,
                "season": year
            })

        df["position_id"] = df[id_col].map(id_to_pos).fillna(0).astype(int)

        if "Participou" in df.columns:
            played_series = (df["Participou"] == 1)
        else:
            df_sorted = df.sort_values([id_col, round_col])
            diff_games = df_sorted.groupby(id_col)["Jogos"].diff().fillna(df_sorted["Jogos"])
            played_series = (diff_games > 0) | (df[pts_col] != 0)
    else:  # 2017
        id_col = "atletas.atleta_id"
        round_col = "Rodada"
        team_col = "atletas.clube_id"
        full_club_col = "atletas.clube.id.full.name"
        pos_col = "atletas.posicao_id"
        pts_col = "atletas.pontos_num"
        price_col = "atletas.preco_num"
        var_col = "atletas.variacao_num"
        df["position_id"] = df[pos_col].apply(normalize_position).astype(int)

        df_sorted = df.sort_values([id_col, round_col])
        diff_games = df_sorted.groupby(id_col)["atletas.jogos_num"].diff().fillna(df_sorted["atletas.jogos_num"])
        played_series = (diff_games > 0) | (df[pts_col] != 0)

        for _, row in df[[id_col, "atletas.nome", "atletas.apelido", pos_col]].drop_duplicates(subset=[id_col]).iterrows():
            pos_id = normalize_position(row.get(pos_col, 0))
            player_meta.append({
                "player_id": int(row[id_col]),
                "name": clean_text(str(row.get("atletas.nome", ""))),
                "nickname": clean_text(str(row.get("atletas.apelido", ""))),
                "slug": "",
                "position_id": pos_id,
                "season": year
            })

    active_scouts = [c for c in ALL_POSSIBLE_SCOUTS if c in df.columns]

    df = df[df[round_col] > 0].copy()

    if is_cumulative:
        df = difference_scouts(df, id_col, round_col, active_scouts)

    df_out = pd.DataFrame()
    df_out["player_id"] = df[id_col].astype(int)
    df_out["season"] = year
    df_out["round"] = df[round_col].astype(int)
    df_out["team_id"] = resolve_team_ids(df, id_col, team_col, full_club_col, pid_to_club)
    df_out["position_id"] = df["position_id"].astype(int)
    df_out["played"] = played_series.astype(bool)
    df_out["points"] = pd.to_numeric(df[pts_col], errors="coerce").fillna(0.0)
    df_out["price"] = pd.to_numeric(df[price_col], errors="coerce").fillna(0.0)
    df_out["price_variation"] = pd.to_numeric(df[var_col], errors="coerce").fillna(0.0)

    for s in active_scouts:
        df_out[s] = df[s].astype(float)

    season_dir = SCOUTS_DIR / f"season={year}"
    season_dir.mkdir(parents=True, exist_ok=True)
    df_out.to_parquet(season_dir / "data.parquet", index=False)
    print(f"-> Saved Season {year}: {len(df_out)} rows ({df_out['played'].sum()} active appearances) to {season_dir / 'data.parquet'}")

    return player_meta

def process_round_csv_season(year: int):
    print(f"\nProcessing Season {year} (Round CSVs, is_cumulative=True)...")
    dfs = []
    player_meta = []

    for r in range(1, 39):
        url = f"{BASE_RAW}/{year}/rodada-{r}.csv"
        try:
            r_df = pd.read_csv(url, encoding="latin-1", low_memory=False)
            r_df["actual_round"] = r
            dfs.append(r_df)
        except Exception as e:
            print(f"Warning: Missing round {r} in {year}: {e}")

    if not dfs:
        print(f"Error: No round CSVs found for {year}")
        return []

    df = pd.concat(dfs, ignore_index=True)

    id_col = "atletas.atleta_id" if "atletas.atleta_id" in df.columns else "atleta_id"
    round_col = "actual_round"
    team_col = "atletas.clube_id" if "atletas.clube_id" in df.columns else "clube_id"
    full_club_col = "atletas.clube.id.full.name" if "atletas.clube.id.full.name" in df.columns else None
    pos_col = "atletas.posicao_id" if "atletas.posicao_id" in df.columns else "posicao_id"
    pts_col = "atletas.pontos_num" if "atletas.pontos_num" in df.columns else "pontos_num"
    price_col = "atletas.preco_num" if "atletas.preco_num" in df.columns else "preco_num"
    var_col = "atletas.variacao_num" if "atletas.variacao_num" in df.columns else "variacao_num"
    games_col = "atletas.jogos_num" if "atletas.jogos_num" in df.columns else "jogos_num"
    played_col = "atletas.entrou_em_campo" if "atletas.entrou_em_campo" in df.columns else None

    active_scouts = [c for c in ALL_POSSIBLE_SCOUTS if c in df.columns]

    if played_col and played_col in df.columns:
        played_mask = df[played_col].fillna(False).astype(bool)
    elif games_col and games_col in df.columns:
        df_sort = df.sort_values([id_col, round_col])
        diff_g = df_sort.groupby(id_col)[games_col].diff().fillna(df_sort[games_col])
        played_mask = (diff_g > 0) | (df[pts_col] != 0)
    else:
        played_mask = (df[pts_col] != 0)

    df = difference_scouts(df, id_col, round_col, active_scouts)

    df_out = pd.DataFrame()
    df_out["player_id"] = df[id_col].astype(int)
    df_out["season"] = year
    df_out["round"] = df[round_col].astype(int)
    df_out["team_id"] = resolve_team_ids(df, id_col, team_col, full_club_col)
    df_out["position_id"] = df[pos_col].apply(normalize_position).astype(int)
    df_out["played"] = played_mask.astype(bool)
    df_out["points"] = pd.to_numeric(df[pts_col], errors="coerce").fillna(0.0)
    df_out["price"] = pd.to_numeric(df[price_col], errors="coerce").fillna(0.0)
    df_out["price_variation"] = pd.to_numeric(df[var_col], errors="coerce").fillna(0.0)

    for s in active_scouts:
        df_out[s] = df[s].astype(float)

    name_col = "atletas.nome" if "atletas.nome" in df.columns else "nome"
    nick_col = "atletas.apelido" if "atletas.apelido" in df.columns else "apelido"
    slug_col = "atletas.slug" if "atletas.slug" in df.columns else "slug"

    meta_cols = [id_col, pos_col]
    if name_col in df.columns: meta_cols.append(name_col)
    if nick_col in df.columns: meta_cols.append(nick_col)
    if slug_col in df.columns: meta_cols.append(slug_col)

    for _, row in df[meta_cols].drop_duplicates(subset=[id_col]).iterrows():
        pos_id = normalize_position(row.get(pos_col, 0))
        player_meta.append({
            "player_id": int(row[id_col]),
            "name": clean_text(str(row.get(name_col, ""))),
            "nickname": clean_text(str(row.get(nick_col, ""))),
            "slug": clean_text(str(row.get(slug_col, ""))),
            "position_id": pos_id,
            "season": year
        })

    season_dir = SCOUTS_DIR / f"season={year}"
    season_dir.mkdir(parents=True, exist_ok=True)
    df_out.to_parquet(season_dir / "data.parquet", index=False)
    print(f"-> Saved Season {year}: {len(df_out)} rows ({df_out['played'].sum()} active appearances) to {season_dir / 'data.parquet'}")

    return player_meta

def process_2021_json():
    year = 2021
    print(f"\nProcessing Season {year} (JSON Mercado_X.txt, is_cumulative=True)...")
    records = []
    player_meta = []

    for r in range(1, 39):
        url = f"{BASE_RAW}/2021/Mercado_{r}.txt"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = json.loads(urllib.request.urlopen(req).read().decode("latin-1"))
            for a in data.get("atletas", []):
                aid = a.get("atleta_id")
                if not aid:
                    continue
                row = {
                    "atleta_id": aid,
                    "round": r,
                    "team_id": a.get("clube_id", 0),
                    "posicao_id": a.get("posicao_id", 0),
                    "pontos_num": a.get("pontos_num", 0.0),
                    "preco_num": a.get("preco_num", 0.0),
                    "variacao_num": a.get("variacao_num", 0.0),
                    "entrou_em_campo": a.get("entrou_em_campo", False),
                    "jogos_num": a.get("jogos_num", 0)
                }
                scout = a.get("scout") or {}
                for s in ALL_POSSIBLE_SCOUTS:
                    row[s] = scout.get(s, 0.0)
                records.append(row)

                pos_id = normalize_position(a.get("posicao_id", 0))
                player_meta.append({
                    "player_id": int(aid),
                    "name": clean_text(a.get("nome", "")),
                    "nickname": clean_text(a.get("apelido", "")),
                    "slug": clean_text(a.get("slug", "")),
                    "position_id": pos_id,
                    "season": year
                })
        except Exception as e:
            print(f"Warning: Round {r} in 2021 failed: {e}")

    df = pd.DataFrame(records)
    active_scouts = [c for c in ALL_POSSIBLE_SCOUTS if c in df.columns]

    df = difference_scouts(df, "atleta_id", "round", active_scouts)

    df_out = pd.DataFrame()
    df_out["player_id"] = df["atleta_id"].astype(int)
    df_out["season"] = year
    df_out["round"] = df["round"].astype(int)
    df_out["team_id"] = resolve_team_ids(df, "atleta_id", "team_id")
    df_out["position_id"] = df["posicao_id"].apply(normalize_position).astype(int)
    df_out["played"] = df["entrou_em_campo"].fillna(False).astype(bool)
    df_out["points"] = df["pontos_num"].fillna(0.0).astype(float)
    df_out["price"] = df["preco_num"].fillna(0.0).astype(float)
    df_out["price_variation"] = df["variacao_num"].fillna(0.0).astype(float)

    for s in active_scouts:
        df_out[s] = df[s].astype(float)

    season_dir = SCOUTS_DIR / f"season={year}"
    season_dir.mkdir(parents=True, exist_ok=True)
    df_out.to_parquet(season_dir / "data.parquet", index=False)
    print(f"-> Saved Season {year}: {len(df_out)} rows to {season_dir / 'data.parquet'}")

    return player_meta

if __name__ == "__main__":
    process_legacy_season(2014, is_cumulative=False)
    process_legacy_season(2015, is_cumulative=True)
    process_legacy_season(2016, is_cumulative=False)
    process_legacy_season(2017, is_cumulative=True)
    for yr in [2018, 2019, 2020]:
        process_round_csv_season(yr)
    process_2021_json()
    for yr in [2022, 2023, 2024, 2025]:
        process_round_csv_season(yr)
    print("\n=== CLT DATA ENGINE EXTRACTION COMPLETE (2014-2025) ===")
