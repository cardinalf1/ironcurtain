"""
The Iron Curtain - Palantir Gotham / Foundry C2 Strategic Operations Platform
Multiplayer Classroom Geopolitics Simulator (1945-1953)
"""

import streamlit as st
import pydeck as pdk
import json
import os
import pandas as pd
from typing import Optional, Tuple, Dict, Any

from state_engine import StateEngine, UNSC_PERM_5
from groq_service import GroqService, ADVISER_PERSONAS, HISTORICAL_YEARS

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
    st.caption("TACTICAL GEOPOLITICAL COMMAND • 1945–1953")

    view_options = ["🏛️ PROJECTOR / UN JOINT CHIEFS"] + [f"🚩 {c}" for c in countries.keys()]
    selected_view = st.selectbox("TERMINAL VIEW SELECTOR", view_options, index=0)

    st.markdown("---")
    st.markdown(f"**GLOBAL SITUATION CLOCK:**")
    st.markdown(f"• **YEAR:** `{world['year']}` | **CYCLE:** `TURN {world['turn']}`")
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
# MUTUALLY ASSURED DESTRUCTION (MAD) OVERLAY
# ==============================================================================
if world["mad_triggered"] or world["defcon"] == 1:
    st.markdown(
        """
        <div class='hud-panel-danger' style='text-align: center; padding: 40px;'>
            <h1 style='color: #f85149; font-size: 2.4rem;'>⚠️ DEFCON 1: STRATEGIC APOCALYPSE ⚠️</h1>
            <p style='color: #ff7b72; font-size: 1.15rem; font-weight: 600;'>MUTUALLY ASSURED DESTRUCTION (MAD) PROTOCOL DETONATED</p>
            <p style='color: #e6edf3; max-width: 800px; margin: 0 auto; line-height: 1.6;'>
                Strategic nuclear strikes have hit major population centers. The global balance of power has collapsed into total atomic devastation. 
                Atmospheric fallout halts civilization. The simulation is terminated.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("RESTART FROM YEAR 1945"):
        state_engine.reset_game()
        st.rerun()
    st.stop()

# ==============================================================================
# PYDECK STRATEGIC MAP COMPONENT
# ==============================================================================
def render_strategic_map(highlight_target: Optional[str] = None):
    geojson_features = []
    for feature in WORLD_GEOJSON["features"]:
        feat = dict(feature)
        feat["properties"] = dict(feat.get("properties", {}))
        c_name = feat["properties"].get("name", "")
        
        if c_name in countries:
            c = countries[c_name]
            align = c["alignment"]
            status_text = f"Major Power • Treasury: ${c['treasury']}M • Warheads: {c['bombs']}"
        elif c_name in buffers:
            b = buffers[c_name]
            align = b["alignment"]
            status_text = "Contested Frontier Buffer State"
        else:
            align = 0.0
            status_text = "Non-Aligned Sovereign Territory"

        align_text = f"{align:+.1f} ({'Pro-Western Alliance' if align > 0.2 else ('Pro-Soviet Bloc' if align < -0.2 else 'Non-Aligned')})"

        is_hl = (c_name == highlight_target)
        feat["properties"]["fill_color"] = [255, 176, 0, 240] if is_hl else alignment_to_rgb(align)
        feat["properties"]["name"] = c_name
        feat["properties"]["status"] = status_text
        feat["properties"]["alignment"] = align_text
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
        get_line_color=[38, 51, 69, 255],
        line_width_min_pixels=1.2
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
    
    # 1. Permanent Strategic Geopolitical Lifelines
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

    # 2. Dynamic map events flight arcs
    map_events = state_engine.get_map_events()
    for ev in map_events[:20]:
        src_name = ev.get("source_name")
        tgt_name = ev.get("target_name")
        if src_name in all_locs and tgt_name in all_locs:
            src = all_locs[src_name]
            tgt = all_locs[tgt_name]
            ev_type = (ev.get("event_type") or "").lower()
            if any(k in ev_type for k in ["strike", "offensive", "attack", "invasion", "military"]):
                arc_color = [248, 81, 73, 255] # Crimson Combat Assault
                align_tag = "Tactical Military Vector"
            elif any(k in ev_type for k in ["espionage", "spy", "intel"]):
                arc_color = [210, 153, 34, 250] # Amber HUMINT Infiltration
                align_tag = "Intelligence Vector"
            else:
                arc_color = [46, 160, 67, 240] # Emerald Foreign Aid / Trade
                align_tag = "Economic / Treaty Vector"

            arc_data.append({
                "from_lon": src["lon"], "from_lat": src["lat"],
                "to_lon": tgt["lon"], "to_lat": tgt["lat"],
                "color": arc_color,
                "name": f"ACTIVE OPERATION: {src_name} ➔ {tgt_name}",
                "status": ev.get("description", "Field Operation"),
                "alignment": align_tag
            })

    # 3. Active Spy Network Infiltration Arcs
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
        layers=[geojson_layer, arc_layer, capitals_layer],
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
        "📡 STRATEGIC ARCS & TACTICAL VECTORS DIRECTORY:"
        "</div>"
        "<div style='display: flex; flex-wrap: wrap; gap: 16px; line-height: 1.5;'>"
        "<span><b style='color: #f85149;'>━━━ Crimson Arc:</b> Military Offensives, Strikes & Armed Invasions</span>"
        "<span><b style='color: #d29922;'>━━━ Amber Arc:</b> Infiltrated HUMINT Spy Rings & Nuclear Espionage</span>"
        "<span><b style='color: #58a6ff;'>━━━ Blue Arc:</b> Western Defense Treaties & Bilateral Alliances</span>"
        "<span><b style='color: #2ea043;'>━━━ Emerald Arc:</b> Foreign Financial Aid & Commercial Trade Pacts</span>"
        "<span><b style='color: #a371f7;'>━━━ Purple Arc:</b> Non-Aligned Diplomatic Channels</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )


# ==============================================================================
# VIEW 1: PROJECTOR / UN JOINT CHIEFS COMMAND PLATFORM
# ==============================================================================
if selected_view == "🏛️ PROJECTOR / UN JOINT CHIEFS":
    st.markdown(
        f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>"
        f"<div>"
        f"<h2 style='margin: 0;'>THE IRON CURTAIN // C2 DEFENSE INTELLIGENCE PLATFORM</h2>"
        f"<span style='color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.85rem;'>"
        f"CENTRAL WARGAME PROJECTION • DEFCON {world['defcon']} • YEAR {world['year']}"
        f"</span>"
        f"</div>"
        f"<div>"
        f"<span class='badge-c2 badge-secret'>RESTRICTED // NATO-WARSAW THEATER</span>"
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
        st.markdown(f"<div class='metric-box'><div class='metric-label'>CURRENT YEAR</div><div class='metric-val'>{world['year']}</div></div>", unsafe_allow_html=True)
    with m5:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TURN CYCLE</div><div class='metric-val'>CYCLE {world['turn']}</div></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([8, 4])

    with col_left:
        st.markdown("#### 🌍 GLOBAL SITUATION MAP")
        render_strategic_map()

        # Teacher Analytics: Historical vs Classroom Doom Clock Divergence
        st.markdown("#### 📈 HISTORICAL DOOM CLOCK VS. CLASSROOM TIMELINE DIVERGENCE")
        hist_timeline = {
            1945: 20, 1946: 35, 1947: 45, 1948: 75,
            1949: 80, 1950: 90, 1951: 85, 1952: 80, 1953: 75
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
        st.progress(ready_count / len(sub_status), text=f"{ready_count} of {len(sub_status)} Powers Submitted")

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
        admin_pass = st.text_input("HOST AUTHORIZATION PIN", type="password", value="POTSDAM1945")

        if st.button("EXECUTE TURN RESOLUTION ⚡", type="primary", use_container_width=True, disabled=(world.get("phase") == "DEBRIEF")):
            if admin_pass != "POTSDAM1945":
                st.error("INCORRECT AUTHORIZATION PIN.")
            else:
                with st.spinner("Omniscient Game Master adjudicating directives, crises, and economy..."):
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

                st.success(f"Turn {world['turn']} Adjudicated! Proceed to Year {world['year'] + 1}.")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

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
                f"Active HUMINT Spy: {'YES (INFILTRATED)' if has_spy else 'NO (SIGNALS ONLY)'}"
            )
    intel_briefings_str = "\n".join(briefings)

    # --------------------------------------------------------------------------
    # MODAL DIALOG 1: RED PHONE (HOTLINE)
    # --------------------------------------------------------------------------
    @st.dialog("📞 RED PHONE: ENCRYPTED DIPLOMATIC HOTLINE")
    def show_red_phone_dialog(curr_country, all_countries):
        st.caption("Direct encrypted telex channel between superpower leaderships. Warning: Enemy HUMINT spy networks have a 35% chance to tap and leak transmissions!")
        
        other_countries = [c for c in all_countries.keys() if c != curr_country]
        h_target = st.selectbox("RECIPIENT POWER:", other_countries, key="dlg_phone_target")
        h_text = st.text_input("ENCRYPTED TRANSMISSION:", key="dlg_phone_msg", placeholder=f"Draft diplomatic communique to {h_target}...")
        
        if st.button("DISPATCH ENCRYPTED CABLE 📨", type="primary", use_container_width=True):
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
            if st.button("📞 RED PHONE", use_container_width=True):
                show_red_phone_dialog(country_name, countries)
        with btn_c2:
            if st.button(f"🔔 ALERTS ({cables_count})", use_container_width=True):
                show_notifications_dialog(country_name)
        st.markdown("</div>", unsafe_allow_html=True)

    # Telemetry Ribbon
    t1, t2, t3, t4, t5, t6, t7 = st.columns(7)
    with t1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TREASURY</div><div class='metric-val metric-val-mono'>${c_data['treasury']}M</div></div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>WARHEADS</div><div class='metric-val metric-val-mono'>{c_data['bombs']}</div></div>", unsafe_allow_html=True)
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
        f"<span class='badge-c2 badge-secret'>{target_dossier.get('confidence_label', 'CONFIDENTIAL')}</span> "
        f"<span style='font-size: 0.8rem; font-family: var(--font-mono); color: var(--text-secondary);'>ACTIVE SPY: <b>{'YES' if target_dossier.get('has_active_spy') else 'NO'}</b></span>"
        f"</div>"
        f"</div>"
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

    # Quick Tactical Directive Chips
    st.markdown("<span style='font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);'>QUICK TACTICAL DIRECTIVES:</span>", unsafe_allow_html=True)
    c_btn0, c_btn1, c_btn2, c_btn3, c_btn4, c_btn5 = st.columns(6)
    with c_btn0:
        if st.button(f"⚔️ Attack {inspected_target} ($120M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Launch a military offensive / attack on {inspected_target} ($120M budget)"
            st.rerun()
    with c_btn1:
        if st.button(f"🕵️ Spy on {inspected_target} ($40M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Deploy an intelligence spy network to {inspected_target} ($40M) to check their nuclear weapons stockpile and capability"
            st.rerun()
    with c_btn2:
        if st.button(f"⚛️ Commission Bomb ($80M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Assemble 1 atomic bomb under $80M budget"
            st.rerun()
    with c_btn3:
        if st.button(f"💵 War Bonds (+$150M)", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Issue emergency sovereign war bonds to raise $150M cash"
            st.rerun()
    with c_btn4:
        if st.button(f"🤝 Trade Pact with {inspected_target}", use_container_width=True, disabled=(orders_count >= 3)):
            st.session_state[f"staged_cmd_{country_name}"] = f"Propose a bilateral commercial trade pact with {inspected_target}"
            st.rerun()
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
