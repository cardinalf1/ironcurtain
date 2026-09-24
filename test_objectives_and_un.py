"""
Automated Verification Suite for Cold War Objectives, UN Dungeon Master Console,
Non-Terminal DEFCON 1, and Dynamic Shifting Borders.
"""

import unittest
from state_engine import StateEngine
from groq_service import GroqService

class TestObjectivesAndUN(unittest.TestCase):
    def setUp(self):
        self.engine = StateEngine()
        self.engine.reset_game(student_countries=["USA", "USSR"])
        self.groq = GroqService()

    def test_database_initialization(self):
        """Verify all new tables and initial states are seeded properly."""
        countries = self.engine.get_countries()
        self.assertEqual(len(countries), 8)
        self.assertEqual(countries["USA"]["controller"], "STUDENT")
        self.assertEqual(countries["USSR"]["controller"], "STUDENT")
        self.assertEqual(countries["United Kingdom"]["controller"], "AI")
        self.assertTrue(len(countries["USA"]["long_term_objective"]) > 10)

        # Check territories
        territories = self.engine.get_territories()
        self.assertGreaterEqual(len(territories), 16)
        self.assertIn("KOR_SOUTH", territories)
        self.assertIn("KOR_NORTH", territories)
        self.assertIn("GER_WEST", territories)
        self.assertIn("GER_EAST", territories)
        self.assertEqual(territories["KOR_SOUTH"]["current_controller"], "USA")
        self.assertEqual(territories["KOR_NORTH"]["current_controller"], "USSR")

        # Check world events
        ev = self.engine.get_annual_world_event(1945)
        self.assertIsNotNone(ev)
        self.assertIn("POTSDAM", ev["headline"].upper())

    def test_territory_occupation_and_partition(self):
        """Verify dynamic borders, occupation, and partition."""
        # Occupy Iran
        self.engine.occupy_territory("Iran", "USSR")
        t = self.engine.get_territory("Iran")
        self.assertEqual(t["current_controller"], "USSR")
        self.assertEqual(t["status"], "OCCUPIED")

        # Partition a territory
        self.engine.partition_territory(
            parent_name="Korea",
            part_a_id="KOR_ROK",
            part_a_name="Republic of Korea",
            part_a_iso="KOR",
            part_a_controller="USA",
            part_a_align=0.6,
            part_b_id="KOR_DPRK",
            part_b_name="Democratic People's Republic of Korea",
            part_b_iso="PRK",
            part_b_controller="USSR",
            part_b_align=-0.6
        )
        rok = self.engine.get_territory("KOR_ROK")
        self.assertIsNotNone(rok)
        self.assertEqual(rok["current_controller"], "USA")
        self.assertEqual(rok["status"], "PARTITIONED")

        dprk = self.engine.get_territory("KOR_DPRK")
        self.assertIsNotNone(dprk)
        self.assertEqual(dprk["current_controller"], "USSR")
        self.assertEqual(dprk["status"], "PARTITIONED")

    def test_un_conference_lifecycle(self):
        """Verify UN conference convening, speech submission, and adjournment."""
        conf_id = self.engine.convene_un_conference(
            year=1946,
            title="Emergency Assembly on Iranian Crisis",
            agenda="Soviet forces have not evacuated northern Azerbaijan."
        )
        self.assertIsInstance(conf_id, int)

        active = self.engine.get_active_un_conference()
        self.assertIsNotNone(active)
        self.assertEqual(active["id"], conf_id)

        # Submit speeches
        self.engine.submit_conference_speech(conf_id, "USA", "The United States demands immediate Soviet withdrawal under UN Charter.")
        self.engine.submit_conference_speech(conf_id, "USSR", "Soviet security concerns in the Caspian basin must be acknowledged.")

        speeches = self.engine.get_conference_speeches(conf_id)
        self.assertEqual(len(speeches), 2)
        self.assertEqual(speeches[0]["country"], "USA")
        self.assertEqual(speeches[1]["country"], "USSR")

        # Adjourn conference with ruling
        self.engine.adjourn_conference(conf_id, "UN Resolution 2: Soviet forces shall withdraw within 60 days.")
        self.assertIsNone(self.engine.get_active_un_conference())

    def test_un_admin_chaos_controls(self):
        """Verify UN Dungeon Master controls: tension, DEFCON, aid, sanctions, ceasefires."""
        self.engine.admin_set_tension(85)
        w = self.engine.get_world_state()
        self.assertEqual(w["global_tension"], 85)
        self.assertEqual(w["defcon"], 1)

        # Enforce ceasefire
        self.engine.admin_enforce_ceasefire("Berlin")
        w_after = self.engine.get_world_state()
        self.assertEqual(w_after["global_tension"], 70)

        # Inject aid and sanctions
        c_before = self.engine.get_country("France")
        self.engine.admin_inject_aid("France", 100)
        c_after = self.engine.get_country("France")
        self.assertEqual(c_after["treasury"], c_before["treasury"] + 100)

        self.engine.admin_impose_sanctions("France")
        c_sanctioned = self.engine.get_country("France")
        self.assertEqual(c_sanctioned["treasury"], c_after["treasury"] - 50)

    def test_non_terminal_defcon_1_and_escalation_debuff(self):
        """Verify that nuclear launch drops world to DEFCON 1 without ending game, and applies debuffs."""
        # Setup USA directive to launch atomic strike
        ok, msg = self.engine.submit_directive(
            country_name="USA",
            action_type="MILITARY_POSTURE",
            cost_m=50,
            target="USSR",
            description="Launch tactical atomic strike on frontline positions."
        )
        self.assertTrue(ok)

        # Apply turn deltas with extreme tension jump
        deltas = {
            "USA": {"tension_delta": 25, "approval_delta": -5},
            "USSR": {"tension_delta": 20, "approval_delta": -5}
        }
        self.engine.apply_turn_deltas(deltas)
        w = self.engine.get_world_state()

        # Confirm DEFCON escalated and game is NOT over
        self.assertFalse(bool(w.get("game_over", 0)))
        self.assertIn(w["defcon"], [1, 2])
        self.assertEqual(w["year"], 1948)
        self.assertEqual(w["turn"], 2)

        # Check nuclear strike logging
        strikes = self.engine.get_nuclear_strikes()
        self.assertGreaterEqual(len(strikes), 1)
        self.assertEqual(strikes[0]["attacker"], "USA")
        self.assertEqual(strikes[0]["target"], "USSR")

    def test_objectives_evaluation_and_gradebook(self):
        """Verify that objectives are evaluated and gradebook produces valid letter grades."""
        gradebook = self.engine.get_final_gradebook()
        self.assertEqual(len(gradebook), 8)
        for c_name, g in gradebook.items():
            self.assertIn(g["letter_grade"], ["A+", "A", "B", "C", "F"])
            self.assertGreaterEqual(g["final_score"], 0)
            self.assertLessEqual(g["final_score"], 100)
            self.assertTrue(len(g["verdict"]) > 10)

    def test_autonomous_ai_directives(self):
        """Verify AI directive generation for non-student powers."""
        world = self.engine.get_world_state()
        countries = self.engine.get_countries()
        buffers = self.engine.get_buffers()
        uk_dirs = self.groq.generate_ai_country_directives("United Kingdom", world, countries, buffers)
        self.assertIsInstance(uk_dirs, list)
        self.assertGreaterEqual(len(uk_dirs), 1)
        self.assertIn("description", uk_dirs[0])
        self.assertIn("type", uk_dirs[0])

    def test_peacemaking_advice(self):
        """Verify UN peacemaking recommendations."""
        world = self.engine.get_world_state()
        countries = self.engine.get_countries()
        buffers = self.engine.get_buffers()
        recs = self.groq.get_un_peacemaking_advice(world, countries, buffers, [])
        self.assertEqual(len(recs), 3)
        for r in recs:
            self.assertIn("title", r)
            self.assertIn("action", r)
            self.assertIn("rationale", r)

if __name__ == "__main__":
    unittest.main()
