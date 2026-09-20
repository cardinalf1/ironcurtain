/*!
 * The Iron Curtain - Palantir C2 Strategic Operations Platform (React Component)
 * Mounted atop Open-Historia canvas map engine.
 */

import React, { useState, useEffect } from 'react';

const DEFCON_STYLES = {
  5: { bg: '#0f2d1e', color: '#3fb950', border: '#238636', label: 'DEFCON 5 // PEACETIME' },
  4: { bg: '#162c38', color: '#58a6ff', border: '#388bfd', label: 'DEFCON 4 // INTELLIGENCE WATCH' },
  3: { bg: '#302611', color: '#d29922', border: '#9e6a03', label: 'DEFCON 3 // FORWARD DEPLOYED' },
  2: { bg: '#3b1e15', color: '#f0883e', border: '#bd561d', label: 'DEFCON 2 // ARMED FORCES READY' },
  1: { bg: '#3d1419', color: '#f85149', border: '#da3633', label: 'DEFCON 1 // MAXIMUM ALERT (WAR)' }
};

export default function ClassroomPlatform() {
  const [selectedRole, setSelectedRole] = useState('PROJECTOR');
  const [state, setState] = useState(null);
  const [inspectedTarget, setInspectedTarget] = useState('USSR');
  const [dossier, setDossier] = useState(null);
  const [activeTab, setActiveTab] = useState('DOSSIER');
  const [isMinimized, setIsMinimized] = useState(false);
  
  // Chat / Adviser
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [pendingProposal, setPendingProposal] = useState(null);
  const [isThinking, setIsThinking] = useState(false);

  // Hotline
  const [hotlineTarget, setHotlineTarget] = useState('USSR');
  const [hotlineMsg, setHotlineMsg] = useState('');
  const [hotlineLogs, setHotlineLogs] = useState([]);

  // Host PIN
  const [hostPin, setHostPin] = useState('POTSDAM1945');

  // Polling State
  const fetchState = async () => {
    try {
      const res = await fetch('/api/classroom/state');
      if (res.ok) {
        const data = await res.json();
        setState(data);
      }
    } catch (e) {
      console.warn('Could not reach classroom server:', e);
    }
  };

  useEffect(() => {
    fetchState();
    const timer = setInterval(fetchState, 3500);
    return () => clearInterval(timer);
  }, []);

  // Fetch Dossier
  useEffect(() => {
    if (!state || selectedRole === 'PROJECTOR') return;
    const fetchDossier = async () => {
      try {
        const res = await fetch(`/api/classroom/dossier/${selectedRole}/${inspectedTarget}`);
        if (res.ok) {
          const d = await res.json();
          setDossier(d);
        }
      } catch (e) {
        console.warn('Dossier fetch error:', e);
      }
    };
    fetchDossier();
  }, [selectedRole, inspectedTarget, state]);

  if (!state) {
    return (
      <div style={{ position: 'fixed', top: 12, right: 12, zIndex: 9999, background: '#121822', padding: '8px 14px', borderRadius: '4px', border: '1px solid #222d3d', color: '#79c0ff', fontFamily: 'monospace' }}>
        CONNECTING TO CLASSROOM C2 SERVER...
      </div>
    );
  }

  const { world, countries, buffers, unscResolutions, crises, newsFeed } = state;
  const currentCountry = countries[selectedRole];
  const isP5 = ["USA", "USSR", "United Kingdom", "France", "China"].includes(selectedRole);

  // Send Command to Adviser
  const handleSendMessage = async (customPrompt) => {
    const promptToSend = customPrompt || chatInput;
    if (!promptToSend.trim()) return;

    const newHistory = [...chatMessages, { role: 'user', text: promptToSend }];
    setChatMessages(newHistory);
    setChatInput('');
    setIsThinking(true);

    try {
      const res = await fetch('/api/classroom/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ countryName: selectedRole, message: promptToSend })
      });
      const data = await res.json();
      setIsThinking(false);

      if (data.action_command && data.action_command.status === 'PROPOSED') {
        setPendingProposal(data.action_command);
      }

      setChatMessages([...newHistory, { role: 'assistant', text: data.reply_narrative }]);
    } catch (e) {
      setIsThinking(false);
      setChatMessages([...newHistory, { role: 'assistant', text: 'Adviser telex offline. Check network connection.' }]);
    }
  };

  // Authorize Proposal
  const handleAuthorizeProposal = async () => {
    if (!pendingProposal) return;
    try {
      const res = await fetch('/api/classroom/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ countryName: selectedRole, action: pendingProposal })
      });
      const data = await res.json();
      setPendingProposal(null);
      fetchState();
      setChatMessages(prev => [...prev, { role: 'assistant', text: `Directive authorized and transmitted to General Staff. ${data.message}` }]);
    } catch (e) {
      alert('Action authorization failed');
    }
  };

  // Hotline Send
  const handleSendHotline = async () => {
    if (!hotlineMsg.trim()) return;
    try {
      const res = await fetch('/api/classroom/hotline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender: selectedRole, recipient: hotlineTarget, content: hotlineMsg })
      });
      const data = await res.json();
      setHotlineLogs(prev => [data.message, ...prev]);
      setHotlineMsg('');
      alert(data.note);
    } catch (e) {
      alert('Hotline telex failed');
    }
  };

  // UNSC Vote
  const handleUnscVote = async (resId, vote) => {
    await fetch('/api/classroom/unsc/vote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resolutionId: resId, countryName: selectedRole, vote })
    });
    fetchState();
  };

  // Turn Resolution
  const handleResolveTurn = async () => {
    const res = await fetch('/api/classroom/resolve-turn', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pin: hostPin })
    });
    if (res.ok) {
      alert('Turn resolved successfully! Advanced to next historical year.');
      fetchState();
    } else {
      alert('Incorrect Host Authorization PIN');
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      pointerEvents: 'none',
      zIndex: 900,
      fontFamily: "'Inter', -apple-system, sans-serif",
      color: '#e6edf3'
    }}>
      {/* TOP DEFENSE RIBBON */}
      <div style={{
        pointerEvents: 'auto',
        background: 'rgba(10, 13, 18, 0.94)',
        borderBottom: '1px solid #222d3d',
        backdropFilter: 'blur(10px)',
        padding: '8px 16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontWeight: 700, fontSize: '0.95rem', letterSpacing: '-0.02em', color: '#388bfd' }}>
            THE IRON CURTAIN // PALANTIR C2
          </span>
          <span style={{ background: '#162c38', color: '#58a6ff', border: '1px solid #388bfd', borderRadius: '4px', fontSize: '0.72rem', padding: '2px 6px', fontWeight: 600 }}>
            YEAR {world.year}
          </span>
          <span style={{ background: DEFCON_STYLES[world.defcon]?.bg, color: DEFCON_STYLES[world.defcon]?.color, border: `1px solid ${DEFCON_STYLES[world.defcon]?.border}`, borderRadius: '4px', fontSize: '0.72rem', padding: '2px 6px', fontWeight: 700 }}>
            {DEFCON_STYLES[world.defcon]?.label}
          </span>
          <span style={{ fontSize: '0.78rem', color: '#8b949e', fontFamily: 'monospace' }}>
            GLOBAL TENSION: {world.globalTension}%
          </span>
        </div>

        {/* ROLE SELECTOR */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.75rem', color: '#8b949e', fontWeight: 600 }}>TERMINAL:</span>
          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            style={{
              background: '#121822',
              color: '#e6edf3',
              border: '1px solid #30363d',
              borderRadius: '4px',
              padding: '4px 8px',
              fontSize: '0.8rem',
              fontWeight: 600
            }}
          >
            <option value="PROJECTOR">🏛️ TEACHER PROJECTOR VIEW</option>
            {Object.keys(countries).map(c => (
              <option key={c} value={c}>🚩 {c.toUpperCase()} TERMINAL</option>
            ))}
          </select>
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            style={{
              background: isMinimized ? '#238636' : '#21262d',
              color: '#e6edf3',
              border: '1px solid #30363d',
              borderRadius: '4px',
              padding: '4px 10px',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            {isMinimized ? '⛶ EXPAND C2 PANELS' : '− MINIMIZE C2 PANELS'}
          </button>
        </div>
      </div>

      {/* VIEW PANELS */}
      {!isMinimized && (
        selectedRole === 'PROJECTOR' ? (
        <div style={{
          pointerEvents: 'auto',
          position: 'absolute',
          top: 60, right: 16, width: 380,
          background: 'rgba(18, 24, 34, 0.96)',
          border: '1px solid #222d3d',
          borderRadius: '6px',
          padding: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.6)'
        }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: '#79c0ff' }}>🏛️ JOINT CHIEFS COMMAND CONSOLE</h4>
          <p style={{ fontSize: '0.8rem', color: '#8b949e', margin: '0 0 14px 0' }}>
            Central host projection. Monitor student orders and execute turn arbitration.
          </p>

          <div style={{ background: '#18202d', border: '1px solid #222d3d', borderRadius: '4px', padding: '10px', marginBottom: '12px' }}>
            <div style={{ fontSize: '0.72rem', color: '#8b949e', textTransform: 'uppercase', fontWeight: 600 }}>Active Dynamic Crises</div>
            {crises.map(cr => (
              <div key={cr.id} style={{ fontSize: '0.8rem', marginTop: '4px' }}>
                • <b>{cr.title}</b>: <span style={{ color: cr.status === 'ACTIVE' ? '#f85149' : '#d29922' }}>[{cr.status}]</span>
              </div>
            ))}
          </div>

          <div style={{ marginBottom: '12px' }}>
            <label style={{ fontSize: '0.72rem', color: '#8b949e', display: 'block', marginBottom: '4px' }}>HOST AUTHORIZATION PIN:</label>
            <input
              type="password"
              value={hostPin}
              onChange={(e) => setHostPin(e.target.value)}
              style={{ width: '100%', background: '#0a0d12', border: '1px solid #30363d', color: '#e6edf3', borderRadius: '4px', padding: '6px' }}
            />
          </div>

          <button
            onClick={handleResolveTurn}
            style={{
              width: '100%',
              background: '#238636',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              padding: '10px',
              fontWeight: 700,
              fontSize: '0.85rem',
              cursor: 'pointer'
            }}
          >
            EXECUTE TURN RESOLUTION ⚡
          </button>
        </div>
      ) : (
        /* VIEW: STUDENT NATION TERMINAL */
        <div style={{
          pointerEvents: 'auto',
          position: 'absolute',
          top: 56, bottom: 0, left: 0, right: 0,
          display: 'grid',
          gridTemplateColumns: '1fr 420px',
          background: 'transparent'
        }}>
          {/* LEFT: CLASSIFIED DOSSIER & TACTICAL TABS OVERLAY */}
          <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px', overflowY: 'auto' }}>
            {/* Country Telemetry Strip */}
            {currentCountry && (
              <div style={{
                background: 'rgba(18, 24, 34, 0.94)',
                border: '1px solid #222d3d',
                borderRadius: '6px',
                padding: '10px 14px',
                display: 'grid',
                gridTemplateColumns: 'repeat(6, 1fr)',
                gap: '10px',
                backdropFilter: 'blur(8px)'
              }}>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>National Treasury</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace', color: '#79c0ff' }}>${currentCountry.treasury}M</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>Atomic Warheads</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace', color: currentCountry.bombs > 0 ? '#f85149' : '#8b949e' }}>{currentCountry.bombs}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>Uranium Supply</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace' }}>{currentCountry.uranium} MT</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>Oil Reserves</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace' }}>{currentCountry.oil}%</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>Domestic Stability</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace' }}>{currentCountry.domesticApproval}%</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.65rem', color: '#8b949e', textTransform: 'uppercase' }}>Domestic Tension</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace', color: currentCountry.tension > 30 ? '#d29922' : '#3fb950' }}>{currentCountry.tension}%</div>
                </div>
              </div>
            )}

            {/* Target Territory Inspector Selector */}
            <div style={{
              background: 'rgba(18, 24, 34, 0.94)',
              border: '1px solid #222d3d',
              borderRadius: '6px',
              padding: '12px 14px',
              backdropFilter: 'blur(8px)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#388bfd' }}>
                  📂 PALANTIR C2 // TARGET INTELLIGENCE DOSSIER
                </span>
                <select
                  value={inspectedTarget}
                  onChange={(e) => setInspectedTarget(e.target.value)}
                  style={{ background: '#0a0d12', color: '#e6edf3', border: '1px solid #30363d', borderRadius: '4px', fontSize: '0.8rem', padding: '3px 8px' }}
                >
                  {Object.keys(countries).concat(Object.keys(buffers)).map(t => (
                    <option key={t} value={t}>{t.toUpperCase()}</option>
                  ))}
                </select>
              </div>

              {dossier && (
                <div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px' }}>
                    <span style={{ fontSize: '1.05rem', fontWeight: 700 }}>{dossier.targetName}</span>
                    <span style={{ background: 'rgba(56, 139, 253, 0.15)', color: '#79c0ff', border: '1px solid rgba(56, 139, 253, 0.35)', borderRadius: '4px', fontSize: '0.65rem', padding: '2px 6px', fontWeight: 600 }}>
                      {dossier.confidenceLabel}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#8b949e', marginLeft: 'auto' }}>
                      STANCE: <b>{dossier.stance}</b>
                    </span>
                  </div>

                  {!dossier.isBuffer && (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px', marginBottom: '10px' }}>
                      <div style={{ background: '#0a0d12', padding: '6px 8px', borderRadius: '4px', border: '1px solid #222d3d' }}>
                        <div style={{ fontSize: '0.6rem', color: '#8b949e' }}>Atomic Weapons</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, fontFamily: 'monospace' }}>{dossier.bombsDisplay}</div>
                      </div>
                      <div style={{ background: '#0a0d12', padding: '6px 8px', borderRadius: '4px', border: '1px solid #222d3d' }}>
                        <div style={{ fontSize: '0.6rem', color: '#8b949e' }}>Treasury Reserves</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, fontFamily: 'monospace' }}>{dossier.treasuryDisplay}</div>
                      </div>
                      <div style={{ background: '#0a0d12', padding: '6px 8px', borderRadius: '4px', border: '1px solid #222d3d' }}>
                        <div style={{ fontSize: '0.6rem', color: '#8b949e' }}>Fissile Uranium</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, fontFamily: 'monospace' }}>{dossier.uraniumDisplay}</div>
                      </div>
                      <div style={{ background: '#0a0d12', padding: '6px 8px', borderRadius: '4px', border: '1px solid #222d3d' }}>
                        <div style={{ fontSize: '0.6rem', color: '#8b949e' }}>Domestic Stability</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, fontFamily: 'monospace' }}>{dossier.approvalDisplay}</div>
                      </div>
                    </div>
                  )}

                  {/* 1-Click Action Bar */}
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button
                      onClick={() => handleSendMessage(`Deploy an intelligence spy network to ${inspectedTarget} with $50M`)}
                      style={{ flex: 1, background: '#1f2a3a', border: '1px solid #30363d', color: '#e6edf3', borderRadius: '4px', padding: '6px 4px', fontSize: '0.72rem', cursor: 'pointer', fontWeight: 600 }}
                    >
                      🕵️ Spy ($50M)
                    </button>
                    <button
                      onClick={() => handleSendMessage(`Send $40M economic reconstruction aid to ${inspectedTarget}`)}
                      style={{ flex: 1, background: '#1f2a3a', border: '1px solid #30363d', color: '#e6edf3', borderRadius: '4px', padding: '6px 4px', fontSize: '0.72rem', cursor: 'pointer', fontWeight: 600 }}
                    >
                      💵 Grant Aid ($40M)
                    </button>
                    <button
                      onClick={() => handleSendMessage(`Propose a bilateral commercial trade pact with ${inspectedTarget}`)}
                      style={{ flex: 1, background: '#1f2a3a', border: '1px solid #30363d', color: '#e6edf3', borderRadius: '4px', padding: '6px 4px', fontSize: '0.72rem', cursor: 'pointer', fontWeight: 600 }}
                    >
                      🤝 Trade Treaty
                    </button>
                    <button
                      onClick={() => handleSendMessage(`Table a formal resolution in the UN Security Council regarding ${inspectedTarget}`)}
                      style={{ flex: 1, background: '#1f2a3a', border: '1px solid #30363d', color: '#e6edf3', borderRadius: '4px', padding: '6px 4px', fontSize: '0.72rem', cursor: 'pointer', fontWeight: 600 }}
                    >
                      📜 UNSC Sanction
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Tactical C2 Tabs */}
            <div style={{ background: 'rgba(18, 24, 34, 0.94)', border: '1px solid #222d3d', borderRadius: '6px', padding: '12px 14px', backdropFilter: 'blur(8px)' }}>
              <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid #222d3d', paddingBottom: '8px', marginBottom: '10px' }}>
                <button onClick={() => setActiveTab('DOSSIER')} style={{ background: activeTab === 'DOSSIER' ? '#388bfd' : '#1f2a3a', color: '#fff', border: 'none', borderRadius: '4px', padding: '4px 10px', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }}>
                  🇺🇳 UN SECURITY COUNCIL
                </button>
                <button onClick={() => setActiveTab('HOTLINE')} style={{ background: activeTab === 'HOTLINE' ? '#388bfd' : '#1f2a3a', color: '#fff', border: 'none', borderRadius: '4px', padding: '4px 10px', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }}>
                  📞 RED PHONE HOTLINE
                </button>
                <button onClick={() => setActiveTab('BONDS')} style={{ background: activeTab === 'BONDS' ? '#388bfd' : '#1f2a3a', color: '#fff', border: 'none', borderRadius: '4px', padding: '4px 10px', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }}>
                  ⚡ WAR BONDS
                </button>
              </div>

              {activeTab === 'DOSSIER' && (
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#8b949e', marginBottom: '8px' }}>
                    Active Resolutions ({isP5 ? 'Permanent 5 VETO Active' : 'General Member'}):
                  </div>
                  {unscResolutions.length === 0 ? (
                    <div style={{ fontSize: '0.8rem', color: '#8b949e' }}>No resolutions tabled this turn.</div>
                  ) : (
                    unscResolutions.map(r => (
                      <div key={r.id} style={{ background: '#0a0d12', padding: '8px 10px', borderRadius: '4px', border: '1px solid #222d3d', marginBottom: '6px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                          <b>{r.title}</b>
                          <span style={{ color: r.status === 'PASSED' ? '#3fb950' : (r.status === 'VETOED' ? '#f85149' : '#d29922') }}>[{r.status}]</span>
                        </div>
                        <div style={{ fontSize: '0.72rem', color: '#8b949e', margin: '4px 0' }}>{r.description}</div>
                        {r.status === 'PENDING' && (
                          <div style={{ display: 'flex', gap: '6px', marginTop: '6px' }}>
                            <button onClick={() => handleUnscVote(r.id, 'YES')} style={{ background: '#238636', border: 'none', color: '#fff', borderRadius: '3px', padding: '2px 8px', fontSize: '0.7rem', cursor: 'pointer' }}>
                              Vote YES
                            </button>
                            <button onClick={() => handleUnscVote(r.id, 'NO')} style={{ background: '#da3633', border: 'none', color: '#fff', borderRadius: '3px', padding: '2px 8px', fontSize: '0.7rem', cursor: 'pointer' }}>
                              {isP5 ? 'VETO (NO)' : 'Vote NO'}
                            </button>
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </div>
              )}

              {activeTab === 'HOTLINE' && (
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#8b949e', marginBottom: '6px' }}>
                    Confidential telex to another nation leader (35% spy wiretap risk):
                  </div>
                  <div style={{ display: 'flex', gap: '6px', marginBottom: '8px' }}>
                    <select
                      value={hotlineTarget}
                      onChange={(e) => setHotlineTarget(e.target.value)}
                      style={{ background: '#0a0d12', color: '#e6edf3', border: '1px solid #30363d', borderRadius: '4px', fontSize: '0.75rem', padding: '4px' }}
                    >
                      {Object.keys(countries).filter(c => c !== selectedRole).map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                    <input
                      type="text"
                      placeholder="Type confidential cable..."
                      value={hotlineMsg}
                      onChange={(e) => setHotlineMsg(e.target.value)}
                      style={{ flex: 1, background: '#0a0d12', color: '#e6edf3', border: '1px solid #30363d', borderRadius: '4px', padding: '4px 8px', fontSize: '0.75rem' }}
                    />
                    <button onClick={handleSendHotline} style={{ background: '#388bfd', color: '#fff', border: 'none', borderRadius: '4px', padding: '4px 10px', fontSize: '0.75rem', cursor: 'pointer' }}>
                      Dispatch 📨
                    </button>
                  </div>
                  <div style={{ maxHeight: 100, overflowY: 'auto' }}>
                    {hotlineLogs.map(m => (
                      <div key={m.id} style={{ fontSize: '0.72rem', background: '#0a0d12', padding: '4px 6px', borderRadius: '3px', marginBottom: '3px' }}>
                        <b>To {m.recipient}:</b> {m.content}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'BONDS' && (
                <div>
                  <p style={{ fontSize: '0.78rem', color: '#8b949e', margin: '0 0 10px 0' }}>
                    Float domestic emergency sovereign bonds to immediately inject <b>+$50M cash</b> into the national treasury (+5% domestic tension).
                  </p>
                  <button
                    onClick={() => handleSendMessage('Float emergency sovereign war bonds')}
                    style={{ background: '#d29922', color: '#000', border: 'none', borderRadius: '4px', padding: '8px 14px', fontSize: '0.8rem', fontWeight: 700, cursor: 'pointer' }}
                  >
                    ⚡ FLOAT EMERGENCY WAR BONDS (+$50M CASH)
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* RIGHT: ADVISER COMMAND LOG */}
          <div style={{
            background: 'rgba(14, 18, 24, 0.97)',
            borderLeft: '1px solid #222d3d',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '-4px 0 20px rgba(0,0,0,0.5)'
          }}>
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#388bfd', marginBottom: '2px' }}>
                🎙️ ADVISER COMMAND LOG
              </div>
              <div style={{ fontSize: '0.72rem', color: '#8b949e', marginBottom: '12px' }}>
                Direct telex to General Staff. Instruct in plain English.
              </div>

              {/* Chat Message Stream */}
              <div style={{ maxHeight: 'calc(100vh - 340px)', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', paddingRight: '4px' }}>
                {chatMessages.map((m, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: m.role === 'user' ? '#1c2433' : '#121822',
                      border: `1px solid ${m.role === 'user' ? '#388bfd' : '#222d3d'}`,
                      borderRadius: '6px',
                      padding: '8px 10px',
                      fontSize: '0.8rem',
                      lineHeight: '1.4'
                    }}
                  >
                    <b style={{ color: m.role === 'user' ? '#79c0ff' : '#3fb950', fontSize: '0.7rem', display: 'block', marginBottom: '2px' }}>
                      {m.role === 'user' ? 'COMMANDER:' : 'ADVISER:'}
                    </b>
                    {m.text}
                  </div>
                ))}
                {isThinking && (
                  <div style={{ fontSize: '0.75rem', color: '#8b949e', fontStyle: 'italic' }}>
                    Adviser calculating operational options...
                  </div>
                )}
              </div>
            </div>

            {/* Bottom Controls: Proposal & Input */}
            <div>
              {/* Amber Proposed Directive Card */}
              {pendingProposal && (
                <div style={{
                  background: 'rgba(210, 153, 34, 0.1)',
                  border: '1px solid #d29922',
                  borderRadius: '4px',
                  padding: '8px 10px',
                  marginBottom: '10px'
                }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#d29922', marginBottom: '4px' }}>
                    📋 PROPOSED DIRECTIVE (AWAITING YOUR AUTHORIZATION)
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#e6edf3', marginBottom: '6px' }}>
                    • Action: <b>{pendingProposal.type}</b> | Budget: <b>${pendingProposal.cost_m || 0}M</b><br />
                    • Effect: {pendingProposal.description}
                  </div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button
                      onClick={handleAuthorizeProposal}
                      style={{ flex: 1, background: '#238636', color: '#fff', border: 'none', borderRadius: '3px', padding: '6px', fontSize: '0.75rem', fontWeight: 700, cursor: 'pointer' }}
                    >
                      AUTHORIZE & EXECUTE 🚀
                    </button>
                    <button
                      onClick={() => setPendingProposal(null)}
                      style={{ background: '#30363d', color: '#fff', border: 'none', borderRadius: '3px', padding: '6px 10px', fontSize: '0.75rem', cursor: 'pointer' }}
                    >
                      CANCEL ❌
                    </button>
                  </div>
                </div>
              )}

              {/* Chat Input */}
              <div style={{ display: 'flex', gap: '6px' }}>
                <input
                  type="text"
                  placeholder="Tell your adviser (e.g. 'Build 2 bombs under 40m', 'Go')..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
                  style={{
                    flex: 1,
                    background: '#0a0d12',
                    border: '1px solid #30363d',
                    color: '#e6edf3',
                    borderRadius: '4px',
                    padding: '8px 10px',
                    fontSize: '0.8rem'
                  }}
                />
                <button
                  onClick={() => handleSendMessage()}
                  style={{
                    background: '#388bfd',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '8px 14px',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      )
    )}
  </div>
);
}
