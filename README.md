# The Iron Curtain // Cold War Geopolitics Simulator (1945–1953)

<div align="center">
  <h3>Palantir Gotham / Foundry C2 Defense-Intelligence Geopolitical Simulation</h3>
  <p>Multiplayer Classroom Crisis Platform powered by Groq LLM Historical Advisers</p>
</div>

---

## 🎖️ Operational Capabilities

- **Direct Start**: Launches straight into the 1945 Cold War post-Potsdam theater. Zero scenario pickers or unnecessary setup screens.
- **Palantir C2 Defense Interface**: Dark slate/charcoal defense aesthetic (`#0a0d12`), hairline grid borders, high-density telemetry, and verified intelligence classifications (`[TOP SECRET // NOFORN]`).
- **Country Intelligence Dossiers with Fog-of-War**: Click any nation or contested buffer state to inspect estimated warhead stockpiles, strategic reserves, uranium deposits, and domestic stability filtered by your nation's intelligence confidence (Audited, HUMINT ±1, or Signals bounds).
- **1-Click Tactical Directives**: Instantly stage espionage rings, grant reconstruction aid, propose commercial treaties, or table UN sanctions.
- **AI Historical Advisers (Groq `llama-3.1-8b-instant`)**: Negotiate orders in natural language with in-character national advisers (Marshall, Molotov, Eden, Bidault, Zhou Enlai). Advisers understand budget caps (*"build as many bombs under $20M"*), draft formal authorization cards, and execute directives upon your confirmation.
- **UN Security Council (UNSC) with P5 Vetoes**: Permanent Five members (USA, USSR, UK, France, China) wield instant veto power over peacekeeper deployments, sanctions, and arms limitations.
- **Dynamic Flashpoint Theaters**: Real-time crisis arbitration for the Berlin Airlift (1948) and the Korean War (1950).
- **Encrypted Red Phone Hotline**: Confidential bilateral diplomatic channels with dynamic counter-espionage wiretaps (35% interception risk that can leak cables directly to the UN Public Wire).
- **Macro-Economy & War Bonds**: Annual base industrial tax collection, bilateral commercial treaties, and sovereign war bond issuances for emergency cash injections.
- **Emergent Historical Shocks**: Random historical events including the 1946–47 Soviet famine, UK coal rationing, and laboratory nuclear criticality accidents.

---

## 🚀 Quick Start

### 1. Launch via Launcher (Windows)
Double-click **`run_game.bat`**. It starts the server and immediately opens your default browser at:
```
http://localhost:8501
```

### 2. Manual Startup
```bash
# Activate virtual environment
.venv\Scripts\activate

# Launch Streamlit server
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

### 3. Student LAN Connectivity
Other students or teams in the classroom can connect from their own laptops, tablets, or phones using:
```
http://<host-ip-address>:8501
```

---

## 🧪 Automated Testing

Run the comprehensive test suite verifying the intelligence dossier, UNSC veto arbitration, hotline wiretaps, war bonds, tax collection, and random events:
```bash
.venv\Scripts\python.exe test_systems.py
.venv\Scripts\python.exe test_simulation_e2e.py
```
