import io
import json
import urllib.request
from pathlib import Path
import pandas as pd
from PIL import Image

ROOT_DIR = Path(r"C:\Users\thiag\Documents\CLT")
DATA_DIR = ROOT_DIR / "data"
CLUBS_DIR = ROOT_DIR / "assets" / "clubs"
UI_DIR = ROOT_DIR / "assets" / "ui"
CLUBS_DIR.mkdir(parents=True, exist_ok=True)
UI_DIR.mkdir(parents=True, exist_ok=True)

# Verified official GloboEsporte SDE & Wikimedia Commons transparent PNG URLs for all 39 clubs
FALLBACK_URLS = {
    "FLA": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/FLA/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2018/04/09/Flamengo-65.png",
    ],
    "BOT": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/BOT/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/02/04/botafogo-65.png",
    ],
    "COR": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/COR/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/09/30/Corinthians_65.png",
    ],
    "BAH": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/BAH/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/bahia_60x60.png",
    ],
    "FLU": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/FLU/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/fluminense_60x60.png",
    ],
    "VAS": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/VAS/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2016/07/29/Vasco-65.png",
    ],
    "POR": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/portuguesa_60x60.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Associa%C3%A7%C3%A3o_Portuguesa_de_Desportos.svg/120px-Associa%C3%A7%C3%A3o_Portuguesa_de_Desportos.svg.png",
    ],
    "PAL": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/PAL/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/palmeiras_60x60.png",
    ],
    "SAO": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/SAO/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/sao_paulo_60x60.png",
    ],
    "SAN": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/SAN/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/santos_60x60.png",
    ],
    "RBB": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/RBB/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2020/01/01/65.png",
    ],
    "CAM": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/CAM/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2017/11/23/Atletico-Mineiro-escudo65px.png",
    ],
    "CRU": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/CRU/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2015/04/29/cruzeiro_65.png",
    ],
    "GRE": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/GRE/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/gremio_60x60.png",
    ],
    "INT": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/INT/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2016/05/03/inter65.png",
    ],
    "JUV": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2016/05/08/juventude65.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/juventude_60x60.png",
    ],
    "VIT": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/VIT/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/vitoria_60x60.png",
    ],
    "CRI": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/criciuma_60x60.png",
    ],
    "PAR": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/parana_60x60.png",
    ],
    "GOI": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/05/01/Goias_65px.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/goias_60x60.png",
    ],
    "SPT": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2015/07/21/sport65.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/sport_60x60.png",
    ],
    "CAP": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/CAP/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/09/09/Athletico-PR-65x65.png",
    ],
    "CFC": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/CFC/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2017/03/29/coritiba65.png",
    ],
    "PON": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/ponte_preta_60x60.png",
    ],
    "AVA": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2018/09/04/escudo-avai-65x65.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/avai_60x60.png",
    ],
    "CHA": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/CHA/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2015/08/03/Escudo-Chape-165.png",
    ],
    "FIG": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/figueirense_60x60.png",
    ],
    "JOI": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/joinville_60x60.png",
    ],
    "AME": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/02/28/escudo65_1.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/america_mg_60x60.png",
    ],
    "CSA": [
        "https://s2-ge.glbimg.com/mZOP8YVyTHk6N5tzf3CK62onJ5o=/212x0/https://s3.glbimg.com/v1/AUTH_180b9dd048d9434295d27c4b6dadc248/media_kit/program/trademark/097e/097e52054a8583aa.svg",
    ],
    "STA": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/santa_cruz_60x60.png",
    ],
    "CEA": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2019/10/10/ceara-65x65.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/ceara_60x60.png",
    ],
    "FOR": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2018/06/10/fortaleza-ec-65px.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/fortaleza_60x60.png",
    ],
    "ACG": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2020/07/02/atletico-go-2020-65.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/atletico_go_60x60.png",
    ],
    "CUI": [
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/16/cuiaba65.png",
    ],
    "AMA": [
        "https://s2-ge.glbimg.com/eMicNaKRmpbuOWFea6hxj7GghfM=/212x0/https://s3.glbimg.com/v1/AUTH_180b9dd048d9434295d27c4b6dadc248/media_kit/program/trademark/bde4/bde451c525a01428.svg",
    ],
    "NOV": [
        "https://s2-ge.glbimg.com/CmU7G1a4a0Vtv1AYOQdn6W8b3cg=/212x0/https://s3.glbimg.com/v1/AUTH_180b9dd048d9434295d27c4b6dadc248/media_kit/program/trademark/2fac/2fac1d083b020354.svg",
    ],
    "REM": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/REM/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/remo_60x60.png",
    ],
    "MIR": [
        "https://s3.glbimg.com/v1/AUTH_58d78b787ec34892b5aaa0c7a146155f/clubes_2026/escudos/MIR/60x60.png",
        "https://s.glbimg.com/es/sde/f/organizacoes/2014/04/14/mirassol_60x60.png",
    ],
}


def download_and_normalize_64x64(urls, out_path: Path) -> bool:
    if out_path.exists() and out_path.stat().st_size > 200:
        return True
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            raw = urllib.request.urlopen(req, timeout=8).read()
            if len(raw) < 100:
                continue
            img = Image.open(io.BytesIO(raw)).convert("RGBA")
            img.thumbnail((60, 60), Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            ox = (64 - img.width) // 2
            oy = (64 - img.height) // 2
            canvas.paste(img, (ox, oy), img)
            canvas.save(out_path, format="PNG")
            return True
        except Exception:
            continue
    return False


def main():
    df = pd.read_parquet(DATA_DIR / "teams.parquet")
    ok_list = []
    fail_list = []
    for idx, row in df.iterrows():
        abbr = row["abbreviation"]
        out_file = CLUBS_DIR / f"{abbr}.png"
        urls = FALLBACK_URLS.get(abbr, []) + [row["badge_url"]]
        if download_and_normalize_64x64(urls, out_file):
            ok_list.append(abbr)
            local_url = f"/assets/clubs/{abbr}.png"
            df.at[idx, "badge_url"] = local_url
            df.at[idx, "badge_small_url"] = local_url
        else:
            fail_list.append((row["team_id"], abbr, row["team_name"]))

    df.to_parquet(DATA_DIR / "teams.parquet", index=False)
    print(f"Downloaded & normalized to 64x64 PNG: {len(ok_list)}/39")
    if fail_list:
        print("Failed clubs:", fail_list)


if __name__ == "__main__":
    main()
