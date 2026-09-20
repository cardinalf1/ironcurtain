"""
Verification script for all newly added systems in state_engine.py
"""
import os
import sys

# Ensure local imports work
sys.path.insert(0, os.path.dirname(__file__))

from state_engine import StateEngine

def run_tests():
    test_db = "test_scratch.db"
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass
    se = StateEngine(db_path=test_db)
    print("1. Testing Country Dossier (Fog-of-War)...")
    dossier_enemy = se.get_country_dossier("USA", "USSR")
    print(f"   USA looking at USSR -> Confidence: {dossier_enemy['confidence_label']} ({dossier_enemy['confidence_pct']}%)")
    print(f"   Estimated bombs: {dossier_enemy['bombs_display']}")

    dossier_ally = se.get_country_dossier("USA", "United Kingdom")
    print(f"   USA looking at UK -> Confidence: {dossier_ally['confidence_label']} ({dossier_ally['confidence_pct']}%)")

    print("\n2. Testing UN Security Council (UNSC) with Veto...")
    ok, msg = se.propose_unsc_resolution("USA", "Embargo on Contested Frontiers", "Prohibit trade with belligerent buffer zones", "Korea", "SANCTIONS")
    print(f"   Propose resolution: {msg}")
    res_list = se.get_unsc_resolutions()
    res_id = res_list[0]["id"]
    se.vote_unsc_resolution(res_id, "USA", "YES")
    se.vote_unsc_resolution(res_id, "United Kingdom", "YES")
    se.vote_unsc_resolution(res_id, "USSR", "NO") # P5 VETO
    se.resolve_unsc_resolutions(res_list[0]["turn"])
    updated_res = se.get_unsc_resolutions()[0]
    print(f"   Resolution Status after USSR vote: {updated_res['status']} (Vetoed by: {updated_res.get('vetoed_by')})")
    assert updated_res["status"] == "VETOED"

    print("\n3. Testing Red Phone Encrypted Hotline...")
    ok, note, intercepted = se.send_hotline_message("USA", "USSR", "President Truman: We propose formal bilateral consultation in Geneva.")
    print(f"   Hotline message sent: {note}")
    logs = se.get_hotline_messages("USA")
    print(f"   Hotline log count for USA: {len(logs)}")
    assert len(logs) > 0

    print("\n4. Testing Economic Engine & War Bonds...")
    usa_before = se.get_country("USA")["treasury"]
    se.execute_structured_action("USA", {"type": "WAR_BONDS"})
    usa_after = se.get_country("USA")["treasury"]
    print(f"   USA Treasury before war bonds: ${usa_before}M -> after: ${usa_after}M")
    assert usa_after == usa_before + 150

    print("\n5. Testing Annual Turn Economy Collection...")
    se.execute_turn_economy(1)
    usa_after_tax = se.get_country("USA")["treasury"]
    print(f"   USA Treasury after annual tax collection: ${usa_after_tax}M (+$250M base tax)")
    assert usa_after_tax > usa_after

    print("\n6. Testing Random Events Engine...")
    se.roll_turn_random_events(1946, 2)
    events = se.get_random_events()
    print(f"   Random Events logged count: {len(events)}")
    for ev in events[:2]:
        print(f"   - [{ev['event_type']}] {ev['title']}: {ev['description'][:60]}...")

    print("\n7. Testing Directive Limits & Military Offensive against Germany...")
    curr_turn = se.get_world_state()["turn"]
    ussr_before = se.get_country("USSR")["treasury"]
    # 1st order: Attack Germany
    ok1, msg1, rej1 = se.execute_structured_action("USSR", {"type": "MILITARY_OFFENSIVE", "target": "Germany", "cost_m": 120})
    assert ok1 is True
    ussr_after1 = se.get_country("USSR")["treasury"]
    assert ussr_after1 == ussr_before - 120
    print(f"   USSR attacked Germany: Cost ${ussr_before - ussr_after1}M deducted cleanly.")

    # 2nd order: Espionage
    ok2, msg2, rej2 = se.execute_structured_action("USSR", {"type": "ESPIONAGE", "target": "USA", "cost_m": 40})
    assert ok2 is True

    # 3rd order: Nuclear expansion
    ok3, msg3, rej3 = se.execute_structured_action("USSR", {"type": "NUCLEAR_EXPANSION", "cost_m": 80})
    assert ok3 is True
    assert se.get_directive_count("USSR", curr_turn) == 3

    # 4th order: Should be blocked by MAX_DIRECTIVES_PER_TURN (3)
    ok4, msg4, rej4 = se.execute_structured_action("USSR", {"type": "MILITARY_OFFENSIVE", "target": "Poland", "cost_m": 120})
    assert ok4 is False
    assert "capacity reached" in (rej4 or "").lower() or "capacity exceeded" in (rej4 or "").lower()
    print("   Directive limit verified: 4th order correctly blocked.")

    print("\n8. Testing Nation Turn Submission...")
    sub_before = se.get_submission_status(curr_turn)
    assert sub_before["USSR"] is True  # True because USSR has pending directives
    se.submit_turn("USSR", curr_turn)
    assert se.is_turn_submitted("USSR", curr_turn) is True
    print("   Nation Turn Submission verified.")

    print("\n9. Testing Diplomatic Stance Alignment (Ally vs Neutral)...")
    ok_st, msg_st, _ = se.execute_structured_action("India", {"type": "DIPLOMATIC_STANCE", "target": "USSR", "stance": "Ally"})
    assert "Ally" in msg_st
    stances = {s["to_country"]: s["stance"] for s in se.get_stances("India")}
    assert stances.get("USSR") == "Ally"
    print("   Diplomatic Stance verified: Stance correctly set to 'Ally'.")

    print("\n10. Testing Non-Nuclear Power Bomb Request Guard...")
    india_pre = se.get_country("India")
    assert india_pre["nuclear"] == 0 and india_pre["bombs"] == 0
    ok_nuke, msg_nuke, _ = se.execute_structured_action("India", {"type": "NUCLEAR_EXPANSION", "cost_m": 100, "bombs_delta": 5})
    assert ok_nuke is True
    india_post = se.get_country("India")
    assert india_post["bombs"] == 0, f"Expected 0 bombs, got {india_post['bombs']}"
    assert india_post["nuclear"] == 1
    assert "RESEARCH" in msg_nuke
    print("   Non-nuclear guard verified: 0 bombs granted, redirected to Nuclear Research.")

    print("\n11. Testing Nuclear Strike with 0 Bombs...")
    ok_strike, _, rej_strike = se.execute_structured_action("India", {"type": "NUCLEAR_STRIKE", "target": "USA"})
    assert ok_strike is False
    assert "Stockpile depleted" in (rej_strike or "")
    print("   Nuclear strike guard verified: Correctly rejected due to 0 warheads.")

    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
