"""
End-to-End Simulation Test for The Iron Curtain
Verifies StateEngine, validation rules, Groq turn resolution, and History Mirror debrief generation.
"""

import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from state_engine import StateEngine
from groq_service import GroqService

def run_e2e_test():
    print("=== STARTING THE IRON CURTAIN E2E VERIFICATION ===")
    
    # 1. State Engine reset & verify
    se = StateEngine("test_game.db")
    se.reset_game()
    world = se.get_world_state()
    countries = se.get_countries()
    buffers = se.get_buffers()
    
    assert world["year"] == 1945, f"Expected 1945, got {world['year']}"
    assert world["defcon"] == 4, f"Expected DEFCON 4, got {world['defcon']}"
    assert len(countries) == 8, f"Expected 8 countries, got {len(countries)}"
    assert len(buffers) == 6, f"Expected 6 buffers, got {len(buffers)}"
    print("✓ Initial state verified: Year 1945, DEFCON 4, 8 playable nations, 6 buffer states.")

    # 2. Hard validation rules test
    # A) USA submits espionage to Moscow ($50M) -> Valid
    ok, msg = se.submit_directive("USA", "ESPIONAGE_DEPLOY", 50, "USSR", "Infiltrate nuclear facilities at Semipalatinsk")
    assert ok, f"Expected success: {msg}"
    print("✓ Directive 1 (USA Espionage) validated & queued.")

    # B) USSR submits economic aid to East Germany ($40M) -> Valid
    ok, msg = se.submit_directive("USSR", "ECONOMIC_AID", 40, "East Germany", "Rebuild factories and consolidate socialist front")
    assert ok, f"Expected success: {msg}"
    print("✓ Directive 2 (USSR Economic Aid) validated & queued.")

    # C) China tries to spend $500M (treasury is $80M) -> Must Fail
    ok, msg = se.submit_directive("China", "ECONOMIC_AID", 500, "India", "Excessive loan")
    assert not ok, "Expected failure on overspending"
    print("✓ Constraint 1 passed: Blocked overspending correctly.")

    # D) UK tries to launch nuclear strike without bombs -> Must Fail
    ok, msg = se.submit_directive("United Kingdom", "NUCLEAR_STRIKE", 50, "USSR", "Atomic strike")
    assert not ok, "Expected failure on non-nuclear strike"
    print("✓ Constraint 2 passed: Blocked non-nuclear power from launching strike.")

    # 3. Communications Hub verification
    se.send_comms("PUBLIC_UN", "India", None, "We appeal to the great powers for global nuclear restraint.")
    se.send_comms("BILATERAL", "United Kingdom", "USA", "Requesting additional economic credits under the loan agreement.")
    
    un_comms = se.get_comms()
    assert len(un_comms) >= 2, "Expected comms messages saved"
    print("✓ Comms hub verified: UN teletype and bilateral encrypted cables stored.")

    # 4. Turn resolution & History Mirror execution
    directives = se.get_pending_directives(world["turn"])
    stances = se.get_stances()
    assert len(directives) == 2, f"Expected 2 pending directives, got {len(directives)}"

    print("\nExecuting Groq Game Master resolution with History Mirror debrief...")
    gs = GroqService()
    resolution = gs.resolve_turn(world, countries, buffers, directives, stances)
    
    assert "country_updates" in resolution, "Missing country_updates"
    assert "world_updates" in resolution, "Missing world_updates"
    assert "history_mirror" in resolution, "Missing history_mirror"
    
    hm = resolution["history_mirror"]
    print(f"✓ History Mirror generated successfully:")
    print(f"  - Simulation Summary: {hm.get('sim_summary', '')[:120]}...")
    print(f"  - Divergence (Butterfly Effect): {hm.get('divergence_analysis', '')[:120]}...")
    print(f"  - Discussion Questions: {len(hm.get('discussion_questions', []))} prompts generated.")

    # Apply deltas
    se.apply_turn_deltas(resolution)
    new_world = se.get_world_state()
    assert new_world["year"] == 1946, f"Expected year 1946, got {new_world['year']}"
    assert new_world["phase"] == "DEBRIEF", f"Expected DEBRIEF phase, got {new_world['phase']}"
    print(f"✓ World state advanced to Year {new_world['year']}, Phase: {new_world['phase']}")

    # Save History Mirror
    se.save_history_mirror(
        year=1945,
        turn=1,
        real_history="Real 1945 Potsdam and atomic dawn",
        sim_history=hm.get("sim_summary", ""),
        divergence=hm.get("divergence_analysis", ""),
        questions=hm.get("discussion_questions", []),
        legacy=hm.get("legacy_verdict", None)
    )

    mirror_read = se.get_history_mirror(1945)
    assert mirror_read is not None, "Failed to read saved History Mirror"
    print("✓ History Mirror debrief successfully stored and retrieved.")

    print("\n=== ALL E2E INTEGRATION TESTS PASSED WITH 100% SUCCESS! ===")

if __name__ == "__main__":
    run_e2e_test()
