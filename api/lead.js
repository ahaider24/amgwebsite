// Vercel serverless function: lead-capture POST -> AMG engine webhook.
//
// History: the original version wrote straight to Airtable and needed
// AIRTABLE_* env vars that were never set on this Vercel project, so it
// returned 500 for ~2 months (flagged July 5, fixed Sep 2). This version
// needs NO env vars: it forwards to the engine's droplet endpoint, which
// holds credentials server-side and alerts Slack + stores the lead.

const ENGINE_LEAD_URL = 'https://n8n.amirgetsjobs.com/hooks/lead';

// GET /api/lead?health=1 is the uptime probe (Checkly). It sends
// {"health": true} down the same path a real lead takes; the engine checks
// the lead store and the Slack alert pipe and answers 200 or 503 without
// saving anything. Any other GET is still 405.
async function health(res) {
  try {
    const r = await fetch(ENGINE_LEAD_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ health: true }),
    });
    const text = await r.text();
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Content-Type', 'application/json');
    return res.status(r.status === 200 ? 200 : 503).send(text);
  } catch (err) {
    console.error('Lead health error', err);
    return res.status(503).json({ ok: false, error: 'engine unreachable' });
  }
}

export default async function handler(req, res) {
  if (req.method === 'GET' && req.query && req.query.health === '1') {
    return health(res);
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const email = (body.email || '').toString().trim();
  const phone = (body.phone || '').toString().trim();
  if (!email && !phone) {
    return res.status(400).json({ error: 'Email or phone required.' });
  }

  try {
    const r = await fetch(ENGINE_LEAD_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...body, source: body.source || 'api/lead' }),
    });
    const text = await r.text();
    res.status(r.status);
    res.setHeader('Content-Type', 'application/json');
    return res.send(text);
  } catch (err) {
    console.error('Lead forward error', err);
    return res.status(502).json({ error: 'Could not save the lead.' });
  }
}
