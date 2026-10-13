// Értesítés mindig ide megy (Gmail postaláda). Env-vel felülírható.
const TO_EMAIL = (process.env.CONTACT_TO_EMAIL || "fatimegor8@gmail.com").trim();
// Saját domain ellenőrzése után állítsd: CONTACT_FROM_EMAIL=Fatime Beauty Nails <noreply@yourdomain.ch>
const FROM_EMAIL = (
  process.env.CONTACT_FROM_EMAIL || "Fatime Beauty Nails <onboarding@resend.dev>"
).trim();
const SUBJECT = "Fatime Beauty Nails üzenet";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8",
  };
}

function json(statusCode, body) {
  return {
    statusCode,
    headers: corsHeaders(),
    body: JSON.stringify(body),
  };
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function buildOwnerHtml({ name, email, message, lang }) {
  return `
    <div style="font-family:Georgia,serif;line-height:1.6;color:#2b523a">
      <h2 style="margin:0 0 1rem;font-weight:400">Új üzenet a weboldalról</h2>
      <p><strong>Név:</strong> ${escapeHtml(name)}</p>
      <p><strong>E-mail:</strong> ${escapeHtml(email)}</p>
      <p><strong>Nyelv:</strong> ${escapeHtml(lang)}</p>
      <p><strong>Üzenet:</strong></p>
      <p style="white-space:pre-wrap">${escapeHtml(message)}</p>
    </div>
  `;
}

function buildReply({ name, lang }) {
  const safeName = name || (lang === "de" ? "Hallo" : "Szia");
  if (lang === "de") {
    return {
      subject: "Danke für deine Nachricht — Fatime Beauty Nails",
      html: `
        <div style="font-family:Georgia,serif;line-height:1.7;color:#2b523a">
          <p>Hallo ${escapeHtml(safeName)},</p>
          <p>vielen Dank für deine Nachricht an Fatime Beauty Nails.</p>
          <p>Ich habe deine Anfrage erhalten und melde mich so bald wie möglich bei dir.</p>
          <p style="margin-top:1.5rem">Liebe Grüsse<br/>Fatime Beauty Nails</p>
        </div>
      `,
    };
  }
  return {
    subject: "Köszönjük megkeresésed — Fatime Beauty Nails",
    html: `
      <div style="font-family:Georgia,serif;line-height:1.7;color:#2b523a">
        <p>Kedves ${escapeHtml(safeName)}!</p>
        <p>Köszönjük, hogy írtál a Fatime Beauty Nails-nak.</p>
        <p>Üzeneted megérkezett, és amint tudok, felvesszük veled a kapcsolatot.</p>
        <p style="margin-top:1.5rem">Üdvözlettel<br/>Fatime Beauty Nails</p>
      </div>
    `,
  };
}

async function sendResendEmail(payload) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    const err = new Error("Missing RESEND_API_KEY");
    err.code = "CONFIG";
    throw err;
  }

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + apiKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(function () {
    return {};
  });

  if (!response.ok) {
    const err = new Error(data.message || "Resend request failed");
    err.code = "RESEND";
    err.details = data;
    throw err;
  }

  return data;
}

export async function handler(event) {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: corsHeaders(), body: "" };
  }

  if (event.httpMethod !== "POST") {
    return json(405, { ok: false, error: "method_not_allowed" });
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch (e) {
    return json(400, { ok: false, error: "invalid_json" });
  }

  // Honeypot: bots fill this; humans leave it empty
  if (body.website) {
    return json(200, { ok: true });
  }

  const name = String(body.name || "").trim();
  const email = String(body.email || "").trim();
  const message = String(body.message || "").trim();
  const privacy = body.privacy === true || body.privacy === "1" || body.privacy === "on";
  const lang = String(body.lang || "hu").toLowerCase().indexOf("de") === 0 ? "de" : "hu";

  if (!name || !email || !message || !privacy) {
    return json(400, { ok: false, error: "missing_fields" });
  }

  if (!isValidEmail(email)) {
    return json(400, { ok: false, error: "invalid_email" });
  }

  if (name.length > 200 || email.length > 320 || message.length > 5000) {
    return json(400, { ok: false, error: "too_long" });
  }

  try {
    await sendResendEmail({
      from: FROM_EMAIL,
      to: [TO_EMAIL],
      reply_to: email,
      subject: SUBJECT,
      html: buildOwnerHtml({ name, email, message, lang }),
    });
  } catch (err) {
    console.error("contact owner mail error:", err && err.message, err && err.details);
    return json(500, {
      ok: false,
      error: err && err.code === "CONFIG" ? "config" : "send_failed",
    });
  }

  // Auto-reply: ne bukjon el a fő küldés, ha a válaszlevél nem megy ki
  try {
    const reply = buildReply({ name, lang });
    await sendResendEmail({
      from: FROM_EMAIL,
      to: [email],
      subject: reply.subject,
      html: reply.html,
    });
  } catch (err) {
    console.error("contact auto-reply error:", err && err.message, err && err.details);
  }

  return json(200, { ok: true });
}
