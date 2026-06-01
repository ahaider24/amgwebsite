// Vercel serverless function: receives the lead-capture POST from
// what-ai-can-do.html and writes the lead to Airtable, server-side.
//
// Required Vercel env vars (Project Settings > Environment Variables).
// Never put these in client code:
//   AIRTABLE_TOKEN    personal access token with data.records:write on the base
//   AIRTABLE_BASE_ID  the base id, e.g. appXXXXXXXXXXXXXX
//   AIRTABLE_TABLE    table name or id (optional, defaults to "Leads")
//
// The target Airtable table needs these columns (typecast is on, so single
// selects can be created on the fly, but the column names must match):
//   First Name (text), Last Name (text), Company (text), Email (email),
//   Phone (phone), Trade (single select or text), Source (text)

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const token = process.env.AIRTABLE_TOKEN;
  const baseId = process.env.AIRTABLE_BASE_ID;
  const table = process.env.AIRTABLE_TABLE || 'Leads';
  if (!token || !baseId) {
    return res.status(500).json({ error: 'Lead capture is not configured yet.' });
  }

  // Vercel parses JSON bodies automatically, but guard for string bodies too.
  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const firstName = (body.firstName || '').toString().trim();
  const lastName = (body.lastName || '').toString().trim();
  const company = (body.company || '').toString().trim();
  const email = (body.email || '').toString().trim();
  const phone = (body.phone || '').toString().trim();
  const trade = (body.trade || '').toString().trim();

  if (!firstName || !lastName || !email || !phone) {
    return res.status(400).json({ error: 'Missing required fields.' });
  }

  const url = 'https://api.airtable.com/v0/' + baseId + '/' + encodeURIComponent(table);
  const record = {
    fields: {
      'First Name': firstName,
      'Last Name': lastName,
      Company: company,
      Email: email,
      Phone: phone,
      Trade: trade,
      Source: 'what-ai-can-do',
    },
    typecast: true,
  };

  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + token,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(record),
    });
    if (!r.ok) {
      const detail = await r.text();
      console.error('Airtable error', r.status, detail);
      return res.status(502).json({ error: 'Could not save the lead.' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Lead handler error', err);
    return res.status(500).json({ error: 'Unexpected error.' });
  }
}
