"""
The Iron Curtain - Palantir Gotham / Foundry C2 Strategic Operations Platform
Multiplayer Classroom Geopolitics Simulator (1945–1991)
"""

import streamlit as st
import pydeck as pdk
import json
import os
import pandas as pd
from typing import Optional, Tuple, Dict, Any

from state_engine import StateEngine, UNSC_PERM_5, COUNTRY_SPECIALTIES
from groq_service import GroqService, ADVISER_PERSONAS, HISTORICAL_YEARS
from objectives_data import COLD_WAR_ERAS

st.set_page_config(
    page_title="THE IRON CURTAIN // C2 STRATEGIC PLATFORM",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Palantir C2 Stylesheet
css_path = os.path.join(os.path.dirname(__file__), "static", "terminal.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Authentic World GeoJSON
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "data", "world_borders.json")
with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
    WORLD_GEOJSON = json.load(f)

# Initialize Core Services
@st.cache_resource
def get_services():
    return StateEngine(), GroqService()

state_engine, groq_service = get_services()

# Multi-Tab Real-Time Reactive Synchronization
@st.fragment(run_every="3s")
def check_realtime_sync():
    current_ver = state_engine.get_state_version()
    last_ver = st.session_state.get("_last_state_version")
    if last_ver is None:
        st.session_state["_last_state_version"] = current_ver
    elif last_ver != current_ver:
        st.session_state["_last_state_version"] = current_ver
        st.rerun(scope="app")

check_realtime_sync()

world = state_engine.get_world_state()
countries = state_engine.get_countries()
buffers = state_engine.get_buffers()


def alignment_to_rgb(align: float):
    # Palantir defense palette: Blue (West) to Red (East), Muted Slate (Neutral)
    if align >= 0:
        r = int(22 + (56 - 22) * align)
        g = int(32 + (139 - 32) * align)
        b = int(45 + (253 - 45) * align)
    else:
        mag = abs(align)
        r = int(22 + (248 - 22) * mag)
        g = int(32 + (81 - 32) * mag)
        b = int(45 + (73 - 45) * mag)
    return [r, g, b, 210]

# ==============================================================================
# SIDEBAR: C2 THEATER SELECTOR & TELEMETRY
# ==============================================================================
with st.sidebar:
    st.markdown("### 🌐 C2 OPERATIONS CONTROL")
    st.caption("TACTICAL GEOPOLITICAL COMMAND • 1945–1991 (10 ERAS)")

    if st.session_state.get("auth_role") == "TEACHER":
        view_options = ["🏛️ UN SECRETARY-GENERAL & DM CONSOLE"] + [f"🚩 {c}" for c in countries.keys()]
        selected_view = st.selectbox("TERMINAL VIEW SELECTOR", view_options, index=0)
    else:
        selected_view = f"🚩 {st.session_state.get('auth_country', 'USA')}"

    st.markdown("---")
    era_id = min(10, max(1, world['turn']))
    current_era = COLD_WAR_ERAS.get(era_id, COLD_WAR_ERAS[1])
    st.markdown(f"**GLOBAL SITUATION CLOCK:**")
    st.markdown(f"• **ERA:** `{current_era['name']}`")
    st.markdown(f"• **YEARS:** `{current_era['years_label']}` — *{current_era['title']}*")
    st.markdown(f"• **STATUS:** `PHASE {world.get('phase', 'DIRECTIVES')}`")
    st.markdown(f"• **DEFCON:** `{world['defcon']}` | **TENSION:** `{world['global_tension']}%`")

    st.markdown("---")
    st.markdown("**DEFCON READINESS PROTOCOL:**")
    defcon_levels = {
        5: ("DEFCON 5", "PEACETIME // NORMAL ALERT"),
        4: ("DEFCON 4", "INTELLIGENCE WATCH // COLD WAR"),
        3: ("DEFCON 3", "TROOPS FORWARD DEPLOYED"),
        2: ("DEFCON 2", "ARMED FORCES READY TO STRIKE"),
        1: ("DEFCON 1", "MAXIMUM ALERT // NUCLEAR WAR")
    }
    for lvl in [5, 4, 3, 2, 1]:
        tag, desc = defcon_levels[lvl]
        active = "active" if world["defcon"] == lvl else ""
        st.markdown(
            f"<div class='defcon-box defcon-{lvl} {active}' style='margin-bottom: 4px;'>"
            f"{tag} — <span style='font-size: 0.7rem;'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    if st.button("🔄 RE-INITIALIZE SIMULATION", use_container_width=True):
        state_engine.reset_game()
        st.success("Simulation re-anchored to Potsdam 1945.")
        st.rerun()

# ==============================================================================
# SESSION AUTHENTICATION & ROLE-BASED ACCESS CONTROL
# ==============================================================================
if "auth_role" not in st.session_state:
    st.session_state["auth_role"] = None
if "auth_country" not in st.session_state:
    st.session_state["auth_country"] = None

with st.sidebar:
    if st.session_state["auth_role"] is not None:
        st.markdown("---")
        role_label = "🏛️ UN SECRETARY-GENERAL (TEACHER)" if st.session_state["auth_role"] == "TEACHER" else f"🚩 {st.session_state['auth_country']} DELEGATION"
        st.markdown(f"**ACTIVE STATION:**\n`{role_label}`")
        if st.button("🔓 LOGOUT / SWITCH STATION", use_container_width=True):
            st.session_state["auth_role"] = None
            st.session_state["auth_country"] = None
            st.rerun()

if st.session_state["auth_role"] is None:
    st.markdown("<div style='text-align: center; margin-top: 25px; margin-bottom: 25px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='letter-spacing: 0.08em; color: #58a6ff;'>THE IRON CURTAIN // ACCESS CONTROL GATEWAY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.95rem;'>COLD WAR STRATEGIC SIMULATION COMMAND & CONTROL (1945–1991 • 10 PLAYABLE ERAS)</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_t, col_s = st.columns(2)
    with col_t:
        st.markdown("<div class='hud-panel' style='border-color: #58a6ff; min-height: 290px;'>", unsafe_allow_html=True)
        st.markdown("### 🏛️ UN SECRETARY-GENERAL (TEACHER)")
        st.caption("Game Master / Dungeon Master command console. Enforce ceasefires, shift contested borders, moderate conferences, view peacemaking advice, and manage gradebook.")
        pin = st.text_input("TEACHER AUTHORIZATION PIN", type="password", value="POTSDAM1945", key="teacher_login_pin")
        if st.button("ENTER UN COMMAND CONSOLE ⚡", type="primary", use_container_width=True):
            if pin == "POTSDAM1945":
                st.session_state["auth_role"] = "TEACHER"
                st.session_state["auth_country"] = None
                st.rerun()
            else:
                st.error("INVALID AUTHORIZATION PIN.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s:
        st.markdown("<div class='hud-panel' style='border-color: #2ea043; min-height: 290px;'>", unsafe_allow_html=True)
        st.markdown("### 🚩 NATIONAL DELEGATION (STUDENT)")
        st.caption("Command your nation's sovereign cabinet. Execute strategic directives, consult AI advisers, negotiate on the Red Phone, and fulfill annual historical objectives.")
        student_countries = [c_name for c_name, c in countries.items() if c.get("controller", "STUDENT") == "STUDENT"]
        if not student_countries:
            student_countries = list(countries.keys())
        chosen_c = st.selectbox("SELECT YOUR NATION DELEGATION", student_countries, key="student_login_country")
        if st.button("ACCESS NATIONAL TERMINAL 🚀", use_container_width=True):
            st.session_state["auth_role"] = "STUDENT"
            st.session_state["auth_country"] = chosen_c
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ==============================================================================
# NON-TERMINAL DEFCON 1 & STRATEGIC APOCALYPSE ALERT BANNER
# ==============================================================================
if world["defcon"] == 1:
    st.markdown(
        """
        <div class='hud-panel-danger' style='margin-bottom: 16px; padding: 18px 24px; border-left: 6px solid #f85149;'>
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div>
                    <h3 style='color: #f85149; margin: 0; font-size: 1.35rem;'>⚠️ DEFCON 1: STRATEGIC NUCLEAR EMERGENCY IN PROGRESS</h3>
                    <p style='color: #ff7b72; margin: 4px 0 0 0; font-size: 0.95rem; font-weight: 500;'>
                        Atomic threshold has been breached. Radiation fallout monitored across contested theaters. 
                        Global diplomacy is in an emergency state. The simulation continues—world leaders and the UN must face the consequences.
                    </p>
                </div>
                <span class='badge-c2 badge-secret' style='background: rgba(248, 81, 73, 0.2); color: #f85149; border-color: #f85149; font-size: 0.8rem;'>
                    CRISIS ACTIVE
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# PYDECK STRATEGIC MAP COMPONENT (DYNAMIC BORDERS & COMBAT VECTORS)
# ==============================================================================
def render_strategic_map(highlight_target: Optional[str] = None):
    territory_map = state_engine.get_territories() if hasattr(state_engine, "get_territories") else {}

    geojson_features = []
    for feature in WORLD_GEOJSON["features"]:
        feat = dict(feature)
        feat["properties"] = dict(feat.get("properties", {}))
        c_name = feat["properties"].get("name", "")
        iso = feat["properties"].get("ISO3166-1-Alpha-3")

        # Dynamic territorial controller lookup
        t = None
        if iso == "KOR":
            t = territory_map.get("KOR_SOUTH")
        elif iso == "PRK":
            t = territory_map.get("KOR_NORTH")
        elif iso == "DEU":
            t = territory_map.get("GER_WEST") or territory_map.get("DEU") or territory_map.get("Germany")
        elif iso == "IND" or c_name == "India":
            t = territory_map.get("India") or territory_map.get("IND")
        elif c_name in territory_map:
            t = territory_map.get(c_name)
        elif iso in territory_map:
            t = territory_map.get(iso)
        else:
            for cand in territory_map.values():
                if cand.get("iso_code") == iso or cand.get("name") == c_name:
                    t = cand
                    break

        line_col = [38, 51, 69, 255]
        if t:
            disp_name = t["name"]
            ctrl = t["current_controller"]
            t_status = t["status"]
            align = t["alignment"]

            if t_status == "OCCUPIED":
                status_text = f"OCCUPIED TERRITORY • Controlled by {ctrl} (Garrison: {t.get('military_garrison', 2)} Divs)"
                if ctrl in countries:
                    align = countries[ctrl]["alignment"]
                line_col = [248, 81, 73, 255]
            elif t_status == "PARTITIONED":
                status_text = f"PARTITIONED SOVEREIGNTY • Controlled by {ctrl}"
                line_col = [210, 153, 34, 255]
            elif t_status == "COLONY_TRANSITION":
                reg_name = t.get("region", "Colonial Dependency")
                disp_name = f"{t['name']} ({reg_name})"
                status_text = f"COLONIAL TRANSITION TERRITORY • Administered by {ctrl} (Garrison: {t.get('military_garrison', 4)} Divs)"
                if ctrl in countries:
                    align = countries[ctrl]["alignment"]
                line_col = [186, 104, 200, 255]
            else:
                status_text = f"Sovereign Territory • Controlled by {ctrl}"
        elif c_name in countries:
            disp_name = c_name
            c = countries[c_name]
            align = c["alignment"]
            status_text = f"Major Power • Stockpile: {c['bombs']} Nukes • Treasury: ${c['treasury']}M"
        elif c_name in buffers:
            disp_name = c_name
            b = buffers[c_name]
            align = b["alignment"]
            status_text = "Contested Frontier Buffer State"
        else:
            disp_name = c_name
            align = 0.0
            status_text = "Non-Aligned Sovereign Territory"

        align_text = f"{align:+.1f} ({'Pro-Western Alliance' if align > 0.2 else ('Pro-Soviet Bloc' if align < -0.2 else 'Non-Aligned')})"

        is_hl = (c_name == highlight_target or (t and t["name"] == highlight_target))
        feat["properties"]["fill_color"] = [255, 176, 0, 240] if is_hl else alignment_to_rgb(align)
        feat["properties"]["name"] = disp_name
        feat["properties"]["status"] = status_text
        feat["properties"]["alignment"] = align_text
        feat["properties"]["line_color"] = line_col
        geojson_features.append(feat)

    geojson_data = {"type": "FeatureCollection", "features": geojson_features}

    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_fill_color="properties.fill_color",
        get_line_color="properties.line_color",
        line_width_min_pixels=1.4
    )

    capitals_data = []
    for name, c in countries.items():
        is_hl = (name == highlight_target)
        capitals_data.append({
            "name": name,
            "status": f"Capital: {c['capital']} • Stockpile: {c['bombs']} Warheads • Treasury: ${c['treasury']}M",
            "alignment": f"Alignment: {c['alignment']:+.1f}",
            "lat": c["lat"],
            "lon": c["lon"],
            "color": [255, 255, 255, 255] if is_hl else ([248, 81, 73, 230] if c["nuclear"] else [56, 139, 253, 200]),
            "radius": 360000 if is_hl else (260000 if c["nuclear"] else 180000)
        })

    capitals_layer = pdk.Layer(
        "ScatterplotLayer",
        capitals_data,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True
    )

    # Nuclear Detonation Blast Ground Zeroes & Fallout Rings
    nuclear_strikes = state_engine.get_nuclear_strikes() if hasattr(state_engine, "get_nuclear_strikes") else []
    nuke_blast_data = []
    for ns in nuclear_strikes:
        # Fiery Epicenter
        nuke_blast_data.append({
            "name": f"💥 GROUND ZERO: {ns['target']}",
            "status": f"Detonated by {ns['attacker']} in Year {ns['year']}. {ns['damage_description']}",
            "alignment": "ATOMIC DETONATION (CRISIS)",
            "lat": ns["target_lat"],
            "lon": ns["target_lon"],
            "color": [255, 69, 0, 255],
            "radius": 220000
        })
        # Radiation Fallout Zone
        nuke_blast_data.append({
            "name": f"☢️ RADIATION FALLOUT ZONE: {ns['target']}",
            "status": f"Radioactive fallout cloud extending 550km across theater.",
            "alignment": "CONTAMINATION ZONE",
            "lat": ns["target_lat"],
            "lon": ns["target_lon"],
            "color": [255, 140, 0, 80],
            "radius": 550000
        })

    nuke_layer = pdk.Layer(
        "ScatterplotLayer",
        nuke_blast_data,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True
    )

    # 3D Geopolitical Strategic Arcs (Transatlantic, Sino-Soviet, Deterrence, Operations)
    all_locs = {}
    for cn, cd in countries.items():
        all_locs[cn] = {"lat": cd["lat"], "lon": cd["lon"]}
    for bn, bd in buffers.items():
        all_locs[bn] = {"lat": bd["lat"], "lon": bd["lon"]}

    canonical_aliases = {
        "Germany": {"lat": 51.16, "lon": 10.45},
        "East Germany": {"lat": 52.0, "lon": 12.5},
        "West Germany": {"lat": 50.5, "lon": 9.5},
        "Japan": {"lat": 36.2, "lon": 138.25},
        "Korea": {"lat": 38.0, "lon": 127.5},
        "North Korea": {"lat": 39.0, "lon": 125.75},
        "South Korea": {"lat": 37.5, "lon": 127.0},
        "Poland": {"lat": 51.91, "lon": 19.14},
        "Iran": {"lat": 32.42, "lon": 53.68},
        "Turkey": {"lat": 38.96, "lon": 35.24},
        "Greece": {"lat": 39.07, "lon": 21.82},
        "Austria": {"lat": 47.51, "lon": 14.55},
        "Czechoslovakia": {"lat": 49.81, "lon": 15.47},
        "Russia": all_locs.get("USSR", {"lat": 55.75, "lon": 37.61}),
        "America": all_locs.get("USA", {"lat": 38.89, "lon": -77.03}),
        "Britain": all_locs.get("United Kingdom", {"lat": 51.50, "lon": -0.12}),
        "UK": all_locs.get("United Kingdom", {"lat": 51.50, "lon": -0.12})
    }
    for k, v in canonical_aliases.items():
        if k not in all_locs:
            all_locs[k] = v

    arc_data = []
    base_arcs = [
        ("USA", "United Kingdom", [56, 139, 253, 220], "Transatlantic Special Relationship"),
        ("United Kingdom", "France", [56, 139, 253, 190], "Western European Defense Corridor"),
        ("USA", "France", [56, 139, 253, 190], "Marshall Plan Economic Bridge"),
        ("USSR", "China", [248, 81, 73, 230], "Sino-Soviet Treaty Axis"),
        ("USA", "USSR", [210, 153, 34, 250], "Nuclear Deterrence Standoff"),
        ("USSR", "Yugoslavia", [163, 113, 247, 200], "Danubian Diplomatic Lifeline"),
    ]
    for src_n, tgt_n, col, desc in base_arcs:
        if src_n in all_locs and tgt_n in all_locs:
            s = all_locs[src_n]
            t = all_locs[tgt_n]
            arc_data.append({
                "from_lon": s["lon"], "from_lat": s["lat"],
                "to_lon": t["lon"], "to_lat": t["lat"],
                "color": col,
                "name": f"{src_n} ➔ {tgt_n}",
                "status": desc,
                "alignment": "Strategic Axis"
            })

    # Tactical Combat Vectors & Battlefield Clash Markers
    combat_clash_data = []
    map_events = state_engine.get_map_events()
    for ev in map_events[:25]:
        src_name = ev.get("source_name")
        tgt_name = ev.get("target_name")
        ev_type = (ev.get("event_type") or "").lower()

        if src_name in all_locs and tgt_name in all_locs:
            src = all_locs[src_name]
            tgt = all_locs[tgt_name]
            if any(k in ev_type for k in ["strike", "offensive", "attack", "invasion", "military"]):
                arc_color = [248, 81, 73, 255]
                align_tag = "Tactical Military Vector"
                combat_clash_data.append({
                    "name": f"⚔️ ACTIVE BATTLEFIELD: {src_name} assault on {tgt_name}",
                    "status": ev.get("description", "Armed clashes and frontline assaults."),
                    "alignment": "BATTLEFIELD ENGAGEMENT",
                    "lat": tgt["lat"],
                    "lon": tgt["lon"],
                    "color": [248, 81, 73, 240],
                    "radius": 280000
                })
            elif any(k in ev_type for k in ["espionage", "spy", "intel"]):
                arc_color = [210, 153, 34, 250]
                align_tag = "Intelligence Vector"
            else:
                arc_color = [46, 160, 67, 240]
                align_tag = "Economic / Treaty Vector"

            arc_data.append({
                "from_lon": src["lon"], "from_lat": src["lat"],
                "to_lon": tgt["lon"], "to_lat": tgt["lat"],
                "color": arc_color,
                "name": f"ACTIVE OPERATION: {src_name} ➔ {tgt_name}",
                "status": ev.get("description", "Field Operation"),
                "alignment": align_tag
            })

    # Active Spy Network Infiltration Arcs
    active_spies = state_engine.get_active_agents() if hasattr(state_engine, 'get_active_agents') else []
    for sp in active_spies:
        o = sp.get("owner_country")
        t = sp.get("target")
        if o in all_locs and t in all_locs:
            s = all_locs[o]
            tgt = all_locs[t]
            arc_data.append({
                "from_lon": s["lon"], "from_lat": s["lat"],
                "to_lon": tgt["lon"], "to_lat": tgt["lat"],
                "color": [210, 153, 34, 255],
                "name": f"ACTIVE ESPIONAGE RING: {o} ➔ {t}",
                "status": f"Covert Intelligence Operation ({sp.get('mission', 'Infiltration')})",
                "alignment": "HUMINT Vector"
            })

    combat_clash_layer = pdk.Layer(
        "ScatterplotLayer",
        combat_clash_data,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True
    )

    arc_layer = pdk.Layer(
        "ArcLayer",
        arc_data,
        get_source_position=["from_lon", "from_lat"],
        get_target_position=["to_lon", "to_lat"],
        get_source_color="color",
        get_target_color="color",
        get_width=3.5,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=34.0,
        longitude=18.0,
        zoom=1.35,
        pitch=42,
        bearing=-10,
        min_zoom=0.8,
        max_zoom=6.0
    )

    deck = pdk.Deck(
        layers=[geojson_layer, arc_layer, capitals_layer, combat_clash_layer, nuke_layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<div style='font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; font-size: 12px; color: #e6edf3; background: #0a0d12; border: 1px solid #30363d; border-radius: 4px; padding: 8px 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.6);'>"
                    "<b style='color: #58a6ff; font-size: 13px;'>{name}</b><br/>"
                    "<span style='color: #8b949e;'>{status}</span><br/>"
                    "<span style='color: #d29922; font-size: 11px;'><b>{alignment}</b></span>"
                    "</div>",
            "style": {
                "backgroundColor": "transparent",
                "border": "none"
            }
        },
        map_style=None
    )
    st.pydeck_chart(deck, use_container_width=True)

    # Tactical Map Legend
    st.markdown(
        "<div class='hud-panel' style='margin-top: -6px; margin-bottom: 12px; padding: 8px 14px; font-size: 0.8rem; background: #0c1017; border-color: #21262d;'>"
        "<div style='font-family: var(--font-mono); font-weight: 700; color: var(--text-secondary); margin-bottom: 6px; letter-spacing: 0.05em;'>"
        "📡 STRATEGIC MAP & VISUAL COMBAT AID DIRECTORY:"
        "</div>"
        "<div style='display: flex; flex-wrap: wrap; gap: 16px; line-height: 1.5;'>"
        "<span><b style='color: #f85149;'>💥 Orange/Crimson Rings:</b> Nuclear Detonations & Radiation Shockwaves</span>"
        "<span><b style='color: #f85149;'>⚔️ Red Pulsing Nodes:</b> Active Army Offensives & Battlefield Clash Zones</span>"
        "<span><b style='color: #f85149;'>━━━ Crimson Vector:</b> Military Assaults & Troop Incursions</span>"
        "<span><b style='color: #d29922;'>━━━ Amber Vector:</b> HUMINT Spy Infiltration</span>"
        "<span><b style='color: #58a6ff;'>━━━ Blue Vector:</b> Western Defense Corridors</span>"
        "<span><b style='color: #2ea043;'>━━━ Emerald Vector:</b> Foreign Trade & Aid Lifelines</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )


# ==============================================================================
# VIEW 1: PROJECTOR / UN JOINT CHIEFS COMMAND PLATFORM
# ==============================================================================
if selected_view.startswith("🏛️"):
    un_era_id = min(10, max(1, world['turn']))
    un_era = COLD_WAR_ERAS.get(un_era_id, COLD_WAR_ERAS[1])
    st.markdown(
        f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>"
        f"<div>"
        f"<h2 style='margin: 0;'>UNITED NATIONS // SECRETARY-GENERAL & DM COMMAND CONSOLE</h2>"
        f"<span style='color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.85rem;'>"
        f"GLOBAL WARGAME MODERATION • DEFCON {world['defcon']} • {un_era['name']} ({un_era['years_label']}) • ERA {world['turn']}/10"
        f"</span>"
        f"</div>"
        f"<div>"
        f"<span class='badge-c2 badge-secret'>UN DUNGEON MASTER PERMISSIONS ACTIVE</span>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Top Metric Ribbon
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>GLOBAL DEFCON</div><div class='metric-val metric-val-mono'>{world['defcon']}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>WORLD TENSION</div><div class='metric-val'>{world['global_tension']}%</div></div>", unsafe_allow_html=True)
    with m3:
        nuke_count = sum(c["bombs"] for c in countries.values())
        st.markdown(f"<div class='metric-box'><div class='metric-label'>ATOMIC WARHEADS</div><div class='metric-val metric-val-mono'>{nuke_count}</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>COLD WAR ERA</div><div class='metric-val'>{un_era['name'].split(':')[0]}</div></div>", unsafe_allow_html=True)
    with m5:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>ERA CHRONOLOGY</div><div class='metric-val metric-val-mono'>{un_era['years_label']}</div></div>", unsafe_allow_html=True)

    tab_map, tab_un, tab_dm, tab_ai, tab_grades, tab_setup = st.tabs([
        "🌐 STRATEGIC MAP & COMMAND",
        "🏛️ UN DIPLOMATIC SUMMITS",
        "⚡ DM CHAOS CONTROL & MOVING BORDERS",
        "🕊️ AI PEACEKEEPER ADVISORIES",
        "🎓 CLASSROOM GRADEBOOK",
        "⚙️ ROSTER SETUP"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: STRATEGIC MAP & TURN COMMAND
    # --------------------------------------------------------------------------
    with tab_map:
        col_left, col_right = st.columns([8, 4])

        with col_left:
            st.markdown("#### 🌍 GLOBAL SITUATION MAP (DYNAMIC BORDERS & COMBAT VECTORS)")
            render_strategic_map()

            st.markdown("#### 📈 HISTORICAL DOOM CLOCK VS. CLASSROOM TIMELINE DIVERGENCE (1945–1991)")
            hist_timeline = {
                1945: 30,  # Era 1: Dawn of Atomic Age & Decolonization
                1949: 75,  # Era 2: Hardening Blocs & Red China
                1955: 60,  # Era 3: Post-Stalin Thaw & Non-Aligned Movement
                1962: 95,  # Era 4: Brink of Armageddon (Cuban Missile Crisis)
                1968: 75,  # Era 5: Proxy Quagmires & Cultural Revolution
                1973: 60,  # Era 6: Détente & Triangular Diplomacy
                1979: 80,  # Era 7: Second Cold War & Afghan Trap
                1983: 90,  # Era 8: Star Wars & Nuclear Brinkmanship
                1989: 45,  # Era 9: Glasnost, Perestroika & Fall of Berlin Wall
                1991: 20   # Era 10: Final Curtain & Soviet Dissolution
            }
            all_mirrors = state_engine.get_all_history_mirrors()
            sim_data = {m["year"]: world["global_tension"] for m in all_mirrors}
            sim_data[world["year"]] = world["global_tension"]

            years = sorted(list(hist_timeline.keys()))
            chart_rows = []
            for y in years:
                chart_rows.append({
                    "Year": str(y),
                    "Real History Tension": hist_timeline.get(y, 50),
                    "Classroom Simulated Tension": sim_data.get(y, None)
                })
            df_chart = pd.DataFrame(chart_rows).set_index("Year")
            st.line_chart(df_chart, height=220)

            st.markdown("#### 📡 UN PUBLIC WIRE & GLOBAL DISPATCHES")
            news_items = state_engine.get_news(5)
            for item in news_items:
                st.markdown(
                    f"<div class='cable-card'>"
                    f"<div class='cable-header'><span>YEAR {item['year']}</span><span>PUBLIC WIRE CABLE</span></div>"
                    f"<b>{item['headline']}</b><br>"
                    f"<span style='color: var(--text-secondary); font-size: 0.9rem;'>{item['body']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        with col_right:
            st.markdown("#### 📋 TURN COMMAND CONSOLE")

            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>NATION SUBMISSION STATUS:</b>", unsafe_allow_html=True)
            sub_status = state_engine.get_submission_status(world["turn"])
            ready_count = sum(sub_status.values())
            st.progress(ready_count / max(1, len(sub_status)), text=f"{ready_count} of {len(sub_status)} Powers Submitted")

            st_cols = st.columns(2)
            for idx, (c_name, ready) in enumerate(sub_status.items()):
                col = st_cols[idx % 2]
                tag = "<span style='color:var(--accent-green);'>✓ READY</span>" if ready else "<span style='color:var(--accent-amber);'>⏳ PENDING</span>"
                with col:
                    st.markdown(f"<span style='font-size:0.82rem;'>{c_name}: {tag}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # UN Security Council Live Box
            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>🇺🇳 UN SECURITY COUNCIL CHAMBER:</b>", unsafe_allow_html=True)
            resolutions = state_engine.get_unsc_resolutions(world["turn"])
            if resolutions:
                for res in resolutions[:2]:
                    st.markdown(f"<span class='badge-c2 badge-unsc'>{res['status']}</span> <b>{res['title']}</b>", unsafe_allow_html=True)
                    st.caption(f"Proposed by {res['proposer']} • Target: {res['target']}")
            else:
                st.caption("No pending resolutions this cycle.")
            st.markdown("</div>", unsafe_allow_html=True)

            # Game Master Adjudication
            st.markdown("<div class='hud-panel-primary'>", unsafe_allow_html=True)
            st.markdown("<b>GAME MASTER ARBITRATION:</b>", unsafe_allow_html=True)
            admin_pass = st.text_input("HOST AUTHORIZATION PIN", type="password", value="POTSDAM1945", key="host_auth_pin_tab1")

            if st.button("EXECUTE TURN RESOLUTION ⚡", type="primary", use_container_width=True, disabled=(world.get("phase") == "DEBRIEF")):
                if admin_pass != "POTSDAM1945":
                    st.error("INCORRECT AUTHORIZATION PIN.")
                else:
                    with st.spinner("Omniscient Game Master adjudicating directives, AI nations, and crises..."):
                        # Autonomous AI country simulation for AI-assigned powers
                        for c_name, c_info in countries.items():
                            if c_info.get("controller") == "AI" and not state_engine.is_turn_submitted(c_name, world["turn"]):
                                c_objs = state_engine.get_country_objectives(c_name, world["year"])
                                cur_obj = c_objs[0] if c_objs else None
                                ai_dirs = groq_service.generate_ai_country_directives(c_name, c_info, world, cur_obj)
                                for d in ai_dirs:
                                    act = d.get("type", "MILITARY_POSTURE")
                                    tgt = d.get("target", c_name)
                                    desc = d.get("description", "Maintain strategic deterrence.")
                                    cost = state_engine.get_action_cost(c_name, act, tgt)
                                    state_engine.submit_directive(c_name, act, cost, tgt, desc)
                                state_engine.submit_turn(c_name, world["turn"])

                        directives = state_engine.get_pending_directives(world["turn"])
                        stances = state_engine.get_stances()
                        resolution = groq_service.resolve_turn(world, countries, buffers, directives, stances)
                        state_engine.apply_turn_deltas(resolution)

                        for cable in resolution.get("intel_cables", []):
                            state_engine.add_intel_cable(
                                turn=world["turn"],
                                recipient=cable["recipient"],
                                target=cable["target"],
                                summary=cable["intel_summary"],
                                apparent_data=cable["apparent_data"],
                                confidence=cable["confidence_rating"],
                                status=cable["agent_status"]
                            )

                        for news in resolution.get("public_news", []):
                            state_engine.add_news(world["turn"], world["year"], news["headline"], news["body"])

                        hm = resolution.get("history_mirror", {})
                        hist_ref = HISTORICAL_YEARS.get(world["year"], HISTORICAL_YEARS[1945])
                        state_engine.save_history_mirror(
                            year=world["year"],
                            turn=world["turn"],
                            real_history=hist_ref["summary"],
                            sim_history=(hm.get("sim_summary") or hm.get("simulated_summary") or f"In Year {world['year']}, world powers issued {len(directives)} major directives and shifted geopolitical spheres of influence across the globe."),
                            divergence=(hm.get("divergence_analysis") or hm.get("divergence") or "Course diverged dynamically based on player directives."),
                            questions=(hm.get("discussion_questions") or ["What was the primary driver of tension this cycle?"]),
                            legacy=(hm.get("legacy_verdict") or "Strategic balance preserved through deterrence.")
                        )

                    next_turn = world["turn"] + 1
                    if next_turn > 10:
                        st.success(f"Turn {world['turn']} Adjudicated! Cold War Simulation Concluded (1945–1991). Review Final Classroom Gradebook!")
                    else:
                        next_era = COLD_WAR_ERAS.get(next_turn, {})
                        st.success(f"Turn {world['turn']} Adjudicated! Proceeding to {next_era.get('name', f'Era {next_turn}')} ({next_era.get('years_label', '')}).")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 2: UN DIPLOMATIC SUMMITS & CONFERENCES
    # --------------------------------------------------------------------------
    with tab_un:
        st.markdown("### 🏛️ UN GENERAL ASSEMBLY & DIPLOMATIC SUMMIT CHAMBER")
        st.caption("As UN Secretary-General, convene global diplomatic conferences, moderate national delegation speeches, and issue binding arbitration rulings.")

        active_conf = state_engine.get_active_un_conference()
        if active_conf:
            st.markdown(
                f"<div class='hud-panel' style='border-left: 5px solid var(--accent-cyan);'>"
                f"<h4>CONFERENCE IN SESSION: {active_conf['title']}</h4>"
                f"<p style='color: var(--text-secondary);'><b>Year:</b> {active_conf['year']} | <b>Turn:</b> {active_conf['turn']}</p>"
                f"<p><b>Agenda & Flashpoint:</b> {active_conf['agenda']}</p>"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown("##### 🎙️ DELEGATION SPEECHES DELIVERED TO THE PLENARY:")
            speeches = state_engine.get_conference_speeches(active_conf["id"])
            if speeches:
                for sp in speeches:
                    st.markdown(
                        f"<div class='cable-card'>"
                        f"<div class='cable-header'><span>{sp['country']} DELEGATION</span><span>{sp['timestamp']}</span></div>"
                        f"<p style='margin: 4px 0;'>\"{sp['speech_text']}\"</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No delegation speeches submitted yet. Students can speak from their country terminals.")

            st.markdown("---")
            st.markdown("##### ⚖️ ADJOURN & ISSUE BINDING UN RULING:")
            ruling_text = st.text_area("Secretary-General Final Ruling / Demilitarization Decree", "The United Nations orders an immediate ceasefire and deploys peacekeepers to the partition line.")
            if st.button("ISSUE BINDING RESOLUTION & ADJOURN SUMMIT 📜", type="primary"):
                state_engine.adjourn_conference(active_conf["id"], ruling_text)
                st.success("Summit adjourned and binding decree entered into global record.")
                st.rerun()
        else:
            st.markdown("##### 📢 CONVENE AN EXTRAORDINARY UN CONFERENCE:")
            with st.form("convene_conf_form"):
                conf_title = st.text_input("Conference Title", f"Emergency General Assembly on {world['year']} Flashpoints")
                conf_agenda = st.text_area("Summit Agenda & Flashpoint", f"In Year {world['year']}, escalating superpower rivalry threatens world peace. Member states must address contested borders and nuclear proliferation.")
                if st.form_submit_button("CONVENE EMERGENCY UN SUMMIT 🔔"):
                    state_engine.convene_un_conference(world["year"], conf_title, conf_agenda)
                    st.success("UN General Assembly convened into active session!")
                    st.rerun()

    # --------------------------------------------------------------------------
    # TAB 3: DUNGEON MASTER CHAOS CONTROL & MOVING BORDERS
    # --------------------------------------------------------------------------
    with tab_dm:
        st.markdown("### ⚡ DUNGEON MASTER CHAOS CONTROL & MOVING BORDERS")
        st.caption("Absolute teacher oversight: override world tension, move borders, transfer occupied regions, enforce ceasefires, and inject aid or sanctions.")

        dm_col1, dm_col2 = st.columns(2)
        with dm_col1:
            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>DEFCON & TENSION ARBITRATION:</b>", unsafe_allow_html=True)
            new_def = st.slider("MANUAL DEFCON OVERRIDE", 1, 5, world["defcon"], key="dm_defcon_slider")
            if st.button("APPLY DEFCON LEVEL"):
                state_engine.admin_set_defcon(new_def)
                st.success(f"DEFCON manually updated to {new_def}.")
                st.rerun()

            new_ten = st.slider("GLOBAL TENSION OVERRIDE (%)", 0, 100, world["global_tension"], key="dm_tension_slider")
            if st.button("APPLY WORLD TENSION"):
                state_engine.admin_set_tension(new_ten)
                st.success(f"World Tension set to {new_ten}%.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>🕊️ ENFORCE EMERGENCY CEASEFIRE:</b>", unsafe_allow_html=True)
            ceasefire_target = st.selectbox("SELECT THEATER TO PACIFY", ["Korea", "Germany", "Greece", "Iran", "Poland", "Japan"], key="ceasefire_sel")
            if st.button("DEPLOY UN PEACEKEEPERS & HALT HOSTILITIES"):
                state_engine.admin_enforce_ceasefire(ceasefire_target)
                st.success(f"UN Peacekeeping ceasefire deployed to {ceasefire_target} (-15% Global Tension).")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with dm_col2:
            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>🗺️ MOVING BORDERS & TERRITORY TRANSFER:</b>", unsafe_allow_html=True)
            territories = state_engine.get_territories()
            terr_options = list(territories.keys())
            chosen_terr = st.selectbox("SELECT TERRITORY / PROVINCE", terr_options, format_func=lambda x: f"{territories[x]['name']} (Current: {territories[x]['current_controller']})", key="terr_sel")
            new_occupier = st.selectbox("TRANSFER TO OCCUPYING POWER", list(countries.keys()), key="new_occupier_sel")
            if st.button("REDRAW BORDER & TRANSFER CONTROL 🚩"):
                state_engine.admin_transfer_territory(chosen_terr, new_occupier)
                st.success(f"Territory {territories[chosen_terr]['name']} transferred to {new_occupier}! Border color dynamically updated on map.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
            st.markdown("<b>💰 AID & SANCTIONS ARBITRATION:</b>", unsafe_allow_html=True)
            target_nation = st.selectbox("TARGET NATION", list(countries.keys()), key="aid_target_nation")
            col_aid1, col_aid2 = st.columns(2)
            with col_aid1:
                if st.button(f"INJECT $100M AID TO {target_nation}"):
                    state_engine.admin_inject_aid(target_nation, 100)
                    st.success(f"+$100M injected into {target_nation} treasury.")
                    st.rerun()
            with col_aid2:
                if st.button(f"IMPOSE SANCTIONS ON {target_nation}"):
                    state_engine.admin_impose_sanctions(target_nation)
                    st.warning(f"Sanctions imposed on {target_nation} (-$50M, +10 tension).")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 4: AI PEACEKEEPER ADVISORIES
    # --------------------------------------------------------------------------
    with tab_ai:
        st.markdown("### 🕊️ UN PEACEMAKING ADVISORIES & STRATEGIC RECOMMENDATIONS")
        st.caption("AI Diplomatic Envoy analysis of the wargame board providing 3 actionable, non-partisan strategies to preserve world peace.")

        if st.button("GENERATE FRESH PEACEKEEPING RECOMMENDATIONS 🕊️", key="gen_peace_btn"):
            with st.spinner("Analyzing superpower flashpoints and military friction..."):
                recs = groq_service.get_un_peacemaking_advice(world, countries, buffers, state_engine.get_active_crises())
                st.session_state["_cached_un_recs"] = recs

        recs = st.session_state.get("_cached_un_recs", groq_service.get_un_peacemaking_advice(world, countries, buffers, []))
        for idx, r in enumerate(recs, 1):
            st.markdown(
                f"<div class='hud-panel' style='border-left: 4px solid var(--accent-green); margin-bottom: 12px;'>"
                f"<b style='color: var(--accent-green); font-size: 1.05rem;'>RECOMMENDATION {idx}: {r['title']}</b><br/>"
                f"<p style='margin: 6px 0;'><b>Proposed Action:</b> {r['action']}</p>"
                f"<span style='color: var(--text-secondary); font-size: 0.88rem;'><i>Rationale: {r['rationale']}</i></span>"
                f"</div>",
                unsafe_allow_html=True
            )

    # --------------------------------------------------------------------------
    # TAB 5: CLASSROOM GRADEBOOK & OBJECTIVES PROGRESS
    # --------------------------------------------------------------------------
    with tab_grades:
        st.markdown("### 🎓 CLASSROOM GRADEBOOK & NATIONAL OBJECTIVES")
        st.caption("Live scoring and end-game grading (A–F) based on historical annual objectives and long-term doctrine fulfillment.")

        gradebook = state_engine.get_final_gradebook()
        for c_name, g in gradebook.items():
            badge_color = "var(--accent-green)" if "A" in g["letter_grade"] else ("var(--accent-cyan)" if g["letter_grade"] == "B" else "var(--accent-amber)")
            st.markdown(
                f"<div class='hud-panel' style='margin-bottom: 10px;'>"
                f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<div><b>{c_name}</b> <span style='color:var(--text-secondary); font-size:0.85rem;'>({g['controller']} DELEGATION)</span></div>"
                f"<div style='font-size:1.3rem; font-weight:800; color:{badge_color};'>GRADE: {g['letter_grade']} ({g['final_score']}/100)</div>"
                f"</div>"
                f"<div style='margin-top:6px; font-size:0.88rem; color:var(--text-secondary);'>"
                f"• <b>Long-Term Objective:</b> {g['long_term_objective']}<br/>"
                f"• <b>Annual Objectives Earned:</b> {g['annual_earned']} / {g['annual_total']} pts | <b>Doctrine Bonus:</b> +{g['long_term_bonus']} pts<br/>"
                f"• <b>UN Assessment:</b> <i>{g['verdict']}</i>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    # --------------------------------------------------------------------------
    # TAB 6: ROSTER SETUP (STUDENT VS AI)
    # --------------------------------------------------------------------------
    with tab_setup:
        st.markdown("### ⚙️ GAME SETUP & STUDENT/AI ROSTER CONFIGURATION")
        st.caption("Select which nations are controlled by human students vs autonomous AI agents.")

        curr_ctrls = state_engine.get_country_controllers()
        selected_students = []
        c_cols = st.columns(4)
        for idx, (c_name, ctrl) in enumerate(curr_ctrls.items()):
            col = c_cols[idx % 4]
            with col:
                is_student = (ctrl == "STUDENT")
                checked = st.checkbox(f"{c_name}", value=is_student, key=f"roster_{c_name}")
                if checked:
                    selected_students.append(c_name)

        st.markdown("---")
        if st.button("SAVE ROSTER & RE-INITIALIZE GAME FROM 1945 🔄", type="primary"):
            state_engine.reset_game(student_countries=selected_students)
            st.success(f"Simulation re-anchored to 1945! {len(selected_students)} powers assigned to students, {8 - len(selected_students)} to autonomous AI.")
            st.rerun()

    # Historical Debrief Modal / Expander
    if world.get("phase") == "DEBRIEF" or st.session_state.get("show_debrief", False):
        st.markdown("---")
        st.markdown(f"### 📚 YEAR {world['year'] - 1} HISTORICAL DEBRIEF & DISCUSSION")
        hm_record = state_engine.get_history_mirror(world["year"] - 1)
        if hm_record:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
                st.markdown("<b style='color: var(--accent-cyan);'>WHAT ACTUALLY HAPPENED IN HISTORY:</b>", unsafe_allow_html=True)
                st.write(hm_record["real_history"])
                st.markdown("</div>", unsafe_allow_html=True)
            with col_b:
                st.markdown("<div class='hud-panel'>", unsafe_allow_html=True)
                st.markdown("<b style='color: var(--accent-amber);'>WHAT YOUR CLASSROOM DID:</b>", unsafe_allow_html=True)
                st.write(hm_record["sim_history"])
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='hud-panel-primary'>", unsafe_allow_html=True)
            st.markdown("<b>TEACHER DISCUSSION PROMPTS:</b>", unsafe_allow_html=True)
            for q in hm_record["discussion_questions"]:
                st.markdown(f"• *{q}*")
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("OPEN NEXT YEAR DIRECTIVES ➡️"):
            state_engine.set_phase("DIRECTIVES")
            st.rerun()

# ==============================================================================
# VIEW 2: STUDENT NATION TERMINAL (AI ADVISER CENTRAL HUB, 3D MAP, RED PHONE, NOTIFICATIONS)
# ==============================================================================
else:
    country_name = selected_view.replace("🚩 ", "").strip()
    c_data = state_engine.get_country(country_name)
    if not c_data:
        st.error(f"Nation '{country_name}' not cataloged.")
        st.stop()

    persona = ADVISER_PERSONAS.get(country_name, {
        "name": f"Chief Strategic Adviser of {country_name}",
        "title": "Diplomatic & Defense Envoy",
        "system_prompt": "You advise the national leadership."
    })

    # Prepare Classified Intelligence Dossiers for AI Adviser
    briefings = []
    for other_c in countries.keys():
        if other_c != country_name:
            dos = state_engine.get_country_dossier(country_name, other_c)
            has_spy = dos.get("has_active_spy", False)
            briefings.append(
                f"- {other_c}: Stockpile: {dos.get('bombs_display', 'Unknown')}, "
                f"Capability: {dos.get('nuclear_status', 'Unknown')}, "
                f"Treasury: {dos.get('treasury_display', 'Unknown')}, "
                f"Confidence: {dos.get('confidence_label', 'Unknown')}, "
                f"Active HUMINT Spy Network: {'YES (ACTIVE INFILTRATION)' if has_spy else 'NO (CRUDE DIPLOMATIC RUMORS ONLY)'}"
            )
    intel_briefings_str = "\n".join(briefings)

    # --------------------------------------------------------------------------
    # MODAL DIALOG 1: RED PHONE (HOTLINE & BILATERAL PACTS)
    # --------------------------------------------------------------------------
    @st.dialog("📞 RED PHONE: ENCRYPTED DIPLOMATIC HOTLINE & TREATIES")
    def show_red_phone_dialog(curr_country, all_countries):
        st.caption("Direct encrypted channel between world powers. Negotiate bilateral trade accords, financial assistance, and non-aggression treaties. Warning: Enemy HUMINT spy networks have a 35% chance to tap telex lines!")

        tab_pacts, tab_telex = st.tabs([
            "🤝 BILATERAL PACTS & AID REQUESTS",
            "💬 ENCRYPTED TELEX HOTLINE"
        ])

        other_countries = [c for c in all_countries.keys() if c != curr_country]

        with tab_pacts:
            incoming_pacts = state_engine.get_pact_proposals(curr_country, status="PENDING")
            if incoming_pacts:
                st.markdown("###### 📬 INCOMING PACT PROPOSALS (AWAITING YOUR SIGNATURE):")
                for p in incoming_pacts:
                    st.markdown(
                        f"<div class='pact-card'>"
                        f"<div class='pact-card-header'><span>PROPOSAL #{p['id']} FROM: <b>{p['proposer']}</b></span><span>TYPE: <b>{p.get('proposal_type') or p.get('pact_type')}</b></span></div>"
                        f"<b>Terms:</b> {p['terms']}<br/>"
                        f"<span style='font-size: 0.85rem; color: var(--text-secondary);'><i>\"{p['message']}\"</i></span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    col_p_acc, col_p_rej = st.columns(2)
                    with col_p_acc:
                        if st.button(f"✅ ACCEPT & RATIFY #{p['id']}", key=f"acc_pact_{p['id']}", type="primary", use_container_width=True):
                            ok, msg = state_engine.respond_to_pact(p["id"], curr_country, "ACCEPTED")
                            if ok:
                                st.success(msg)
                            else:
                                st.error(msg)
                            st.rerun()
                    with col_p_rej:
                        if st.button(f"❌ DECLINE #{p['id']}", key=f"rej_pact_{p['id']}", use_container_width=True):
                            ok, msg = state_engine.respond_to_pact(p["id"], curr_country, "REJECTED")
                            st.info(msg)
                            st.rerun()
                st.markdown("---")

            st.markdown("###### 📝 DRAFT FORMAL BILATERAL PROPOSAL / FINANCIAL REQUEST:")
            p_target = st.selectbox("RECIPIENT POWER:", other_countries, key="dlg_pact_target")
            p_type_option = st.selectbox("PROPOSAL TYPE:", [
                "Commercial Trade Accord (+$25M/turn mutual revenue)",
                "Request Sovereign Financial Loan / Aid ($25M–$100M)",
                "Atomic Technology Sharing & Reactor Collab (+50% R&D, +1 MT Uranium)",
                "Bilateral Non-Aggression Pact"
            ], key="dlg_pact_type_opt")

            if "Trade Accord" in p_type_option:
                p_type = "TRADE_PACT"
                p_terms = "Bilateral trade accord: +$25M treasury revenue each turn for both nations"
            elif "Financial Loan" in p_type_option:
                p_type = "FINANCIAL_AID"
                aid_amt = st.slider("REQUESTED AID AMOUNT ($M):", min_value=25, max_value=100, step=25, value=50, key="dlg_pact_aid_slider")
                p_terms = f"Emergency financial grant / sovereign loan transfer of ${aid_amt}M"
            elif "Atomic Technology" in p_type_option:
                p_type = "ATOMIC_COLLAB"
                p_terms = "Bilateral nuclear reactor blueprints, isotope separation physics, and 1 MT Uranium"
            else:
                p_type = "NON_AGGRESSION"
                p_terms = "Bilateral non-aggression and frontier border demilitarization"

            p_msg = st.text_input("DIPLOMATIC NOTE / REASONING:", placeholder=f"Draft diplomatic argument to {p_target}...", key="dlg_pact_note")

            if st.button("DISPATCH PROPOSAL VIA RED PHONE 📨", type="primary", use_container_width=True):
                if not p_msg.strip():
                    p_msg = f"Formal diplomatic proposal dispatched from {curr_country}."
                pact_id = state_engine.propose_bilateral_pact(curr_country, p_target, p_type, p_terms, p_msg.strip())

                with st.spinner(f"Transmitting encrypted proposal to {p_target}..."):
                    tgt_state = all_countries.get(p_target, {})
                    ai_decision = groq_service.evaluate_ai_pact_proposal(p_target, curr_country, p_type, p_terms, p_msg.strip(), tgt_state)

                    if ai_decision.get("accepted"):
                        state_engine.respond_to_pact(pact_id, p_target, "ACCEPTED")
                        state_engine.send_hotline_message(p_target, curr_country, f"[TREATY ACCEPTED]: {ai_decision.get('reply')}")
                        st.success(f"🤝 TREATY RATIFIED! {p_target} accepted: \"{ai_decision.get('reply')}\"")
                    else:
                        state_engine.respond_to_pact(pact_id, p_target, "REJECTED")
                        state_engine.send_hotline_message(p_target, curr_country, f"[PROPOSAL DECLINED]: {ai_decision.get('reply')}")
                        st.warning(f"❌ PROPOSAL DECLINED by {p_target}: \"{ai_decision.get('reply')}\"")
                st.rerun()

        with tab_telex:
            h_target = st.selectbox("TELEX RECIPIENT:", other_countries, key="dlg_phone_target")
            h_text = st.text_input("ENCRYPTED TRANSMISSION:", key="dlg_phone_msg", placeholder=f"Draft diplomatic communique to {h_target}...")

            if st.button("DISPATCH ENCRYPTED CABLE 📨", type="primary", key="btn_send_telex", use_container_width=True):
                if h_text.strip():
                    _, note, intercepted = state_engine.send_hotline_message(curr_country, h_target, h_text.strip())
                    st.success(note)
                    st.rerun()
                else:
                    st.warning("Please type a message before transmitting.")

            st.markdown("---")
            st.markdown("###### 📜 ARCHIVED HOTLINE CABLES:")
            hotline_logs = state_engine.get_hotline_messages(curr_country)
            if not hotline_logs:
                st.caption("No diplomatic cables on this frequency.")
            else:
                for m in hotline_logs:
                    intercept_tag = "<span style='color:var(--accent-red); font-weight: 700;'>[INTERCEPTED]</span>" if m.get("is_intercepted") else "<span style='color:var(--accent-green); font-weight: 700;'>[ENCRYPTED]</span>"
                    st.markdown(
                        f"<div class='cable-card'>"
                        f"<div class='cable-header'><span>FROM: <b>{m['sender']}</b> ➔ TO: <b>{m['recipient']}</b></span><span>{intercept_tag}</span></div>"
                        f"<div style='font-size: 0.88rem; font-family: var(--font-mono); margin-top: 4px;'>{m['content']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )


    # --------------------------------------------------------------------------
    # MODAL DIALOG 2: NOTIFICATION CENTRE
    # --------------------------------------------------------------------------
    @st.dialog("📡 C2 NOTIFICATION & FIELD CABLE CENTRE")
    def show_notifications_dialog(curr_country):
        tab_cables, tab_unsc, tab_dispatches = st.tabs([
            "🕵️ DECRYPTED SPY CABLES",
            "🇺🇳 UN SECURITY COUNCIL",
            "📰 WORLD & CRISIS DISPATCHES"
        ])

        with tab_cables:
            cables = state_engine.get_intel_cables(curr_country)
            if not cables:
                st.info("No decrypted field spy cables on file. Deploy intelligence operatives via your AI adviser to monitor foreign atomic programs.")
            else:
                for c in cables:
                    st.markdown(
                        f"<div class='cable-card cable-card-secret'>"
                        f"<div class='cable-header'><span>TARGET: <b>{c['target']}</b></span><span class='badge-c2 badge-secret'>{c['confidence_rating']}</span></div>"
                        f"<b>{c['intel_summary']}</b><br/>"
                        f"<div style='font-size: 0.9rem; font-family: var(--font-mono); color: var(--accent-amber); margin-top: 4px;'>{c['apparent_data']}</div>"
                        f"<div style='font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px;'>ASSET STATUS: {c['agent_status']} • TURN {c['turn']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        with tab_unsc:
            resolutions = state_engine.get_unsc_resolutions()
            if not resolutions:
                st.caption("No resolutions currently pending before the council.")
            else:
                for res in resolutions:
                    st.markdown(
                        f"<div class='cable-card cable-card-unsc'>"
                        f"<div class='cable-header'><span>RESOLUTION #{res['id']} • TARGET: {res['target']}</span><span>STATUS: <b>{res['status']}</b></span></div>"
                        f"<b>{res['title']}</b><br/>"
                        f"<span style='font-size: 0.85rem;'>{res['description']}</span><br/>"
                        f"<span style='font-size: 0.8rem; color: var(--text-secondary);'>Votes Recorded: {res['votes']}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    if res["status"] == "PENDING":
                        is_p5 = curr_country in UNSC_PERM_5
                        v_col1, v_col2 = st.columns(2)
                        with v_col1:
                            if st.button("Vote YES", key=f"dlg_v_yes_{res['id']}", use_container_width=True):
                                state_engine.vote_unsc_resolution(res["id"], curr_country, "YES")
                                st.rerun()
                        with v_col2:
                            lbl = "VETO (NO)" if is_p5 else "Vote NO"
                            if st.button(lbl, key=f"dlg_v_no_{res['id']}", use_container_width=True):
                                state_engine.vote_unsc_resolution(res["id"], curr_country, "NO")
                                st.rerun()

        with tab_dispatches:
            events = state_engine.get_random_events()
            for ev in events[:4]:
                st.markdown(
                    f"<div class='cable-card cable-card-secret'>"
                    f"<div class='cable-header'><span>YEAR {ev['year']} • STRATEGIC EVENT</span><span>{ev['event_type']}</span></div>"
                    f"<b>{ev['title']}</b><br/>"
                    f"<span style='font-size: 0.85rem; color: var(--text-secondary);'>{ev['description']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            news = state_engine.get_news(limit=10)
            for n in news:
                st.markdown(
                    f"<div class='cable-card'>"
                    f"<div class='cable-header'><span>YEAR {n['year']}</span><span>GLOBAL TELEGRAPH</span></div>"
                    f"<b>{n['headline']}</b><br/>"
                    f"<span style='font-size: 0.85rem; color: var(--text-secondary);'>{n['body']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------------------------
    # TOP HEADER & POPUP ACTION BUTTONS
    # --------------------------------------------------------------------------
    is_p5 = country_name in UNSC_PERM_5
    cables_count = len(state_engine.get_intel_cables(country_name))
    orders_count = state_engine.get_directive_count(country_name, world["turn"])
    is_submitted = state_engine.is_turn_submitted(country_name, world["turn"])

    col_hdr_left, col_hdr_right = st.columns([7, 5])
    with col_hdr_left:
        st.markdown(
            f"<div>"
            f"<h2 style='margin: 0;'>{country_name.upper()} // STRATEGIC COMMAND</h2>"
            f"<span style='color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.85rem;'>"
            f"HEAD OF MISSION: <b>{persona['name']}</b> ({persona['title']}) • CAPITAL: {c_data['capital']}"
            f"</span><br/>"
            f"<span class='badge-c2 {'badge-unsc' if is_p5 else 'badge-conf'}'>{'UNSC PERM-5 (VETO)' if is_p5 else 'UN GENERAL MEMBER'}</span> "
            f"<span class='badge-c2 {'badge-secret' if c_data['nuclear'] else 'badge-conf'}'>{'ATOMIC CAPABLE' if c_data['nuclear'] else 'CONVENTIONAL'}</span> "
            f"<span class='badge-c2' style='background: {'#238636' if is_submitted else '#1f6feb'}; color: white;'>{'STATUS: SUBMITTED' if is_submitted else f'ORDERS: {orders_count}/3'}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col_hdr_right:
        st.markdown("<div style='display: flex; gap: 8px; justify-content: flex-end; align-items: center; height: 100%;'>", unsafe_allow_html=True)
        btn_c0, btn_c1, btn_c2 = st.columns([4, 4, 4])
        with btn_c0:
            if is_submitted:
                st.button("✅ SUBMITTED", disabled=True, key=f"sub_btn_{country_name}", use_container_width=True)
            else:
                if st.button(f"🏁 SUBMIT TURN ({orders_count}/3)", type="primary", key=f"sub_btn_{country_name}", use_container_width=True):
                    state_engine.submit_turn(country_name, world["turn"])
                    st.toast(f"Strategic orders submitted for {country_name}!")
                    st.rerun()
        with btn_c1:
            pending_pacts = state_engine.get_pending_pacts_count(country_name)
            phone_lbl = f"📞 RED PHONE ({pending_pacts} PACTS)" if pending_pacts > 0 else "📞 RED PHONE"
            if st.button(phone_lbl, type="primary" if pending_pacts > 0 else "secondary", use_container_width=True):
                show_red_phone_dialog(country_name, countries)
        with btn_c2:
            if st.button(f"🔔 ALERTS ({cables_count})", use_container_width=True):
                show_notifications_dialog(country_name)
        st.markdown("</div>", unsafe_allow_html=True)

    # Country Specialty & Historical Cold War Doctrine Banner
    spec = COUNTRY_SPECIALTIES.get(country_name, {})
    if spec:
        traits_html = "".join([f"<div class='specialty-trait-pill'>• {t}</div>" for t in spec.get("traits", [])])
        st.markdown(
            f"<div class='specialty-card'>"
            f"<div class='specialty-title'>🏛️ {spec.get('title', '').upper()}</div>"
            f"<div class='specialty-doctrine'>DOCTRINE: {spec.get('doctrine', '')}</div>"
            f"<div class='specialty-desc'>{spec.get('description', '')}</div>"
            f"<div class='specialty-traits'>{traits_html}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Telemetry Ribbon
    t1, t2, t3, t4, t5, t6, t7 = st.columns(7)
    with t1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TREASURY</div><div class='metric-val metric-val-mono'>${c_data['treasury']}M</div></div>", unsafe_allow_html=True)
    with t2:
        if c_data['nuclear']:
            st.markdown(f"<div class='metric-box'><div class='metric-label'>WARHEADS</div><div class='metric-val metric-val-mono'>{c_data['bombs']}</div></div>", unsafe_allow_html=True)
        else:
            prog = c_data.get('nuclear_progress', 0)
            st.markdown(f"<div class='metric-box'><div class='metric-label'>ATOMIC R&D</div><div class='metric-val metric-val-mono' style='color: var(--accent-cyan);'>{prog}%</div></div>", unsafe_allow_html=True)
    with t3:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>ORDERS</div><div class='metric-val metric-val-mono' style='color: {'#f85149' if orders_count >= 3 else '#58a6ff'};'>{orders_count}/3</div></div>", unsafe_allow_html=True)
    with t4:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>URANIUM</div><div class='metric-val'>{c_data.get('uranium', 0)} MT</div></div>", unsafe_allow_html=True)
    with t5:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>OIL SUPPLY</div><div class='metric-val'>{c_data.get('oil', 50)}%</div></div>", unsafe_allow_html=True)
    with t6:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>STABILITY</div><div class='metric-val'>{c_data.get('domestic_approval', 75)}%</div></div>", unsafe_allow_html=True)
    with t7:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TENSION</div><div class='metric-val'>{c_data['tension']}%</div></div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # START-OF-YEAR WORLD FLASHPOINT & CRISIS BRIEFING
    # --------------------------------------------------------------------------
    std_era_id = min(10, max(1, world['turn']))
    std_era = COLD_WAR_ERAS.get(std_era_id, COLD_WAR_ERAS[1])
    curr_event = state_engine.get_annual_world_event(world["year"]) or state_engine.get_annual_world_event(world["turn"])
    if curr_event:
        st.markdown(
            f"<div class='hud-panel' style='border-left: 5px solid #d29922; margin-top: 14px; margin-bottom: 12px; background: #0c1017;'>"
            f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
            f"<div>"
            f"<span style='color: #d29922; font-family: var(--font-mono); font-weight: 800; font-size: 0.95rem; letter-spacing: 0.05em;'>"
            f"🌍 {std_era['name'].upper()} FLASHPOINT: {curr_event['headline'].upper()}"
            f"</span>"
            f"</div>"
            f"<span class='badge-c2 badge-secret'>THEATER: {curr_event['affected_theaters']}</span>"
            f"</div>"
            f"<p style='margin: 8px 0 6px 0; font-size: 0.92rem; line-height: 1.5;'>{curr_event['briefing']}</p>"
            f"<div style='font-size: 0.8rem; color: var(--text-secondary); border-top: 1px solid #21262d; padding-top: 6px;'>"
            f"<b>Historical Record:</b> <i>{curr_event['historical_baseline']}</i>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------------------------
    # ACTIVE UN DIPLOMATIC SUMMIT PLENARY (IF IN SESSION)
    # --------------------------------------------------------------------------
    active_conf = state_engine.get_active_un_conference()
    if active_conf:
        with st.expander(f"🏛️ EMERGENCY UN SUMMIT IN SESSION: {active_conf['title'].upper()}", expanded=True):
            st.markdown(
                f"<div style='margin-bottom: 8px; font-size: 0.9rem;'>"
                f"<b>Summit Agenda:</b> {active_conf['agenda']}"
                f"</div>",
                unsafe_allow_html=True
            )
            speeches = state_engine.get_conference_speeches(active_conf["id"])
            if speeches:
                st.markdown("<b style='font-size: 0.85rem; color: var(--accent-cyan);'>DELEGATION STATEMENTS:</b>", unsafe_allow_html=True)
                for sp in speeches[-4:]:
                    st.markdown(
                        f"<div class='cable-card' style='padding: 6px 12px; margin-bottom: 6px;'>"
                        f"<span style='font-weight: 700; color: #58a6ff;'>{sp['country']}:</span> \"{sp['speech_text']}\""
                        f"</div>",
                        unsafe_allow_html=True
                    )

            c_speech_input = st.text_input(
                f"SUBMIT {country_name.upper()} DELEGATION STATEMENT TO THE GENERAL ASSEMBLY:",
                placeholder="State your nation's diplomatic position on the current crisis...",
                key=f"student_speech_in_{active_conf['id']}"
            )
            if st.button("DELIVER SPEECH TO GENERAL ASSEMBLY 🎙️", key=f"btn_send_speech_{active_conf['id']}", type="primary"):
                if c_speech_input.strip():
                    state_engine.submit_conference_speech(active_conf["id"], country_name, c_speech_input.strip())
                    st.success("Your diplomatic statement has been entered into the official UN plenary record!")
                    st.rerun()
                else:
                    st.warning("Please type a diplomatic statement before submitting.")

    # --------------------------------------------------------------------------
    # NATIONAL STRATEGIC OBJECTIVES HUD
    # --------------------------------------------------------------------------
    c_objs = state_engine.get_country_objectives(country_name, world["year"]) or state_engine.get_country_objectives(country_name, world["turn"])
    lt_obj = c_data.get("long_term_objective", "Maintain sovereign independence and national prestige.")
    
    with st.expander(f"🎯 STRATEGIC OBJECTIVES & DIPLOMATIC SCORECARD ({std_era['name']} • {std_era['title']})", expanded=True):
        st.markdown(
            f"<div style='margin-bottom: 10px; padding: 8px 12px; background: rgba(88, 166, 255, 0.08); border-left: 3px solid #58a6ff; border-radius: 4px;'>"
            f"<b style='color: #58a6ff;'>🌟 GRAND DOCTRINE (LONG-TERM):</b> {lt_obj}"
            f"</div>",
            unsafe_allow_html=True
        )
        if c_objs:
            obj_cols = st.columns(len(c_objs))
            for idx, obj in enumerate(c_objs):
                with obj_cols[idx]:
                    st_val = obj["status"]
                    if st_val == "COMPLETED":
                        st_badge = "<span style='color: #3fb950; font-weight: 700;'>✅ COMPLETED</span>"
                        b_col = "#238636"
                    elif st_val == "FAILED":
                        st_badge = "<span style='color: #f85149; font-weight: 700;'>❌ FAILED</span>"
                        b_col = "#da3633"
                    else:
                        st_badge = "<span style='color: #d29922; font-weight: 700;'>⏳ PENDING</span>"
                        b_col = "#9e6a03"

                    obj_pts = obj.get("weight") or obj.get("points", 10)
                    st.markdown(
                        f"<div class='hud-panel' style='border-top: 3px solid {b_col}; min-height: 140px; padding: 10px;'>"
                        f"<div style='display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;'>"
                        f"<span><b>OBJECTIVE #{idx+1}</b></span>"
                        f"<span>+{obj_pts} PTS</span>"
                        f"</div>"
                        f"<b style='font-size: 0.88rem;'>{obj['title']}</b>"
                        f"<p style='font-size: 0.8rem; color: var(--text-secondary); margin: 6px 0;'>{obj['description']}</p>"
                        f"<div style='font-size: 0.75rem; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;'>"
                        f"<span>Status:</span> {st_badge}"
                        f"</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
        else:
            st.caption("No specific tactical directives recorded for this calendar year.")

    # --------------------------------------------------------------------------
    # SECTION 1: THE 3D STRATEGIC MAP & TARGET INSPECTOR
    # --------------------------------------------------------------------------
    st.markdown("---")
    col_map_hdr, col_map_sel = st.columns([6, 6])
    with col_map_hdr:
        st.markdown("#### 🌐 3D GLOBAL SITUATION & STRATEGIC ARCS")
    with col_map_sel:
        all_territories = list(countries.keys()) + list(buffers.keys())
        default_target = "USSR" if country_name != "USSR" else "USA"
        inspected_target = st.selectbox(
            "SELECT TARGET NATION FOR SATELLITE HIGHLIGHT & INTELLIGENCE DOSSIER:",
            all_territories,
            index=all_territories.index(default_target) if default_target in all_territories else 0
        )

    # Quick Dossier Banner for the selected target
    target_dossier = state_engine.get_country_dossier(country_name, inspected_target)
    has_spy = target_dossier.get('has_active_spy', False)
    spy_badge = "<span class='badge-c2' style='background: #238636; color: white;'>ACTIVE HUMINT SPY RING</span>" if has_spy else "<span class='badge-c2' style='background: #9e6a03; color: white;'>UNVERIFIED (NO ACTIVE SPY)</span>"
    warning_note = "" if has_spy else f"<div style='font-size: 0.76rem; color: var(--accent-amber); margin-top: 5px;'>⚠️ Lacking an active spy network in {inspected_target}, our ministry relies on crude diplomatic rumors and speculative embassy gossip. Deploy an intelligence operative to unlock high-precision telemetry.</div>"
    st.markdown(
        f"<div class='dossier-card' style='margin-bottom: 8px; padding: 10px 14px;'>"
        f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
        f"<div>"
        f"<b>TARGET: {inspected_target.upper()}</b> • "
        f"Atomic Stockpile: <b style='color: var(--accent-amber);'>{target_dossier.get('bombs_display', 'Classified')}</b> • "
        f"Capability: <b>{target_dossier.get('nuclear_status', 'Conventional')}</b> • "
        f"Treasury: <b>{target_dossier.get('treasury_display', 'Unknown')}</b>"
        f"</div>"
        f"<div>"
        f"{spy_badge} "
        f"<span class='badge-c2 badge-secret'>{target_dossier.get('confidence_label', 'CONFIDENTIAL')}</span>"
        f"</div>"
        f"</div>"
        f"{warning_note}"
        f"</div>",
        unsafe_allow_html=True
    )

    # Render The 3D Map (with 3D arcs, capitals, fixed labels, pitch/bearing)
    render_strategic_map(highlight_target=inspected_target)

    # --------------------------------------------------------------------------
    # SECTION 2: THE AI ADVISER CONSOLE (THE CENTRAL POINT OF EVERYTHING)
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"#### 🎙️ AI ADVISER CONSOLE // {persona['name'].upper()}")
    st.caption(f"Instruct your senior adviser in plain English. Maximum 3 directives per cycle. Treasury reserves fund all military, intelligence, and diplomatic actions.")

    if orders_count >= 3:
        st.warning(f"⚠️ **DIRECTIVE CAPACITY REACHED (3/3):** {country_name} has dispatched all authorized directives for Turn Cycle {world['turn']}. Click '🏁 SUBMIT TURN' above to lock in your strategy.")

    # Dynamic Action Costs based on Country Specialties & Friction
    atk_cost = state_engine.get_action_cost(country_name, "ATTACK", inspected_target)
    spy_cost = state_engine.get_action_cost(country_name, "SPY", inspected_target)
    bomb_cost = state_engine.get_action_cost(country_name, "BUILD_BOMB")
    bond_amount = 200 if country_name == "China" else 150

    # Quick Tactical Directive Chips
    st.markdown("<span style='font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);'>QUICK TACTICAL DIRECTIVES:</span>", unsafe_allow_html=True)
    c_btn0, c_btn1, c_btn2, c_btn3, c_btn4, c_btn5 = st.columns(6)
    with c_btn0:
        if st.button(f"⚔️ Attack {inspected_target} (${atk_cost}M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Launch a military offensive / attack on {inspected_target} (${atk_cost}M budget)"
            st.rerun()
    with c_btn1:
        if st.button(f"🕵️ Spy on {inspected_target} (${spy_cost}M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Deploy an intelligence spy network to {inspected_target} (${spy_cost}M) to check their nuclear weapons stockpile and capability"
            st.rerun()
    with c_btn2:
        if c_data['nuclear']:
            if st.button(f"⚛️ Commission Bomb (${bomb_cost}M)", use_container_width=True, disabled=(orders_count >= 3)):
                st.session_state[f"staged_cmd_{country_name}"] = f"Assemble 1 atomic bomb under ${bomb_cost}M budget"
                st.rerun()
        else:
            rd_cost = 90 if country_name == "France" else 100
            prog = c_data.get('nuclear_progress', 0)
            if st.button(f"🔬 Atomic R&D ({prog}% | ${rd_cost}M)", use_container_width=True, disabled=(orders_count >= 3)):
                st.session_state[f"staged_cmd_{country_name}"] = f"Fund domestic atomic research reactor and nuclear physics program (${rd_cost}M)"
                st.rerun()
    with c_btn3:
        if st.button(f"💵 War Bonds (+${bond_amount}M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Issue emergency sovereign war bonds to raise ${bond_amount}M cash"
            st.rerun()
    with c_btn4:
        if st.button(f"🤝 Treaty with {inspected_target}", use_container_width=True):
            show_red_phone_dialog(country_name, countries)
    with c_btn5:
        if st.button(f"📜 UNSC Sanction on {inspected_target}", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Table a formal resolution in the UN Security Council against {inspected_target}"
            st.rerun()


    chat_key = f"chat_history_{country_name}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {"role": "assistant", "content": f"Commander, {persona['name']} standing by. The year is {world['year']}. You hold ${c_data['treasury']}M in Treasury reserves, {c_data['bombs']} atomic warheads, and have issued {orders_count}/3 directives this cycle. Instruct me on our nuclear expansion, intelligence operations, military maneuvers, or diplomatic treaties."}
        ]

    # Staged quick commands
    staged_key = f"staged_cmd_{country_name}"
    staged_val = st.session_state.get(staged_key, "")
    if staged_val:
        st.session_state[staged_key] = ""

    # Chat Transcript Container
    chat_container = st.container(height=380)
    with chat_container:
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Directive Authorization Card
    proposal_key = f"pending_proposal_{country_name}"
    if proposal_key in st.session_state and st.session_state[proposal_key]:
        prop = st.session_state[proposal_key]
        st.markdown(
            f"<div class='hud-panel-amber' style='margin-bottom: 12px;'>"
            f"<b style='color: var(--accent-amber); font-size: 1.05rem;'>📋 PENDING OPERATIONAL DIRECTIVE (AWAITING YOUR AUTHORIZATION):</b><br>"
            f"<span style='font-size: 0.9rem;'>• Action: <b>{prop.get('type')}</b> | Target: <b>{prop.get('target')}</b></span><br>"
            f"<span style='font-size: 0.9rem;'>• Budget: <b>${prop.get('cost_m', 0)}M</b> | Effect: <b>{prop.get('description', '')}</b></span>"
            f"</div>",
            unsafe_allow_html=True
        )
        col_auth1, col_auth2 = st.columns(2)
        with col_auth1:
            if st.button("🚀 AUTHORIZE & EXECUTE ORDER", type="primary", use_container_width=True):
                success, exec_msg, rej = state_engine.execute_structured_action(country_name, prop)
                st.session_state[proposal_key] = None
                if success:
                    conf_reply = f"**{persona['name']} to Commander:** Directive confirmed and executed.\n\n{exec_msg}"
                else:
                    conf_reply = f"**{persona['name']} to Commander:** Directive ABORTED.\n\n⚠️ {rej or exec_msg}"
                st.session_state[chat_key].append({"role": "assistant", "content": conf_reply})
                st.rerun()
        with col_auth2:
            if st.button("❌ CANCEL / REVISE", use_container_width=True):
                st.session_state[proposal_key] = None
                st.rerun()

    # Chat Input
    user_prompt = st.chat_input(f"Instruct {persona['name']} (e.g. 'Attack Germany', 'Spy on USSR', 'Build bomb', 'Authorize')...")
    if staged_val and not user_prompt:
        user_prompt = staged_val

    if user_prompt:
        st.session_state[chat_key].append({"role": "user", "content": user_prompt})

        # Check if confirming existing proposal via natural language
        u_clean = user_prompt.lower().strip()
        if u_clean in ["go", "confirm", "do it", "approved", "authorize", "execute", "yes", "proceed"] and proposal_key in st.session_state and st.session_state[proposal_key]:
            prop = st.session_state[proposal_key]
            success, exec_msg, rejection = state_engine.execute_structured_action(country_name, prop)
            st.session_state[proposal_key] = None
            if success:
                reply = f"**{persona['name']} to Commander:** Directive confirmed and executed.\n\n{exec_msg}"
            else:
                reply = f"**{persona['name']} to Commander:** Directive ABORTED.\n\n⚠️ {rejection or exec_msg}"
            st.session_state[chat_key].append({"role": "assistant", "content": reply})
            st.rerun()

        # Query AI adviser with full intelligence briefing context
        with st.spinner("Adviser evaluating strategic options and intelligence cables..."):
            action_cmd, reply = groq_service.chat_with_adviser(
                country=country_name,
                conversation_history=st.session_state[chat_key],
                user_message=user_prompt,
                current_year=world["year"],
                country_state=c_data,
                intelligence_briefings=intel_briefings_str
            )

        act_status = action_cmd.get("status", "NONE")
        act_type = action_cmd.get("type", "NONE")

        if act_status == "CONFIRMED" and act_type not in ["NONE", "", "ADVISORY"]:
            success, exec_msg, rejection = state_engine.execute_structured_action(country_name, action_cmd)
            st.session_state[proposal_key] = None
            if success and exec_msg:
                reply += f"\n\n**[OPERATIONAL EXECUTION CONFIRMED]:**\n{exec_msg}"
            else:
                reply += f"\n\n**[DIRECTIVE ABORTED]:**\n⚠️ {rejection or exec_msg}"
        elif act_type not in ["NONE", "", "ADVISORY"]:
            st.session_state[proposal_key] = action_cmd

        st.session_state[chat_key].append({"role": "assistant", "content": reply})
        st.rerun()
