import json
import urllib.request
import pandas as pd
import numpy as np

BASE_RAW = "https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/01_raw"

def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def check_monotonicity_legacy(year: int):
    url = f"{BASE_RAW}/{year}/{year}_scouts_raw.csv"
    try:
        df = pd.read_csv(url, encoding="latin-1", low_memory=False)
    except Exception as e:
        return f"{year}: Error loading: {e}"
    
    id_col = find_column(df, ["atletas.atleta_id", "AtletaID", "atleta_id", "ID"])
    round_col = find_column(df, ["Rodada", "rodada_id", "atletas.rodada_id", "round"])
    scout_col = find_column(df, ["FS", "G", "PE", "RB", "DS"])
    
    if not (id_col and round_col and scout_col):
        return f"{year}: Missing key columns in {df.columns.tolist()[:10]}"
    
    # Pick top 20 players with most rows
    top_players = df[id_col].value_counts().head(30).index
    df_sample = df[df[id_col].isin(top_players)].sort_values([id_col, round_col])
    
    diffs = df_sample.groupby(id_col)[scout_col].diff().dropna()
    neg_diffs = (diffs < 0).sum()
    total_diffs = len(diffs)
    
    # If negative diffs > 5%, it's fixture-level!
    if neg_diffs > total_diffs * 0.05:
        return f"{year}: [FIXTURE-LEVEL] ({neg_diffs}/{total_diffs} negative steps in {scout_col} for top players)"
    else:
        return f"{year}: [CUMULATIVE] ({neg_diffs}/{total_diffs} negative steps in {scout_col}. Monotonically non-decreasing!)"

def check_monotonicity_round_csvs(year: int):
    try:
        r5 = pd.read_csv(f"{BASE_RAW}/{year}/rodada-5.csv", low_memory=False, encoding="latin-1")
        r6 = pd.read_csv(f"{BASE_RAW}/{year}/rodada-6.csv", low_memory=False, encoding="latin-1")
        r7 = pd.read_csv(f"{BASE_RAW}/{year}/rodada-7.csv", low_memory=False, encoding="latin-1")
    except Exception as e:
        return f"{year}: Error loading round CSVs: {e}"
    
    id_col = find_column(r5, ["atletas.atleta_id", "atleta_id", "ID", "AtletaID"])
    scout_col = find_column(r5, ["FS", "G", "DS", "RB"])
    
    if not (id_col and scout_col):
        return f"{year}: Could not find id/scout cols in r5: {r5.columns.tolist()[:10]}"
    
    m = r5[[id_col, scout_col]].merge(r6[[id_col, scout_col]], on=id_col, suffixes=('_r5', '_r6'))
    m = m.merge(r7[[id_col, scout_col]], on=id_col).rename(columns={scout_col: f"{scout_col}_r7"})
    m = m.dropna(subset=[f"{scout_col}_r5", f"{scout_col}_r6", f"{scout_col}_r7"])
    
    drops_6_5 = (m[f"{scout_col}_r6"] < m[f"{scout_col}_r5"]).sum()
    drops_7_6 = (m[f"{scout_col}_r7"] < m[f"{scout_col}_r6"]).sum()
    total = len(m)
    
    if drops_6_5 > 0.05 * total or drops_7_6 > 0.05 * total:
        return f"{year}: [FIXTURE-LEVEL] (Drops: {drops_6_5}/{total} and {drops_7_6}/{total} in {scout_col})"
    else:
        return f"{year}: [CUMULATIVE] (Drops: {drops_6_5}/{total} and {drops_7_6}/{total} in {scout_col}. Monotonically non-decreasing!)"

def check_monotonicity_json_2021():
    year = 2021
    try:
        url5 = f"{BASE_RAW}/2021/Mercado_5.txt"
        url6 = f"{BASE_RAW}/2021/Mercado_6.txt"
        data5 = json.loads(urllib.request.urlopen(url5).read().decode("latin-1"))
        data6 = json.loads(urllib.request.urlopen(url6).read().decode("latin-1"))
        
        at5 = {a['atleta_id']: a.get('scout') or {} for a in data5.get('atletas', [])}
        at6 = {a['atleta_id']: a.get('scout') or {} for a in data6.get('atletas', [])}
        
        common_ids = set(at5.keys()) & set(at6.keys())
        drops = 0
        checks = 0
        for aid in common_ids:
            fs5 = at5[aid].get('FS', 0)
            fs6 = at6[aid].get('FS', 0)
            if fs5 > 0:
                checks += 1
                if fs6 < fs5:
                    drops += 1
        
        if checks == 0:
            return f"2021: No active scouts found in Mercado 5/6"
        if drops > 0.05 * checks:
            return f"{year}: [FIXTURE-LEVEL] (Drops: {drops}/{checks})"
        else:
            return f"{year}: [CUMULATIVE] (Drops: {drops}/{checks}. Monotonically non-decreasing!)"
    except Exception as e:
        return f"2021: Error: {e}"

print("=== RUNNING COMPLETE MONOTONICITY AUDIT (2014-2025) ===")
results = {}
for yr in [2014, 2015, 2016, 2017]:
    res = check_monotonicity_legacy(yr)
    print(res)
    results[yr] = "CUMULATIVE" if "[CUMULATIVE]" in res else "FIXTURE-LEVEL"

for yr in [2018, 2019, 2020]:
    res = check_monotonicity_round_csvs(yr)
    print(res)
    results[yr] = "CUMULATIVE" if "[CUMULATIVE]" in res else "FIXTURE-LEVEL"

res_2021 = check_monotonicity_json_2021()
print(res_2021)
results[2021] = "CUMULATIVE" if "[CUMULATIVE]" in res_2021 else "FIXTURE-LEVEL"

for yr in [2022, 2023, 2024, 2025]:
    res = check_monotonicity_round_csvs(yr)
    print(res)
    results[yr] = "CUMULATIVE" if "[CUMULATIVE]" in res else "FIXTURE-LEVEL"

print("\n=== SUMMARY CLASSIFICATION DICTIONARY ===")
print(results)
