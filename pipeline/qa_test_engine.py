import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT_DIR = Path(r"C:\Users\thiag\Documents\CLT")
sys.path.insert(0, str(ROOT_DIR / "app"))

from engine.game_state import CLTDataStore, CLTGameEngine


def main():
    store = CLTDataStore()
    eng = CLTGameEngine(store)

    # Stage 1 -> Stage 2
    st = eng.select_rooster(0, ai_difficulty="veteran", series_mode="bo5")
    assert st["stage"] == 2
    print(f"[Stage 1->2] Human picked {st['roosters'][0]['name']} vs AI {st['roosters'][st['ai_rooster_index']]['name']}")

    # Stage 2 -> Stage 3
    st = eng.submit_stage_2_parameter("round", 15)
    assert st["stage"] == 3
    s2 = st["stage2"]
    s3 = st["stage3"]
    print(f"[Stage 2->3] Locked ({s2['season']}, Round {s2['round']}) | Bucket cards: {len(s3['bucket_cards'])} | First picker: {s3['first_picker']}")
    print(f"             AI Bucket decision: {s3['ai_decision']['reason'] if s3['ai_decision'] else 'Pending'}")

    # Verify Bucket cards hide avg_score and rounds_played
    for c in s3["bucket_cards"]:
        assert "avg_score" not in c and "rounds_played" not in c, "Bucket card leaked stats!"

    # Stage 3 -> Stage 4 (Swap a player from Bucket into Human squad)
    avail_card = next(c for c in s3["bucket_cards"] if c["picked_by"] is None)
    h_squad = st["roosters"][st["human_rooster_index"]]["players"]
    drop_cand = next(p for p in h_squad if p["position_code"] == avail_card["position_code"])
    st = eng.submit_stage_3_bucket("swap", avail_card["player_id"], drop_cand["player_id"])
    assert st["stage"] == 4
    print(f"[Stage 3->4] {st['stage3']['human_decision']['reason']}")

    # Anti-Rigging Check 1: Attempting a 2nd pick from Bucket of the Souls must raise ValueError
    try:
        eng.submit_stage_3_bucket("pass")
        raise AssertionError("Expected ValueError on 2nd Bucket submission!")
    except ValueError as e:
        print(f"[Anti-Rigging Stage 3 OK] Blocked repeat Bucket submission: {e}")

    # Stage 4 -> Stage 5
    st = eng.submit_stage_4_highlights("2_scores")
    assert st["stage"] == 5
    revealed = [s for s in st["stage4"]["slots"] if s["revealed"]]
    print(f"[Stage 4->5] Revealed {len(revealed)} matches with scores: {[(m['home_team']['abbreviation'], m['home_score'], m['away_score'], m['away_team']['abbreviation']) for m in revealed]}")

    # Anti-Rigging Check 2: Attempting to also click Option A ('5_matches') after Option B must raise ValueError
    try:
        eng.submit_stage_4_highlights("5_matches")
        raise AssertionError("Expected ValueError on 2nd Highlights submission!")
    except ValueError as e:
        print(f"[Anti-Rigging Stage 4 OK] Blocked double-dipping Highlights of Destiny: {e}")

    print(f"[Stage 5]    Active Crazy Rule: {st['stage5']['active_rule']['name']} — {st['stage5']['active_rule']['tagline']}")

    # Stage 5 -> Stage 6 -> Stage 7 -> Stage 8
    st = eng.prepare_stage_6()
    assert st["stage"] == 6
    h_squad = st["roosters"][st["human_rooster_index"]]["players"]
    quotas = {"GOL": 1, "ZAG": 2, "LAT": 2, "MEI": 4, "ATA": 2, "TEC": 1}
    starters = []
    for pos, cnt in quotas.items():
        starters.extend([p["player_id"] for p in h_squad if p["position_code"] == pos][:cnt])
    st = eng.submit_stage_6_lineup("4-4-2", starters, starters[0])
    assert st["stage"] == 7
    print(f"[Stage 6->7] Half-Time 6v6 sample: Human {st['stage7']['halftime_sample']['human_sample_score']} x {st['stage7']['halftime_sample']['ai_sample_score']} AI")

    st = eng.use_stage_7_powerup("reveal_zeroed")
    print(f"[Stage 7]    Used REVEAL ZEROED -> zeroed starters: {st['stage7']['zeroed_starter_ids']}")

    st = eng.submit_stage_7_halftime("4-4-2", starters, starters[0])
    assert st["stage"] == 8
    s8 = st["stage8"]
    print(f"[Stage 8]    Final Score: Human {s8['human_total']} x {s8['ai_total']} AI | Winner: {s8['winner']} | MVP: {s8['mvp']['short_name']} ({s8['mvp']['eval']['final_score']} pts)")
    print("ALL ENGINE STAGES 1-8 PASSED SMOKE TEST!")


if __name__ == "__main__":
    main()
