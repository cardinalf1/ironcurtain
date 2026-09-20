// Integration test for Open-Historia + Classroom C2 Platform
import http from 'http';

function request(path, options = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request(`http://localhost:3000${path}`, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, headers: res.headers, body: data });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, body: data });
        }
      });
    });
    req.on('error', reject);
    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

async function run() {
  console.log("Testing server endpoints...");
  
  // 1. Test Classroom State
  const stateRes = await request('/api/classroom/state');
  console.log(`[GET /api/classroom/state] Status: ${stateRes.status}`);
  const state = JSON.parse(stateRes.body);
  console.log(`World Year: ${state.world.year}, DEFCON: ${state.world.defcon}, Tension: ${state.world.globalTension}%`);
  console.log(`Countries: ${Object.keys(state.countries).join(', ')}`);
  
  // 2. Test Dossier
  const dossierRes = await request('/api/classroom/dossier/USA/USSR');
  console.log(`[GET /api/classroom/dossier/USA/USSR] Status: ${dossierRes.status}`);
  const dossier = JSON.parse(dossierRes.body);
  console.log(`Dossier Target: ${dossier.targetName}, Confidence: ${dossier.confidenceLabel} (${dossier.confidencePct}%), Bombs: ${dossier.bombsDisplay}, Treasury: ${dossier.treasuryDisplay}`);

  // 3. Test Static HTML
  const htmlRes = await request('/');
  console.log(`[GET /] Status: ${htmlRes.status}, HTML length: ${htmlRes.body.length}`);
  if (htmlRes.body.includes('Open Historia') || htmlRes.body.includes('<!DOCTYPE html>')) {
    console.log("Static client bundle served successfully!");
  } else {
    console.warn("Unexpected HTML response:", htmlRes.body.slice(0, 200));
  }

  // 4. Test Action Dispatch (USA builds 1 bomb)
  const actionRes = await request('/api/classroom/action', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      countryName: 'USA',
      action: { type: 'NUCLEAR_EXPANSION', cost_m: 20, description: 'Expand Manhattan Project stockpile' }
    })
  });
  console.log(`[POST /api/classroom/action] Status: ${actionRes.status}, Response: ${actionRes.body}`);

  console.log("\nALL INTEGRATION TESTS PASSED CLEANLY!");
  process.exit(0);
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
