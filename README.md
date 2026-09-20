# 🌐 THE IRON CURTAIN: Cold War Geopolitics Simulator (1945–1953)

A multiplayer classroom geopolitics simulator set in the early Cold War (post-Potsdam 1945 through 1953), designed to run on a single host computer over a school local area network (LAN) with zero cloud fees.

---

## 🎯 Core Objectives & Mechanics

1. **Collective Mission: Prevent World Nuclear Destruction (MAD)**
   - The Cold War was an existential tightrope. All nations share the collective imperative to navigate 1945 to 1953 without triggering **DEFCON 1** (Mutually Assured Destruction).
   - If DEFCON 1 is reached, the game triggers an apocalyptic emergency siren screen, and all nations lose.
   - If the world navigates through 1953 without MAD, human civilization survives, and powers are ranked on diplomacy, economic health, domestic stability, and strategic sphere of influence.

2. **The History Mirror (Yearly Reality vs. Simulation Engine)**
   - At the conclusion of each year, the system enters a **Dedicated History Mirror Debrief Stage** (Option A).
   - Side-by-side comparison:
     - **What Actually Happened in History** (Potsdam, Truman Doctrine, Berlin Airlift, Soviet Bomb, Korean War, etc.)
     - **What Happened in Our Simulation** (Student directives, espionage operations, coups, alliances)
     - **The Butterfly Effect**: AI-driven divergence analysis explaining how student decisions reshaped the timeline.
     - **Teacher Discussion Prompts**: 3 curated pedagogical questions for classroom reflection before the next year opens.

3. **Inference Core (Groq SDK)**
   - **Cabinet Adviser**: Ultra-low latency historical roleplay (`George Marshall/Acheson` for USA, `Molotov` for USSR, `Attlee/Bevin` for UK, `Nehru` for India, `Tito` for Yugoslavia, `Zhou Enlai` for China, etc.).
   - **Omniscient Game Master**: Adjudicates student directives with raw stochastic entropy rolls (0–100) to manage fog of war, espionage risks (Clean, Fog of War, Double Agent, Compromised), and emergent state deltas.

4. **Deterministic Hard Constraints**
   - Cannot spend more than available Treasury.
   - Cannot launch nuclear strikes or tests without atomic capability (`Nuclear: True` and `Bombs >= 1`).
   - Intelligence deployments require at least `$50M`.
   - Domestic unrest (>85% tension) restricts offensive military actions.

---

## 🚀 Quickstart & Classroom LAN Setup

### 1. Requirements & Prerequisites
- Python 3.10+ (or use the included virtual environment `.venv`)
- Packages: `streamlit`, `groq`, `pydeck`, `pandas`

### 2. Launching the Simulator for Classroom Play
Open PowerShell or Command Prompt in this folder and run:

```powershell
.venv\Scripts\streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

Or simply double-click **`run_game.bat`**.

The host machine's IP will be displayed in the terminal and in the top-right header of the app (e.g., `http://192.168.1.50:8501`).

---

## 👥 Roles & URLs

Students and the teacher access the game from their own laptops, tablets, or Chromebooks using their browser:

| Role / Station | URL | Description |
|---|---|---|
| **War Room Projector** | `http://<host-ip>:8501/?view=projector` | Big-screen map, alignment coloring, DEFCON meter, public teletype, History Mirror debrief, and admin turn execution controls. |
| **USA Terminal** | `http://<host-ip>:8501/?country=USA` | George Marshall adviser telex, atomic stockpile, directives console, intel cables. |
| **USSR Terminal** | `http://<host-ip>:8501/?country=USSR` | Molotov adviser telex, atomic R&D, Eastern European buffer influence, intel cables. |
| **United Kingdom** | `http://<host-ip>:8501/?country=United%20Kingdom` | Attlee & Bevin adviser telex, post-war reconstruction, naval lifelines. |
| **France** | `http://<host-ip>:8501/?country=France` | De Gaulle & Bidault adviser telex, Rhine/Ruhr control, colonial defense. |
| **China** | `http://<host-ip>:8501/?country=China` | Zhou Enlai adviser telex, revolutionary consolidation, border defense. |
| **India** | `http://<host-ip>:8501/?country=India` | Jawaharlal Nehru adviser telex, Non-Aligned Movement leadership, anticolonialism. |
| **Yugoslavia** | `http://<host-ip>:8501/?country=Yugoslavia` | Marshal Tito adviser telex, independent socialism, resisting Soviet hegemony. |
| **Cuba** | `http://<host-ip>:8501/?country=Cuba` | Nationalist envoy telex, Caribbean sovereignty, navigating superpower proximity. |

*Note: Any student can also use the drop-down selector at the top of the interface to switch to their assigned station.*

---

## 🕹️ Game Flow for Teachers

1. **Step 1: Directives Phase (10–15 mins)**
   - Projector displays the Strategic Situation Map and DEFCON meter.
   - Student teams consult their historical AI advisers, draft covert/overt actions, negotiate in the Comms Hub, and submit directives.
   - Host monitors the live "Nations Ready" progress bar on the projector.
2. **Step 2: Turn Execution (1 min)**
   - Host enters the PIN (`POTSDAM1945`) and clicks **EXECUTE TURN RESOLUTION ⚡**.
   - The Groq Game Master evaluates actions with stochastic dice rolls and compiles state deltas.
3. **Step 3: The History Mirror Debrief (3–5 mins)**
   - The projector transitions into the **Dedicated Debrief Screen**:
     - *Left Column*: Real 1940s/50s history that took place this year.
     - *Right Column*: What the students caused in the simulation.
     - *Center*: "The Butterfly Effect" divergence analysis.
   - Teacher uses the **Classroom Discussion Prompts** to engage students in a historical reflection.
4. **Step 4: Advance to Next Year**
   - Host clicks **PROCEED TO YEAR X ➡️** to open the next year's directives.
   - Continue until 1953 (or DEFCON 1 apocalypse).
