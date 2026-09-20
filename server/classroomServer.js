/*!
 * The Iron Curtain - Classroom C2 Server
 * Synchronized Multiplayer LAN Backend & Rules Arbiter (1945–1953)
 */

import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Load local .env if present
function loadEnv() {
  const envPath = path.resolve(__dirname, '..', '.env');
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const [k, ...rest] = trimmed.split('=');
        const v = rest.join('=').trim().replace(/^["']|["']$/g, '');
        if (!process.env[k.trim()]) {
          process.env[k.trim()] = v;
        }
      }
    }
  }
}
loadEnv();

const GROQ_API_KEY = process.env.GROQ_API_KEY || '';

const INITIAL_COUNTRIES = {
  "USA": {
    alignment: 1.0, nuclear: true, bombs: 2, treasury: 500, tension: 10,
    objective: "Contain Soviet expansion, support Western European recovery, and maintain atomic deterrence.",
    capital: "Washington D.C.", lat: 38.9, lon: -77.0,
    uranium: 4, oil: 80, domesticApproval: 78, missileTech: "STRATEGIC_BOMBERS", paperclipScientists: 1
  },
  "USSR": {
    alignment: -1.0, nuclear: false, bombs: 0, treasury: 250, tension: 15,
    objective: "Consolidate Eastern European buffer states, complete atomic weapon R&D, and break capitalist encirclement.",
    capital: "Moscow", lat: 55.75, lon: 37.62,
    uranium: 2, oil: 70, domesticApproval: 82, missileTech: "STRATEGIC_BOMBERS", paperclipScientists: 1
  },
  "United Kingdom": {
    alignment: 0.7, nuclear: false, bombs: 0, treasury: 120, tension: 20,
    objective: "Rebuild domestic economy, sustain global strategic lifelines, and preserve Anglo-American alliance.",
    capital: "London", lat: 51.5, lon: -0.12,
    uranium: 1, oil: 40, domesticApproval: 65, missileTech: "STRATEGIC_BOMBERS", paperclipScientists: 0
  },
  "France": {
    alignment: 0.4, nuclear: false, bombs: 0, treasury: 100, tension: 30,
    objective: "Restore national sovereignty, maintain control over colonial frontiers, and counter German resurgence.",
    capital: "Paris", lat: 48.85, lon: 2.35,
    uranium: 1, oil: 30, domesticApproval: 55, missileTech: "STRATEGIC_BOMBERS", paperclipScientists: 0
  },
  "China": {
    alignment: -0.3, nuclear: false, bombs: 0, treasury: 80, tension: 40,
    objective: "Consolidate the Communist revolution, resist imperialist encroachment, and rebuild agrarian economy.",
    capital: "Beijing", lat: 39.9, lon: 116.4,
    uranium: 0, oil: 20, domesticApproval: 70, missileTech: "INFANTRY_CORPS", paperclipScientists: 0
  },
  "India": {
    alignment: 0.0, nuclear: false, bombs: 0, treasury: 90, tension: 15,
    objective: "Lead the Non-Aligned Movement, maintain complete sovereignty, and promote decolonization.",
    capital: "New Delhi", lat: 28.61, lon: 77.2,
    uranium: 0, oil: 25, domesticApproval: 80, missileTech: "INFANTRY_CORPS", paperclipScientists: 0
  },
  "Yugoslavia": {
    alignment: -0.6, nuclear: false, bombs: 0, treasury: 70, tension: 25,
    objective: "Pioneer self-managed socialism, resist Soviet domination, and secure economic independence.",
    capital: "Belgrade", lat: 44.78, lon: 20.44,
    uranium: 0, oil: 20, domesticApproval: 75, missileTech: "INFANTRY_CORPS", paperclipScientists: 0
  },
  "Cuba": {
    alignment: -0.2, nuclear: false, bombs: 0, treasury: 50, tension: 20,
    objective: "Protect national resources, resist external dominance, and navigate strategic Caribbean tensions.",
    capital: "Havana", lat: 23.12, lon: -82.38,
    uranium: 0, oil: 15, domesticApproval: 60, missileTech: "INFANTRY_CORPS", paperclipScientists: 0
  }
};

const INITIAL_BUFFERS = {
  "West Germany": { alignment: 0.8, lat: 50.73, lon: 7.1 },
  "East Germany": { alignment: -0.8, lat: 52.52, lon: 13.4 },
  "Greece": { alignment: 0.2, lat: 37.98, lon: 23.72 },
  "Turkey": { alignment: 0.3, lat: 39.93, lon: 32.85 },
  "Iran": { alignment: 0.0, lat: 35.68, lon: 51.38 },
  "Korea": { alignment: 0.0, lat: 37.56, lon: 126.97 }
};

const UNSC_PERM_5 = ["USA", "USSR", "United Kingdom", "France", "China"];

const ADVISER_PERSONAS = {
  "USA": {
    name: "General George C. Marshall & Dean Acheson",
    title: "Secretary of State & Chairman of the Joint Chiefs",
    prompt: "You are General George C. Marshall advising the President of the United States. You champion European recovery, NATO containment, and sober atomic deterrence."
  },
  "USSR": {
    name: "Vyacheslav Molotov & Lavrentiy Beria",
    title: "Minister of Foreign Affairs & Chief of Atomic Project",
    prompt: "You are Vyacheslav Molotov advising Generalissimo Stalin. You speak with steely Bolshevik discipline, guarding against capitalist encirclement."
  },
  "United Kingdom": {
    name: "Anthony Eden & Clement Attlee",
    title: "Foreign Secretary & Prime Minister",
    prompt: "You are Anthony Eden advising the British Crown. You balance empire retrenchment, the special relationship with Washington, and domestic recovery."
  },
  "France": {
    name: "Georges Bidault & Jean Monnet",
    title: "Foreign Minister & Planning Commissioner",
    prompt: "You are Georges Bidault advising the French Fourth Republic. You guard against German resurgence and advocate European economic integration."
  },
  "China": {
    name: "Premier Zhou Enlai",
    title: "Premier & Foreign Minister",
    prompt: "You are Premier Zhou Enlai, master diplomat of China. You speak with courtly courtesy, revolutionary patience, and strategic depth."
  },
  "India": {
    name: "Jawaharlal Nehru",
    title: "Prime Minister & External Affairs Minister",
    prompt: "You are Jawaharlal Nehru, leader of independent India and champion of the Non-Aligned Movement."
  },
  "Yugoslavia": {
    name: "Marshal Josip Broz Tito",
    title: "President of Yugoslavia",
    prompt: "You are Marshal Josip Broz Tito. You navigate an independent socialist path, defying Soviet hegemony and Western capitalism."
  },
  "Cuba": {
    name: "Envoy of the Republic of Cuba",
    title: "Undersecretary of External Relations",
    prompt: "You are the senior envoy of Cuba navigating intense geopolitical friction 90 miles from Florida."
  }
};

class ClassroomState {
  constructor() {
    this.reset();
  }

  reset() {
    this.world = {
      year: 1945,
      turn: 1,
      defcon: 4,
      globalTension: 20,
      madTriggered: false,
      gameOver: false,
      phase: "DIRECTIVES"
    };

    this.countries = JSON.parse(JSON.stringify(INITIAL_COUNTRIES));
    this.buffers = JSON.parse(JSON.stringify(INITIAL_BUFFERS));

    // Stances
    this.stances = {};
    const names = Object.keys(INITIAL_COUNTRIES);
    for (const c1 of names) {
      this.stances[c1] = {};
      for (const c2 of names) {
        if (c1 === c2) continue;
        if (["USA", "United Kingdom", "France"].includes(c1) && ["USA", "United Kingdom", "France"].includes(c2)) {
          this.stances[c1][c2] = "Ally";
        } else if ((["USA", "United Kingdom"].includes(c1) && c2 === "USSR") || (c1 === "USSR" && ["USA", "United Kingdom"].includes(c2))) {
          this.stances[c1][c2] = "Rival";
        } else {
          this.stances[c1][c2] = "Neutral";
        }
      }
    }

    this.directives = [];
    this.activeAgents = [];
    this.unscResolutions = [];
    this.crises = [
      {
        id: "BERLIN_BLOCKADE",
        title: "Berlin Ground Corridors Access Dispute",
        status: "DORMANT",
        yearStarted: 1948,
        theatre: "Central Europe (Germany)",
        description: "Soviet forces challenge Western ground rail and road transit through East Germany into divided Berlin.",
        stateData: { airliftActive: false, corridorBlocked: false, suppliesDeliveredPct: 100 }
      },
      {
        id: "KOREAN_WAR",
        title: "Korean Peninsula 38th Parallel Flashpoint",
        status: "DORMANT",
        yearStarted: 1950,
        theatre: "East Asia (Korea)",
        description: "Ideological division between the Soviet-backed North and US-supported South threatens open warfare across the 38th Parallel.",
        stateData: { frontline: "38th Parallel", unCoalitionActive: false, chineseVolunteersActive: false }
      }
    ];

    this.hotlineMessages = [];
    this.tradeAgreements = [];
    this.randomEvents = [];
    this.newsFeed = [
      {
        id: 1, turn: 1, year: 1945,
        headline: "POST-POTSDAM ERA COMMENCES",
        body: "World War II concludes. The United States conducts Trinity and holds the atomic monopoly. Superpower balance established."
      }
    ];
    this.historyMirror = [];
    this.mapEvents = [];
  }

  getDossier(viewerCountry, targetName) {
    const target = this.countries[targetName];
    const isBuffer = !target && Boolean(this.buffers[targetName]);

    if (isBuffer) {
      const b = this.buffers[targetName];
      return {
        targetName, isBuffer: true, capital: "Regional Seat",
        alignment: b.alignment,
        confidenceLabel: "HIGH // OPEN GEOPOLITICAL SPHERE",
        confidencePct: 80,
        stance: "Neutral",
        strategicNotes: `Contested buffer territory. Alignment: ${b.alignment > 0 ? 'Pro-West' : 'Pro-Soviet'}.`
      };
    }

    if (!target) return { error: `Territory ${targetName} not cataloged.` };

    const isSelf = viewerCountry === targetName;
    const stance = this.stances[viewerCountry]?.[targetName] || "Neutral";
    const hasSpy = this.activeAgents.some(a => a.owner === viewerCountry && a.target === targetName);

    let confLabel = "LOW // SIGNALS INTELLIGENCE";
    let confPct = 25;
    let bombsText = `Classified / Est. 0–${target.bombs + 3} Warheads`;
    let treasuryText = "State Secret (Estimated Strained)";

    if (isSelf || stance === "Ally") {
      confLabel = "VERIFIED // TOP SECRET NOFORN";
      confPct = 100;
      bombsText = `${target.bombs} Warheads (VERIFIED)`;
      treasuryText = `$${target.treasury}M (AUDITED)`;
    } else if (hasSpy) {
      confLabel = "HIGH // HUMINT FIELD ASSET";
      confPct = 85;
      bombsText = `Est. ${target.bombs} Warheads (±1 Delta)`;
      treasuryText = `Est. $${target.treasury}M (Reported)`;
    } else if (["Friendly", "Neutral"].includes(stance)) {
      confLabel = "MODERATE // DIPLOMATIC ATTACHÉ";
      confPct = 55;
      bombsText = `Est. ${Math.max(0, target.bombs - 1)}–${target.bombs + 2} Warheads`;
      treasuryText = `~$${Math.floor(target.treasury / 50) * 50}M Macro Reserves`;
    }

    return {
      targetName, isBuffer: false,
      capital: target.capital,
      alignment: target.alignment,
      stance, confidenceLabel: confLabel, confidencePct: confPct,
      nuclearStatus: target.nuclear ? "ATOMIC CAPABLE" : "CONVENTIONAL ONLY",
      bombsDisplay: bombsText,
      treasuryDisplay: treasuryText,
      uraniumDisplay: `${target.uranium} MT Fissile Grade`,
      oilDisplay: `${target.oil}% Reserves`,
      approvalDisplay: `${target.domesticApproval}% Stability`,
      missileTech: target.missileTech
    };
  }
}

export function setupClassroomServer(app) {
  const sim = new ClassroomState();

  app.use(express.json());

  // 1. Live State
  app.get('/api/classroom/state', (req, res) => {
    res.json({
      world: sim.world,
      countries: sim.countries,
      buffers: sim.buffers,
      stances: sim.stances,
      unscResolutions: sim.unscResolutions,
      crises: sim.crises,
      newsFeed: sim.newsFeed.slice(-15),
      mapEvents: sim.mapEvents.slice(-15),
      randomEvents: sim.randomEvents.slice(-10),
      historyMirror: sim.historyMirror
    });
  });

  // 2. Classified Country Dossier
  app.get('/api/classroom/dossier/:viewerCountry/:targetName', (req, res) => {
    const { viewerCountry, targetName } = req.params;
    const dossier = sim.getDossier(viewerCountry, targetName);
    res.json(dossier);
  });

  // 3. Structured Action Execution
  app.post('/api/classroom/action', (req, res) => {
    const { countryName, action } = req.body;
    const c = sim.countries[countryName];
    if (!c) return res.status(400).json({ error: "Invalid country." });

    const actType = (action.type || "NONE").toUpperCase();
    const cost = Number(action.cost_m || action.costM || 0);

    if (actType === "WAR_BONDS") {
      c.treasury += 50;
      c.tension = Math.min(100, c.tension + 5);
      sim.newsFeed.push({
        id: Date.now(), turn: sim.world.turn, year: sim.world.year,
        headline: "WAR BONDS ISSUED",
        body: `${countryName} floated sovereign war bonds, raising +$50M cash.`
      });
      return res.json({ success: true, message: `War bonds issued! Injected +$50M into ${countryName} treasury.` });
    }

    if (actType === "NUCLEAR_STRIKE") {
      if (!c.nuclear || c.bombs < 1) {
        return res.status(400).json({ error: "No atomic warheads available." });
      }
      c.bombs = Math.max(0, c.bombs - 1);
      sim.world.defcon = 1;
      sim.world.globalTension = 100;
      sim.world.madTriggered = true;
      sim.mapEvents.push({
        id: Date.now(), turn: sim.world.turn, eventType: "strike",
        sourceName: countryName, targetName: action.target || "USSR",
        description: `CRITICAL: ${countryName} detonated an atomic warhead on ${action.target}! DEFCON 1 triggered.`
      });
      return res.json({ success: true, message: "ATOMIC STRIKE LAUNCHED: DEFCON 1 triggered. Armageddon protocol active." });
    }

    if (actType === "NUCLEAR_EXPANSION") {
      if (c.treasury < cost) return res.status(400).json({ error: "Insufficient funds." });
      const bombsAdded = Number(action.bombs_delta || action.bombsDelta || 1);
      c.treasury -= cost;
      c.bombs += bombsAdded;
      c.nuclear = true;
      sim.mapEvents.push({
        id: Date.now(), turn: sim.world.turn, eventType: "nuclear_test",
        sourceName: countryName, targetName: countryName,
        description: `ATOMIC EXPANSION: ${countryName} assembled +${bombsAdded} warhead(s).`
      });
      return res.json({ success: true, message: `Atomic production expanded: +${bombsAdded} bomb(s).` });
    }

    if (actType === "ESPIONAGE") {
      if (c.treasury < 50) return res.status(400).json({ error: "Espionage requires minimum $50M." });
      c.treasury -= 50;
      sim.activeAgents.push({ owner: countryName, target: action.target, status: "ACTIVE" });
      sim.mapEvents.push({
        id: Date.now(), turn: sim.world.turn, eventType: "espionage",
        sourceName: countryName, targetName: action.target,
        description: `${countryName} deployed intelligence operative to ${action.target}.`
      });
      return res.json({ success: true, message: `Covert spy network deployed to ${action.target}.` });
    }

    if (actType === "ECONOMIC_AID") {
      if (c.treasury < cost) return res.status(400).json({ error: "Insufficient funds." });
      c.treasury -= cost;
      if (sim.countries[action.target]) sim.countries[action.target].treasury += cost;
      sim.mapEvents.push({
        id: Date.now(), turn: sim.world.turn, eventType: "aid",
        sourceName: countryName, targetName: action.target,
        description: `ECONOMIC TRANSFER: $${cost}M transferred from ${countryName} to ${action.target}.`
      });
      return res.json({ success: true, message: `Transferred $${cost}M aid to ${action.target}.` });
    }

    res.json({ success: true, message: "Directive acknowledged." });
  });

  // 4. UN Security Council Resolution & Veto
  app.post('/api/classroom/unsc/propose', (req, res) => {
    const { proposer, title, description, target, effectType } = req.body;
    const newRes = {
      id: sim.unscResolutions.length + 1,
      turn: sim.world.turn,
      proposer, title, description, target, effectType,
      status: "PENDING",
      votes: { [proposer]: "YES" },
      vetoedBy: null
    };
    sim.unscResolutions.push(newRes);
    res.json({ success: true, resolution: newRes });
  });

  app.post('/api/classroom/unsc/vote', (req, res) => {
    const { resolutionId, countryName, vote } = req.body;
    const r = sim.unscResolutions.find(x => x.id === resolutionId);
    if (!r) return res.status(404).json({ error: "Resolution not found." });

    r.votes[countryName] = vote.toUpperCase();
    if (UNSC_PERM_5.includes(countryName) && vote.toUpperCase() === "NO") {
      r.status = "VETOED";
      r.vetoedBy = countryName;
    }
    res.json({ success: true, resolution: r });
  });

  // 5. Red Phone Hotline with Wiretaps
  app.post('/api/classroom/hotline', (req, res) => {
    const { sender, recipient, content } = req.body;
    // 35% chance of spy wiretap if third party has spy in sender or recipient
    const spyMasters = sim.activeAgents
      .filter(a => (a.target === sender || a.target === recipient) && a.owner !== sender && a.owner !== recipient)
      .map(a => a.owner);

    let isIntercepted = false;
    let interceptedBy = null;
    if (spyMasters.length > 0 && Math.random() < 0.40) {
      isIntercepted = true;
      interceptedBy = spyMasters[Math.floor(Math.random() * spyMasters.length)];
    }

    const msg = {
      id: Date.now(),
      turn: sim.world.turn,
      sender, recipient, content,
      isIntercepted, interceptedBy,
      timestamp: new Date().toLocaleTimeString()
    };
    sim.hotlineMessages.push(msg);

    res.json({ success: true, message: msg, note: isIntercepted ? "⚠️ WIRETAP ALERT: Cable intercepted by enemy reconnaissance." : "Encrypted telex dispatched." });
  });

  // 6. Groq AI Adviser Chat
  app.post('/api/classroom/chat', async (req, res) => {
    const { countryName, message } = req.body;
    const persona = ADVISER_PERSONAS[countryName] || ADVISER_PERSONAS["USA"];
    const c = sim.countries[countryName] || INITIAL_COUNTRIES["USA"];

    const systemPrompt = `
      EDUCATIONAL HISTORICAL SIMULATION CONTEXT:
      You are ${persona.name} (${persona.title}) advising the leadership of ${countryName} in 1945–1953.
      Speak with authentic historical gravitas.
      CURRENT STATE:
      - Year: ${sim.world.year} | Turn: ${sim.world.turn} | Treasury: $${c.treasury}M | Bombs: ${c.bombs} | Tension: ${c.tension}%
      - DEFCON: ${sim.world.defcon} | Global Tension: ${sim.world.globalTension}%
      
      RULES & COSTS:
      - Nuclear warheads cost ~$20M each.
      - If player says 'make as many under 20m', calculate 1 bomb for $20M and propose it.
      - War bonds cost $0 and inject +$50M into treasury.
      - Espionage costs $50M.
      - Strategic strikes trigger DEFCON 1 immediately.
      
      If player wants an order, formulate action_command with:
      {"type": "NUCLEAR_EXPANSION"|"ESPIONAGE"|"ECONOMIC_AID"|"WAR_BONDS"|"NUCLEAR_STRIKE"|"NONE", "status": "PROPOSED"|"CONFIRMED", "cost_m": number, "bombs_delta": number, "target": string, "description": string}
      Return JSON: {"action_command": {...}, "reply_narrative": "..."}
    `;

    if (!GROQ_API_KEY) {
      // Heuristic fallback
      let act = { type: "NONE", status: "NONE", cost_m: 0, bombs_delta: 0, target: countryName, description: "Consultation" };
      let narrative = `Commander, ${persona.name} standing by. Instruct me on our diplomatic stance, covert operations, economic aid, or atomic posture.`;
      const lower = message.toLowerCase();

      if (lower.includes("under 20m") || lower.includes("more bombs") || lower.includes("build bomb")) {
        act = { type: "NUCLEAR_EXPANSION", status: "PROPOSED", cost_m: 20, bombs_delta: 1, target: countryName, description: "1 atomic bomb under $20M budget" };
        narrative = `At ~$20M per warhead, a $20M budget cap permits assembling 1 bomb (leaving $${c.treasury - 20}M in Treasury). Click Authorize to execute.`;
      } else if (lower.includes("war bond") || lower.includes("gain money") || lower.includes("make money")) {
        act = { type: "WAR_BONDS", status: "PROPOSED", cost_m: 0, bombs_delta: 0, target: countryName, description: "Emergency sovereign war bonds (+$50M cash)" };
        narrative = `We can float emergency sovereign bonds on the domestic market for an immediate +$50M cash injection (+5% tension). Click Authorize to execute.`;
      }

      return res.json({ action_command: act, reply_narrative: narrative });
    }

    try {
      const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${GROQ_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "llama-3.1-8b-instant",
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: message }
          ],
          response_format: { type: "json_object" },
          temperature: 0.5
        })
      });

      const data = await response.json();
      const parsed = JSON.parse(data.choices[0].message.content);
      res.json(parsed);
    } catch (err) {
      res.json({
        action_command: { type: "NONE", status: "NONE" },
        reply_narrative: `Adviser telex received. Ready for operational directives for ${countryName}.`
      });
    }
  });

  // 7. Host Turn Resolution (PIN POTSDAM1945)
  app.post('/api/classroom/resolve-turn', (req, res) => {
    const { pin } = req.body;
    if (pin !== "POTSDAM1945") {
      return res.status(403).json({ error: "Invalid Host Authorization PIN." });
    }

    // Fiscal collection & tax
    for (const [name, c] of Object.entries(sim.countries)) {
      const baseTax = (name === "USA" ? 75 : (name === "USSR" ? 50 : 30));
      const penalty = c.tension >= 50 ? 0.6 : (c.tension >= 30 ? 0.8 : 1.0);
      c.treasury += Math.floor(baseTax * penalty);
    }

    // Advance Year
    sim.world.year += 1;
    sim.world.turn += 1;

    // Check Crisis triggers
    for (const cr of sim.crises) {
      if (cr.status === "DORMANT" && sim.world.year >= cr.yearStarted) {
        cr.status = "ACTIVE";
        sim.newsFeed.push({
          id: Date.now(), turn: sim.world.turn, year: sim.world.year,
          headline: `CRISIS ERUPTS: ${cr.title}`,
          body: cr.description
        });
      }
    }

    res.json({ success: true, world: sim.world });
  });

  // 8. Reset Game
  app.post('/api/classroom/reset', (req, res) => {
    sim.reset();
    res.json({ success: true, message: "Simulation restored to Potsdam 1945." });
  });
}
