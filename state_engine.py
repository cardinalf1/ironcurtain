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

from objectives_data import LONG_TERM_OBJECTIVES, ANNUAL_OBJECTIVES, COLD_WAR_ERAS, ERA_TERRITORY_DEFAULTS

DB_PATH = os.path.join(os.path.dirname(__file__), "game_state.db")
_db_lock = threading.RLock()

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
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 1,
        "nuclear_progress": 100
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
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 1,
        "nuclear_progress": 30
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
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 0,
        "nuclear_progress": 15
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
        "missile_tech": "STRATEGIC_BOMBERS", "paperclip_scientists": 0,
        "nuclear_progress": 10
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
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0,
        "nuclear_progress": 0
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
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0,
        "nuclear_progress": 0
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
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0,
        "nuclear_progress": 0
    },
    "Cuba": {
        "alignment": -0.2,
        "nuclear": False,
        "bombs": 0,
        "treasury": 100,
        "tension": 20,
        "objective": "Overcome neo-colonial economic subservience, organize revolutionary vanguards, and maintain Caribbean autonomy.",
        "capital": "Havana",
        "lat": 23.11, "lon": -82.36,
        "uranium": 0, "oil": 15, "domestic_approval": 65,
        "missile_tech": "INFANTRY_CORPS", "paperclip_scientists": 0,
        "nuclear_progress": 0
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

COUNTRY_SPECIALTIES = {
    "USA": {
        "title": "The Dollar Arsenal & Marshall Plan",
        "doctrine": "Financial Hegemony, Strategic Deterrence & Global Airlift",
        "description": "Unrivaled industrial output and currency dominance enable massive economic reconstruction programs across Western democracies.",
        "traits": [
            "Economic Aid costs 40% less ($60M vs $100M) and has 1.5x diplomatic alignment shift.",
            "Vast starting Treasury ($2,500M) and top-tier base tax collection ($250M/yr).",
            "Possesses operational atomic weapons deterrence (2 warheads in 1945)."
        ],
        "bonuses": {
            "aid_discount": 0.40,
            "aid_effect_mult": 1.5,
            "offensive_cost": 120,
            "espionage_cost": 45,
            "coup_cost": 60,
            "posture_cost": 50,
            "trade_income_bonus": 0,
            "war_bonds_yield": 150
        }
    },
    "USSR": {
        "title": "KGB Deep Cover & Comintern Subversion",
        "doctrine": "Ideological Subversion, Cambridge Spy Ring & Deep Buffer Defense",
        "description": "Formidable HUMINT penetration of Western institutions and massive Red Army forward armor across Eastern Europe.",
        "traits": [
            "Espionage operations cost 50% less ($20M vs $40M) with superior infiltration fidelity.",
            "Covert Coups in buffer states cost 33% less ($40M vs $60M).",
            "Massive Eurasian land army deterrence; high initial domestic ideological control."
        ],
        "bonuses": {
            "aid_discount": 0.0,
            "aid_effect_mult": 1.0,
            "offensive_cost": 100,
            "espionage_cost": 20,
            "coup_cost": 40,
            "posture_cost": 45,
            "trade_income_bonus": 0,
            "war_bonds_yield": 150
        }
    },
    "United Kingdom": {
        "title": "Bletchley Cryptanalysis & Imperial Diplomacy",
        "doctrine": "Signals Intelligence, Enigma Legacy & Atlantic Alliance Brokerage",
        "description": "Centuries of diplomatic tradecraft and legendary codebreaking give London outsized clandestine reach despite domestic post-war rationing.",
        "traits": [
            "Espionage operations cost 25% less ($30M vs $40M) with higher chance to intercept enemy hotline cables.",
            "UN Security Council resolutions carry priority diplomatic weight.",
            "Paperclip Rocket Scientist recruitment is discounted ($40M vs $50M)."
        ],
        "bonuses": {
            "aid_discount": 0.15,
            "aid_effect_mult": 1.1,
            "offensive_cost": 110,
            "espionage_cost": 30,
            "coup_cost": 55,
            "posture_cost": 45,
            "trade_income_bonus": 5,
            "war_bonds_yield": 150
        }
    },
    "France": {
        "title": "Colonial Sovereignty & Force de Frappe",
        "doctrine": "Gaullist Strategic Autonomy & European Integration",
        "description": "Fiercely protective of sovereign independence, France balances between Anglo-American pressure and European continental leadership.",
        "traits": [
            "Military Posture along borders and contested buffers costs 40% less ($30M vs $50M).",
            "Heightened cultural and diplomatic sway in European buffer negotiations.",
            "Nuclear research reactors receive sovereign subsidy ($90M vs $120M)."
        ],
        "bonuses": {
            "aid_discount": 0.10,
            "aid_effect_mult": 1.0,
            "offensive_cost": 110,
            "espionage_cost": 40,
            "coup_cost": 50,
            "posture_cost": 30,
            "trade_income_bonus": 0,
            "war_bonds_yield": 150
        }
    },
    "China": {
        "title": "People's War & Mass Peasant Mobilization",
        "doctrine": "Asymmetric Guerrilla Warfare & Agrarian Revolution",
        "description": "Inexhaustible manpower reserves and revolutionary fervor allow low-cost military expansion into adjacent Asian frontiers.",
        "traits": [
            "Military Offensives into adjacent Asian territories cost 50% less ($60M vs $120M).",
            "Emergency Sovereign War Bonds yield +$200M cash (vs $150M standard).",
            "Resilient domestic endurance against foreign economic blockades."
        ],
        "bonuses": {
            "aid_discount": 0.0,
            "aid_effect_mult": 0.8,
            "offensive_cost": 60,
            "espionage_cost": 40,
            "coup_cost": 45,
            "posture_cost": 35,
            "trade_income_bonus": 0,
            "war_bonds_yield": 200
        }
    },
    "India": {
        "title": "Non-Aligned Movement & Panchsheel Diplomacy",
        "doctrine": "Non-Alignment, Anti-Colonialism & Moral Mediation",
        "description": "Architect of the Non-Aligned Movement, New Delhi refuses bloc subservience and trades neutrally across both East and West.",
        "traits": [
            "Bilateral Trade Pacts generate +$35M/turn (+$10M non-aligned commerce bonus over standard pacts).",
            "UN Security Council mediation proposals cost $0 and have universal international credibility.",
            "Military offensive aggression costs double ($240M) due to strict non-aggression constitution."
        ],
        "bonuses": {
            "aid_discount": 0.0,
            "aid_effect_mult": 1.2,
            "offensive_cost": 240,
            "espionage_cost": 45,
            "coup_cost": 75,
            "posture_cost": 40,
            "trade_income_bonus": 10,
            "war_bonds_yield": 150
        }
    },
    "Yugoslavia": {
        "title": "Titoist Third Way & Partisan Territorial Defense",
        "doctrine": "Independent Socialism, Balkan Autonomy & Total People's Defense",
        "description": "Having liberated itself from Axis occupation, Yugoslavia defiantly rejects Stalinist diktats while maintaining a rugged partisan defense.",
        "traits": [
            "Border Defense & Military Posture costs 50% less ($25M vs $50M).",
            "Immune to foreign Cominform/bloc sanctions; trades freely with both East and West.",
            "Partisan counter-intelligence: foreign coups and espionage in Yugoslavia suffer higher failure rates."
        ],
        "bonuses": {
            "aid_discount": 0.0,
            "aid_effect_mult": 1.0,
            "offensive_cost": 100,
            "espionage_cost": 35,
            "coup_cost": 50,
            "posture_cost": 25,
            "trade_income_bonus": 5,
            "war_bonds_yield": 150
        }
    },
    "Cuba": {
        "title": "Caribbean Vanguard & Strategic Resource Export",
        "doctrine": "Island Bastion, Maritime Geography & Sugar Diplomacy",
        "description": "Controlling vital Caribbean shipping lanes, Cuba leverages strategic commodity exports and revolutionary covert logistics.",
        "traits": [
            "Commodity Exports (Sugar, Nickel) yield +$45M immediate cash (vs $30M standard).",
            "Covert revolutionary operations in the Caribbean/Latin America cost 40% less ($35M vs $60M).",
            "Strategic alliances yield high economic subsidies."
        ],
        "bonuses": {
            "aid_discount": 0.0,
            "aid_effect_mult": 1.0,
            "offensive_cost": 90,
            "espionage_cost": 35,
            "coup_cost": 35,
            "posture_cost": 35,
            "trade_income_bonus": 5,
            "war_bonds_yield": 150
        }
    }
}


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

    def _init_db(self, force_reset: bool = False, student_countries: Optional[List[str]] = None):
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
                cursor.execute("DROP TABLE IF EXISTS territory_control")
                cursor.execute("DROP TABLE IF EXISTS country_annual_objectives")
                cursor.execute("DROP TABLE IF EXISTS annual_world_events")
                cursor.execute("DROP TABLE IF EXISTS un_conferences")
                cursor.execute("DROP TABLE IF EXISTS un_conference_speeches")
                cursor.execute("DROP TABLE IF EXISTS nuclear_strikes_log")

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
                    paperclip_scientists INTEGER DEFAULT 0,
                    nuclear_progress INTEGER DEFAULT 0,
                    controller TEXT DEFAULT 'STUDENT',
                    long_term_objective TEXT DEFAULT ''
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
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN nuclear_progress INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN controller TEXT DEFAULT 'STUDENT'")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE countries ADD COLUMN long_term_objective TEXT DEFAULT ''")
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

            # Bilateral Pact Proposals (Red Phone Treaties & Loans)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pact_proposals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    proposer TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    proposal_type TEXT NOT NULL,
                    terms_json TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Known Intelligence telemetry cache (Fog-of-War ground truth snapshot when spies deployed)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS known_intelligence (
                    viewer_country TEXT NOT NULL,
                    target_country TEXT NOT NULL,
                    last_updated_turn INTEGER NOT NULL,
                    bombs INTEGER,
                    treasury INTEGER,
                    nuclear BOOLEAN,
                    PRIMARY KEY (viewer_country, target_country)
                )
            """)

            # Dynamic Territory Control & Moving Borders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS territory_control (
                    territory_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    iso_code TEXT,
                    original_owner TEXT NOT NULL,
                    current_controller TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'SOVEREIGN',
                    alignment REAL NOT NULL DEFAULT 0.0,
                    military_garrison INTEGER DEFAULT 0,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL
                )
            """)

            # Country Annual Objectives (1945–1953) & Grading
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS country_annual_objectives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    turn INTEGER NOT NULL,
                    country TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    target TEXT,
                    threshold REAL,
                    weight INTEGER NOT NULL DEFAULT 10,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    score INTEGER NOT NULL DEFAULT 0,
                    evaluation_notes TEXT DEFAULT '',
                    is_dynamic BOOLEAN DEFAULT 0
                )
            """)

            # Annual World Events (Contextual Shocks at the start of each year)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS annual_world_events (
                    year INTEGER PRIMARY KEY,
                    turn INTEGER NOT NULL,
                    headline TEXT NOT NULL,
                    briefing TEXT NOT NULL,
                    historical_baseline TEXT NOT NULL,
                    affected_theaters TEXT NOT NULL,
                    impact_tension INTEGER NOT NULL DEFAULT 0
                )
            """)

            # UN General Assembly & Security Council Conferences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS un_conferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    agenda TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'IN_SESSION',
                    ruling TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS un_conference_speeches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conference_id INTEGER NOT NULL,
                    country TEXT NOT NULL,
                    speech_text TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Nuclear Detonations & Strikes Log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nuclear_strikes_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    attacker TEXT NOT NULL,
                    target TEXT NOT NULL,
                    target_lat REAL NOT NULL,
                    target_lon REAL NOT NULL,
                    damage_description TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                    ctrl = "STUDENT"
                    if student_countries is not None:
                        ctrl = "STUDENT" if name in student_countries else "AI"
                    lt_obj = LONG_TERM_OBJECTIVES.get(name, {})
                    lt_desc = f"{lt_obj.get('title', '')}: {lt_obj.get('description', '')}" if lt_obj else ""

                    cursor.execute("""
                        INSERT INTO countries (name, alignment, nuclear, bombs, treasury, tension, objective, capital, lat, lon, uranium, oil, domestic_approval, missile_tech, paperclip_scientists, nuclear_progress, controller, long_term_objective)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, data["alignment"], data["nuclear"], data["bombs"], data["treasury"], data["tension"],
                          data["objective"], data["capital"], data["lat"], data["lon"],
                          data["uranium"], data["oil"], data["domestic_approval"], data["missile_tech"], data["paperclip_scientists"], data.get("nuclear_progress", 0),
                          ctrl, lt_desc))

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

            # Seed territory control if empty
            cursor.execute("SELECT COUNT(*) FROM territory_control")
            if cursor.fetchone()[0] == 0:
                initial_territories = [
                    ("India", "British Raj (Crown Colony)", "IND", "India", "United Kingdom", "COLONY_TRANSITION", 0.4, 4, 28.61, 77.2),
                    ("KOR_SOUTH", "US Army Military Zone (Korea)", "KOR", "Korea", "USA", "OCCUPIED", 0.6, 3, 37.56, 126.97),
                    ("KOR_NORTH", "Soviet Civil Administration (Korea)", "PRK", "Korea", "USSR", "OCCUPIED", -0.6, 3, 39.03, 125.75),
                    ("GER_WEST", "Western Allied Zones (Germany)", "DEU", "Germany", "USA", "OCCUPIED", 0.8, 5, 50.73, 7.1),
                    ("GER_EAST", "Soviet Occupation Zone (Germany)", "DDR", "Germany", "USSR", "OCCUPIED", -0.8, 5, 52.52, 13.4),
                    ("Vietnam", "French Indochina", "VNM", "Vietnam", "France", "OCCUPIED", 0.5, 3, 21.02, 105.83),
                    ("POLAND", "Poland", "POL", "Poland", "Poland", "SOVEREIGN", -0.7, 2, 52.23, 21.01),
                    ("GREECE", "Greece", "GRC", "Greece", "Greece", "SOVEREIGN", 0.2, 1, 37.98, 23.72),
                    ("TURKEY", "Turkey", "TUR", "Turkey", "Turkey", "SOVEREIGN", 0.3, 1, 39.93, 32.85),
                    ("IRAN", "Iran", "IRN", "Iran", "Iran", "SOVEREIGN", 0.0, 1, 35.68, 51.38),
                    ("JAPAN", "Japan", "JPN", "Japan", "Japan", "SOVEREIGN", 0.6, 2, 35.68, 139.69),
                    ("USA", "USA", "USA", "USA", "USA", "SOVEREIGN", 1.0, 5, 38.9, -77.0),
                    ("USSR", "USSR", "RUS", "USSR", "USSR", "SOVEREIGN", -1.0, 5, 55.75, 37.62),
                    ("United Kingdom", "United Kingdom", "GBR", "United Kingdom", "United Kingdom", "SOVEREIGN", 0.7, 3, 51.5, -0.12),
                    ("France", "France", "FRA", "France", "France", "SOVEREIGN", 0.4, 2, 48.85, 2.35),
                    ("China", "China", "CHN", "China", "China", "SOVEREIGN", -0.3, 4, 39.9, 116.4),
                    ("Yugoslavia", "Yugoslavia", "YUG", "Yugoslavia", "Yugoslavia", "SOVEREIGN", -0.6, 2, 44.78, 20.44),
                    ("Cuba", "Cuba", "CUB", "Cuba", "Cuba", "SOVEREIGN", 0.7, 1, 23.11, -82.36),
                ]
                for t in initial_territories:
                    cursor.execute("""
                        INSERT INTO territory_control (territory_id, name, iso_code, original_owner, current_controller, status, alignment, military_garrison, lat, lon)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, t)

            # Seed annual world events from COLD_WAR_ERAS if empty
            cursor.execute("SELECT COUNT(*) FROM annual_world_events")
            if cursor.fetchone()[0] == 0:
                for era_id, era in COLD_WAR_ERAS.items():
                    fp = era.get("flashpoint", {})
                    cursor.execute("""
                        INSERT INTO annual_world_events (year, turn, headline, briefing, historical_baseline, affected_theaters, impact_tension)
                        VALUES (?, ?, ?, ?, ?, ?, 0)
                    """, (era["year_start"], era_id, fp.get("headline", era["title"]), fp.get("briefing", era["summary"]), fp.get("historical_baseline", era["theme"]), fp.get("affected_theaters", "Global")))

            # Seed annual objectives from objectives_data if empty
            cursor.execute("SELECT COUNT(*) FROM country_annual_objectives")
            if cursor.fetchone()[0] == 0:
                for era_id, c_dict in ANNUAL_OBJECTIVES.items():
                    era_data = COLD_WAR_ERAS.get(era_id, {})
                    yr_start = era_data.get("year_start", 1945)
                    for c_name, obj_list in c_dict.items():
                        if isinstance(obj_list, dict):
                            obj_list = [obj_list]
                        for obj in obj_list:
                            cursor.execute("""
                                INSERT INTO country_annual_objectives (year, turn, country, title, description, metric_type, target, threshold, weight, status, score)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', 0)
                            """, (yr_start, era_id, c_name, obj["title"], obj["description"], obj["metric_type"], obj.get("target"), obj.get("threshold"), obj.get("weight", 10)))

            # Populate long-term objectives and controllers on countries
            for c_name, lt_obj in LONG_TERM_OBJECTIVES.items():
                desc_text = f"{lt_obj['title']}: {lt_obj['description']}"
                ctrl = "STUDENT"
                if student_countries is not None:
                    ctrl = "STUDENT" if c_name in student_countries else "AI"
                cursor.execute("""
                    UPDATE countries 
                    SET long_term_objective = ?, controller = ?
                    WHERE name = ?
                """, (desc_text, ctrl, c_name))

            conn.commit()
            conn.close()

    def reset_game(self, student_countries: Optional[List[str]] = None):
        self._init_db(force_reset=True, student_countries=student_countries)

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
    # DYNAMIC TERRITORY CONTROL & SHIFTING BORDERS
    # =========================================================================
    def get_territories(self) -> Dict[str, Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM territory_control")
            rows = cursor.fetchall()
            conn.close()
            return {r["territory_id"]: dict(r) for r in rows}

    def get_territory(self, territory_id: str) -> Optional[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM territory_control WHERE territory_id = ? OR name = ? OR iso_code = ?", (territory_id, territory_id, territory_id))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None

    def set_territory_controller(self, territory_id: str, controller: str, status: str = "OCCUPIED", alignment: Optional[float] = None):
        with _db_lock:
            conn = self._get_connection()
            if alignment is not None:
                conn.execute("""
                    UPDATE territory_control 
                    SET current_controller = ?, status = ?, alignment = ?
                    WHERE territory_id = ? OR name = ? OR iso_code = ?
                """, (controller, status, alignment, territory_id, territory_id, territory_id))
            else:
                conn.execute("""
                    UPDATE territory_control 
                    SET current_controller = ?, status = ?
                    WHERE territory_id = ? OR name = ? OR iso_code = ?
                """, (controller, status, territory_id, territory_id, territory_id))
            conn.commit()
            conn.close()

    def occupy_territory(self, territory_name_or_id: str, occupier: str):
        """Transfers control of a territory to an invading or occupying power."""
        t = self.get_territory(territory_name_or_id)
        if not t:
            return
        target_id = t["territory_id"]
        c = self.get_country(occupier)
        new_align = c["alignment"] if c else 0.0
        self.set_territory_controller(target_id, occupier, status="OCCUPIED", alignment=new_align)
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE buffer_states SET alignment = ? WHERE name = ?", (new_align, t["name"]))
            conn.commit()
            conn.close()

    def partition_territory(self, parent_name: str, part_a_id: str, part_a_name: str, part_a_iso: str, part_a_controller: str, part_a_align: float,
                            part_b_id: str, part_b_name: str, part_b_iso: str, part_b_controller: str, part_b_align: float):
        """Formally partitions a country into two separate sovereign or occupied entities."""
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO territory_control (territory_id, name, iso_code, original_owner, current_controller, status, alignment, military_garrison, lat, lon)
                VALUES (?, ?, ?, ?, ?, 'PARTITIONED', ?, 2, 0, 0)
                ON CONFLICT(territory_id) DO UPDATE SET 
                    name=excluded.name, iso_code=excluded.iso_code, current_controller=excluded.current_controller,
                    status='PARTITIONED', alignment=excluded.alignment
            """, (part_a_id, part_a_name, part_a_iso, parent_name, part_a_controller, part_a_align))
            conn.execute("""
                INSERT INTO territory_control (territory_id, name, iso_code, original_owner, current_controller, status, alignment, military_garrison, lat, lon)
                VALUES (?, ?, ?, ?, ?, 'PARTITIONED', ?, 2, 0, 0)
                ON CONFLICT(territory_id) DO UPDATE SET 
                    name=excluded.name, iso_code=excluded.iso_code, current_controller=excluded.current_controller,
                    status='PARTITIONED', alignment=excluded.alignment
            """, (part_b_id, part_b_name, part_b_iso, parent_name, part_b_controller, part_b_align))
            conn.commit()
            conn.close()

    def apply_era_boundaries_db(self, cursor, era_id: int):
        """Applies era-specific dynamic shifting boundaries, decolonization, and partitions."""
        defaults = ERA_TERRITORY_DEFAULTS.get(era_id, {})
        for t_id, data in defaults.items():
            cursor.execute("SELECT status, current_controller FROM territory_control WHERE territory_id = ? OR name = ?", (t_id, t_id))
            row = cursor.fetchone()
            if row:
                cursor.execute("""
                    UPDATE territory_control 
                    SET current_controller = ?, status = ?, alignment = ?, name = COALESCE(?, name)
                    WHERE territory_id = ? OR name = ?
                """, (data["current_controller"], data["status"], data["alignment"], data.get("name"), t_id, t_id))
            else:
                cursor.execute("""
                    INSERT INTO territory_control (territory_id, name, iso_code, original_owner, current_controller, status, alignment, military_garrison, lat, lon)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (t_id, data.get("name", t_id), data.get("iso_code", t_id[:3]), t_id, data["current_controller"], data["status"], data["alignment"], data.get("military_garrison", 2), 50.0, 10.0))

    def apply_era_boundaries(self, era_id: int):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            self.apply_era_boundaries_db(cursor, era_id)
            conn.commit()
            conn.close()

    # =========================================================================
    # ANNUAL & LONG-TERM OBJECTIVES AND GRADING SYSTEM
    # =========================================================================
    def get_country_objectives(self, country: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            if year is not None:
                cursor.execute("""
                    SELECT * FROM country_annual_objectives 
                    WHERE country = ? AND (year = ? OR turn = ?) 
                    ORDER BY id ASC
                """, (country, year, year))
            else:
                cursor.execute("SELECT * FROM country_annual_objectives WHERE country = ? ORDER BY turn ASC, id ASC", (country,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def set_country_controller(self, country: str, controller: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE countries SET controller = ? WHERE name = ?", (controller, country))
            conn.commit()
            conn.close()

    def get_country_controllers(self) -> Dict[str, str]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, controller FROM countries")
            rows = cursor.fetchall()
            conn.close()
            return {r["name"]: r["controller"] for r in rows}

    def evaluate_turn_objectives(self, turn: int, year: int):
        """Evaluates completion of country annual objectives for the concluded year/turn."""
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM country_annual_objectives WHERE year = ? OR turn = ?", (year, turn))
            objs = cursor.fetchall()

            cursor.execute("SELECT defcon, global_tension FROM world_state WHERE id = 1")
            w_row = cursor.fetchone()
            cur_defcon = w_row["defcon"] if w_row else 4

            for obj in objs:
                c_name = obj["country"]
                cursor.execute("SELECT * FROM countries WHERE name = ?", (c_name,))
                c_data = cursor.fetchone()
                if not c_data:
                    continue

                m_type = obj["metric_type"]
                weight = obj["weight"]
                target = obj["target"]
                threshold = obj["threshold"]

                status = "PARTIAL"
                score = weight // 2
                notes = "Moderate progress toward national objective."

                if m_type == "DETERRENCE_STABILITY":
                    if c_data["nuclear"] and cur_defcon >= 3:
                        status = "COMPLETED"
                        score = weight
                        notes = "Atomic deterrence maintained without global war."
                    elif cur_defcon >= 3:
                        status = "COMPLETED"
                        score = weight
                        notes = "Global stability sustained under diplomatic deterrence."
                    else:
                        status = "PARTIAL"
                        score = weight // 2
                        notes = "Tension destabilized strategic security."

                elif m_type == "BUFFER_ALIGNMENT" and target:
                    cursor.execute("SELECT alignment FROM buffer_states WHERE name = ?", (target,))
                    b_row = cursor.fetchone()
                    if b_row:
                        b_align = b_row["alignment"]
                        expected_sign = 1 if c_data["alignment"] >= 0 else -1
                        if expected_sign * b_align >= 0.2:
                            status = "COMPLETED"
                            score = weight
                            notes = f"Successfully aligned {target} with national bloc."
                        elif expected_sign * b_align >= -0.2:
                            status = "PARTIAL"
                            score = weight // 2
                            notes = f"{target} remains fiercely contested."
                        else:
                            status = "FAILED"
                            score = 0
                            notes = f"{target} has slipped into the rival sphere of influence."

                elif m_type == "TREASURY_SOLVENCY":
                    thresh = threshold or 300
                    if c_data["treasury"] >= thresh:
                        status = "COMPLETED"
                        score = weight
                        notes = f"Treasury reserves (${c_data['treasury']}M) surpassed target solvency (${int(thresh)}M)."
                    elif c_data["treasury"] >= thresh * 0.7:
                        status = "PARTIAL"
                        score = weight // 2
                        notes = f"Treasury (${c_data['treasury']}M) strained under deficit spending."
                    else:
                        status = "FAILED"
                        score = 0
                        notes = f"Severe financial exhaustion (${c_data['treasury']}M) below minimum stability."

                elif m_type == "DOMESTIC_APPROVAL":
                    thresh = threshold or 70
                    if c_data["domestic_approval"] >= thresh:
                        status = "COMPLETED"
                        score = weight
                        notes = f"Domestic approval ({c_data['domestic_approval']}%) remains robust."
                    elif c_data["domestic_approval"] >= thresh * 0.75:
                        status = "PARTIAL"
                        score = weight // 2
                        notes = f"Domestic discontent emerging ({c_data['domestic_approval']}% approval)."
                    else:
                        status = "FAILED"
                        score = 0
                        notes = f"Severe domestic unrest ({c_data['domestic_approval']}% approval) threatens governance."

                elif m_type in ["NUCLEAR_DETERRENCE", "NUCLEAR_R_D"]:
                    if c_data["nuclear"] or c_data["nuclear_progress"] >= 60:
                        status = "COMPLETED"
                        score = weight
                        notes = f"Nuclear weapon project capability secured ({c_data['bombs']} bombs, {c_data['nuclear_progress']}% R&D)."
                    else:
                        status = "PARTIAL"
                        score = weight // 2
                        notes = f"Nuclear research underway ({c_data['nuclear_progress']}% progress)."

                elif m_type == "AVOID_DEFCON_1":
                    if cur_defcon > 1:
                        status = "COMPLETED"
                        score = weight
                        notes = "Averted DEFCON 1 nuclear apocalypse."
                    else:
                        status = "FAILED"
                        score = 0
                        notes = "World has collapsed into DEFCON 1 nuclear crisis."

                elif m_type in ["TERRITORIAL_CONTROL", "TERRITORIAL_DEFENSE"]:
                    status = "COMPLETED"
                    score = weight
                    notes = "National territorial integrity preserved."

                else:
                    status = "COMPLETED"
                    score = weight
                    notes = "Strategic milestone accomplished."

                cursor.execute("""
                    UPDATE country_annual_objectives
                    SET status = ?, score = ?, evaluation_notes = ?
                    WHERE id = ?
                """, (status, score, notes, obj["id"]))

            conn.commit()
            conn.close()

    def get_final_gradebook(self) -> Dict[str, Dict[str, Any]]:
        """Generates comprehensive end-game grading report cards for all countries."""
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM countries")
            c_rows = cursor.fetchall()

            gradebook = {}
            for c in c_rows:
                c_name = c["name"]
                cursor.execute("SELECT SUM(score) as earned, SUM(weight) as total FROM country_annual_objectives WHERE country = ?", (c_name,))
                sc = cursor.fetchone()
                earned = sc["earned"] or 0
                total = sc["total"] or 100

                lt_bonus = 0
                if c["treasury"] >= 200:
                    lt_bonus += 5
                if c["domestic_approval"] >= 65:
                    lt_bonus += 5
                if c["nuclear"] or c["alignment"] != 0:
                    lt_bonus += 5
                cursor.execute("SELECT defcon FROM world_state WHERE id = 1")
                defcon_row = cursor.fetchone()
                if defcon_row and defcon_row["defcon"] >= 2:
                    lt_bonus += 5

                final_score = min(100, int((earned / max(1, total)) * 80) + lt_bonus)

                if final_score >= 90:
                    letter = "A+"
                    verdict = "Historic Triumph: Exemplary Cold War statecraft, strategic deterrence, and national prestige."
                elif final_score >= 80:
                    letter = "A"
                    verdict = "Distinguished Leadership: Met primary national objectives and safeguarded sovereign lifelines."
                elif final_score >= 70:
                    letter = "B"
                    verdict = "Competent Governance: Navigated superpower crises with moderate compromises and economic strains."
                elif final_score >= 55:
                    letter = "C"
                    verdict = "Troubled Tenure: Domestic discontent and territorial friction compromised national standing."
                else:
                    letter = "F"
                    verdict = "Strategic Collapse: Failed critical annual objectives, incurring severe crises and international isolation."

                gradebook[c_name] = {
                    "letter_grade": letter,
                    "final_score": final_score,
                    "annual_earned": earned,
                    "annual_total": total,
                    "long_term_bonus": lt_bonus,
                    "verdict": verdict,
                    "controller": c["controller"],
                    "long_term_objective": c["long_term_objective"]
                }
            conn.close()
            return gradebook

    # =========================================================================
    # ANNUAL WORLD SHOCKS & FLASHPOINTS
    # =========================================================================
    def get_annual_world_event(self, year_or_turn: int) -> Optional[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM annual_world_events WHERE year = ? OR turn = ? ORDER BY year DESC LIMIT 1", (year_or_turn, year_or_turn))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None

    def set_annual_world_event(self, year: int, turn: int, headline: str, briefing: str, historical_baseline: str, affected_theaters: str, impact_tension: int = 0):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO annual_world_events (year, turn, headline, briefing, historical_baseline, affected_theaters, impact_tension)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(year) DO UPDATE SET 
                    headline=excluded.headline, briefing=excluded.briefing, historical_baseline=excluded.historical_baseline,
                    affected_theaters=excluded.affected_theaters, impact_tension=excluded.impact_tension
            """, (year, turn, headline, briefing, historical_baseline, affected_theaters, impact_tension))
            conn.commit()
            conn.close()

    # =========================================================================
    # UN SECRETARY-GENERAL / DUNGEON MASTER ADMIN CONSOLE
    # =========================================================================
    def convene_un_conference(self, year: int, title: str, agenda: str) -> int:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT turn FROM world_state WHERE id = 1")
            turn = cursor.fetchone()["turn"]
            cursor.execute("""
                INSERT INTO un_conferences (turn, year, title, agenda, status)
                VALUES (?, ?, ?, ?, 'IN_SESSION')
            """, (turn, year, title, agenda))
            conf_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return conf_id

    def get_active_un_conference(self) -> Optional[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM un_conferences WHERE status = 'IN_SESSION' ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None

    def submit_conference_speech(self, conference_id: int, country: str, speech_text: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO un_conference_speeches (conference_id, country, speech_text)
                VALUES (?, ?, ?)
            """, (conference_id, country, speech_text))
            conn.commit()
            conn.close()

    def get_conference_speeches(self, conference_id: int) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM un_conference_speeches WHERE conference_id = ? ORDER BY id ASC", (conference_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def adjourn_conference(self, conference_id: int, ruling: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("""
                UPDATE un_conferences 
                SET status = 'ADJOURNED', ruling = ?
                WHERE id = ?
            """, (ruling, conference_id))
            conn.commit()
            conn.close()

    def admin_set_defcon(self, defcon: int):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE world_state SET defcon = ? WHERE id = 1", (max(1, min(5, defcon)),))
            conn.commit()
            conn.close()

    def admin_set_tension(self, tension: int):
        with _db_lock:
            conn = self._get_connection()
            t = max(0, min(100, tension))
            conn.execute("UPDATE world_state SET global_tension = ? WHERE id = 1", (t,))
            cursor = conn.cursor()
            self._sync_defcon(cursor)
            conn.commit()
            conn.close()

    def admin_enforce_ceasefire(self, target: str):
        """Imposes an immediate UN Peacekeeping ceasefire and resets tension on the target."""
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT turn, year FROM world_state WHERE id = 1")
            w = cursor.fetchone()
            conn.execute("UPDATE world_state SET global_tension = MAX(10, global_tension - 15) WHERE id = 1")
            self._sync_defcon(cursor)
            conn.execute("""
                INSERT INTO news_feed (turn, year, headline, body)
                VALUES (?, ?, 'UN ENFORCES BINDING ARMED CEASEFIRE', ?)
            """, (w["turn"], w["year"], f"UN Emergency Peacekeeping Resolution dispatched 'Blue Helmets' to enforce immediate demilitarization around {target}."))
            conn.commit()
            conn.close()

    def admin_transfer_territory(self, territory_id: str, new_controller: str):
        self.occupy_territory(territory_id, new_controller)

    def admin_inject_aid(self, country: str, amount_m: int):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE countries SET treasury = treasury + ? WHERE name = ?", (amount_m, country))
            conn.commit()
            conn.close()

    def admin_impose_sanctions(self, country: str):
        with _db_lock:
            conn = self._get_connection()
            conn.execute("UPDATE countries SET treasury = MAX(0, treasury - 50), tension = MIN(100, tension + 10) WHERE name = ?", (country,))
            conn.commit()
            conn.close()

    # =========================================================================
    # NUCLEAR DETONATIONS LOG & NON-TERMINAL DEFCON 1
    # =========================================================================
    def record_nuclear_strike(self, attacker: str, target: str, target_lat: float, target_lon: float, damage_desc: str):
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT turn, year FROM world_state WHERE id = 1")
            w = cursor.fetchone()
            cursor.execute("""
                INSERT INTO nuclear_strikes_log (turn, year, attacker, target, target_lat, target_lon, damage_description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (w["turn"], w["year"], attacker, target, target_lat, target_lon, damage_desc))
            cursor.execute("UPDATE world_state SET defcon = 1, global_tension = 100, mad_triggered = 1 WHERE id = 1")
            conn.commit()
            conn.close()

    def get_nuclear_strikes(self) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nuclear_strikes_log ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            return [dict(r) for r in rows]

    def _detect_escalation_instigator_db(self, cursor, turn: int) -> Optional[str]:
        """Identifies the country that submitted the most provocative action leading to a DEFCON escalation."""
        cursor.execute("""
            SELECT country, action_type FROM pending_directives 
            WHERE turn = ?
            ORDER BY 
                CASE 
                    WHEN action_type IN ('NUCLEAR_STRIKE', 'DETONATE') THEN 1
                    WHEN action_type IN ('MILITARY_OFFENSIVE', 'INVASION', 'ATTACK') THEN 2
                    WHEN action_type IN ('COVERT_COUP', 'COUP') THEN 3
                    WHEN action_type IN ('MILITARY_POSTURE') THEN 4
                    ELSE 5
                END ASC
            LIMIT 1
        """, (turn,))
        row = cursor.fetchone()
        return row["country"] if row else None

    def _apply_escalation_debuff_db(self, cursor, instigator: str, old_defcon: int, new_defcon: int, turn: int, year: int):
        """Applies severe economic, domestic, and diplomatic debuffs to the country causing a DEFCON alert increase."""
        cursor.execute("""
            UPDATE countries 
            SET treasury = MAX(0, treasury - 60), 
                domestic_approval = MAX(10, domestic_approval - 15),
                tension = MIN(100, tension + 15)
            WHERE name = ?
        """, (instigator,))

        cursor.execute("SELECT alignment FROM countries WHERE name = ?", (instigator,))
        c_row = cursor.fetchone()
        if c_row:
            inst_align = c_row["alignment"]
            shift = -0.15 if inst_align >= 0 else 0.15
            cursor.execute("UPDATE buffer_states SET alignment = MAX(-1.0, MIN(1.0, alignment + ?))", (shift,))

        headline = f"DEFCON {new_defcon} ALERT: {instigator.upper()} BLAMED FOR GLOBAL ESCALATION"
        body = (f"Aggressive military maneuvers by {instigator} have dropped world alert to DEFCON {new_defcon}! "
                f"Emergency international economic sanctions imposed (-$60M), domestic anti-war strikes erupt, "
                f"and neutral buffer states recoil from {instigator}'s sphere of influence.")
        cursor.execute("""
            INSERT INTO news_feed (turn, year, headline, body)
            VALUES (?, ?, ?, ?)
        """, (turn, year, headline, body))

    def _check_and_log_nuclear_strikes_db(self, cursor, turn: int, year: int) -> bool:
        """Inspects directives to log any nuclear strikes executed during the turn."""
        cursor.execute("""
            SELECT country, target, description, action_type FROM pending_directives 
            WHERE turn = ?
        """, (turn,))
        all_dirs = cursor.fetchall()
        strikes = []
        for d in all_dirs:
            desc = (d["description"] or "").lower()
            act = (d["action_type"] or "").upper()
            if act in ('NUCLEAR_STRIKE', 'DETONATE', 'ATOMIC_ATTACK') or ('atomic strike' in desc or 'nuclear strike' in desc or ('launch' in desc and 'atomic' in desc)):
                strikes.append(d)

        for s in strikes:
            tgt = s["target"]
            # Look up target coords
            cursor.execute("SELECT lat, lon FROM countries WHERE name = ?", (tgt,))
            loc = cursor.fetchone()
            if not loc:
                cursor.execute("SELECT lat, lon FROM buffer_states WHERE name = ?", (tgt,))
                loc = cursor.fetchone()
            lat = loc["lat"] if loc else 50.0
            lon = loc["lon"] if loc else 10.0

            cursor.execute("""
                INSERT INTO nuclear_strikes_log (turn, year, attacker, target, target_lat, target_lon, damage_description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (turn, year, s["country"], tgt, lat, lon, f"Strategic atomic strike detonated over {tgt}. Extreme blast destruction and radiation fallout."))

            # Target suffers massive infrastructure damage
            cursor.execute("""
                UPDATE countries 
                SET treasury = MAX(0, treasury * 0.4),
                    domestic_approval = MAX(10, domestic_approval - 30),
                    tension = 100
                WHERE name = ?
            """, (tgt,))
        return len(strikes) > 0

    def _sync_defcon(self, cursor):
        """Dynamically synchronize world_state.defcon based on global_tension."""
        cursor.execute("SELECT global_tension FROM world_state WHERE id = 1")
        row = cursor.fetchone()
        if row:
            t = row[0]
            if t >= 85: d = 1
            elif t >= 65: d = 2
            elif t >= 45: d = 3
            elif t >= 25: d = 4
            else: d = 5
            cursor.execute("UPDATE world_state SET defcon = ? WHERE id = 1", (d,))

    def get_action_cost(self, country_name: str, action_type: str, target: Optional[str] = None) -> int:
        """Computes tailored action costs based on Cold War country specialties and target friction."""
        specialty = COUNTRY_SPECIALTIES.get(country_name, {})
        bonuses = specialty.get("bonuses", {})
        act = (action_type or "").upper()

        if act in ["ESPIONAGE", "ESPIONAGE_DEPLOY", "SPY"]:
            cost = bonuses.get("espionage_cost", 40)
        elif act in ["MILITARY_OFFENSIVE", "INVASION", "ATTACK", "OFFENSIVE", "MILITARY_STRIKE", "WAR"]:
            cost = bonuses.get("offensive_cost", 120)
        elif act in ["ECONOMIC_AID", "AID", "LOAN", "FOREIGN_AID", "MARSHALL_PLAN"]:
            cost = int(100 * (1.0 - bonuses.get("aid_discount", 0.0)))

        elif act in ["COVERT_COUP", "COUP", "INSURGENCY"]:
            cost = bonuses.get("coup_cost", 60)
        elif act in ["MILITARY_POSTURE", "POSTURE", "DEFENSE_LINE"]:
            cost = bonuses.get("posture_cost", 50)
        elif act in ["NUCLEAR_EXPANSION", "BUILD_BOMB", "BUILD_BOMBS"]:
            cost = 80
        elif act in ["NUCLEAR_RESEARCH"]:
            cost = 90 if country_name == "France" else 120
        elif act in ["PAPERCLIP_RECRUIT", "MISSILE_RESEARCH"]:
            cost = 40 if country_name == "United Kingdom" else 50
        elif act in ["WAR_BONDS", "BONDS"]:
            cost = 0
        else:
            cost = 0

        # Adjust for target stance if target is known
        if target and target != country_name:
            stances = {s["to_country"]: s["stance"] for s in self.get_stances(country_name)}
            target_stance = stances.get(target, "Neutral")
            if target_stance == "Enemy" and act in ["MILITARY_OFFENSIVE", "COVERT_COUP"]:
                cost = int(cost * 1.15)
        return max(0, cost)

    # =========================================================================
    # CLASSIFIED INTELLIGENCE DOSSIER (FOG-OF-WAR ENGINE)
    # =========================================================================
    def get_country_dossier(self, viewer_country: str, target_name: str) -> Dict[str, Any]:
        """
        Generates Palantir C2 classified intelligence dossier on the target territory/country.
        Information accuracy and detail are strictly filtered through intelligence confidence:
        - Self or Ally: Confirmed (100% ground truth NOFORN)
        - Active Spy Asset: High (85% precision with small HUMINT margin)
        - No Active Spy: Crude, inaccurate, noisy estimates based on rumors/whispers with explicit warnings.
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
            bombs_text = f"{country['bombs']} Warheads (VERIFIED AUDITED)"
            treasury_text = f"${country['treasury']}M (AUDITED)"
            uranium_text = f"{country['uranium']} MT Fissile Grade"
            oil_text = f"{country['oil']}% Strategic Reserves"
            approval_text = f"{country['domestic_approval']}% Stability"
            nuke_status = "CONFIRMED // ATOMIC CAPABLE" if country["nuclear"] else "CONFIRMED // CONVENTIONAL ONLY"
            missile_status = country["missile_tech"]
        elif has_spy:
            conf_label = "CONFIRMED // ACTIVE HUMINT SPY NETWORK"
            conf_pct = 85
            # Small jitter for realistic field reporting
            delta = secrets.choice([-1, 0, 1]) if country["bombs"] > 0 else 0
            est_b = max(0, country["bombs"] + delta)
            t_jitter = secrets.choice([-25, 0, 25])
            est_t = max(20, country["treasury"] + t_jitter)
            bombs_text = f"Est. {est_b} Warheads (±1 Delta, VERIFIED BY ACTIVE SPY NETWORK)"
            treasury_text = f"Est. ${est_t}M (±$25M, Infiltrated Station Reports)"
            uranium_text = f"~{country['uranium']} MT Fissile Ore (Infiltrated Station Reports)"
            oil_text = f"{country['oil']}% Reserves (Verified)"
            approval_text = f"{country['domestic_approval']}% (Verified)"
            nuke_status = "CONFIRMED // ATOMIC CAPABLE" if country["nuclear"] else "CONFIRMED // CONVENTIONAL ONLY"
            missile_status = country["missile_tech"]

            # Save confirmed ground truth snapshot to known_intelligence
            try:
                with _db_lock:
                    c_conn = self._get_connection()
                    c_cur = c_conn.cursor()
                    c_cur.execute("""
                        INSERT OR REPLACE INTO known_intelligence (viewer_country, target_country, last_updated_turn, bombs, treasury, nuclear)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (viewer_country, target_name, self.get_world_state()["turn"], country["bombs"], country["treasury"], country["nuclear"]))
                    c_conn.commit()
                    c_conn.close()
            except Exception:
                pass
        else:
            # NO ACTIVE SPY: Bad, noisy, speculative estimates
            conf_label = "CRUDE ESTIMATE // EMBASSY RUMORS (NO ACTIVE SPY)"
            conf_pct = 20

            if target_name == "USA":
                bombs_text = "Classified // Rumored 0–8 Warheads (Unconfirmed Rumors, NO ACTIVE SPY)"
            elif target_name == "USSR":
                bombs_text = "Unknown // Suspected Atomic Research (Rumored 0–6 Warheads, NO ACTIVE SPY)"
            else:
                bombs_text = "Unconfirmed // Foreign Ministry Assumes 0 Warheads (NO ACTIVE SPY)"

            t_raw = country["treasury"]
            lower_b = max(40, (t_raw // 200) * 150)
            upper_b = max(350, (t_raw // 150) * 200 + 400)
            treasury_text = f"Vague Speculation: ${lower_b}M – ${upper_b}M (Embassy Gossip, NO ACTIVE SPY)"
            uranium_text = "Unmonitored // Ore trade completely unverified (NO ACTIVE SPY)"
            oil_text = "Unverified // Macro trade gossip only (NO ACTIVE SPY)"
            approval_text = "State Secret // Information Blackout (NO ACTIVE SPY)"
            nuke_status = "UNVERIFIED // NO ACTIVE SPY INFILTRATED"
            missile_status = "UNKNOWN // UNVERIFIED LAUNCH CAPABILITY"

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
            "nuclear_status": nuke_status,
            "bombs_display": bombs_text,
            "treasury_display": treasury_text,
            "uranium_display": uranium_text,
            "oil_display": oil_text,
            "approval_display": approval_text,
            "missile_tech": missile_status,
            "has_active_spy": has_spy,
            "intel_source": "ACTIVE_SPY" if has_spy else ("ALLIANCE" if (is_self or bilateral_stance == "Ally") else "RUMORS_NO_SPY"),
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
    # BILATERAL PACTS, SOVEREIGN LOANS & TREATY PROPOSALS (RED PHONE DIPLOMACY)
    # =========================================================================
    def propose_bilateral_pact(self, proposer: str, recipient: str, proposal_type: str, terms: Dict[str, Any], message: str) -> Tuple[bool, str, int]:
        """
        Dispatches formal treaty or financial loan proposal via the Red Phone encrypted channel.
        Cannot take effect until recipient explicitly reviews, confirms, or counters the agreement.
        Returns: (success: bool, status_msg: str, pact_id: int)
        """
        world = self.get_world_state()
        turn = world["turn"]

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()

            if isinstance(terms, dict):
                terms_dict = terms
                terms_str_save = json.dumps(terms)
            else:
                terms_dict = {"description": str(terms)}
                terms_str_save = json.dumps(terms_dict)


            cursor.execute("""
                INSERT INTO pact_proposals (turn, proposer, recipient, proposal_type, terms_json, status, message)
                VALUES (?, ?, ?, ?, ?, 'PENDING', ?)
            """, (turn, proposer, recipient, proposal_type, terms_str_save, message))
            pact_id = cursor.lastrowid

            terms_summary = ""
            if proposal_type == "TRADE_PACT":
                val = terms_dict.get("annual_value", 25)
                terms_summary = f"[TRADE ACCORD: +${val}M/turn each]"
            elif proposal_type in ["FINANCIAL_AID_REQUEST", "SOVEREIGN_LOAN", "FINANCIAL_AID"]:
                amt = terms_dict.get("amount_m", 50)
                terms_summary = f"[FINANCIAL TRANSFER REQUEST: ${amt}M]"
            elif proposal_type in ["ATOMIC_COLLAB", "TECH_TRANSFER", "NUCLEAR_COLLAB"]:
                terms_summary = "[ATOMIC TECHNOLOGY SHARING & REACTOR COLLAB (+50% R&D, +1 MT Uranium)]"
            elif proposal_type == "NON_AGGRESSION":
                terms_summary = "[NON-AGGRESSION & MUTUAL DEFENSE ACCORD]"
            else:
                terms_summary = f"[{proposal_type}]"

            cable_text = f"📜 FORMAL DIPLOMATIC PROPOSAL #{pact_id} {terms_summary}: {message}"
            cursor.execute("""
                INSERT INTO hotline_messages (turn, sender, recipient, content, is_intercepted, intercepted_by, leak_level)
                VALUES (?, ?, ?, ?, 0, NULL, 'NONE')
            """, (turn, proposer, recipient, cable_text))

            conn.commit()
            conn.close()

        return pact_id


    def get_pact_proposals(self, country_name: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM pact_proposals WHERE 1=1"
            params = []
            if country_name:
                query += " AND (recipient = ? OR proposer = ?)"
                params.extend([country_name, country_name])
            if status:
                query += " AND status = ?"
                params.append(status)
            query += " ORDER BY id DESC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            pacts = []
            for r in rows:
                d = dict(r)
                try:
                    d["terms"] = json.loads(d.get("terms_json", "{}"))
                except Exception:
                    d["terms"] = {}
                pacts.append(d)
            return pacts

    def get_pending_pacts_count(self, country_name: str) -> int:
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pact_proposals WHERE recipient = ? AND status = 'PENDING'", (country_name,))
            count = cursor.fetchone()[0]
            conn.close()
            return count

    def respond_to_pact(self, pact_id: int, responder: str, decision: str, response_note: Optional[str] = None) -> Tuple[bool, str]:
        """
        Processes formal response ('ACCEPT' or 'REJECT') to a pending bilateral pact proposal.
        """
        world = self.get_world_state()
        turn = world["turn"]

        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pact_proposals WHERE id = ?", (pact_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False, f"Proposal #{pact_id} not found on diplomatic register."

            pact = dict(row)
            if pact["status"] != "PENDING":
                conn.close()
                return False, f"Proposal #{pact_id} has already been resolved ({pact['status']})."

            if responder != pact["recipient"]:
                conn.close()
                return False, f"Unauthorized: Only {pact['recipient']} leadership can ratify or reject this treaty."

            proposer = pact["proposer"]
            p_type = pact["proposal_type"]
            try:

                terms = json.loads(pact.get("terms_json") or "{}")
            except Exception:
                terms = {}
            if not isinstance(terms, dict):
                terms = {}


            dec = decision.upper()
            if dec in ["REJECT", "REJECTED", "DECLINE", "DECLINED"]:
                cursor.execute("UPDATE pact_proposals SET status = 'REJECTED' WHERE id = ?", (pact_id,))
                decline_msg = response_note or f"{responder} has formally reviewed and declined the terms of Proposal #{pact_id}."
                cursor.execute("""
                    INSERT INTO hotline_messages (turn, sender, recipient, content, is_intercepted, intercepted_by, leak_level)
                    VALUES (?, ?, ?, ?, 0, NULL, 'NONE')
                """, (turn, responder, proposer, f"❌ DIPLOMATIC DECLINE: {decline_msg}"))
                conn.commit()
                conn.close()
                return True, f"Proposal #{pact_id} declined. Diplomatic notification returned to {proposer}."

            elif dec in ["ACCEPT", "ACCEPTED", "RATIFY", "RATIFIED"]:
                cursor.execute("UPDATE pact_proposals SET status = 'ACCEPTED' WHERE id = ?", (pact_id,))


                # Execute specific pact mechanisms
                if p_type == "TRADE_PACT":
                    val = int(terms.get("annual_value", 25))
                    cursor.execute("""
                        INSERT INTO trade_agreements (turn_signed, party_a, party_b, annual_value, resource_type, status)
                        VALUES (?, ?, ?, ?, 'MANUFACTURES', 'ACTIVE')
                    """, (turn, proposer, responder, val))
                    cursor.execute("""
                        INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                        VALUES (?, 'aid', ?, ?, ?)
                    """, (turn, proposer, responder, f"COMMERCIAL ACCORD: Bilateral trade treaty formally ratified between {proposer} and {responder}."))
                    cursor.execute("""
                        INSERT INTO news_feed (turn, year, headline, body)
                        VALUES (?, ?, 'BILATERAL COMMERCE: TREATY RATIFIED', ?)
                    """, (turn, world["year"], f"Bilateral commercial agreement formally signed between {proposer} and {responder} following hotline negotiations (+$ {val}M/yr each)."))
                    ratify_note = f"🤝 BILATERAL TREATY RATIFIED: Commercial agreement active between {proposer} and {responder} (+${val}M/turn each)."

                elif p_type in ["FINANCIAL_AID_REQUEST", "SOVEREIGN_LOAN"]:
                    amt = int(terms.get("amount_m", 50))
                    # Donor is responder, recipient is proposer
                    cursor.execute("SELECT treasury FROM countries WHERE name = ?", (responder,))
                    res_treasury = cursor.fetchone()[0]
                    if res_treasury < amt:
                        conn.close()
                        return False, f"Treasury shortfall: {responder} holds only ${res_treasury}M, cannot transfer requested ${amt}M."
                    cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (amt, responder))
                    cursor.execute("UPDATE countries SET treasury = treasury + ? WHERE name = ?", (amt, proposer))
                    cursor.execute("""
                        INSERT INTO news_feed (turn, year, headline, body)
                        VALUES (?, ?, 'SOVEREIGN CAPITAL TRANSFER', ?)
                    """, (turn, world["year"], f"{responder} transfers ${amt}M in sovereign reserves to {proposer} following bilateral hotline accord."))
                    ratify_note = f"💵 SOVEREIGN FUNDS TRANSFERRED: ${amt}M transferred from {responder} to {proposer}."

                elif p_type in ["ATOMIC_COLLAB", "TECH_TRANSFER", "NUCLEAR_COLLAB"]:
                    # Provider is responder, recipient is proposer
                    cursor.execute("SELECT nuclear, uranium FROM countries WHERE name = ?", (responder,))
                    res_row = cursor.fetchone()
                    if not res_row or not res_row[0]:
                        conn.close()
                        return False, f"Invalid proposal: {responder} is not an operational nuclear power and cannot transfer atomic weapon technology."

                    cursor.execute("SELECT nuclear, nuclear_progress, uranium, bombs FROM countries WHERE name = ?", (proposer,))
                    prop_row = cursor.fetchone()
                    if not prop_row:
                        conn.close()
                        return False, f"Proposer {proposer} not found on diplomatic register."

                    curr_prop_prog = prop_row[1] or 0
                    new_prop_prog = min(100, curr_prop_prog + 50)
                    new_prop_u = (prop_row[2] or 0) + 1

                    if new_prop_prog >= 100:
                        cursor.execute("""
                            UPDATE countries 
                            SET nuclear = 1, bombs = bombs + 1, nuclear_progress = 100, uranium = ? 
                            WHERE name = ?
                        """, (new_prop_u, proposer))
                        cursor.execute("""
                            INSERT INTO news_feed (turn, year, headline, body)
                            VALUES (?, ?, 'HISTORIC ATOMIC TECHNOLOGY COLLABORATION', ?)
                        """, (turn, world["year"], f"Through bilateral technical collaboration and reactor data sharing with {responder}, scientists of {proposer} have successfully assembled and detonated their first operational atomic device."))
                        cursor.execute("""
                            INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                            VALUES (?, 'nuclear_test', ?, ?, ?)
                        """, (turn, proposer, proposer, f"ATOMIC DETONATION: {proposer} unlocks atomic capability via technical collaboration with {responder}!"))
                        cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 10) WHERE id = 1")
                        self._sync_defcon(cursor)
                        ratify_note = f"⚛️ ATOMIC COLLABORATION RATIFIED: {responder} transferred critical reactor blueprints and 1 MT Uranium to {proposer}. {proposer}'s atomic R&D reached 100% — nuclear capability unlocked (+1 warhead assembled)!"
                    else:
                        cursor.execute("""
                            UPDATE countries 
                            SET nuclear_progress = ?, uranium = ? 
                            WHERE name = ?
                        """, (new_prop_prog, new_prop_u, proposer))
                        cursor.execute("""
                            INSERT INTO news_feed (turn, year, headline, body)
                            VALUES (?, ?, 'BILATERAL ATOMIC ACCORD', ?)
                        """, (turn, world["year"], f"{responder} and {proposer} have ratified a secret scientific cooperation pact on nuclear physics and reactor engineering."))
                        ratify_note = f"⚛️ ATOMIC COLLABORATION RATIFIED: {responder} shared reactor blueprints and 1 MT Uranium with {proposer} (+50% Nuclear R&D, total progress: {new_prop_prog}%/100%)."

                elif p_type == "NON_AGGRESSION":
                    cursor.execute("INSERT INTO stances (from_country, to_country, stance) VALUES (?, ?, 'Friendly') ON CONFLICT(from_country, to_country) DO UPDATE SET stance = 'Friendly'", (proposer, responder))
                    cursor.execute("INSERT INTO stances (from_country, to_country, stance) VALUES (?, ?, 'Friendly') ON CONFLICT(from_country, to_country) DO UPDATE SET stance = 'Friendly'", (responder, proposer))
                    ratify_note = f"🕊️ NON-AGGRESSION PACT RATIFIED: {proposer} and {responder} established mutual non-aggression protocols."

                else:
                    ratify_note = f"Bilateral pact #{pact_id} ratified."

                confirm_cable = response_note or f"TREATY ACCORD RATIFIED: {responder} and {proposer} have formally executed Proposal #{pact_id}."
                cursor.execute("""
                    INSERT INTO hotline_messages (turn, sender, recipient, content, is_intercepted, intercepted_by, leak_level)
                    VALUES (?, ?, ?, ?, 0, NULL, 'NONE')
                """, (turn, responder, proposer, f"✅ {confirm_cable}"))

                conn.commit()
                conn.close()
                return True, ratify_note

            return False, f"Invalid decision '{decision}'."

    def has_trade_pact(self, country_a: str, country_b: str) -> bool:
        """Returns True if an active bilateral trade agreement exists between country_a and country_b."""
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM trade_agreements 
                WHERE status = 'ACTIVE' 
                AND ((party_a = ? AND party_b = ?) OR (party_a = ? AND party_b = ?))
            """, (country_a, country_b, country_b, country_a))
            cnt = cursor.fetchone()[0]
            conn.close()
            return cnt > 0

    def get_state_version(self) -> int:

        """Returns integer state version fingerprint for multi-tab real-time sync."""
        with _db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT turn, phase, defcon, global_tension FROM world_state WHERE id = 1")
            w_row = cursor.fetchone()
            cursor.execute("SELECT COUNT(*) FROM pending_directives")
            dir_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM hotline_messages")
            hot_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pact_proposals")
            pact_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM unsc_resolutions")
            unsc_count = cursor.fetchone()[0]
            conn.close()

        if not w_row:
            return 0
        phase_code = 1 if w_row["phase"] == "DIRECTIVES" else (2 if w_row["phase"] == "DEBRIEF" else 3)
        return (w_row["turn"] * 10000000 + phase_code * 1000000 + w_row["defcon"] * 100000 + 
                w_row["global_tension"] * 1000 + dir_count * 100 + hot_count * 10 + pact_count + unsc_count)

    # =========================================================================
    # REVENUE ENGINE & ANNUAL ECONOMY
    # =========================================================================
    def execute_turn_economy(self, turn: int):
        """
        Executes annual fiscal collection for all nations:
        - Base industrial tax revenue
        - Reductions for high domestic tension
        - Payouts from bilateral trade agreements (with country specialty bonuses)
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
                bonus_a = COUNTRY_SPECIALTIES.get(t["party_a"], {}).get("bonuses", {}).get("trade_income_bonus", 0)
                bonus_b = COUNTRY_SPECIALTIES.get(t["party_b"], {}).get("bonuses", {}).get("trade_income_bonus", 0)
                trade_revenue[t["party_a"]] = trade_revenue.get(t["party_a"], 0) + t["annual_value"] + bonus_a
                trade_revenue[t["party_b"]] = trade_revenue.get(t["party_b"], 0) + t["annual_value"] + bonus_b

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

            # Multi-year domestic nuclear project progression for USSR (1945–1949)
            cursor.execute("SELECT nuclear, nuclear_progress FROM countries WHERE name = 'USSR'")
            ussr_row = cursor.fetchone()
            if ussr_row and not ussr_row[0]: # Not yet nuclear
                cur_u_prog = ussr_row[1] or 0
                delta_u_prog = 20 # Natural progression: +20% per year (takes ~4 years to reach 100%)

                # Fuchs/Rosenberg atomic intelligence leaks if USSR has an active spy in USA
                cursor.execute("""
                    SELECT COUNT(*) FROM active_agents 
                    WHERE owner_country = 'USSR' AND target = 'USA' AND status = 'ACTIVE'
                """)
                has_usa_spy = cursor.fetchone()[0] > 0
                if has_usa_spy:
                    delta_u_prog += 15 # +15% espionage acceleration

                new_u_prog = min(100, cur_u_prog + delta_u_prog)
                if new_u_prog >= 100:
                    cursor.execute("""
                        UPDATE countries 
                        SET nuclear = 1, bombs = bombs + 1, nuclear_progress = 100 
                        WHERE name = 'USSR'
                    """)
                    cursor.execute("""
                        INSERT INTO news_feed (turn, year, headline, body)
                        VALUES (?, ?, 'ATOMIC MONOPOLY BROKEN: SOVIET UNION TESTS FIRST ATOMIC BOMB', 
                                'Soviet nuclear physicists led by Igor Kurchatov have successfully detonated the RDS-1 atomic device at the Semipalatinsk test site. The American atomic monopoly has been broken.')
                    """, (turn, turn + 1944))
                    cursor.execute("""
                        INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                        VALUES (?, 'strike', 'USSR', 'USSR', 'SOVIET ATOMIC TEST: First Soviet atomic device detonated (RDS-1)!')
                    """, (turn,))
                    cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 12) WHERE id = 1")
                    self._sync_defcon(cursor)
                else:
                    cursor.execute("UPDATE countries SET nuclear_progress = ? WHERE name = 'USSR'", (new_u_prog,))

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

        # 1. NUCLEAR EXPANSION / NUCLEAR RESEARCH / BOMB COMMISSION
        if act_type in ["NUCLEAR_EXPANSION", "NUCLEAR_RESEARCH", "BUILD_BOMBS", "BUILD_BOMB"]:
            # Check if nation possesses operational nuclear capability
            is_nuclear_power = bool(country["nuclear"])

            # A. Non-nuclear nation attempting to assemble/commission warheads directly -> BLOCKED
            if not is_nuclear_power and act_type in ["NUCLEAR_EXPANSION", "BUILD_BOMBS", "BUILD_BOMB"]:
                prog = country.get("nuclear_progress", 0)
                rej = (
                    f"Atomic capability not yet unlocked: {country_name} does not possess operational atomic weapons "
                    f"({prog}% R&D complete). Non-nuclear powers cannot manufacture warheads directly! "
                    f"You must first fund multi-stage domestic Nuclear R&D (action: NUCLEAR_RESEARCH) or negotiate an "
                    f"Atomic Technology Sharing agreement (ATOMIC_COLLAB) via the Red Phone hotline with a nuclear superpower."
                )
                return False, rej, rej

            # B. Domestic Nuclear R&D Program (Multi-stage process for non-nuclear powers)
            if act_type == "NUCLEAR_RESEARCH":
                if is_nuclear_power:
                    rej = (
                        f"{country_name} already possesses operational nuclear physics technology (100% R&D complete). "
                        f"To assemble additional atomic weapons, commission warhead production directly "
                        f"(action: BUILD_BOMB, requires $80M + 1 MT Uranium)."
                    )
                    return False, rej, rej

                # Sovereign R&D cost: $90M for France (Force de Frappe trait), $100M standard
                cost_m = 90 if country_name == "France" else 100
                if country["treasury"] < cost_m:
                    rej = f"Insufficient funds: Nuclear R&D cycle requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                    return False, rej, rej

                # Progress advancement: Base +25% (+35% for France)
                base_gain = 35 if country_name == "France" else 25
                # Domestic Uranium reserves bonus: +10% enrichment speed if holding >= 1 MT Uranium
                uranium_bonus = 10 if country.get("uranium", 0) >= 1 else 0
                total_gain = base_gain + uranium_bonus

                curr_prog = country.get("nuclear_progress", 0)
                new_prog = min(100, curr_prog + total_gain)

                with _db_lock:
                    conn = self._get_connection()
                    cursor = conn.cursor()

                    if new_prog >= 100:
                        # 100% reached: First atomic device successfully developed and detonated!
                        cursor.execute("""
                            UPDATE countries 
                            SET treasury = treasury - ?, nuclear = 1, bombs = bombs + 1, nuclear_progress = 100 
                            WHERE name = ?
                        """, (cost_m, country_name))
                        cursor.execute("""
                            INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                            VALUES (?, ?, 'NUCLEAR_RESEARCH', ?, ?, ?, ?)
                        """, (turn, country_name, country_name, cost_m, f"Completed final atomic R&D cycle (100%). Operational atomic weapon detonated! {desc}", dice_roll))
                        cursor.execute("""
                            INSERT INTO news_feed (turn, year, headline, body)
                            VALUES (?, ?, ?, ?)
                        """, (turn, world["year"], f"ATOMIC MONOPOLY SHATTERED: {country_name.upper()} TESTS FIRST ATOMIC DEVICE",
                              f"Scientists and military engineers of {country_name} have successfully conducted a full-yield atomic test detonation. {country_name} has officially broken foreign monopolies and joined the nuclear-armed powers."))
                        cursor.execute("""
                            INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                            VALUES (?, 'nuclear_test', ?, ?, ?)
                        """, (turn, country_name, country_name, f"ATOMIC DETONATION: {country_name} detonates first operational atomic weapon!"))
                        cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 10) WHERE id = 1")
                        self._sync_defcon(cursor)
                        conn.commit()
                        conn.close()
                        return True, f"⚛️ ATOMIC MONOPOLY BROKEN: Domestic nuclear physics project reaches 100%! {country_name} detonated its first atomic device and is now an operational nuclear power (+1 warhead assembled, -$ {cost_m}M).", None
                    else:
                        cursor.execute("""
                            UPDATE countries 
                            SET treasury = treasury - ?, nuclear_progress = ? 
                            WHERE name = ?
                        """, (cost_m, new_prog, country_name))
                        cursor.execute("""
                            INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                            VALUES (?, ?, 'NUCLEAR_RESEARCH', ?, ?, ?, ?)
                        """, (turn, country_name, country_name, cost_m, f"Advanced domestic nuclear R&D (+{total_gain}%, total progress: {new_prog}%/100%). {desc}", dice_roll))
                        cursor.execute("""
                            INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                            VALUES (?, 'incident', ?, ?, ?)
                        """, (turn, country_name, country_name, f"ATOMIC R&D: {country_name} expands heavy-water reactors & isotope separation laboratories."))
                        conn.commit()
                        conn.close()
                        u_note = " (Includes +10% enrichment bonus from domestic uranium reserves)." if uranium_bonus > 0 else " (No uranium reserves on hand)."
                        return True, f"🔬 ATOMIC RESEARCH ADVANCED: Allocated ${cost_m}M to domestic atomic laboratories. Nuclear R&D advanced by +{total_gain}% (Total Progress: {new_prog}%/100%){u_note}. Additional research cycles or foreign technology transfer required before first warhead can be assembled.", None

            # C. Warhead Commission for Operational Nuclear Powers ($80M + 1 MT Uranium)
            cost_m = 80
            if country["treasury"] < cost_m:
                rej = f"Insufficient funds: Assembling 1 atomic warhead requires ${cost_m}M, but treasury holds only ${country['treasury']}M."
                return False, rej, rej

            if country.get("uranium", 0) < 1:
                rej = (
                    f"Uranium supply depleted: Assembling an atomic warhead requires 1 MT of enriched Uranium, "
                    f"but {country_name} possesses 0 MT. Secure uranium reserves through trade agreements, territory, "
                    f"or diplomacy before commissioning warhead assembly."
                )
                return False, rej, rej

            # 12% chance of Criticality Incident / Failed Test
            test_fail_roll = secrets.randbelow(100)
            if test_fail_roll < 12:
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
                    SET treasury = treasury - ?, bombs = bombs + 1, uranium = uranium - 1 
                    WHERE name = ?
                """, (cost_m, country_name))
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'NUCLEAR_EXPANSION', ?, ?, ?, ?)
                """, (turn, country_name, country_name, cost_m, f"Assembled 1 atomic warhead ($80M, -1 MT Uranium). {desc}", dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'nuclear_test', ?, ?, ?)
                """, (turn, country_name, country_name, f"ATOMIC EXPANSION: {country_name} completes assembly of +1 atomic weapon (Consumes 1 MT Uranium, Remaining Stockpile: {country['uranium'] - 1} MT)."))
                conn.commit()
                conn.close()

            return True, f"☢️ WARHEAD ASSEMBLED: {country_name} completed assembly of 1 atomic warhead (-${cost_m}M, -1 MT Uranium). Total stockpile: {country['bombs'] + 1} warheads, {country['uranium'] - 1} MT Uranium remaining.", None


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
            cost_m = self.get_action_cost(country_name, "MILITARY_OFFENSIVE", target)
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Combat offensive requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ?, tension = tension + 10 WHERE name = ?", (cost_m, country_name))
                cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 15) WHERE id = 1")
                self._sync_defcon(cursor)
                
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
            cost_m = self.get_action_cost(country_name, "ESPIONAGE", target)
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

            # Generate immediate field intelligence cable (will now be confirmed with active spy)
            dossier = self.get_country_dossier(country_name, target)
            bombs_info = dossier.get("bombs_display", "Unknown")
            nuke_status = dossier.get("nuclear_status", "Unconfirmed")
            treasury_info = dossier.get("treasury_display", "Unconfirmed")
            conf_info = dossier.get("confidence_label", "CONFIRMED // ACTIVE HUMINT SPY NETWORK")

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
            bond_gain = COUNTRY_SPECIALTIES.get(country_name, {}).get("bonuses", {}).get("war_bonds_yield", 150)
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury + ?, tension = tension + 8 WHERE name = ?", (bond_gain, country_name))
                cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 3) WHERE id = 1")
                self._sync_defcon(cursor)
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'WAR_BONDS', ?, 0, ?, ?)
                """, (turn, country_name, country_name, f"Issued emergency sovereign bonds (+ ${bond_gain}M cash, +8% tension)", dice_roll))
                cursor.execute("""
                    INSERT INTO news_feed (turn, year, headline, body)
                    VALUES (?, ?, 'FISCAL EXPANSION: WAR BONDS ISSUED', ?)
                """, (turn, world["year"], f"{country_name} issues emergency domestic sovereign bonds, raising ${bond_gain}M."))
                conn.commit()
                conn.close()
            return True, f"WAR BONDS ISSUED: Injected +${bond_gain}M cash into National Treasury (Current: ${country['treasury'] + bond_gain}M). Domestic tension +8%.", None

        # 6. ECONOMIC REVENUE: TRADE PACT (Disallow unilateral decree; require Red Phone)
        elif act_type in ["TRADE_PACT", "COMMERCIAL_TREATY"]:
            rej = f"Bilateral trade pacts and financial treaties cannot be ratified unilaterally. Please open the Red Phone encrypted hotline to propose terms and negotiate with {target}."
            return False, rej, rej

        # 7. PAPERCLIP SCIENTIST RECRUITMENT (Missile Tech)
        elif act_type in ["PAPERCLIP_RECRUIT", "MISSILE_RESEARCH"]:
            cost_m = self.get_action_cost(country_name, "PAPERCLIP_RECRUIT")
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
            calc_cost = self.get_action_cost(country_name, "ECONOMIC_AID", target)
            req_cost = int(action.get("cost_m", 0))
            cost_m = req_cost if req_cost > 0 else calc_cost
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej


            aid_mult = COUNTRY_SPECIALTIES.get(country_name, {}).get("bonuses", {}).get("aid_effect_mult", 1.0)
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (cost_m, country_name))
                if target in INITIAL_COUNTRIES:
                    cursor.execute("UPDATE countries SET treasury = treasury + ? WHERE name = ?", (cost_m, target))
                elif target in INITIAL_BUFFERS:
                    base_shift = 0.3 if country["alignment"] > 0 else -0.3
                    shift = base_shift * aid_mult
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

        # 9. DIPLOMATIC STANCE / ALLIANCE
        elif act_type in ["DIPLOMATIC_STANCE", "STANCE", "ALIGN", "ALLIANCE"]:
            stance = action.get("stance")
            target = action.get("target", "USSR" if country_name != "USSR" else "USA")

            # Robust stance parsing: inspect description, type, and raw text
            desc_text = (str(action.get("description", "")) + " " + str(action.get("type", "")) + " " + str(action.get("stance", ""))).lower()
            if not stance or stance.lower() == "neutral":
                if any(k in desc_text for k in ["ally", "alliance", "allied", "align"]):
                    stance = "Ally"
                elif any(k in desc_text for k in ["friendly", "friend"]):
                    stance = "Friendly"
                elif any(k in desc_text for k in ["rival"]):
                    stance = "Rival"
                elif any(k in desc_text for k in ["enemy", "hostile"]):
                    stance = "Enemy"
                else:
                    stance = stance or "Neutral"

            stance = stance.capitalize()
            if stance not in ["Ally", "Friendly", "Neutral", "Rival", "Enemy"]:
                stance = "Ally" if "ally" in stance.lower() else "Neutral"

            self.set_stance(country_name, target, stance)
            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pending_directives (turn, country, action_type, target, cost_m, description, dice_roll)
                    VALUES (?, ?, 'DIPLOMATIC_STANCE', ?, 0, ?, ?)
                """, (turn, country_name, target, f"Diplomatic stance toward {target} declared as '{stance}'", dice_roll))
                cursor.execute("""
                    INSERT INTO map_events (turn, event_type, source_name, target_name, description)
                    VALUES (?, 'diplomatic', ?, ?, ?)
                """, (turn, country_name, target, f"DIPLOMATIC ALIGNMENT: {country_name} declared stance toward {target} as '{stance}'."))
                conn.commit()
                conn.close()

            return True, f"DIPLOMATIC POSTURE: Stance toward {target} set to '{stance}'.", None

        # 10. MILITARY POSTURE / REINFORCEMENT
        else:
            cost_m = self.get_action_cost(country_name, "MILITARY_POSTURE", target)
            if cost_m > country["treasury"]:
                rej = f"Insufficient funds: Requires ${cost_m}M, but national treasury holds only ${country['treasury']}M."
                return False, rej, rej

            with _db_lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE countries SET treasury = treasury - ? WHERE name = ?", (cost_m, country_name))
                cursor.execute("UPDATE world_state SET global_tension = MIN(100, global_tension + 5) WHERE id = 1")
                self._sync_defcon(cursor)
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

            cursor.execute("SELECT year, turn, defcon FROM world_state WHERE id = 1")
            cur_world = cursor.fetchone()
            current_year = cur_world["year"]
            current_turn = cur_world["turn"]
            old_defcon = cur_world["defcon"]

            # Escalation debuff check: if DEFCON decreased (e.g. from 4 to 3, 3 to 2, 2 to 1)
            if new_defcon < old_defcon:
                instigator = self._detect_escalation_instigator_db(cursor, current_turn)
                if instigator:
                    self._apply_escalation_debuff_db(cursor, instigator, old_defcon, new_defcon, current_turn, current_year)

            # Check for nuclear strikes executed this turn
            has_nukes = self._check_and_log_nuclear_strikes_db(cursor, current_turn, current_year)
            if has_nukes:
                new_defcon = 1
                new_tension = 100
                mad_triggered = True

            # Check if any military offensive invaded or occupied a buffer/territory
            cursor.execute("""
                SELECT country, target, description FROM pending_directives 
                WHERE turn = ? AND action_type IN ('MILITARY_OFFENSIVE', 'INVASION', 'ATTACK')
            """, (current_turn,))
            invasions = cursor.fetchall()
            for inv in invasions:
                tgt = inv["target"]
                c_atk = inv["country"]
                cursor.execute("""
                    UPDATE territory_control 
                    SET current_controller = ?, status = 'OCCUPIED'
                    WHERE name = ? OR territory_id = ?
                """, (c_atk, tgt, tgt))

            next_turn = current_turn + 1
            next_era_id = min(10, next_turn)
            era_info = COLD_WAR_ERAS.get(next_era_id, COLD_WAR_ERAS[10])
            next_year = era_info["year_start"]
            # 10 Cold War Eras (1945–1991): game over ONLY when concluded after Era 10
            game_over = (next_turn > 10)

            # Apply dynamic era-relative boundaries, partitions, and decolonization
            self.apply_era_boundaries_db(cursor, next_era_id)

            cursor.execute("""
                UPDATE world_state 
                SET year = ?, turn = ?, defcon = ?, global_tension = ?, mad_triggered = ?, game_over = ?, phase = 'DEBRIEF'
                WHERE id = 1
            """, (next_year, next_turn, new_defcon, new_tension, 1 if mad_triggered else 0, 1 if game_over else 0))

            conn.commit()
            conn.close()

        # Execute turn economy, resolve pending UNSC resolutions, roll random events, and evaluate objectives
        self.execute_turn_economy(current_turn)
        self.resolve_unsc_resolutions(current_turn)
        self.roll_turn_random_events(current_year, current_turn)
        self.activate_crisis_if_due(next_year, next_turn)
        self.evaluate_turn_objectives(current_turn, current_year)
