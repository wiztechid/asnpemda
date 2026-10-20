const ALLOWED_ARTICLES = new Set([
  "permenpanrb-9-2026-pppk-paruh-waktu",
  "pppk-paruh-waktu-penuh-waktu-2027",
]);
const PUBLIC_HOST = "asnpemda.pages.dev";
const TURNSTILE_ACTION = "reader-comment";
const MAX_BODY_BYTES = 5000;

function reply(data, status = 200) {
  return Response.json(data, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
  });
}

function sameOrigin(request, requireOrigin = false) {
  const origin = request.headers.get("Origin");
  return requireOrigin ? origin === `https://${PUBLIC_HOST}` : !origin || origin === `https://${PUBLIC_HOST}`;
}

async function parseBody(request) {
  const declared = Number(request.headers.get("Content-Length") || 0);
  if (declared > MAX_BODY_BYTES) return null;
  const text = await request.text();
  if (text.length > MAX_BODY_BYTES) return null;
  try { return JSON.parse(text); } catch { return null; }
}

async function digestIp(request, env, bucket) {
  const ip = request.headers.get("CF-Connecting-IP");
  if (!ip || !env.IP_HASH_SECRET) return null;
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(env.IP_HASH_SECRET),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${bucket}:${ip}`));
  return [...new Uint8Array(signature)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function verifyTurnstile(request, env, token) {
  if (!env.TURNSTILE_SECRET || !token || token.length > 2048) return false;
  try {
    const body = new URLSearchParams({
      secret: env.TURNSTILE_SECRET,
      response: token,
      remoteip: request.headers.get("CF-Connecting-IP") || "",
    });
    const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) return false;
    const result = await response.json();
    return result.success === true && result.action === TURNSTILE_ACTION && result.hostname === PUBLIC_HOST;
  } catch {
    return false;
  }
}

export async function onRequest(context) {
  const { request, env } = context;
  if (!sameOrigin(request, request.method !== "GET")) return reply({ error: "Permintaan ditolak." }, 403);
  if (!env.COMMENTS_DB) return reply({ error: "Layanan komentar sedang disiapkan." }, 503);
  const url = new URL(request.url);
  const article = url.searchParams.get("article") || "";
  if (!ALLOWED_ARTICLES.has(article)) return reply({ error: "Artikel tidak ditemukan." }, 404);

  if (request.method === "GET") {
    const result = await env.COMMENTS_DB.prepare(
      "SELECT id, display_name AS name, comment_text AS comment, created_at AS createdAt FROM reader_comments WHERE article_slug = ? AND status = 'approved' ORDER BY created_at DESC LIMIT 30",
    ).bind(article).all();
    return reply({ comments: result.results || [] });
  }
  if (request.method !== "POST") return reply({ error: "Metode tidak didukung." }, 405);

  const input = await parseBody(request);
  if (!input) return reply({ error: "Isi komentar tidak valid." }, 400);
  // Quietly accept the decoy submission so basic bots do not learn the filter.
  if (typeof input.website === "string" && input.website.trim()) return reply({ ok: true, pending: true }, 202);

  const name = typeof input.name === "string" ? input.name.trim().replace(/[\u0000-\u001f\u007f]/g, "") : "";
  const comment = typeof input.comment === "string" ? input.comment.trim().replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "") : "";
  if (name.length < 2 || name.length > 40 || comment.length < 10 || comment.length > 1200) {
    return reply({ error: "Nama panggilan harus 2–40 karakter dan komentar 10–1.200 karakter." }, 400);
  }
  if (/(https?:\/\/|www\.|wa\.me\/|t\.me\/)/i.test(comment)) {
    return reply({ error: "Tautan dan ajakan promosi tidak dapat dikirim melalui kolom komentar." }, 400);
  }
  if (!(await verifyTurnstile(request, env, input.turnstile))) {
    return reply({ error: "Verifikasi anti-spam belum berhasil. Silakan coba lagi." }, 403);
  }
  const hour = String(Math.floor(Date.now() / 3600000));
  const ipHash = await digestIp(request, env, hour);
  if (!ipHash) return reply({ error: "Verifikasi keamanan sedang tidak tersedia." }, 503);
  await env.COMMENTS_DB.prepare("DELETE FROM comment_rate_limits WHERE bucket < ?").bind(String(Number(hour) - 1)).run();
  await env.COMMENTS_DB.prepare("DELETE FROM reader_comments WHERE (status = 'pending' AND created_at < datetime('now', '-90 days')) OR (status = 'rejected' AND created_at < datetime('now', '-30 days')) OR created_at < datetime('now', '-365 days')").run();
  const limit = await env.COMMENTS_DB.prepare(
    "INSERT INTO comment_rate_limits (ip_hash, bucket, count) VALUES (?, ?, 1) ON CONFLICT(ip_hash, bucket) DO UPDATE SET count = count + 1 WHERE count < 3 RETURNING count",
  ).bind(ipHash, hour).first();
  if (!limit) return reply({ error: "Batas kirim komentar tercapai. Coba lagi setelah satu jam." }, 429);

  await env.COMMENTS_DB.prepare(
    "INSERT INTO reader_comments (id, article_slug, display_name, comment_text, status) VALUES (?, ?, ?, ?, 'pending')",
  ).bind(crypto.randomUUID(), article, name, comment).run();
  return reply({ ok: true, pending: true, message: "Komentar diterima dan akan ditampilkan setelah ditinjau." }, 201);
}
