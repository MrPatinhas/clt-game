import re
import sys
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
DATA_DIR = Path(r"C:\Users\thiag\Documents\CLT\data")
SCOUTS_DIR = DATA_DIR / "player_scouts"
BASE_RAW = "https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/01_raw"

DEFAULT_SILHOUETTE_URL = "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/silhuetas/OUT/220x220.png"

POSITION_MAP = {
    1: "Goleiro",
    2: "Lateral",
    3: "Zagueiro",
    4: "Meia",
    5: "Atacante",
    6: "Técnico"
}

def clean_string(s):
    if not isinstance(s, str) or not s or s == "nan":
        return ""
    # FIRST: Iteratively repair UTF-8 bytes decoded as latin-1 (before stripping \x80-\x9f!)
    for _ in range(3):
        if "Ã" in s or "Â" in s:
            try:
                s = s.encode("latin-1").decode("utf-8")
            except Exception:
                break
    rep = {
        "Ã¡": "á", "Ã©": "é", "Ã­": "í", "Ã\xad": "í", "Ã³": "ó", "Ãº": "ú",
        "Ã£": "ã", "Ãµ": "õ", "Ã¢": "â", "Ãª": "ê", "Ã§": "ç",
        "Ã\x81": "Á", "Ã‰": "É", "Ã\x89": "É", "Ã\x8d": "Í", "Ã“": "Ó", "Ã\x93": "Ó", "Ãš": "Ú", "Ã\x9a": "Ú",
        "Ã\x91": "Ñ", "Ã±": "ñ", "Ã¼": "ü", "Ã\x80": "À", "Ã ": "à",
        "Ãƒ": "Ã", "Ã•": "Õ", "Ã\x95": "Õ", "Ã‚": "Â", "ÃŠ": "Ê", "Ã\x8a": "Ê", "Ã‡": "Ç", "Ã\x87": "Ç",
        "Âº": "º", "Âª": "ª", "Â´": "'", "Â": ""
    }
    for _ in range(2):
        for k, v in rep.items():
            s = s.replace(k, v)
    s = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", s)
    s = s.replace("Saúl Ãíguez", "Saúl Ñíguez")
    s = re.sub(r"\bÃ([a-z])", lambda m: "Í" + m.group(1), s)
    return s.strip()

def format_photo_url(url_str):
    if not isinstance(url_str, str) or not url_str or url_str == "nan":
        return ""
    url_str = url_str.strip()
    if "FORMATO" in url_str:
        return url_str.replace("FORMATO", "220x220")
    return url_str

def compute_greedy_round_cover(scouts_df):
    """Finds the minimal set of rounds per season that covers 100% of player_ids."""
    cover = {}
    for s, grp in scouts_df.groupby("season"):
        rem = set(grp["player_id"])
        by_r = {int(r): set(r_grp["player_id"]) for r, r_grp in grp.groupby("round")}
        rounds_needed = []
        while rem:
            best_r = max(by_r, key=lambda r: len(by_r[r] & rem))
            rounds_needed.append(best_r)
            rem -= by_r[best_r]
        cover[int(s)] = rounds_needed
    return cover

def fetch_round_meta(args):
    y, r = args
    recs = []
    try:
        if y == 2021:
            url = f"{BASE_RAW}/2021/Mercado_{r}.txt"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urllib.request.urlopen(req).read().decode("latin-1"))
            for a in data.get("atletas", []):
                aid = a.get("atleta_id")
                if aid:
                    raw_photo = format_photo_url(a.get("foto", ""))
                    recs.append({
                        "player_id": int(aid),
                        "name": clean_string(str(a.get("nome", ""))),
                        "nickname": clean_string(str(a.get("apelido", ""))),
                        "slug": clean_string(str(a.get("slug", ""))),
                        "position_id": int(a.get("posicao_id", 0)),
                        "photo_url": raw_photo,
                        "season": y
                    })
        else:
            url = f"{BASE_RAW}/{y}/rodada-{r}.csv"
            df = pd.read_csv(url, encoding="latin-1", low_memory=False)
            id_col = "atletas.atleta_id" if "atletas.atleta_id" in df.columns else "atleta_id"
            name_col = "atletas.nome" if "atletas.nome" in df.columns else "nome"
            nick_col = "atletas.apelido" if "atletas.apelido" in df.columns else "apelido"
            slug_col = "atletas.slug" if "atletas.slug" in df.columns else "slug"
            pos_col = "atletas.posicao_id" if "atletas.posicao_id" in df.columns else "posicao_id"
            photo_col = "atletas.foto" if "atletas.foto" in df.columns else ("foto" if "foto" in df.columns else None)
            pos_map = {"gol": 1, "lat": 2, "zag": 3, "mei": 4, "ata": 5, "tec": 6}

            cols = [c for c in [id_col, name_col, nick_col, slug_col, pos_col, photo_col] if c and c in df.columns]
            for _, row in df[cols].drop_duplicates(subset=[id_col]).iterrows():
                aid = int(row[id_col])
                raw_pos = str(row.get(pos_col, "0")).strip().lower()
                pos = int(raw_pos) if raw_pos.isdigit() else pos_map.get(raw_pos, 0)
                raw_photo = format_photo_url(row.get(photo_col, "")) if photo_col else ""
                recs.append({
                    "player_id": aid,
                    "name": clean_string(str(row.get(name_col, ""))) if name_col in cols else "",
                    "nickname": clean_string(str(row.get(nick_col, ""))) if nick_col in cols else "",
                    "slug": clean_string(str(row.get(slug_col, ""))) if slug_col in cols else "",
                    "position_id": pos,
                    "photo_url": raw_photo,
                    "season": y
                })
    except Exception as e:
        print(f"Error ({y}, round {r}): {e}")
    return recs

def main():
    print("Loading player_scouts to compute exact player coverage & career intervals...")
    scouts = pd.concat(
        [pd.read_parquet(p / "data.parquet") for p in sorted(SCOUTS_DIR.glob("season=*"))],
        ignore_index=True
    )
    cover = compute_greedy_round_cover(scouts)

    records = []

    # 1. 2014-2016 from YYYY_jogadores.csv (no photo column in historical dump)
    for y in [2014, 2015, 2016]:
        url = f"{BASE_RAW}/{y}/{y}_jogadores.csv"
        df = pd.read_csv(url, encoding="latin-1")
        for _, r in df.iterrows():
            records.append({
                "player_id": int(r["ID"]),
                "name": clean_string(str(r.get("Nome", ""))),
                "nickname": clean_string(str(r.get("Apelido", ""))),
                "slug": "",
                "position_id": int(r.get("PosicaoID", 0)),
                "photo_url": "",
                "season": y
            })

    # 2. 2017 from 2017_scouts_raw.csv (contains atletas.foto)
    url17 = f"{BASE_RAW}/2017/2017_scouts_raw.csv"
    df17 = pd.read_csv(url17, encoding="latin-1", low_memory=False)
    pos_map = {"gol": 1, "lat": 2, "zag": 3, "mei": 4, "ata": 5, "tec": 6}
    cols17 = ["atletas.atleta_id", "atletas.nome", "atletas.apelido", "atletas.posicao_id"]
    if "atletas.foto" in df17.columns:
        cols17.append("atletas.foto")
    for _, r in df17[cols17].drop_duplicates(subset=["atletas.atleta_id"]).iterrows():
        pos = pos_map.get(str(r["atletas.posicao_id"]).lower().strip(), 0)
        raw_photo = format_photo_url(r.get("atletas.foto", "")) if "atletas.foto" in cols17 else ""
        records.append({
            "player_id": int(r["atletas.atleta_id"]),
            "name": clean_string(str(r.get("atletas.nome", ""))),
            "nickname": clean_string(str(r.get("atletas.apelido", ""))),
            "slug": "",
            "position_id": pos,
            "photo_url": raw_photo,
            "season": 2017
        })

    # 3. 2018-2025 covering 100% of unique player_ids via parallel fetch
    tasks = []
    for y in range(2018, 2026):
        for r in cover.get(y, [1, 10, 38]):
            tasks.append((y, r))

    print(f"Fetching {len(tasks)} round snapshots in parallel to harvest names and photo URLs...")
    with ThreadPoolExecutor(max_workers=16) as ex:
        for batch in ex.map(fetch_round_meta, tasks):
            records.extend(batch)

    df_all = pd.DataFrame(records)
    print(f"Total metadata records collected: {len(df_all):,}")

    # Compute exact first_season, last_season, and fallback position_id directly from player_scouts
    scout_stats = scouts.groupby("player_id").agg(
        first_season=("season", "min"),
        last_season=("season", "max"),
        last_pos=("position_id", "last")
    ).to_dict("index")

    meta_by_pid = {pid: grp for pid, grp in df_all.groupby("player_id")}
    all_pids = sorted(set(scouts["player_id"]).union(set(df_all["player_id"])))

    players = []
    real_photo_count = 0
    silhouette_count = 0

    for pid in all_pids:
        s_info = scout_stats.get(pid)
        if pid in meta_by_pid:
            grp = meta_by_pid[pid]
            sorted_grp = grp.sort_values("season", ascending=False)
            names = [n for n in sorted_grp["name"].tolist() if len(n) > 2]
            nicks = [n for n in sorted_grp["nickname"].tolist() if len(n) > 1]
            slugs = [s for s in sorted_grp["slug"].tolist() if len(s) > 1]

            canonical_name = names[0] if names else (nicks[0] if nicks else f"Player {pid}")
            canonical_nick = nicks[0] if nicks else canonical_name
            canonical_slug = slugs[0] if slugs else canonical_nick.lower().replace(" ", "-")

            aliases = sorted(set(n for n in names + nicks if len(n) > 1))
            pos_id = int(sorted_grp["position_id"].iloc[0])
            if pos_id == 0 and s_info:
                pos_id = int(s_info["last_pos"])
            first_s = int(s_info["first_season"]) if s_info else int(grp["season"].min())
            last_s = int(s_info["last_season"]) if s_info else int(grp["season"].max())

            # Photo resolution: look for valid http links
            raw_photos = [p for p in sorted_grp["photo_url"].dropna().tolist() if len(p) > 10 and p.startswith("http")]
            # Filter real photos (not silhouettes)
            real_photos = [p for p in raw_photos if "silhueta" not in p.lower() and "silhouette" not in p.lower()]
            if real_photos:
                final_photo = real_photos[0]
                is_silh = False
                real_photo_count += 1
            elif raw_photos:
                final_photo = raw_photos[0]
                is_silh = True
                silhouette_count += 1
            else:
                final_photo = DEFAULT_SILHOUETTE_URL
                is_silh = True
                silhouette_count += 1
        else:
            canonical_name = f"Player {pid}"
            canonical_nick = f"Player {pid}"
            canonical_slug = f"player-{pid}"
            aliases = [canonical_name]
            pos_id = int(s_info["last_pos"]) if s_info else 0
            first_s = int(s_info["first_season"]) if s_info else 2014
            last_s = int(s_info["last_season"]) if s_info else 2025
            final_photo = DEFAULT_SILHOUETTE_URL
            is_silh = True
            silhouette_count += 1

        players.append({
            "player_id": int(pid),
            "canonical_name": canonical_name,
            "canonical_nickname": canonical_nick,
            "slug": canonical_slug,
            "position_id": pos_id,
            "position_name": POSITION_MAP.get(pos_id, "Desconhecido"),
            "first_season": first_s,
            "last_season": last_s,
            "photo_url": final_photo,
            "is_silhouette": is_silh,
            "known_aliases": aliases
        })

    df_players = pd.DataFrame(players).sort_values("player_id").reset_index(drop=True)
    out_path = DATA_DIR / "players.parquet"
    df_players.to_parquet(out_path, index=False)
    print(f"-> Successfully saved {len(df_players):,} unique players to {out_path}")
    print(f"-> Real player photos: {real_photo_count:,} ({real_photo_count/len(df_players):.1%}) | Silhouettes: {silhouette_count:,} ({silhouette_count/len(df_players):.1%})")

    orphans = set(scouts["player_id"]) - set(df_players["player_id"])
    moj = df_players["canonical_name"].str.contains(r"Ã|Â|\ufffd", regex=True, na=False).sum()
    print(f"-> Orphan player_ids: {len(orphans)} | Mojibake names remaining: {int(moj)}")

if __name__ == "__main__":
    main()
