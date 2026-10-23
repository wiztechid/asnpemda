const ALLOWED_ARTICLES = new Set([
  "permenpanrb-9-2026-pppk-paruh-waktu",
  "pppk-paruh-waktu-penuh-waktu-2027",
  "aturan-wfh-asn-pemda-2026-se-mendagri-4412-sj",
  "cara-menghitung-gaji-pensiun-pns",
]);
const PUBLIC_HOST = "asnpemda.pages.dev";

function reply(data, status = 200) {
  return Response.json(data, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
  });
}

async function digestIp(request, env, day) {
  const ip = request.headers.get("CF-Connecting-IP");
  if (!ip || !env.IP_HASH_SECRET) return null;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.IP_HASH_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${day}:${ip}`));
  return [...new Uint8Array(signature)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function readJson(request) {
  const size = Number(request.headers.get("Content-Length") || 0);
  if (size > 1000) return null;
  try {
    const text = await request.text();
    return text.length <= 1000 ? JSON.parse(text) : null;
  } catch { return null; }
}

async function cleanup(env) {
  await env.COMMENTS_DB.prepare("DELETE FROM feedback_votes WHERE datetime(updated_at) < datetime('now', '-2 days')").run();
}

export async function onRequest(context) {
  const { request, env } = context;
  const origin = request.headers.get("Origin");
  if (request.method !== "GET" && origin !== `https://${PUBLIC_HOST}`) return reply({ error: "Permintaan ditolak." }, 403);
  if (request.method === "GET" && origin && origin !== `https://${PUBLIC_HOST}`) return reply({ error: "Permintaan ditolak." }, 403);
  if (!env.COMMENTS_DB) return reply({ error: "Layanan umpan balik sedang disiapkan." }, 503);
  const url = new URL(request.url);
  const article = url.searchParams.get("article") || "";
  if (!ALLOWED_ARTICLES.has(article)) return reply({ error: "Artikel tidak ditemukan." }, 404);

  if (request.method === "GET") {
    await cleanup(env);
    const rows = await env.COMMENTS_DB.prepare("SELECT vote, count FROM feedback_totals WHERE article_slug = ?").bind(article).all();
    const counts = { yes: 0, no: 0 };
    for (const row of rows.results || []) counts[row.vote] = Number(row.count) || 0;
    return reply(counts);
  }
  if (request.method !== "POST") return reply({ error: "Metode tidak didukung." }, 405);
  const input = await readJson(request);
  if (!input || !["yes", "no"].includes(input.vote)) return reply({ error: "Pilihan tidak valid." }, 400);
  const day = new Date().toISOString().slice(0, 10);
  const ipHash = await digestIp(request, env, day);
  if (!ipHash) return reply({ error: "Umpan balik belum dapat diproses." }, 503);
  await cleanup(env);
  const prior = await env.COMMENTS_DB.prepare("SELECT vote FROM feedback_votes WHERE article_slug = ? AND ip_hash = ?").bind(article, ipHash).first();
  if (!prior) {
    await env.COMMENTS_DB.batch([
      env.COMMENTS_DB.prepare("INSERT INTO feedback_votes (article_slug, ip_hash, vote) VALUES (?, ?, ?)").bind(article, ipHash, input.vote),
      env.COMMENTS_DB.prepare("INSERT INTO feedback_totals (article_slug, vote, count) VALUES (?, ?, 1) ON CONFLICT(article_slug, vote) DO UPDATE SET count = count + 1").bind(article, input.vote),
    ]);
  } else if (prior.vote !== input.vote) {
    await env.COMMENTS_DB.batch([
      env.COMMENTS_DB.prepare("UPDATE feedback_votes SET vote = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE article_slug = ? AND ip_hash = ?").bind(input.vote, article, ipHash),
      env.COMMENTS_DB.prepare("UPDATE feedback_totals SET count = MAX(count - 1, 0) WHERE article_slug = ? AND vote = ?").bind(article, prior.vote),
      env.COMMENTS_DB.prepare("INSERT INTO feedback_totals (article_slug, vote, count) VALUES (?, ?, 1) ON CONFLICT(article_slug, vote) DO UPDATE SET count = count + 1").bind(article, input.vote),
    ]);
  }
  const rows = await env.COMMENTS_DB.prepare("SELECT vote, count FROM feedback_totals WHERE article_slug = ?").bind(article).all();
  const counts = { yes: 0, no: 0 };
  for (const row of rows.results || []) counts[row.vote] = Number(row.count) || 0;
  return reply({ ok: true, counts });
}
