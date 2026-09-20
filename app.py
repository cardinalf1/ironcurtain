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
        c_name = feat["properties"]["name"]
        
        if c_name in countries:
            align = countries[c_name]["alignment"]
        elif c_name in buffers:
            align = buffers[c_name]["alignment"]
        else:
            align = 0.0

        is_hl = (c_name == highlight_target)
        feat["properties"]["fill_color"] = [255, 176, 0, 240] if is_hl else alignment_to_rgb(align)
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
        line_width_min_pixels=1.1
    )

    capitals_data = []
    for name, c in countries.items():
        is_hl = (name == highlight_target)
        capitals_data.append({
            "name": name,
            "lat": c["lat"],
            "lon": c["lon"],
            "color": [255, 255, 255, 255] if is_hl else ([248, 81, 73, 230] if c["nuclear"] else [56, 139, 253, 200]),
            "radius": 340000 if is_hl else (240000 if c["nuclear"] else 160000)
        })

    capitals_layer = pdk.Layer(
        "ScatterplotLayer",
        capitals_data,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True
    )

    # Active map events flight arcs
    map_events = state_engine.get_map_events()
    arc_data = []
    for ev in map_events[:14]:
        src_name = ev.get("source_name")
        tgt_name = ev.get("target_name")
        if src_name in countries and tgt_name in countries:
            src = countries[src_name]
            tgt = countries[tgt_name]
            ev_type = ev.get("event_type", "")
            arc_color = [248, 81, 73, 255] if "strike" in ev_type else ([210, 153, 34, 230] if "espionage" in ev_type else [46, 160, 67, 220])
            arc_data.append({
                "from_lon": src["lon"],
                "from_lat": src["lat"],
                "to_lon": tgt["lon"],
                "to_lat": tgt["lat"],
                "color": arc_color
            })

    arc_layer = pdk.Layer(
        "ArcLayer",
        arc_data,
        get_source_position=["from_lon", "from_lat"],
        get_target_position=["to_lon", "to_lat"],
        get_source_color="color",
        get_target_color="color",
        get_width=3,
        pickable=True
    )

    view_state = pdk.ViewState(latitude=32.0, longitude=25.0, zoom=1.1, min_zoom=0.8, max_zoom=6)
    deck = pdk.Deck(
        layers=[geojson_layer, arc_layer, capitals_layer],
        initial_view_state=view_state,
        tooltip={"text": "{display_label}\n{alignment_score}"},
        map_style=None
    )
    st.pydeck_chart(deck, use_container_width=True)


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
        sub_status = state_engine.get_submission_status()
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
                        sim_history=hm.get("simulated_summary", "Year evaluated."),
                        divergence=hm.get("divergence_analysis", "Course diverged from history."),
                        questions=hm.get("discussion_questions", ["What was the primary driver of tension?"]),
                        legacy=hm.get("legacy_verdict", "Strategic balance preserved.")
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
# VIEW 2: STUDENT NATION TERMINAL (C2 INTELLIGENCE DOSSIER & ADVISER TELEX)
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
        "system_prompt": "You advise the leadership."
    })

    # Terminal Header
    is_p5 = country_name in UNSC_PERM_5
    st.markdown(
        f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>"
        f"<div>"
        f"<h2 style='margin: 0;'>{country_name.upper()} // STRATEGIC COMMAND</h2>"
        f"<span style='color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.85rem;'>"
        f"HEAD OF MISSION: {persona['name']} ({persona['title']}) • CAPITAL: {c_data['capital']}"
        f"</span>"
        f"</div>"
        f"<div>"
        f"<span class='badge-c2 {'badge-unsc' if is_p5 else 'badge-conf'}'>{'UNSC PERM-5 (VETO)' if is_p5 else 'UN GENERAL MEMBER'}</span> "
        f"<span class='badge-c2 {'badge-secret' if c_data['nuclear'] else 'badge-conf'}'>{'ATOMIC CAPABLE' if c_data['nuclear'] else 'CONVENTIONAL'}</span>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Telemetry Ribbon
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    with t1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TREASURY</div><div class='metric-val metric-val-mono'>${c_data['treasury']}M</div></div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>WARHEADS</div><div class='metric-val metric-val-mono'>{c_data['bombs']}</div></div>", unsafe_allow_html=True)
    with t3:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>URANIUM</div><div class='metric-val'>{c_data.get('uranium', 0)} MT</div></div>", unsafe_allow_html=True)
    with t4:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>OIL SUPPLY</div><div class='metric-val'>{c_data.get('oil', 50)}%</div></div>", unsafe_allow_html=True)
    with t5:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>STABILITY</div><div class='metric-val'>{c_data.get('domestic_approval', 75)}%</div></div>", unsafe_allow_html=True)
    with t6:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>TENSION</div><div class='metric-val'>{c_data['tension']}%</div></div>", unsafe_allow_html=True)

    # Main Workspace: 8 cols Dossier & Map, 4 cols Adviser Command Log
    col_main, col_adviser = st.columns([8, 4])

    with col_main:
        st.markdown("#### 📂 PALANTIR C2 // TARGET INTELLIGENCE DOSSIER")

        # Territory Inspector Selection
        all_territories = list(countries.keys()) + list(buffers.keys())
        default_idx = 1 if country_name == "USA" else 0
        inspected_target = st.selectbox(
            "SELECT GEOPOLITICAL TARGET FOR CLASSIFIED BRIEFING:",
            all_territories,
            index=default_idx
        )

        dossier = state_engine.get_country_dossier(country_name, inspected_target)

        # Classified Dossier Card
        st.markdown(
            f"<div class='dossier-card'>"
            f"<div class='dossier-header'>"
            f"<div>"
            f"<span style='font-size: 1.15rem; font-weight: 700;'>{inspected_target.upper()}</span> "
            f"<span class='badge-c2 badge-secret'>{dossier.get('confidence_label', 'CONFIDENTIAL')}</span>"
            f"</div>"
            f"<div>"
            f"<span style='font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary);'>"
            f"BILATERAL STANCE: <b>{dossier.get('stance', 'Neutral')}</b> • CONFIDENCE: <b>{dossier.get('confidence_pct', 50)}%</b>"
            f"</span>"
            f"</div>"
            f"</div>"
            f"<div class='dossier-meta-grid'>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Atomic Stockpile</div><div class='dossier-meta-value'>{dossier.get('bombs_display', 'Classified')}</div></div>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Treasury Reserves</div><div class='dossier-meta-value'>{dossier.get('treasury_display', 'Classified')}</div></div>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Uranium Supply</div><div class='dossier-meta-value'>{dossier.get('uranium_display', 'Restricted')}</div></div>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Oil Dependency</div><div class='dossier-meta-value'>{dossier.get('oil_display', 'Stable')}</div></div>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Domestic Stability</div><div class='dossier-meta-value'>{dossier.get('approval_display', '75%')}</div></div>"
            f"<div class='dossier-meta-item'><div class='dossier-meta-title'>Delivery Tech</div><div class='dossier-meta-value'>{dossier.get('missile_tech', 'BOMBERS')}</div></div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Direct Tactical Action Bar
        st.markdown("<span style='font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);'>QUICK TACTICAL DIRECTIVES:</span>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns(4)
        with act_col1:
            if st.button(f"🕵️ Spy on {inspected_target} ($50M)", use_container_width=True):
                st.session_state[f"staged_cmd_{country_name}"] = f"Deploy an intelligence spy network to {inspected_target} with $50M"
                st.rerun()
        with act_col2:
            if st.button(f"💵 Grant $40M Aid", use_container_width=True):
                st.session_state[f"staged_cmd_{country_name}"] = f"Send $40M economic reconstruction aid to {inspected_target}"
                st.rerun()
        with act_col3:
            if st.button(f"🤝 Propose Trade Treaty", use_container_width=True):
                st.session_state[f"staged_cmd_{country_name}"] = f"Propose a bilateral commercial trade pact with {inspected_target}"
                st.rerun()
        with act_col4:
            if st.button(f"📜 Table UNSC Sanction", use_container_width=True):
                st.session_state[f"staged_cmd_{country_name}"] = f"Table a formal resolution in the UN Security Council against {inspected_target}"
                st.rerun()

        # Strategic Map
        st.markdown("#### 🌍 GLOBAL SITUATION MAP")
        render_strategic_map(highlight_target=inspected_target)

        # Tactical Tabs
        tab_unsc, tab_crises, tab_hotline, tab_economy, tab_shocks = st.tabs([
            "🇺🇳 UN SECURITY COUNCIL",
            "🔥 CRISIS THEATERS",
            "📞 RED PHONE HOTLINE",
            "💵 TREASURY & REVENUE",
            "📡 SHOCKS & DISPATCHES"
        ])

        # TAB 1: UN SECURITY COUNCIL
        with tab_unsc:
            st.markdown("##### 🇺🇳 UN SECURITY COUNCIL CHAMBER")
            resolutions = state_engine.get_unsc_resolutions(world["turn"])
            if not resolutions:
                st.caption("No resolutions currently pending before the council.")
            for res in resolutions:
                st.markdown(
                    f"<div class='cable-card cable-card-unsc'>"
                    f"<div class='cable-header'><span>RESOLUTION #{res['id']}</span><span>STATUS: <b>{res['status']}</b></span></div>"
                    f"<b>{res['title']}</b><br>"
                    f"<span style='font-size: 0.85rem;'>{res['description']}</span><br>"
                    f"<span style='font-size: 0.8rem; color: var(--text-secondary);'>Votes Recorded: {res['votes']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if res["status"] == "PENDING":
                    v_col1, v_col2, v_col3 = st.columns([1, 1, 4])
                    with v_col1:
                        if st.button(f"Vote YES", key=f"v_yes_{res['id']}"):
                            state_engine.vote_unsc_resolution(res["id"], country_name, "YES")
                            st.rerun()
                    with v_col2:
                        label = "VETO (NO)" if is_p5 else "Vote NO"
                        if st.button(label, key=f"v_no_{res['id']}"):
                            state_engine.vote_unsc_resolution(res["id"], country_name, "NO")
                            st.rerun()

        # TAB 2: DYNAMIC CRISES
        with tab_crises:
            st.markdown("##### 🔥 ACTIVE REGIONAL CRISES")
            crises = state_engine.get_all_crises()
            for cr in crises:
                st.markdown(
                    f"<div class='cable-card'>"
                    f"<div class='cable-header'><span>{cr['theatre']}</span><span>STATUS: <b>{cr['status']}</b></span></div>"
                    f"<b>{cr['title']}</b><br>"
                    f"<span style='font-size: 0.85rem;'>{cr['description']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if cr["crisis_id"] == "BERLIN_BLOCKADE":
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        if st.button("✈️ Mount Berlin Airlift ($20M)", key="btn_airlift"):
                            state_engine.resolve_crisis_action("BERLIN_BLOCKADE", country_name, "AIRLIFT")
                            st.rerun()
                    with b_col2:
                        if st.button("🛡️ Force Armed Corridor (Risk War)", key="btn_convoy"):
                            state_engine.resolve_crisis_action("BERLIN_BLOCKADE", country_name, "ARMED_CONVOY")
                            st.rerun()

        # TAB 3: RED PHONE HOTLINE
        with tab_hotline:
            st.markdown("##### 📞 ENCRYPTED RED PHONE HOTLINE")
            st.caption("Direct diplomatic telex. Counter-espionage warning: Active spy networks have a 35% chance to intercept cables!")
            h_target = st.selectbox("RECIPIENT POWER:", [c for c in countries.keys() if c != country_name], key="hotline_tgt")
            h_text = st.text_input("ENCRYPTED TRANSMISSION:", key="hotline_msg")
            if st.button("DISPATCH CABLE 📨"):
                if h_text:
                    _, note, intercepted = state_engine.send_hotline_message(country_name, h_target, h_text)
                    st.success(note)
                    st.rerun()

            st.markdown("###### ARCHIVED HOTLINE LOGS:")
            hotline_logs = state_engine.get_hotline_messages(country_name)
            for m in hotline_logs:
                intercept_tag = "<span style='color:var(--accent-red);'>[INTERCEPTED]</span>" if m.get("is_intercepted") else "<span style='color:var(--accent-green);'>[ENCRYPTED]</span>"
                st.markdown(
                    f"<div class='cable-card'>"
                    f"<div class='cable-header'><span>FROM: {m['sender']} ➔ TO: {m['recipient']}</span><span>{intercept_tag}</span></div>"
                    f"<span style='font-size: 0.88rem; font-family: var(--font-mono);'>{m['content']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        # TAB 4: TREASURY & REVENUE
        with tab_economy:
            st.markdown("##### 💵 NATIONAL ECONOMY & FISCAL REVENUE")
            st.markdown(
                f"• **Current Treasury:** `${c_data['treasury']}M`\n"
                f"• **Annual Base Tax Collection:** `+${75 if country_name == 'USA' else 50}M / turn`\n"
                f"• **Domestic Tension Deduction:** `{'0%' if c_data['tension'] < 30 else ('-20%' if c_data['tension'] < 50 else '-40%')}`\n"
                f"• **Fissile Uranium Deposits:** `{c_data.get('uranium', 0)} Metric Tons`\n"
                f"• **Strategic Oil Reserves:** `{c_data.get('oil', 50)}%`"
            )
            st.markdown("---")
            st.markdown("<b>EMERGENCY REVENUE GENERATION:</b>", unsafe_allow_html=True)
            if st.button("⚡ FLOAT DOMESTIC WAR BONDS (+$50M CASH, +5% TENSION)"):
                state_engine.execute_structured_action(country_name, {"type": "WAR_BONDS"})
                st.success("Emergency sovereign bonds floated! Injected +$50M into National Treasury.")
                st.rerun()

        # TAB 5: SHOCKS & RANDOM EVENTS
        with tab_shocks:
            st.markdown("##### 📡 FIELD INTELLIGENCE & HISTORICAL SHOCKS")
            events = state_engine.get_random_events()
            for ev in events:
                st.markdown(
                    f"<div class='cable-card cable-card-secret'>"
                    f"<div class='cable-header'><span>YEAR {ev['year']}</span><span>EVENT: {ev['event_type']}</span></div>"
                    f"<b>{ev['title']}</b><br>"
                    f"<span style='font-size: 0.85rem; color: var(--text-secondary);'>{ev['description']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    # RIGHT COLUMN: ADVISER COMMAND LOG
    with col_adviser:
        st.markdown(f"#### 🎙️ ADVISER COMMAND LOG")
        st.caption(f"Direct telex channel to {persona['name']}. Instruct your adviser in plain English.")

        chat_key = f"chat_history_{country_name}"
        if chat_key not in st.session_state:
            st.session_state[chat_key] = [
                {"role": "assistant", "content": f"Commander, {persona['name']} on the line. The year is {world['year']}. Instruct me on our diplomatic stance, covert operations, economic aid, or atomic posture."}
            ]

        # Check for staged quick commands
        staged_key = f"staged_cmd_{country_name}"
        staged_val = st.session_state.get(staged_key, "")
        if staged_val:
            st.session_state[staged_key] = ""

        chat_container = st.container(height=380)
        with chat_container:
            for msg in st.session_state[chat_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Check for unconfirmed pending proposal
        proposal_key = f"pending_proposal_{country_name}"
        if proposal_key in st.session_state and st.session_state[proposal_key]:
            prop = st.session_state[proposal_key]
            st.markdown(
                f"<div class='hud-panel-amber'>"
                f"<b style='color: var(--accent-amber);'>📋 PROPOSED OPERATIONAL DIRECTIVE (AWAITING YOUR AUTHORIZATION):</b><br>"
                f"<span style='font-size: 0.85rem;'>• Action: <b>{prop.get('type')}</b> | Target: <b>{prop.get('target')}</b></span><br>"
                f"<span style='font-size: 0.85rem;'>• Budget: <b>${prop.get('cost_m', 0)}M</b> | Effect: <b>{prop.get('description', '')}</b></span>"
                f"</div>",
                unsafe_allow_html=True
            )
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("AUTHORIZE & EXECUTE ORDER 🚀", type="primary", use_container_width=True):
                    success, exec_msg, rej = state_engine.execute_structured_action(country_name, prop)
                    st.session_state[proposal_key] = None
                    conf_reply = f"**{persona['name']} to Commander:** Directive confirmed and transmitted to General Staff. {exec_msg}"
                    st.session_state[chat_key].append({"role": "assistant", "content": conf_reply})
                    st.rerun()
            with col_conf2:
                if st.button("CANCEL / REVISE ❌", use_container_width=True):
                    st.session_state[proposal_key] = None
                    st.rerun()

        # Chat input
        user_prompt = st.chat_input("Tell your adviser what to do (e.g. 'Build 2 bombs under 40m', 'Issue bonds', 'Go')...")
        if staged_val and not user_prompt:
            user_prompt = staged_val

        if user_prompt:
            st.session_state[chat_key].append({"role": "user", "content": user_prompt})

            # Check if confirming existing proposal
            u_clean = user_prompt.lower().strip()
            if u_clean in ["go", "confirm", "do it", "approved", "authorize", "execute", "yes", "proceed"] and proposal_key in st.session_state and st.session_state[proposal_key]:
                prop = st.session_state[proposal_key]
                success, exec_msg, rejection = state_engine.execute_structured_action(country_name, prop)
                st.session_state[proposal_key] = None
                reply = f"**{persona['name']} to Commander:** Order confirmed and authorized. {exec_msg}"
                st.session_state[chat_key].append({"role": "assistant", "content": reply})
                st.rerun()

            # Otherwise query AI adviser
            with st.spinner("Adviser calculating operational options..."):
                action_cmd, reply = groq_service.chat_with_adviser(
                    country=country_name,
                    conversation_history=st.session_state[chat_key],
                    user_message=user_prompt,
                    current_year=world["year"],
                    country_state=c_data
                )

            act_status = action_cmd.get("status", "NONE")
            act_type = action_cmd.get("type", "NONE")

            if act_status == "PROPOSED" and act_type not in ["NONE", "", "ADVISORY"]:
                st.session_state[proposal_key] = action_cmd
            elif act_status == "CONFIRMED" and act_type not in ["NONE", "", "ADVISORY"]:
                success, exec_msg, rejection = state_engine.execute_structured_action(country_name, action_cmd)
                st.session_state[proposal_key] = None
            elif act_type not in ["NONE", "", "ADVISORY"]:
                st.session_state[proposal_key] = action_cmd

            st.session_state[chat_key].append({"role": "assistant", "content": reply})
            st.rerun()
