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
    cost_atk = se.get_action_cost("USSR", "MILITARY_OFFENSIVE", "Germany")
    ok1, msg1, rej1 = se.execute_structured_action("USSR", {"type": "MILITARY_OFFENSIVE", "target": "Germany", "cost_m": 120})
    assert ok1 is True
    ussr_after1 = se.get_country("USSR")["treasury"]
    assert ussr_after1 == ussr_before - cost_atk
    print(f"   USSR attacked Germany: Cost ${cost_atk}M deducted cleanly.")

    # 2nd order: Espionage
    cost_spy = se.get_action_cost("USSR", "ESPIONAGE", "USA")
    ok2, msg2, rej2 = se.execute_structured_action("USSR", {"type": "ESPIONAGE", "target": "USA", "cost_m": 40})
    assert ok2 is True
    ussr_after2 = se.get_country("USSR")["treasury"]
    assert ussr_after2 == ussr_after1 - cost_spy
    print(f"   USSR deployed spy: Cost ${cost_spy}M (KGB discount) deducted cleanly.")

    # 3rd order: Nuclear research (USSR is non-nuclear initially, must fund research)
    ok3, msg3, rej3 = se.execute_structured_action("USSR", {"type": "NUCLEAR_RESEARCH", "cost_m": 100})
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

    print("\n10. Testing Non-Nuclear Power Instant Bomb Blocking & Incremental R&D...")
    india_pre = se.get_country("India")
    assert india_pre["nuclear"] == 0 and india_pre["bombs"] == 0
    # A: Attempting to build bomb directly should be BLOCKED
    ok_nuke, _, rej_nuke = se.execute_structured_action("India", {"type": "BUILD_BOMB", "cost_m": 80})
    assert ok_nuke is False
    assert "Atomic capability not yet unlocked" in (rej_nuke or "")
    print("   Instant bomb blocked: Non-nuclear power cannot assemble warheads directly.")

    # B: Domestic R&D increases progress incrementally (not instant 100%)
    ok_rd, msg_rd, _ = se.execute_structured_action("India", {"type": "NUCLEAR_RESEARCH", "cost_m": 100})
    assert ok_rd is True
    india_post = se.get_country("India")
    assert india_post["bombs"] == 0, f"Expected 0 bombs, got {india_post['bombs']}"
    assert india_post["nuclear"] == 0, "Expected nuclear capability still locked"
    assert india_post["nuclear_progress"] == 25, f"Expected 25% progress, got {india_post['nuclear_progress']}%"
    print(f"   Incremental domestic R&D verified: Progress reached {india_post['nuclear_progress']}% (0 bombs assembled).")

    print("\n11. Testing Nuclear Strike without Nuclear Capability / Warheads...")
    ok_strike, _, rej_strike = se.execute_structured_action("India", {"type": "NUCLEAR_STRIKE", "target": "USA"})
    assert ok_strike is False
    assert "not unlocked nuclear technology" in (rej_strike or "") or "Stockpile depleted" in (rej_strike or "")
    print("   Nuclear strike guard verified: Correctly rejected because India is non-nuclear.")

    print("\n12. Testing Fog-of-War: Crude Rumor vs Active Spy Network Telemetry...")
    dossier_no_spy = se.get_country_dossier("USA", "USSR")
    assert dossier_no_spy["has_active_spy"] is False
    assert "NO ACTIVE SPY" in dossier_no_spy["confidence_label"]
    assert "rumor" in dossier_no_spy["bombs_display"].lower() or "unverified" in dossier_no_spy["bombs_display"].lower()
    print(f"   Without spy: {dossier_no_spy['bombs_display']} | Confidence: {dossier_no_spy['confidence_label']}")

    # Deploy an active spy to USSR
    se.execute_structured_action("USA", {"type": "ESPIONAGE", "target": "USSR", "cost_m": 40})
    dossier_with_spy = se.get_country_dossier("USA", "USSR")
    assert dossier_with_spy["has_active_spy"] is True
    assert "HUMINT" in dossier_with_spy["confidence_label"]
    assert "ACTIVE SPY NETWORK" in dossier_with_spy["bombs_display"]
    print(f"   With spy: {dossier_with_spy['bombs_display']} | Confidence: {dossier_with_spy['confidence_label']}")



    print("\n13. Testing Unilateral Trade Pact Blocking (Must Use Red Phone)...")
    ok_trade, msg_trade, rej_trade = se.execute_structured_action("Yugoslavia", {"type": "TRADE_PACT", "target": "India"})
    assert ok_trade is False
    assert "red phone" in (rej_trade or "").lower()
    print("   Unilateral trade directive correctly blocked; player redirected to Red Phone.")

    print("\n14. Testing Bilateral Red Phone Pact Proposals & Negotiation...")
    pact_id = se.propose_bilateral_pact("Yugoslavia", "India", "TRADE_PACT", "Mutual trade accord +$25M", "We propose non-aligned trade.")
    assert pact_id > 0
    pending_india = se.get_pact_proposals("India", status="PENDING")
    assert any(p["id"] == pact_id for p in pending_india)
    print(f"   Proposal #{pact_id} dispatched from Yugoslavia to India. India pending count: {len(pending_india)}")

    # India accepts
    ok_resp, msg_resp = se.respond_to_pact(pact_id, "India", "ACCEPTED")
    assert ok_resp is True
    assert se.has_trade_pact("Yugoslavia", "India") is True
    print(f"   India accepted proposal #{pact_id}: Trade accord established bilateral revenue!")

    print("\n15. Testing Cold War Country Specialties & Dynamic Action Costs...")
    cost_ussr_spy = se.get_action_cost("USSR", "SPY", "USA")
    cost_usa_spy = se.get_action_cost("USA", "SPY", "USSR")
    print(f"   KGB spy cost (USSR): ${cost_ussr_spy}M (Base: ${cost_usa_spy}M)")
    assert cost_ussr_spy == 20
    assert cost_usa_spy == 45


    cost_china_atk = se.get_action_cost("China", "ATTACK", "Korea")
    cost_usa_atk = se.get_action_cost("USA", "ATTACK", "Korea")
    print(f"   China offensive cost: ${cost_china_atk}M (USA cost: ${cost_usa_atk}M)")
    assert cost_china_atk == 60
    assert cost_usa_atk == 120

    cost_usa_aid = se.get_action_cost("USA", "FOREIGN_AID", "France")
    assert cost_usa_aid == 60
    print(f"   USA Marshall Plan aid cost: ${cost_usa_aid}M (40% discount)")

    print("\n16. Testing Multi-Tab State Version Fingerprinting...")
    v1 = se.get_state_version()
    se.send_hotline_message("USA", "USSR", "Telex check")
    v2 = se.get_state_version()
    assert v1 != v2, f"State version did not update: {v1} == {v2}"
    print(f"   State version dynamically updated from {v1} to {v2}")

    print("\n17. Testing Red Phone Bilateral Atomic Tech Sharing (ATOMIC_COLLAB)...")
    # UK starts at 15% progress
    uk_pre = se.get_country("United Kingdom")
    assert uk_pre["nuclear"] == 0
    init_uk_prog = uk_pre["nuclear_progress"]
    init_uk_u = uk_pre["uranium"]

    # Propose ATOMIC_COLLAB from UK to USA
    p_id = se.propose_bilateral_pact("United Kingdom", "USA", "ATOMIC_COLLAB", {}, "Request atomic technology and reactor data")
    ok_collab, msg_collab = se.respond_to_pact(p_id, "USA", "ACCEPTED")
    assert ok_collab is True
    uk_post = se.get_country("United Kingdom")
    assert uk_post["nuclear_progress"] == init_uk_prog + 50, f"Expected {init_uk_prog + 50}%, got {uk_post['nuclear_progress']}%"
    assert uk_post["uranium"] == init_uk_u + 1
    print(f"   Atomic Collab ratified: UK R&D advanced from {init_uk_prog}% to {uk_post['nuclear_progress']}%, +1 MT Uranium received.")

    print("\n18. Testing Warhead Commission Constraints (Uranium Consumption & Depletion)...")
    # USA is operational nuclear power with uranium
    usa_pre = se.get_country("USA")
    assert usa_pre["nuclear"] == 1
    u_before = usa_pre["uranium"]
    b_before = usa_pre["bombs"]

    # Assemble 1 bomb successfully
    ok_b, msg_b, _ = se.execute_structured_action("USA", {"type": "BUILD_BOMB", "cost_m": 80})
    assert ok_b is True
    usa_post = se.get_country("USA")
    assert usa_post["bombs"] == b_before + 1
    assert usa_post["uranium"] == u_before - 1
    print(f"   Warhead assembled: +1 bomb added, 1 MT Uranium consumed ({usa_post['uranium']} MT remaining).")

    # Now simulate a country with 0 uranium attempting to assemble a bomb
    with se._get_connection() as conn:
        conn.execute("UPDATE countries SET uranium = 0, nuclear = 1 WHERE name = 'France'")
        conn.commit()
    ok_depleted, _, rej_depleted = se.execute_structured_action("France", {"type": "BUILD_BOMB", "cost_m": 80})
    assert ok_depleted is False
    assert "Uranium supply depleted" in (rej_depleted or "")
    print("   Uranium depletion guard verified: Commission blocked when Uranium is 0 MT.")

    print("\n19. Testing USSR Multi-Year Natural Atomic Program Progression...")
    # USSR has an active spy in USA (deployed earlier in step 7)
    ussr_pre = se.get_country("USSR")
    u_prog_pre = ussr_pre["nuclear_progress"]
    # Execute turn economy collection (simulating year transition)
    se.execute_turn_economy(1)
    ussr_post = se.get_country("USSR")
    print(f"   USSR atomic program: {u_prog_pre}% -> {ussr_post['nuclear_progress']}% (Base +20%/yr + 15% KGB atomic espionage bonus)")
    assert ussr_post["nuclear_progress"] == 100
    assert ussr_post["nuclear"] == 1
    assert ussr_post["bombs"] >= 1
    print("   USSR atomic breakthrough verified: Reached 100% and broke atomic monopoly!")

    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()

