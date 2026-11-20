const PUBLIC_HOST = "asnpemda.pages.dev";
const TURNSTILE_ACTION = "draft-srikandi";
const MAX_BODY_BYTES = 6000;
const MAX_TOPIC_CHARS = 700;
const MAX_DRAFT_CHARS = 14000;
const RATE_LIMIT = 4;

function reply(data, status = 200) {
  return Response.json(data, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
  });
}

function cleanText(value) {
  return typeof value === "string"
    ? value.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "").trim()
    : "";
}

async function readInput(request) {
  const declared = Number(request.headers.get("Content-Length") || 0);
  if (declared > MAX_BODY_BYTES) return null;
  const text = await request.text();
  if (text.length > MAX_BODY_BYTES) return null;
  try { return JSON.parse(text); } catch { return null; }
}

async function verifyTurnstile(request, env, token) {
  if (!env.TURNSTILE_SECRET || !token || token.length > 2048) return false;
  try {
    const form = new URLSearchParams({
      secret: env.TURNSTILE_SECRET,
      response: token,
      remoteip: request.headers.get("CF-Connecting-IP") || "",
    });
    const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) return false;
    const result = await response.json();
    return result.success === true
      && result.action === TURNSTILE_ACTION
      && result.hostname === PUBLIC_HOST;
  } catch {
    return false;
  }
}

async function requestHash(request, env, bucket) {
  const ip = request.headers.get("CF-Connecting-IP");
  if (!ip || !env.IP_HASH_SECRET) return null;
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(env.IP_HASH_SECRET),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const signature = await crypto.subtle.sign(
    "HMAC", key, new TextEncoder().encode("srikandi:" + bucket + ":" + ip),
  );
  return [...new Uint8Array(signature)]
    .map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function consumeRateLimit(request, env) {
  if (!env.COMMENTS_DB) return false;
  const bucket = Math.floor(Date.now() / 3600000);
  const ipHash = await requestHash(request, env, bucket);
  if (!ipHash) return false;
  await env.COMMENTS_DB.prepare(
    "CREATE TABLE IF NOT EXISTS srikandi_ai_rate_limits (ip_hash TEXT NOT NULL, bucket INTEGER NOT NULL, count INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (ip_hash, bucket))",
  ).run();
  await env.COMMENTS_DB.prepare(
    "DELETE FROM srikandi_ai_rate_limits WHERE bucket < ?",
  ).bind(bucket - 1).run();
  const row = await env.COMMENTS_DB.prepare(
    "INSERT INTO srikandi_ai_rate_limits (ip_hash, bucket, count) VALUES (?, ?, 1) ON CONFLICT(ip_hash, bucket) DO UPDATE SET count = count + 1 WHERE count < ? RETURNING count",
  ).bind(ipHash, bucket, RATE_LIMIT).first();
  return Boolean(row);
}

function makePrompt(topic) {
  const instructions = [
    "Anda membantu ASN pemerintah daerah menyusun draf awal naskah dinas dalam Bahasa Indonesia formal dan jelas.",
    "Berdasarkan topik pengguna, tentukan sendiri bentuk naskah yang paling sesuai. Pilih satu: surat dinas, nota dinas, surat undangan, surat tugas, atau telaahan staf. Jika topik meminta telaahan kepada pimpinan, gunakan struktur telaahan staf: Persoalan, Praanggapan, Fakta-fakta yang Mempengaruhi, Analisis, Kesimpulan, Saran.",
    "Tulis draf yang praktis, runtut, dan siap disunting. Gunakan hanya fakta yang dinyatakan pengguna. Jangan mengarang nama orang/instansi, tanggal, nomor surat, jumlah, kejadian, kewenangan, dasar hukum, pasal, atau keputusan. Untuk informasi yang belum tersedia, gunakan penanda [LENGKAPI: uraian singkat]. Jangan menyatakan dasar hukum spesifik kecuali disebut jelas oleh pengguna; jika diperlukan, tulis [PERIKSA DAN TAMBAHKAN DASAR HUKUM YANG BERLAKU]. Jangan membuat seolah-olah draf sudah ditandatangani atau disahkan.",
    "Berikan judul jenis naskah di bagian paling atas, lalu susun format naskah yang lazim untuk bentuk tersebut. Untuk surat dinas/undangan, sertakan bagian penerima, hal, isi, penutup, dan blok penandatangan dengan penanda yang diperlukan. Untuk surat tugas, sertakan dasar, nama/jabatan yang ditugaskan, uraian tugas, waktu/tempat, dan penandatangan dengan penanda yang diperlukan. Akhiri dengan satu baris: CATATAN PEMERIKSAAN: daftar singkat bagian yang wajib dilengkapi atau diverifikasi.",
    "Jangan memberi penjelasan di luar draf dan catatan pemeriksaan. Maksimal sekitar 900 kata.",
    "Topik pengguna:",
    topic,
  ];
  return instructions.join("\\n\\n");
}

export async function onRequest({ request, env }) {
  if (request.method !== "POST") return reply({ error: "Metode tidak didukung." }, 405);
  if (request.headers.get("Origin") !== "https://" + PUBLIC_HOST) {
    return reply({ error: "Permintaan ditolak." }, 403);
  }
  const input = await readInput(request);
  if (!input) return reply({ error: "Permintaan tidak valid atau terlalu besar." }, 400);
  if (typeof input.website === "string" && input.website.trim()) {
    return reply({ error: "Draft tidak dapat dibuat." }, 400);
  }
  const topic = cleanText(input.topic);
  if (topic.length < 8 || topic.length > MAX_TOPIC_CHARS) {
    return reply({ error: "Topik harus berisi 8–700 karakter." }, 400);
  }
  if (!(await verifyTurnstile(request, env, cleanText(input.turnstile)))) {
    return reply({ error: "Verifikasi anti-spam belum berhasil. Silakan coba lagi." }, 403);
  }
  if (!(await consumeRateLimit(request, env))) {
    return reply({ error: "Batas penggunaan tercapai atau layanan keamanan belum siap. Coba lagi nanti." }, 429);
  }
  if (!env.AI || typeof env.AI.run !== "function") {
    return reply({ error: "Layanan AI belum siap. Silakan coba lagi nanti." }, 503);
  }

  try {
    const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fp8-fast", {
      prompt: makePrompt(topic),
      max_tokens: 1400,
      temperature: 0.2,
    });
    const draft = cleanText(result?.response || result?.output_text || "");
    if (!draft) return reply({ error: "AI belum menghasilkan draft. Coba jelaskan topik dengan lebih spesifik." }, 502);
    return reply({
      draft: draft.slice(0, MAX_DRAFT_CHARS),
      document_type: draft.split(/\r?\n/).find((line) => line.trim())?.slice(0, 90) || "Draft selesai",
    });
  } catch {
    return reply({ error: "AI sedang sibuk atau gagal menyusun draft. Silakan coba lagi." }, 502);
  }
}