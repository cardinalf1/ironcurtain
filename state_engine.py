"""
The Iron Curtain - State Engine & Rules Arbiter (Palantir C2 Architecture)
Thread-safe SQLite storage, deterministic action validation, stance matrices,
DEFCON escalation mechanics, Country Intelligence Dossier (Fog-of-War),
UN Security Council, Crisis Theaters, Red Phone Hotline, Economic Revenue Engine,
and Emergent Random Historical Events.
"""

import sqlite3
import threading
import json
import secrets
import os
import re
from typing import Dict, List, Tuple, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "game_state.db")
_db_lock = threading.Lock()

INITIAL_COUNTRIES = {
    "USA": {
        "alignment": 1.0,
        "nuclear": True,
        "bombs": 2,
        "treasury": 2500,
        "tension": 10,
        "objective": "Contain Soviet expansion, support Western European recovery, and maintain atomic deterrence.",
        "capital": "Washington D.C.",
        "lat": 38.9, "lon": -77.0,
        "uranium": 4, "oil": 80, "domestic_approval": 78,
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 1
    },
    "USSR": {
        "alignment": -1.0,
        "nuclear": False,
        "bombs": 0,
        "treasury": 900,
        "tension": 15,
        "objective": "Consolidate Eastern European buffer states, complete atomic weapon R&D, and break capitalist encirclement.",
        "capital": "Moscow",
        "lat": 55.75, "lon": 37.62,
        "uranium": 2, "oil": 70, "domestic_approval": 82,
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 1
    },
    "United Kingdom": {
        "alignment": 0.7,
        "nuclear": False,
        "bombs": 0,
        "treasury": 450,
        "tension": 20,
        "objective": "Rebuild domestic economy, sustain global strategic lifelines, and preserve Anglo-American alliance.",
        "capital": "London",
        "lat": 51.5, "lon": -0.12,
        "uranium": 1, "oil": 40, "domestic_approval": 65,
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 0
    },
    "France": {
        "alignment": 0.4,
        "nuclear": False,
        "bombs": 0,
        "treasury": 350,
        "tension": 30,
        "objective": "Restore national sovereignty, maintain control over colonial frontiers, and counter German resurgence.",
        "capital": "Paris",
        "lat": 48.85, "lon": 2.35,
        "uranium": 1, "oil": 30, "domestic_approval": 55,
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 0
    },
    "China": {
        "alignment": -0.3,
        "nuclear": False,
        "bombs": 0,
        "treasury": 200,
        "tension": 40,
        "objective": "Consolidate the Communist revolution, resist imperialist encroachment, and rebuild agrarian economy.",
        "capital": "Beijing",
        "lat": 39.9, "lon": 116.4,
        "uranium": 0, "oil": 20, "domestic_approval": 70,
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0
    },
    "India": {
        "alignment": 0.0,
        "nuclear": False,
        "bombs": 0,
        "treasury": 180,
        "tension": 15,
        "objective": "Lead the Non-Aligned Movement, maintain complete sovereignty, and promote decolonization.",
        "capital": "New Delhi",
        "lat": 28.61, "lon": 77.2,
        "uranium": 0, "oil": 25, "domestic_approval": 80,
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0
    },
    "Yugoslavia": {
        "alignment": -0.6,
        "nuclear": False,
        "bombs": 0,
        "treasury": 150,
        "tension": 25,
        "objective": "Pioneer self-managed socialism, resist Soviet domination, and secure economic independence.",
        "capital": "Belgrade",
        "lat": 44.78, "lon": 20.44,
        "uranium": 0, "oil": 20, "domestic_approval": 75,
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0
    },
    "Cuba": {
        "alignment": -0.2,
        "nuclear": False,
        "bombs": 0,
        "treasury": 100,
        "tension": 20,
        "objective": "Protect national resources, resist external dominance, and navigate strategic Caribbean tensions.",
        "capital": "Havana",
        "lat": 23.12, "lon": -82.38,
        "uranium": 0, "oil": 15, "domestic_approval": 60,
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0
    }
}

INITIAL_BUFFERS = {
    "Germany": {"alignment": 0.0, "lat": 51.16, "lon": 10.45},
    "West Germany": {"alignment": 0.8, "lat": 50.73, "lon": 7.1},
    "East Germany": {"alignment": -0.8, "lat": 52.52, "lon": 13.4},
    "Greece": {"alignment": 0.2, "lat": 37.98, "lon": 23.72},
    "Turkey": {"alignment": 0.3, "lat": 39.93, "lon": 32.85},
    "Iran": {"alignment": 0.0, "lat": 35.68, "lon": 51.38},
    "Korea": {"alignment": 0.0, "lat": 37.56, "lon": 126.97},
    "Japan": {"alignment": 0.6, "lat": 35.68, "lon": 139.69},
    "Poland": {"alignment": -0.7, "lat": 52.23, "lon": 21.01}
}

UNSC_PERM_5 = ["USA", "USSR", "United Kingdom", "France", "China"]
MAX_DIRECTIVES_PER_TURN = 3

class StateEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self, force_reset: bool = False):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            if force_reset:
                cursor.execute("DROP TABLE IF EXISTS world_state")
                cursor.execute("DROP TABLE IF EXISTS countries")
                cursor.execute("DROP TABLE IF EXISTS buffer_states")
                cursor.execute("DROP TABLE IF EXISTS stances")
                cursor.execute("DROP TABLE IF EXISTS pending_directives")
                cursor.execute("DROP TABLE IF EXISTS intel_cables")
                cursor.execute("DROP TABLE IF EXISTS comms")
                cursor.execute("DROP TABLE IF EXISTS history_mirror")
                cursor.execute("DROP TABLE IF EXISTS news_feed")
                cursor.execute("DROP TABLE IF EXISTS map_events")
                cursor.execute("DROP TABLE IF EXISTS active_agents")
                cursor.execute("DROP TABLE IF EXISTS unsc_resolutions")
                cursor.execute("DROP TABLE IF EXISTS crises")
                cursor.execute("DROP TABLE IF EXISTS hotline_messages")
                cursor.execute("DROP TABLE IF EXISTS trade_agreements")
                cursor.execute("DROP TABLE IF EXISTS random_events")

            # World state
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS world_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    year INTEGER NOT NULL,
                    turn INTEGER NOT NULL,
                    defcon INTEGER NOT NULL,
                    global_tension INTEGER NOT NULL,
                    mad_triggered BOOLEAN NOT NULL,
                    game_over BOOLEAN NOT NULL,
                    phase TEXT NOT NULL DEFAULT 'DIRECTIVES',
                    admin_password TEXT NOT NULL
                )
            """)

            # Countries
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    name TEXT PRIMARY KEY,
                    alignment REAL NOT NULL,
                    nuclear BOOLEAN NOT NULL,
                    bombs INTEGER NOT NULL,
                    treasury INTEGER NOT NULL,
                    tension INTEGER NOT NULL,
                    objective TEXT NOT NULL,
                    capital TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    uranium INTEGER DEFAULT 2,
                    oil INTEGER DEFAULT 50,
                    domestic_approval INTEGER DEFAULT 75,
                    missile_tech TEXT DEFAULT 'STRATEGIC_BOMBERS',
                    paperclip_scientists INTEGER DEFAULT 0
                )
            """)

            # Safe column migration for existing tables
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN uranium INTEGER DEFAULT 2")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN oil INTEGER DEFAULT 50")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN domestic_approval INTEGER DEFAULT 75")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN missile_tech TEXT DEFAULT 'STRATEGIC_BOMBERS'")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN paperclip_scientists INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass

            # Buffer states
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS buffer_states (
                    name TEXT PRIMARY KEY,
                    alignment REAL NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL
                )
            """)

            # Stances
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stances (
                    from_country TEXT NOT NULL,
                    to_country TEXT NOT NULL,
                    stance TEXT NOT NULL,
                    PRIMARY KEY (from_country, to_country)
                )
            """)

            # Directives
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_directives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    country TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    target TEXT NOT NULL,
                    cost_m INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    dice_roll INTEGER NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Classified cables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intel_cables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    recipient TEXT NOT NULL,
                    target TEXT NOT NULL,
                    intel_summary TEXT NOT NULL,
                    apparent_data TEXT NOT NULL,
                    confidence_rating TEXT NOT NULL,
                    agent_status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Comms
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    channel TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # History Mirror
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history_mirror (
                    year INTEGER PRIMARY KEY,
                    turn INTEGER NOT NULL,
                    real_history TEXT NOT NULL,
                    sim_history TEXT NOT NULL,
                    divergence_analysis TEXT NOT NULL,
                    discussion_questions TEXT NOT NULL,
                    legacy_verdict TEXT
                )
            """)

            # News feed
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news_feed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    headline TEXT NOT NULL,
                    body TEXT NOT NULL
                )
            """)

            # Map events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS map_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    source_name TEXT,
                    source_lat REAL,
                    source_lon REAL,
                    target_name TEXT,
                    target_lat REAL,
                    target_lon REAL,
                    description TEXT NOT NULL
                )
            """)

            # Active agents
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active_agents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_country TEXT NOT NULL,
                    target TEXT NOT NULL,
                    mission TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE'
                )
            """)

            # UNSC Resolutions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unsc_resolutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    proposer TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    target TEXT,
                    effect_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    vetoed_by TEXT,
                    votes TEXT NOT NULL DEFAULT '{}'
                )
            """)

            # Dynamic Crises
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crises (
                    crisis_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'DORMANT',
                    turn_started INTEGER,
                    year_started INTEGER,
                    theatre TEXT NOT NULL,
                    description TEXT NOT NULL,
                    state_data TEXT NOT NULL DEFAULT '{}'
                )
            """)

            # Secret Red Phone Hotline
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hotline_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    content TEXT NOT NULL,
                    is_intercepted BOOLEAN DEFAULT 0,
                    intercepted_by TEXT,
                    leak_level TEXT DEFAULT 'NONE',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Trade Agreements
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trade_agreements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn_signed INTEGER NOT NULL,
                    party_a TEXT NOT NULL,
                    party_b TEXT NOT NULL,
                    annual_value INTEGER NOT NULL,
                    resource_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE'
                )
            """)

            # Random Events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS random_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    target_country TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    effect_delta TEXT NOT NULL DEFAULT '{}'
                )
            """)

            # Turn Submissions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS turn_submissions (
                    turn INTEGER NOT NULL,
                    country TEXT NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (turn, country)
                )
            """)

            # Seed World State & Countries if empty
            cursor.execute("SELECT COUNT(*) FROM world_state")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO world_state (id, year, turn, defcon, global_tension, mad_triggered, game_over, phase, admin_password)
                    VALUES (1, 1945, 1, 4, 20, 0, 0, 'DIRECTIVES', 'POTSDAM1945')
                """)

                for name, data in INITIAL_COUNTRIES.items():
                    cursor.execute("""
                        INSERT INTO countries (name, alignment, nuclear, bombs, treasury, tension, objective, capital, lat, lon, uranium, oil, domestic_approval, missile_tech, paperclip_scientists)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, data["alignment"], data["nuclear"], data["bombs"], data["treasury"], data["tension"],
                          data["objective"], data["capital"], data["lat"], data["lon"],
                          data["uranium"], data["oil"], data["domestic_approval"], data["missile_tech"], data["paperclip_scientists"]))

                for name, data in INITIAL_BUFFERS.items():
                    cursor.execute("""
                        INSERT INTO buffer_states (name, alignment, lat, lon)
                        VALUES (?, ?, ?, ?)
                    """, (name, data["alignment"], data["lat"], data["lon"]))

                country_names = list(INITIAL_COUNTRIES.keys())
                for c1 in country_names:
                    for c2 in country_names:
                        if c1 == c2:
                            continue
                        default_stance = "Neutral"
                        if (c1 in ["USA", "United Kingdom", "France"]) and (c2 in ["USA", "United Kingdom", "France"]):
                            default_stance = "Ally"
                        elif (c1 in ["USA", "United Kingdom"] and c2 == "USSR") or (c1 == "USSR" and c2 in ["USA", "United Kingdom"]):
                            default_stance = "Rival"
                        elif c1 == "Yugoslavia" and c2 == "USSR":
                            default_stance = "Friendly"
                        cursor.execute("""
                            INSERT INTO stances (from_country, to_country, stance)
                            VALUES (?, ?, ?)
                        """, (c1, c2, default_stance))

                # Seed Initial News
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (1, 1945, 'POST-POTSDAM ERA COMMENCES', 'World War II concludes. The United States conducts Trinity and holds the atomic monopoly. Superpower balance established across European spheres of influence.')
                """)

                # Seed Initial Dynamic Crises
                cursor.execute("""
                    INSERT INTO crises (crisis_id, title, status, turn_started, year_started, theatre, description, state_data)
                    VALUES 
                    ('BERLIN_BLOCKADE', 'Berlin Ground Corridors Access Dispute', 'DORMANT', 4, 1948, 'Central Europe (Germany)', 
                     'Soviet forces challenge Western ground rail and road transit through East Germany into divided Berlin.',
                     '{"airlift_active": false, "corridor_blocked": false, "supplies_delivered_pct": 100}'),
                    ('KOREAN_WAR', 'Korean Peninsula 38th Parallel Flashpoint', 'DORMANT', 6, 1950, 'East Asia (Korea)',
                     'Ideological division between the Soviet-backed North and US-supported South threatens open warfare across the 38th Parallel.',
                     '{"frontline": "38th Parallel", "un_coalition_active": false, "chinese_volunteers_active": false}'),
                    ('IRAN_OIL', 'Abadan Refinery & Iranian Oil Nationalization', 'DORMANT', 7, 1951, 'Middle East (Iran)',
                     'Iranian Prime Minister Mossadegh challenges Anglo-Iranian Oil Company concessions, precipitating an international embargo.',
                     '{"nationalized": false, "embargo_active": false}')
                """)

            conn.commit()
            conn.close()

    def reset_game(self):
        self._init_db(force_reset=True)

    def get_world_state(self) -> Dict[str, Any]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM world_state WHERE id = 1")
            row = cursor.fetchone()
            conn.close()
            if row:
                return dict(row)
            return {"year": 1945, "turn": 1, "defcon": 4, "global_tension": 20, "mad_triggered": False, "game_over": False, "phase": "DIRECTIVES"}

    def set_phase(self, phase: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE world_state SET phase = ? WHERE id = 1", (phase,))
            conn.commit()
            conn.close()

    def get_countries(self) -> Dict[str, Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM countries")
            rows = cursor.fetchall()
            conn.close()
            return {r["name"]: dict(r) for r in rows}

    def get_country(self, name: str) -> Optional[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM countries WHERE name = ?", (name,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None

    def get_buffers(self) -> Dict[str, Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM buffer_states")
            rows = cursor.fetchall()
            conn.close()
            return {r["name"]: dict(r) for r in rows}

    def get_stances(self, from_country: Optional[str] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if from_country:
                cursor.execute("SELECT * FROM stances WHERE from_country = ?", (from_country,))
            else:
                cursor.execute("SELECT * FROM stances")
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def set_stance(self, from_country: str, to_country: str, stance: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO stances (from_country, to_country, stance)
                VALUES (?, ?, ?)
                ON CONFLICT(from_country, to_country) DO UPDATE SET stance = excluded.stance
            """, (from_country, to_country, stance))
            conn.commit()
            conn.close()

    def has_active_spy(self, owner_country: str, target_country: str) -> bool:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM active_agents 
                WHERE owner_country = ? AND target = ? AND status = 'ACTIVE'
            """, (owner_country, target_country))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0

    def get_active_agents(self, owner_country: Optional[str] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if owner_country:
                cursor.execute("SELECT * FROM active_agents WHERE owner_country = ? AND status = 'ACTIVE'", (owner_country,))
            else:
                cursor.execute("SELECT * FROM active_agents WHERE status = 'ACTIVE'")
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    # =========================================================================
    # CLASSIFIED INTELLIGENCE DOSSIER (FOG-OF-WAR ENGINE)
    # =========================================================================
    def get_country_dossier(self, viewer_country: str, target_name: str) -> Dict[str, Any]:
        """
        Generates Palantir C2 classified intelligence dossier on the target territory/country.
        Information accuracy and detail are filtered through intelligence confidence:
        - Self or Ally: Confirmed (100% ground truth)
        - Active Spy Asset: High (85% precision)
        - Friendly/Neutral: Moderate (Diplomatic attaché estimate)
        - Rival/Enemy: Low (Speculative bounds)
        """
        country = self.get_country(target_name)
        buffer_info = self.get_buffers().get(target_name) if not country else None

        if not country and not buffer_info:
            return {"error": f"Territory '{target_name}' not cataloged in defense registry."}

        # Territory is a buffer state
        if buffer_info:
            align_val = buffer_info["alignment"]
            align_label = "Pro-West / Allied" if align_val > 0.3 else ("Pro-Soviet / East" if align_val < -0.3 else "Contested / Neutral")
            return {
                "target_name": target_name,
                "is_buffer": True,
                "capital": "Regional Seat",
                "alignment": align_val,
                "alignment_label": align_label,
                "confidence_label": "HIGH (OPEN GEOPOLITICAL SPHERE)",
                "confidence_pct": 80,
                "strategic_notes": f"Buffer state on frontier fault line. Alignment index: {align_val:+.2f}.",
                "actions_available": ["COVERT_COUP", "ECONOMIC_AID", "MILITARY_POSTURE", "UNSC_SANCTION"]
            }

        # Territory is a full playable country
        is_self = (viewer_country == target_name)
        stances = {s["to_country"]: s["stance"] for s in self.get_stances(viewer_country)}
        bilateral_stance = stances.get(target_name, "Neutral")
        has_spy = self.has_active_spy(viewer_country, target_name)

        # Determine Confidence Tier
        if is_self or bilateral_stance == "Ally":
            conf_label = "VERIFIED // TOP SECRET NOFORN"
            conf_pct = 100
            bombs_text = f"{country['bombs']} Warheads (VERIFIED)"
            treasury_text = f"${country['treasury']}M (AUDITED)"
            uranium_text = f"{country['uranium']} MT Fissile Grade"
            oil_text = f"{country['oil']}% Strategic Reserves"
            approval_text = f"{country['domestic_approval']}% Stability"
        elif has_spy:
            conf_label = "HIGH // HUMINT FIELD ASSET"
            conf_pct = 85
            # Small jitter for fog-of-war
            delta = secrets.choice([-1, 0, 1]) if country["bombs"] > 0 else 0
            est_b = max(0, country["bombs"] + delta)
            bombs_text = f"Est. {est_b} Warheads (±1 Delta)"
            treasury_text = f"Est. ${country['treasury']}M (HUMINT Reported)"
            uranium_text = f"~{country['uranium']} MT (Reported)"
            oil_text = f"{country['oil']}% Reserves (Estimated)"
            approval_text = f"{country['domestic_approval']}% (Estimated)"
        elif bilateral_stance in ["Friendly", "Neutral"]:
            conf_label = "MODERATE // DIPLOMATIC ATTACHÉ"
            conf_pct = 55
            est_low = max(0, country["bombs"] - 1)
            est_high = country["bombs"] + 2
            bombs_text = f"Est. {est_low} – {est_high} Warheads" if country["nuclear"] else "Unconfirmed R&D Status"
            treasury_text = f"~${(country['treasury'] // 50) * 50}M Macro Reserves"
            uranium_text = "Imports Detected (Volume Unknown)" if country["uranium"] > 0 else "Negligible"
            oil_text = "Stable Trade Flow"
            approval_text = "Domestic Control Established"
        else:
            # Rival or Enemy
            conf_label = "LOW // SIGNALS INTELLIGENCE ONLY"
            conf_pct = 25
            bombs_text = f"Classified / Est. 0 – {country['bombs'] + 4} Warheads"
            treasury_text = "State Secret (Estimated Strained)"
            uranium_text = "Restricted // Suspected Ore Mining"
            oil_text = "Strategic Concession Dependent"
            approval_text = "Information Blackout"

        # Recent cables concerning target
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT intel_summary, apparent_data, confidence_rating 
                FROM intel_cables 
                WHERE recipient = ? AND target = ?
                ORDER BY id DESC LIMIT 3
            """, (viewer_country, target_name))
            recent_cables = [dict(r) for r in cursor.fetchall()]
            conn.close()

        return {
            "target_name": target_name,
            "is_buffer": False,
            "capital": country["capital"],
            "leader": INITIAL_COUNTRIES.get(target_name, {}).get("objective", "National Leadership"),
            "alignment": country["alignment"],
            "stance": bilateral_stance,
            "confidence_label": conf_label,
            "confidence_pct": conf_pct,
            "nuclear_status": "ATOMIC CAPABLE" if country["nuclear"] else "CONVENTIONAL ONLY",
            "bombs_display": bombs_text,
            "treasury_display": treasury_text,
            "uranium_display": uranium_text,
            "oil_display": oil_text,
            "approval_display": approval_text,
            "missile_tech": country["missile_tech"],
            "has_active_spy": has_spy,
            "recent_cables": recent_cables
        }

    # =========================================================================
    # UN SECURITY COUNCIL (UNSC) SYSTEM
    # =========================================================================
    def propose_unsc_resolution(self, proposer: str, title: str, description: str, target: str, effect_type: str) -> Tuple[bool, str]:
        world = self.get_world_state()
        turn = world["turn"]

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            initial_votes = json.dumps({proposer: "YES"})
            cursor.execute("""
                INSERT INTO unsc_resolutions (turn, proposer, title, description, target, effect_type, status, votes)
                VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?)
            """, (turn, proposer, title, description, target, effect_type, initial_votes))

            cursor.execute("""
                INSERT INTO news_feed (turn, year, headline, body)
                VALUES (?, ?, ?, ?)
            """, (turn, world["year"], f"UN DIPLOMACY: {title}", f"{proposer} has formally tabled a resolution in the UN Security Council regarding {target}."))
            conn.commit()
            conn.close()

        return True, f"RESOLUTION TABLED: UNSC draft '{title}' submitted for deliberation and member voting."

    def vote_unsc_resolution(self, resolution_id: int, country: str, vote: str) -> Tuple[bool, str]:
        vote = vote.upper()
        if vote not in ["YES", "NO", "ABSTAIN"]:
            return False, "Invalid vote: Must be YES, NO, or ABSTAIN."

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT votes, status FROM unsc_resolutions WHERE id = ?", (resolution_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False, "Resolution not found."

            votes = json.loads(row["votes"])
            votes[country] = vote

            cursor.execute("UPDATE unsc_resolutions SET votes = ? WHERE id = ?", (json.dumps(votes), resolution_id))
            conn.commit()
            conn.close()

        return True, f"VOTE RECORDED: {country} cast vote '{vote}'."

    def resolve_unsc_resolutions(self, turn: int):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM unsc_resolutions WHERE turn = ? AND status = 'PENDING'", (turn,))
            resolutions = [dict(r) for r in cursor.fetchall()]

            for res in resolutions:
                votes = json.loads(res["votes"])
                res_id = res["id"]
                vetoed_by = None

                # Check P5 Vetoes (USA, USSR, UK, France, China)
                for p5 in UNSC_PERM_5:
                    if votes.get(p5) == "NO":
                        vetoed_by = p5
                        break

                if vetoed_by:
                    status = "VETOED"
                    cursor.execute("UPDATE unsc_resolutions SET status = 'VETOED', vetoed_by = ? WHERE id = ?", (vetoed_by, res_id))
                    cursor.execute("""
                        INSERT INTO news_feed (turn, year, headline, body)
                        VALUES (?, 1945, 'UNSC RESOLUTION VETOED', ?)
                    """, (turn, f"Resolution '{res['title']}' was VETOED by Permanent Member {vetoed_by}."))
                else:
                    yes_count = sum(1 for v in votes.values() if v == "YES")
                    if yes_count >= 4:
                        status = "PASSED"
                        cursor.execute("UPDATE unsc_resolutions SET status = 'PASSED' WHERE id = ?", (res_id,))
                        cursor.execute("""
                            INSERT INTO news_feed (turn, year, headline, body)
                            VALUES (?, 1945, 'UNSC RESOLUTION ADOPTED', ?)
                        """, (turn, f"Resolution '{res['title']}' was ADOPTED by the Security Council ({yes_count} votes in favor)."))
                        
                        # Apply effects
                        if res["effect_type"] == "SANCTIONS" and res["target"]:
                            cursor.execute("UPDATE countries SET treasury = MAX(0, treasury - 40), tension = tension + 10 WHERE name = ?", (res["target"],))
                        elif res["effect_type"] == "PEACEKEEPERS" and res["target"]:
                            cursor.execute("UPDATE buffer_states SET alignment = alignment * 0.5 WHERE name = ?", (res["target"],))
                    else:
                        status = "FAILED"
                        cursor.execute("UPDATE unsc_resolutions SET status = 'FAILED' WHERE id = ?", (res_id,))

            conn.commit()
            conn.close()

    def get_unsc_resolutions(self, turn: Optional[int] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if turn is not None:
                cursor.execute("SELECT * FROM unsc_resolutions WHERE turn = ? ORDER BY id DESC", (turn,))
            else:
                cursor.execute("SELECT * FROM unsc_resolutions ORDER BY id DESC LIMIT 20")
            rows = cursor.fetchall()
            conn.close()
            out = []
            for r in rows:
                item = dict(r)
                item["votes"] = json.loads(item["votes"])
                out.append(item)
            return out

    # =========================================================================
    # DYNAMIC REGIONAL CRISES ENGINE (Berlin, Korea, Iran)
    # =========================================================================
    def get_all_crises(self) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crises ORDER BY turn_started ASC")
            rows = cursor.fetchall()
            conn.close()
            out = []
            for r in rows:
                item = dict(r)
                item["state_data"] = json.loads(item["state_data"])
                out.append(item)
            return out

    def activate_crisis_if_due(self, current_year: int, turn: int):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crises WHERE status = 'DORMANT' AND year_started <= ?", (current_year,))
            due = [dict(r) for r in cursor.fetchall()]

            for cr in due:
                cursor.execute("UPDATE crises SET status = 'ACTIVE' WHERE crisis_id = ?", (cr["crisis_id"],))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, ?, ?)
                """, (turn, current_year, f"CRISIS ERUPTS: {cr['title']}", cr["description"]))
            conn.commit()
            conn.close()

    def resolve_crisis_action(self, crisis_id: str, country_name: str, choice: str) -> Tuple[bool, str]:
        world = self.get_world_state()
        turn = world["turn"]

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crises WHERE crisis_id = ?", (crisis_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False, "Crisis not identified."

            cr = dict(row)
            s_data = json.loads(cr["state_data"])

            msg = ""
            if crisis_id == "BERLIN_BLOCKADE":
                if choice == "AIRLIFT":
                    # Operation Vittles: Costs $20M, raises Berlin supply, de-escalates tension
                    cursor.execute("UPDATE countries SET treasury = treasury - 20 WHERE name = ?", (country_name,))
                    s_data["airlift_active"] = True
                    s_data["supplies_delivered_pct"] = min(100, s_data.get("supplies_delivered_pct", 50) + 30)
                    msg = f"OPERATION VITTLES INITIATED: {country_name} transports air tonnage into Tempelhof. Berlin supplied without ground combat."
                elif choice == "ARMED_CONVOY":
                    # High risk of war!
                    cursor.execute("UPDATE world_state SET defcon = MAX(1, defcon - 1), global_tension = MIN(100, global_tension + 25) WHERE id = 1")
                    msg = f"ARMED CORRIDOR CONVOY ORDERED: {country_name} armor challenges Soviet checkpoints. DEFCON dropped by 1!"
                elif choice == "BLOCKADE":
                    s_data["corridor_blocked"] = True
                    msg = f"CORRIDOR SEALED: Ground highways into Berlin severed."

            elif crisis_id == "KOREAN_WAR":
                if choice == "UN_EXPEDITION":
                    cursor.execute("UPDATE countries SET treasury = treasury - 40 WHERE name = ?", (country_name,))
                    s_data["un_coalition_active"] = True
                    s_data["frontline"] = "Pushing toward Yalu River"
                    msg = f"UN EXPEDITIONARY FORCE: {country_name} deploys divisions to stem the North Korean offensive."
                elif choice == "VOLUNTEER_ARMY":
                    cursor.execute("UPDATE countries SET treasury = treasury - 30 WHERE name = ?", (country_name,))
                    s_data["chinese_volunteers_active"] = True
                    s_data["frontline"] = "Pushed back to 38th Parallel"
                    msg = f"VOLUNTEER DIVISIONS: Chinese People's Volunteers cross the Yalu River."

            cursor.execute("UPDATE crises SET state_data = ? WHERE crisis_id = ?", (json.dumps(s_data), crisis_id))
            cursor.execute("""
                INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                VALUES (?, 'military', ?, ?, ?)
            """, (turn, country_name, cr["theatre"], msg))
            conn.commit()
            conn.close()

        return True, msg

    # =========================================================================
    # RED PHONE ENCRYPTED HOTLINE & COUNTER-ESPIONAGE LEAKS
    # =========================================================================
    def send_hotline_message(self, sender: str, recipient: str, content: str) -> Tuple[bool, str, bool]:
        """
        Sends encrypted diplomatic cable.
        If a rival power has an active espionage ring in sender or recipient capital,
        there is a chance of interception!
        Returns: (success: bool, status_msg: str, was_intercepted: bool)
        """
        world = self.get_world_state()
        turn = world["turn"]

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Check potential interceptors
            cursor.execute("""
                SELECT owner_country FROM active_agents 
                WHERE (target = ? OR target = ?) AND owner_country != ? AND owner_country != ? AND status = 'ACTIVE'
            """, (sender, recipient, sender, recipient))
            interceptors = [r[0] for r in cursor.fetchall()]

            is_intercepted = False
            intercepted_by = None
            leak_level = "NONE"

            if interceptors:
                # 35% chance that spy network taps the telex line
                roll = secrets.randbelow(100)
                if roll < 40:
                    is_intercepted = True
                    intercepted_by = secrets.choice(interceptors)
                    if roll < 15:
                        leak_level = "PUBLIC"  # Leaked to UN wire!
                    else:
                        leak_level = "INTERCEPTED"

            cursor.execute("""
                INSERT INTO hotline_messages (turn, sender, recipient, content, is_intercepted, intercepted_by, leak_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (turn, sender, recipient, content, 1 if is_intercepted else 0, intercepted_by, leak_level))

            if leak_level == "PUBLIC":
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'SIGNALS LEAK: DIPLOMATIC COMMUNIQUE INTERCEPTED', ?)
                """, (turn, world["year"], f"Whistleblowers release leaked cable between {sender} and {recipient}: '{content[:80]}...'"))

            conn.commit()
            conn.close()

        note = f"CONFIDENTIAL TELEX DISPATCHED to {recipient}."
        if leak_level == "PUBLIC":
            note += " ⚠️ ALERT: Communications security breached! Excerpt broadcast on UN wire."
        return True, note, is_intercepted

    def get_hotline_messages(self, country_name: str) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            # Show messages where country is sender, recipient, or the interceptor!
            cursor.execute("""
                SELECT * FROM hotline_messages 
                WHERE sender = ? OR recipient = ? OR (intercepted_by = ? AND is_intercepted = 1)
                ORDER BY id DESC LIMIT 40
            """, (country_name, country_name, country_name))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    # =========================================================================
    # REVENUE ENGINE & ANNUAL ECONOMY
    # =========================================================================
    def execute_turn_economy(self, turn: int):
        """
        Executes annual fiscal collection for all nations:
        - Base industrial tax revenue
        - Reductions for high domestic tension
        - Payouts from bilateral trade agreements
        """
        BASE_TAX = {
            "USA": 250, "USSR": 140, "United Kingdom": 80, "France": 60,
            "China": 40, "India": 35, "Yugoslavia": 30, "Cuba": 20
        }

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Trade agreements lookup
            cursor.execute("SELECT * FROM trade_agreements WHERE status = 'ACTIVE'")
            trades = [dict(r) for r in cursor.fetchall()]

            trade_revenue = {}
            for t in trades:
                trade_revenue[t["party_a"]] = trade_revenue.get(t["party_a"], 0) + t["annual_value"]
                trade_revenue[t["party_b"]] = trade_revenue.get(t["party_b"], 0) + t["annual_value"]

            cursor.execute("SELECT name, tension FROM countries")
            c_rows = cursor.fetchall()

            for r in c_rows:
                c_name = r["name"]
                tension = r["tension"]
                base = BASE_TAX.get(c_name, 25)

                # Unrest deduction
                penalty_mult = 1.0
                if tension >= 50:
                    penalty_mult = 0.60
                elif tension >= 30:
                    penalty_mult = 0.80

                net_income = int(base * penalty_mult) + trade_revenue.get(c_name, 0)
                cursor.execute("UPDATE countries SET treasury = treasury + ? WHERE name = ?", (net_income, c_name))

            conn.commit()
            conn.close()

    # =========================================================================
    # RANDOM EVENTS & ENTROPY ENGINE
    # =========================================================================
    def roll_turn_random_events(self, year: int, turn: int):
        """
        Rolls for historical and emergent shocks:
        - Famines & Crop Blights (e.g. 1946 Soviet Famine)
        - Sterling & Currency Devaluations (e.g. 1947 UK Crisis)
        - Failed nuclear tests / Criticality accidents
        - Dockworker strikes & Industrial slowdowns
        """
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Historical Year-Triggered Events
            if year == 1946:
                cursor.execute("""
                    INSERT INTO random_events (turn, year, target_country, event_type, title, description, effect_delta)
                    VALUES (?, 1946, 'USSR', 'FAMINE', 'Severe Drought & Crop Blight in Ukraine', 
                            'Post-war agricultural disruption triggers grain shortfalls. Domestic tension increases.',
                            '{"treasury": -20, "tension": 12}')
                """, (turn,))
                cursor.execute("UPDATE countries SET treasury = MAX(0, treasury - 20), tension = MIN(100, tension + 12) WHERE name = 'USSR'")
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, 1946, 'ECONOMIC REPORT: SOVIET HARVEST SHORTFALL', 'Agricultural reports from Eastern Europe indicate severe post-war harvest deficit.')
                """, (turn,))

            elif year == 1947:
                cursor.execute("""
                    INSERT INTO random_events (turn, year, target_country, event_type, title, description, effect_delta)
                    VALUES (?, 1947, 'United Kingdom', 'RECESSION', 'Sterling Crisis & Winter Fuel Shortage', 
                            'Freezing blizzards and foreign exchange strain force coal rationing in Britain.',
                            '{"treasury": -25, "tension": 10}')
                """, (turn,))
                cursor.execute("UPDATE countries SET treasury = MAX(0, treasury - 25), tension = MIN(100, tension + 10) WHERE name = 'United Kingdom'")
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, 1947, 'LONDON WIRE: STERLING FISCAL STRAIN', 'British Exchequer announces austerity measures amid severe winter coal rationing.')
                """, (turn,))

            # Emergent Dice-Roll Events (18% probability per turn)
            shock_roll = secrets.randbelow(100)
            if shock_roll < 20:
                # Emergent strike or accident
                targets = ["France", "China", "India", "USA"]
                tgt = secrets.choice(targets)
                cursor.execute("""
                    INSERT INTO random_events (turn, year, target_country, event_type, title, description, effect_delta)
                    VALUES (?, ?, ?, 'STRIKE', 'Transportation Logistics Dockworker Strike', 
                            'Labor union walkouts across major maritime shipping ports disrupt customs receipts.',
                            '{"treasury": -15, "tension": 5}')
                """, (turn, year, tgt))
                cursor.execute("UPDATE countries SET treasury = MAX(0, treasury - 15), tension = MIN(100, tension + 5) WHERE name = ?", (tgt,))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'COMMERCE DISRUPTION: MARITIME STRIKE', ?)
                """, (turn, year, f"Dockworker union general strike in {tgt} temporarily paralyzes commercial freight terminals."))

            conn.commit()
            conn.close()

    def get_random_events(self, turn: Optional[int] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if turn:
                cursor.execute("SELECT * FROM random_events WHERE turn = ? ORDER BY id DESC", (turn,))
            else:
                cursor.execute("SELECT * FROM random_events ORDER BY id DESC LIMIT 15")
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    # =========================================================================
    # STRUCTURED ACTION EXECUTOR (DIRECT AI MUTATIONS)
    # =========================================================================
    def execute_structured_action(self, country_name: str, action: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
        """
        Directly executes action parsed by the AI adviser.
        Mutates real database state, deducts funds/bombs, creates map events,
        and logs active directives immediately.
        Returns: (success: bool, execution_message: str, rejection_reason: Optional[str])
        """
        act_type = action.get("type", "NONE").upper()
        target = action.get("target", "USSR" if country_name != "USSR" else "USA")
        cost_m = int(action.get("cost_m", 50))
        bombs_delta = int(action.get("bombs_delta", 1))
        desc = action.get("description", f"Operational directive targeting {target}.")

        if act_type in ["NONE", "", "ADVISORY"]:
            return True, "Advisory telex logged.", None

        country = self.get_country(country_name)
        if not country:
            return False, f"Unknown country '{country_name}'.", f"Unknown country '{country_name}'."

        world = self.get_world_state()
        turn = world["turn"]
        dice_roll = secrets.randbelow(101)

        # Enforce Directive Capacity (Max 3 orders per turn per country)
        turn_orders = self.get_directive_count(country_name, turn)
        if turn_orders >= MAX_DIRECTIVES_PER_TURN:
            rej = f"Directive capacity reached: {country_name} has already issued {turn_orders}/{MAX_DIRECTIVES_PER_TURN} directives for Year {world['year']}. Directives are locked until year adjudication."
            return False, rej, rej

        # 1. NUCLEAR EXPANSION (Build bombs / Uranium check / Potential test failure)
        if act_type in ["NUCLEAR_EXPANSION", "NUCLEAR_RESEARCH", "BUILD_BOMBS", "BUILD_BOMB"]:
            if cost_m < 60:
                cost_m = 80
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            # 12% chance of Criticality Incident / Failed Test
            test_fail_roll = secrets.randbelow(100)
            if test_fail_roll < 12 and bombs_delta > 0:
                with _db_lock:
                    conn = self._get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE countries SET treasury = treasury - ?, tension = tension + 8 WHERE name = ?", (cost_m, country_name))
                    cursor.execute("""
                        INSERT INTO random_events (turn, year, target_country, event_type, title, description, effect_delta)
                        VALUES (?, ?, ?, 'FAILED_TEST', 'Plutonium Criticality Incident / Radiation Accident', 
                                'A laboratory criticality accident occurred during warhead assembly. Production halted and funds wasted.',
                                '{"treasury": -20, "tension": 8}')
                    """, (turn, world["year"], country_name))
                    cursor.execute("""
                        INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                        VALUES (?, ?, 'FAILED_NUCLEAR_TEST', ?, ?, 'Plutonium assembly criticality failure', ?)
                    """, (turn, country_name, country_name, cost_m, dice_roll))
                    cursor.execute("""
                        INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                        VALUES (?, 'incident', ?, ?, 'CRITICALITY INCIDENT: Atomic assembly failure at secret facility.')
                    """, (turn, country_name, country_name))
                    conn.commit()
                    conn.close()
                return True, f"⚠️ CRITICALITY ACCIDENT: Radiation accident during assembly. Allocated ${cost_m}M consumed from treasury; 0 warheads assembled.", None

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE countries 
                    SET treasury = treasury - ?, bombs = bombs + ?, nuclear = 1 
                    WHERE name = ?
                """, (cost_m, bombs_delta, country_name))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'NUCLEAR_EXPANSION', ?, ?, ?, ?)
                """, (turn, country_name, country_name, cost_m, f"Expanded atomic production: +{bombs_delta} bomb(s). {desc}", dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'nuclear_test', ?, ?, ?)
                """, (turn, country_name, country_name, f"ATOMIC EXPANSION: {country_name} completes assembly of +{bombs_delta} atomic weapon(s)."))
                conn.commit()
                conn.close()

            return True, f"⚛️ ATOMIC EXPANSION COMPLETE: Added +{bombs_delta} bomb(s). -${cost_m}M allocated from defense reserves (Remaining: ${country['treasury'] - cost_m}M).", None

        # 2. NUCLEAR STRIKE
        elif act_type == "NUCLEAR_STRIKE":
            if not country["nuclear"]:
                rej = f"Atomic action unauthorized: {country_name} has not unlocked nuclear technology."
                return False, rej, rej
            if country["bombs"] < 1:
                rej = f"Stockpile depleted: {country_name} possesses 0 atomic warheads."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET bombs = MAX(0, bombs - 1) WHERE name = ?", (country_name,))
                cursor.execute("UPDATE world_state SET defcon = 1, global_tension = 100, mad_triggered = 1 WHERE id = 1")
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'NUCLEAR_STRIKE', ?, 0, 'Strategic nuclear strike launched', 100)
                """, (turn, country_name, target))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'strike', ?, ?, ?)
                """, (turn, country_name, target, f"CRITICAL: {country_name} has launched an atomic strike on {target}! Global retaliation imminent."))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'FLASH: ATOMIC STRIKE LAUNCHED', ?)
                """, (turn, world["year"], f"Strategic nuclear strikes confirmed from {country_name} against {target}. Worldwide DEFCON 1 alerted."))
                conn.commit()
                conn.close()

            return True, f"⚠️ ATOMIC STRIKE LAUNCHED: Strategic warhead detonated on {target}! DEFCON 1 and Mutually Assured Destruction triggered!", None

        # 3. MILITARY OFFENSIVE / INVASION / ATTACK
        elif act_type in ["MILITARY_OFFENSIVE", "INVASION", "ATTACK", "OFFENSIVE", "MILITARY_STRIKE", "WAR"]:
            if cost_m < 100:
                cost_m = 120
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Combat offensive requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ?, tension = tension + 10 WHERE name = ?", (cost_m, country_name))
                cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 15) WHERE id = 1")
                
                # Check if buffer state or full country
                cursor.execute("SELECT alignment FROM buffer_states WHERE name = ?", (target,))
                b_row = cursor.fetchone()
                if b_row:
                    shift = 0.5 if country["alignment"] > 0 else -0.5
                    new_align = max(-1.0, min(1.0, b_row["alignment"] + shift))
                    cursor.execute("UPDATE buffer_states SET alignment = ? WHERE name = ?", (new_align, target))
                elif target in INITIAL_COUNTRIES:
                    cursor.execute("UPDATE countries SET tension = MIN(100, tension + 20) WHERE name = ?", (target,))

                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'MILITARY_OFFENSIVE', ?, ?, ?, ?)
                """, (turn, country_name, target, cost_m, f"Assault offensive on {target}: {desc}", dice_roll))

                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'strike', ?, ?, ?)
                """, (turn, country_name, target, f"COMBAT INVASION: {country_name} forces launch combat operations into {target}!"))

                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'ARMED CONFLICT: INVASION COMMENCED', ?)
                """, (turn, world["year"], f"Urgent wire reports confirm {country_name} armed forces have launched combat operations into {target}."))

                conn.commit()
                conn.close()

            return True, f"💥 COMBAT OFFENSIVE LAUNCHED into {target.upper()}! -${cost_m}M allocated from Defense Treasury (Remaining: ${country['treasury'] - cost_m}M). Assault vector active on theater map.", None

        # 4. ESPIONAGE DEPLOYMENT
        elif act_type in ["ESPIONAGE", "ESPIONAGE_DEPLOY", "SPY"]:
            if cost_m < 30:
                cost_m = 40
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (cost_m, country_name))
                cursor.execute("""
                    INSERT INTO active_agents (owner_country, target, mission, status)
                    VALUES (?, ?, ?, 'ACTIVE')
                """, (country_name, target, desc))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'ESPIONAGE_DEPLOY', ?, ?, ?, ?)
                """, (turn, country_name, target, cost_m, desc, dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'espionage', ?, ?, ?)
                """, (turn, country_name, target, f"INTELLIGENCE ASSET: {country_name} deployed covert network into {target}."))
                conn.commit()
                conn.close()

            # Generate immediate field intelligence cable
            dossier = self.get_country_dossier(country_name, target)
            bombs_info = dossier.get("bombs_display", "Unknown")
            nuke_status = dossier.get("nuclear_status", "Unconfirmed")
            treasury_info = dossier.get("treasury_display", "Unconfirmed")
            conf_info = dossier.get("confidence_label", "HIGH // HUMINT FIELD ASSET")

            self.add_intel_cable(
                turn=turn,
                recipient=country_name,
                target=target,
                summary=f"Infiltration debrief on {target}",
                apparent_data=f"Stockpile: {bombs_info} | Capability: {nuke_status}",
                confidence=conf_info,
                status="ACTIVE"
            )

            msg = (
                f"🕵️ INTELLIGENCE ASSET INFILTRATED {target.upper()} (-${cost_m}M, Remaining: ${country['treasury'] - cost_m}M).\n\n"
                f"**DECRYPTED FIELD INTELLIGENCE CABLE:**\n"
                f"• **Atomic Warhead Stockpile:** {bombs_info}\n"
                f"• **Nuclear Capability:** {nuke_status}\n"
                f"• **Treasury Reserves:** {treasury_info}\n"
                f"• **Confidence Rating:** {conf_info}\n\n"
                f"*Field Station Chief Note: HUMINT assets are active. Continuous telemetry routed to your C2 Notification Centre.*"
            )
            return True, msg, None

        # 5. ECONOMIC REVENUE: WAR BONDS (Gain cash)
        elif act_type in ["WAR_BONDS", "BONDS", "AUSTERITY"]:
            bond_gain = 150
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury + ?, tension = tension + 8 WHERE name = ?", (bond_gain, country_name))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'WAR_BONDS', ?, 0, 'Issued emergency sovereign bonds (+ $150M cash, +8% tension)', ?)
                """, (turn, country_name, country_name, dice_roll))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'FISCAL EXPANSION: WAR BONDS ISSUED', ?)
                """, (turn, world["year"], f"{country_name} issues emergency domestic sovereign bonds, raising ${bond_gain}M."))
                conn.commit()
                conn.close()
            return True, f"WAR BONDS ISSUED: Injected +${bond_gain}M cash into National Treasury (Current: ${country['treasury'] + bond_gain}M). Domestic tension +8%.", None

        # 6. ECONOMIC REVENUE: TRADE PACT
        elif act_type in ["TRADE_PACT", "COMMERCIAL_TREATY"]:
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO trade_agreements (turn_signed, party_a, party_b, annual_value, resource_type, status)
                    VALUES (?, ?, ?, 25, 'MANUFACTURES', 'ACTIVE')
                """, (turn, country_name, target))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'TRADE_PACT', ?, 0, 'Ratified bilateral commerce pact (+$25M/turn)', ?)
                """, (turn, country_name, target, dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'aid', ?, ?, ?)
                """, (turn, country_name, target, f"COMMERCIAL PACT: Bilateral trade treaty established between {country_name} and {target}."))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'BILATERAL COMMERCE: TRADE PACT RATIFIED', ?)
                """, (turn, world["year"], f"Bilateral commercial treaty signed between {country_name} and {target}, yielding mutual recurring revenue."))
                conn.commit()
                conn.close()
            return True, f"TRADE TREATY RATIFIED: Commercial agreement established with {target} (+$25M/turn each).", None

        # 7. PAPERCLIP SCIENTIST RECRUITMENT (Missile Tech)
        elif act_type in ["PAPERCLIP_RECRUIT", "MISSILE_RESEARCH"]:
            if cost_m < 30:
                cost_m = 50
            if cost_m > country["treasury"]:
                rej = f"Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE countries 
                    SET treasury = treasury - ?, paperclip_scientists = paperclip_scientists + 1, missile_tech = 'V2_ADVANCED_MISSILES'
                    WHERE name = ?
                """, (cost_m, country_name))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'PAPERCLIP_RECRUIT', ?, ?, 'Recruited advanced rocketry scientists', ?)
                """, (turn, country_name, country_name, cost_m, dice_roll))
                conn.commit()
                conn.close()
            return True, f"ROCKET SCIENTISTS RECRUITED: Aerospace program advanced to V2_ADVANCED_MISSILES (-${cost_m}M, Remaining: ${country['treasury'] - cost_m}M).", None

        # 8. ECONOMIC AID
        elif act_type in ["ECONOMIC_AID", "AID", "LOAN"]:
            if cost_m < 50:
                cost_m = 100
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (cost_m, country_name))
                if target in INITIAL_COUNTRIES:
                    cursor.execute("UPDATE countries SET treasury = treasury + ? WHERE name = ?", (cost_m, target))
                elif target in INITIAL_BUFFERS:
                    shift = 0.3 if country["alignment"] > 0 else -0.3
                    cursor.execute("UPDATE buffer_states SET alignment = alignment + ? WHERE name = ?", (shift, target))

                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'ECONOMIC_AID', ?, ?, ?, ?)
                """, (turn, country_name, target, cost_m, desc, dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'aid', ?, ?, ?)
                """, (turn, country_name, target, f"ECONOMIC TRANSFER: ${cost_m}M transferred from {country_name} to {target}."))
                conn.commit()
                conn.close()

            return True, f"ECONOMIC AID TRANSFERRED: -${cost_m}M transferred to {target} (Remaining Treasury: ${country['treasury'] - cost_m}M).", None

        # 9. DIPLOMATIC STANCE
        elif act_type in ["DIPLOMATIC_STANCE", "STANCE"]:
            stance = action.get("stance", "Neutral")
            self.set_stance(country_name, target, stance)
            return True, f"DIPLOMATIC POSTURE: Stance toward {target} set to '{stance}'.", None

        # 10. MILITARY POSTURE / REINFORCEMENT
        else:
            if cost_m < 30:
                cost_m = 50
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (cost_m, country_name))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'MILITARY_POSTURE', ?, ?, ?, ?)
                """, (turn, country_name, target, cost_m, desc, dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'military', ?, ?, ?)
                """, (turn, country_name, target, f"MILITARY REINFORCEMENT: {country_name} mobilized combat assets along {target} frontier."))
                conn.commit()
                conn.close()

            return True, f"MILITARY POSTURE TRANSMITTED: Forward divisions reinforced along {target} frontier (-${cost_m}M, Remaining: ${country['treasury'] - cost_m}M).", None

    def submit_directive(self, country_name: str, action_type: str, cost_m: int, target: str, description: str) -> Tuple[bool, str]:
        action = {
            "type": action_type,
            "cost_m": cost_m,
            "target": target,
            "description": description
        }
        ok, msg, rej = self.execute_structured_action(country_name, action)
        return ok, msg or rej or ""

    def get_pending_directives(self, turn: int, country: Optional[str] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if country:
                cursor.execute("SELECT * FROM pending_directives WHERE turn = ? AND country = ?", (turn, country))
            else:
                cursor.execute("SELECT * FROM pending_directives WHERE turn = ?", (turn,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def submit_turn(self, country_name: str, turn: Optional[int] = None) -> Tuple[bool, str]:
        if turn is None:
            turn = self.get_world_state()["turn"]
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO turn_submissions (turn, country)
                VALUES (?, ?)
                ON CONFLICT(turn, country) DO NOTHING
            """, (turn, country_name))
            conn.commit()
            conn.close()
        return True, f"{country_name} directives officially submitted for Turn {turn}."

    def is_turn_submitted(self, country_name: str, turn: Optional[int] = None) -> bool:
        if turn is None:
            turn = self.get_world_state()["turn"]
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM turn_submissions WHERE turn = ? AND country = ?", (turn, country_name))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0

    def get_directive_count(self, country_name: str, turn: Optional[int] = None) -> int:
        if turn is None:
            turn = self.get_world_state()["turn"]
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pending_directives WHERE country = ? AND turn = ?", (country_name, turn))
            count = cursor.fetchone()[0]
            conn.close()
            return count

    def get_submission_status(self, turn: Optional[int] = None) -> Dict[str, bool]:
        if turn is None:
            turn = self.get_world_state()["turn"]
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT country FROM turn_submissions WHERE turn = ?", (turn,))
            explicit_subs = {r[0] for r in cursor.fetchall()}
            cursor.execute("SELECT DISTINCT country FROM pending_directives WHERE turn = ?", (turn,))
            directive_subs = {r[0] for r in cursor.fetchall()}
            conn.close()
            submitted = explicit_subs.union(directive_subs)
            return {c: (c in submitted) for c in INITIAL_COUNTRIES}

    def add_intel_cable(self, turn: int, recipient: str, target: str, summary: str, apparent_data: str, confidence: str, status: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO intel_cables (turn, recipient, target, intel_summary, apparent_data, confidence_rating, agent_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (turn, recipient, target, summary, apparent_data, confidence, status))
            conn.commit()
            conn.close()

    def get_intel_cables(self, recipient: str) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM intel_cables WHERE recipient = ? ORDER BY id DESC", (recipient,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def add_comm(self, turn: int, channel: str, sender: str, recipient: Optional[str], content: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO comms (turn, channel, sender, recipient, content)
                VALUES (?, ?, ?, ?, ?)
            """, (turn, channel, sender, recipient, content))
            conn.commit()
            conn.close()

    def send_comms(self, channel: str, sender: str, recipient: Optional[str], content: str):
        world = self.get_world_state()
        self.add_comm(world["turn"], channel, sender, recipient, content)

    def get_comms(self, country_name: Optional[str] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if not country_name or country_name == "ALL":
                cursor.execute("SELECT * FROM comms ORDER BY id DESC LIMIT 50")
            else:
                cursor.execute("""
                    SELECT * FROM comms 
                    WHERE channel = 'PUBLIC_UN' OR sender = ? OR recipient = ?
                    ORDER BY id DESC LIMIT 50
                """, (country_name, country_name))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def save_history_mirror(self, year: int, turn: int, real_history: str, sim_history: str, divergence: str, questions: List[str], legacy: Optional[str] = None):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO history_mirror (year, turn, real_history, sim_history, divergence_analysis, discussion_questions, legacy_verdict)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(year) DO UPDATE SET
                    sim_history = excluded.sim_history,
                    divergence_analysis = excluded.divergence_analysis,
                    discussion_questions = excluded.discussion_questions,
                    legacy_verdict = excluded.legacy_verdict
            """, (year, turn, real_history, sim_history, divergence, json.dumps(questions), legacy))
            conn.commit()
            conn.close()

    def get_history_mirror(self, year: int) -> Optional[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history_mirror WHERE year = ?", (year,))
            row = cursor.fetchone()
            conn.close()
            if row:
                res = dict(row)
                res["discussion_questions"] = json.loads(res["discussion_questions"])
                return res
            return None

    def get_all_history_mirrors(self) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history_mirror ORDER BY year ASC")
            rows = cursor.fetchall()
            conn.close()
            out = []
            for r in rows:
                item = dict(r)
                item["discussion_questions"] = json.loads(item["discussion_questions"])
                out.append(item)
            return out

    def add_news(self, turn: int, year: int, headline: str, body: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO news_feed (turn, year, headline, body)
                VALUES (?, ?, ?, ?)
            """, (turn, year, headline, body))
            conn.commit()
            conn.close()

    def get_news(self, limit: int = 15) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM news_feed ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def add_map_event(self, turn: int, event_type: str, src_name: Optional[str], src_lat: Optional[float], src_lon: Optional[float],
                      tgt_name: Optional[str], tgt_lat: Optional[float], tgt_lon: Optional[float], description: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO map_events (turn, event_type, source_name, source_lat, source_lon, target_name, target_lat, target_lon, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (turn, event_type, src_name, src_lat, src_lon, tgt_name, tgt_lat, tgt_lon, description))
            conn.commit()
            conn.close()

    def get_map_events(self, turn: Optional[int] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if turn is not None:
                cursor.execute("SELECT * FROM map_events WHERE turn = ? ORDER BY id DESC", (turn,))
            else:
                cursor.execute("SELECT * FROM map_events ORDER BY id DESC LIMIT 25")
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def apply_turn_deltas(self, updates: Dict[str, Any]):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            for name, c_update in updates.get("countries", {}).items():
                cursor.execute("SELECT * FROM countries WHERE name = ?", (name,))
                row = cursor.fetchone()
                if not row:
                    continue

                new_alignment = max(-1.0, min(1.0, row["alignment"] + c_update.get("alignment_delta", 0.0)))
                new_nuclear = True if c_update.get("nuclear_unlocked") else row["nuclear"]
                new_bombs = max(0, row["bombs"] + c_update.get("bombs_delta", 0))
                new_treasury = max(0, row["treasury"] + c_update.get("treasury_delta", 0))
                new_tension = max(0, min(100, row["tension"] + c_update.get("tension_delta", 0)))

                cursor.execute("""
                    UPDATE countries 
                    SET alignment = ?, nuclear = ?, bombs = ?, treasury = ?, tension = ?
                    WHERE name = ?
                """, (new_alignment, new_nuclear, new_bombs, new_treasury, new_tension, name))

            for name, b_update in updates.get("buffers", {}).items():
                cursor.execute("SELECT * FROM buffer_states WHERE name = ?", (name,))
                row = cursor.fetchone()
                if row:
                    new_align = max(-1.0, min(1.0, row["alignment"] + b_update.get("alignment_delta", 0.0)))
                    cursor.execute("UPDATE buffer_states SET alignment = ? WHERE name = ?", (new_align, name))

            w_update = updates.get("world", {})
            new_defcon = max(1, min(5, w_update.get("defcon", 4)))
            new_tension = max(0, min(100, w_update.get("global_tension", 30)))
            mad_triggered = (new_defcon == 1) or bool(w_update.get("mad_triggered", False))

            cursor.execute("SELECT year, turn FROM world_state WHERE id = 1")
            cur_world = cursor.fetchone()
            current_year = cur_world["year"]
            current_turn = cur_world["turn"]

            next_year = current_year + 1
            next_turn = current_turn + 1
            game_over = mad_triggered or (current_year >= 1953)

            cursor.execute("""
                UPDATE world_state 
                SET year = ?, turn = ?, defcon = ?, global_tension = ?, mad_triggered = ?, game_over = ?, phase = 'DEBRIEF'
                WHERE id = 1
            """, (next_year, next_turn, new_defcon, new_tension, 1 if mad_triggered else 0, 1 if game_over else 0))

            conn.commit()
            conn.close()

        # Execute turn economy, resolve pending UNSC resolutions, and roll random events
        self.execute_turn_economy(current_turn)
        self.resolve_unsc_resolutions(current_turn)
        self.roll_turn_random_events(current_year, current_turn)
        self.activate_crisis_if_due(next_year, next_turn)
