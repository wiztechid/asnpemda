const PUBLIC_HOST = "asnpemda.pages.dev";
const TURNSTILE_ACTION = "draft-srikandi";
const MAX_BODY_BYTES = 6000;
const MAX_TOPIC_CHARS = 700;
const MAX_DRAFT_CHARS = 14000;

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

function removeRepeatedParagraphs(text) {
  const seen = new Set();
  const result = [];
  for (const paragraph of text.split(/\n\s*\n+/)) {
    const normalized = paragraph.toLocaleLowerCase("id-ID").replace(/\s+/g, " ").trim();
    if (!normalized) continue;
    const shortClosing = /^(demikian\.|terima kasih\.)$/.test(normalized);
    if (seen.has(normalized) && (normalized.length >= 50 || shortClosing)) continue;
    seen.add(normalized);
    result.push(paragraph.trim());
  }
  return result.join("\n\n");
}

function makePrompt(topic) {
  const instructions = [
    "Anda membantu ASN pemerintah daerah menyusun draf awal naskah dinas dalam Bahasa Indonesia formal dan jelas.",
    "Berdasarkan topik pengguna, tentukan sendiri bentuk naskah yang paling sesuai. Pilih satu: surat dinas, nota dinas, surat undangan, surat tugas, atau telaahan staf. Jika topik meminta telaahan kepada pimpinan, gunakan struktur telaahan staf: Persoalan, Praanggapan, Fakta-fakta yang Mempengaruhi, Analisis, Kesimpulan, Saran.",
    "Susun draf yang ringkas, formal, jelas, dan siap disunting. Gunakan fakta dari topik saja. Jangan mengarang nama, jabatan, instansi, tanggal, nomor, lokasi, jumlah, kewenangan, dasar hukum, pasal, atau keputusan. Data yang tidak disebut tulis sebagai [LENGKAPI: ...]. Dasar hukum yang belum diberikan tulis [PERIKSA DASAR HUKUM YANG BERLAKU]. Jangan menulis seolah-olah naskah sudah ditandatangani atau disahkan.",
    "Untuk SURAT TUGAS gunakan urutan: judul SURAT TUGAS; Nomor; Dasar; frasa MEMERINTAHKAN; Kepada; Untuk; waktu dan tempat; kalimat penutup satu kali; blok penandatangan. Buat 1–3 butir tugas yang spesifik terhadap topik, tanpa mengulang kalimat penutup.",
    "Untuk SURAT UNDANGAN gunakan: nomor, sifat/lampiran bila relevan, hal, penerima, satu paragraf maksud, waktu/tempat/agenda, penutup satu kali, blok penandatangan. Untuk NOTA DINAS atau TELAAHAN STAF gunakan heading yang sesuai dan isi yang ringkas. Pilih hanya format yang paling cocok.",
    "Akhiri seluruh keluaran setelah satu blok penandatangan dan satu baris CATATAN PEMERIKSAAN. Jangan mengulang salam, paragraf, kalimat terima kasih, kata Demikian, atau blok penandatangan. Maksimal 350 kata. Keluarkan draf saja, tanpa pengantar atau komentar lain.",
    "Topik pengguna:",
    topic,
  ];
  return instructions.join("\n\n");
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
  if (!env.AI || typeof env.AI.run !== "function") {
    return reply({ error: "Layanan AI belum siap. Silakan coba lagi nanti." }, 503);
  }

  try {
    const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fp8-fast", {
      prompt: makePrompt(topic),
      max_tokens: 900,
      temperature: 0.15,
      top_p: 0.85,
      repetition_penalty: 1.15,
      frequency_penalty: 0.25,
    });
    const draft = removeRepeatedParagraphs(cleanText(result?.response || result?.output_text || ""));
    if (!draft) return reply({ error: "AI belum menghasilkan draft. Coba jelaskan topik dengan lebih spesifik." }, 502);
    return reply({
      draft: draft.slice(0, MAX_DRAFT_CHARS),
      document_type: draft.split(/\r?\n/).find((line) => line.trim())?.slice(0, 90) || "Draft selesai",
    });
  } catch {
    return reply({ error: "AI sedang sibuk atau gagal menyusun draft. Silakan coba lagi." }, 502);
  }
}