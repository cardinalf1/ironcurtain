"""
Automated verification test for 10 Cold War Eras (1945–1991) and Dynamic Borders.
Tests:
1. Era 1 baseline (India under British Raj, 4-zone Germany, joint-occupied Korea).
2. Era 2 transition (India sovereign, Germany FRG/GDR partition).
3. Era 3 transition (Korea DMZ, Vietnam partition).
4. Era 10 transition (Reunified Germany).
5. Full 10-turn progression and game completion after turn 10.
"""

import os
import sys
import tempfile
import sqlite3

from state_engine import StateEngine
from objectives_data import COLD_WAR_ERAS, ERA_TERRITORY_DEFAULTS, ANNUAL_OBJECTIVES, LONG_TERM_OBJECTIVES


def test_ten_eras_system():
    print(">>> Initializing isolated test database for 10 Cold War Eras...")
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test_eras_game.db")

    engine = StateEngine(db_path=test_db_path)
    engine.reset_game()

    # 1. Verify Era 1 Baseline (1945)
    world = engine.get_world_state()
    assert world["turn"] == 1, f"Expected turn 1, got {world['turn']}"
    assert world["year"] == 1945, f"Expected year 1945, got {world['year']}"
    assert world["game_over"] == 0 or world["game_over"] is False

    territories = engine.get_territories()
    assert "India" in territories or "IND" in territories, "India territory missing"
    india = territories.get("India") or territories.get("IND")
    print(f"Era 1 India Status: {india['status']} | Controller: {india['current_controller']} | Name: {india['name']}")
    assert india["status"] == "COLONY_TRANSITION", f"Expected COLONY_TRANSITION for India in Era 1, got {india['status']}"
    assert india["current_controller"] == "United Kingdom", f"Expected UK controller for India in Era 1, got {india['current_controller']}"

    # Verify Germany in Era 1
    assert "GER_WEST" in territories
    assert "GER_EAST" in territories

    # Verify Korea in Era 1
    assert "KOR_SOUTH" in territories and "KOR_NORTH" in territories
    assert territories["KOR_SOUTH"]["current_controller"] == "USA"
    assert territories["KOR_NORTH"]["current_controller"] == "USSR"

    # Verify all 10 eras have world events and objectives seeded
    for era_id in range(1, 11):
        era_event = engine.get_annual_world_event(era_id)
        assert era_event is not None, f"Missing world event for Era {era_id}"
        for country in ["USA", "USSR", "United Kingdom", "France", "China", "India", "Yugoslavia", "Cuba"]:
            objs = engine.get_country_objectives(country, era_id)
            assert len(objs) > 0, f"Missing objectives for {country} in Era {era_id}"

    print(">>> Era 1 Baseline and 10 Eras Seeding Verified.")

    # 2. Test Dynamic Era Boundaries: Transition to Era 2 (1948–1952)
    engine.apply_era_boundaries(2)
    territories_era2 = engine.get_territories()
    india_era2 = territories_era2.get("India") or territories_era2.get("IND")
    print(f"Era 2 India Status: {india_era2['status']} | Controller: {india_era2['current_controller']} | Name: {india_era2['name']}")
    assert india_era2["status"] == "SOVEREIGN", f"Expected SOVEREIGN India in Era 2, got {india_era2['status']}"
    assert india_era2["current_controller"] == "India", f"Expected India controller in Era 2, got {india_era2['current_controller']}"

    # Verify FRG/GDR partition in Era 2
    assert "GER_WEST" in territories_era2
    assert "GER_EAST" in territories_era2
    assert territories_era2["GER_WEST"]["current_controller"] == "West Germany"
    assert territories_era2["GER_EAST"]["current_controller"] == "East Germany"

    print(">>> Era 2 Dynamic Border Shift (India Decolonization & German Partition) Verified.")

    # 3. Test Dynamic Era Boundaries: Transition to Era 3 (1953–1958)
    engine.apply_era_boundaries(3)
    territories_era3 = engine.get_territories()
    assert "Vietnam" in territories_era3
    assert territories_era3["Vietnam"]["status"] == "PARTITIONED"
    assert territories_era3["KOR_SOUTH"]["status"] == "PARTITIONED"
    print(">>> Era 3 Dynamic Border Shift (Korea DMZ & 17th Parallel Vietnam Partition) Verified.")

    # 4. Test Dynamic Era Boundaries: Transition to Era 10 (1990–1991)
    engine.apply_era_boundaries(10)
    territories_era10 = engine.get_territories()
    assert "GER_WEST" in territories_era10 and "GER_EAST" in territories_era10
    ger_w = territories_era10["GER_WEST"]
    ger_e = territories_era10["GER_EAST"]
    assert ger_w["status"] == "SOVEREIGN" and ger_w["current_controller"] == "Germany"
    assert ger_e["status"] == "SOVEREIGN" and ger_e["current_controller"] == "Germany"
    print(">>> Era 10 Dynamic Border Shift (Reunified Germany) Verified.")

    # 5. Test Full Simulation Progression across 10 Turns
    print(">>> Testing step-by-step turn advancement through all 10 Eras...")
    engine.reset_game()  # Reset back to Era 1

    for turn_idx in range(1, 11):
        cur_w = engine.get_world_state()
        assert cur_w["turn"] == turn_idx, f"Expected turn {turn_idx}, got {cur_w['turn']}"
        era_meta = COLD_WAR_ERAS[turn_idx]
        assert cur_w["year"] == era_meta["year_start"]

        # Advance turn via apply_turn_deltas
        dummy_updates = {
            "countries": {},
            "buffers": {},
            "world": {
                "defcon": 4,
                "global_tension": 40
            }
        }
        engine.apply_turn_deltas(dummy_updates)

    # After 10 turns, game should conclude
    final_w = engine.get_world_state()
    assert final_w["turn"] == 11, f"Expected turn 11, got {final_w['turn']}"
    assert final_w["game_over"] == 1, f"Expected game_over == 1 after Era 10, got {final_w['game_over']}"
    print(f">>> Game Over correctly reached after Era 10: {final_w['game_over'] == 1}")

    # Final Gradebook verification
    gradebook = engine.get_final_gradebook()
    assert len(gradebook) == 8, f"Expected 8 countries in gradebook, got {len(gradebook)}"
    for c_name, g in gradebook.items():
        assert "letter_grade" in g
        assert "final_score" in g
        assert "verdict" in g
        print(f"Gradebook: {c_name:15} | Score: {g['final_score']:2} | Grade: {g['letter_grade']:2} | {g['verdict'][:40]}...")

    print("\n[PASS] ALL 10 COLD WAR ERAS & DYNAMIC BORDER TESTS PASSED PERFECTLY!")


if __name__ == "__main__":
    test_ten_eras_system()
