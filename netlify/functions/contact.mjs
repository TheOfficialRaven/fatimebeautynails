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
  const langLabel = lang === "de" ? "Német" : "Magyar";
  const safeName = escapeHtml(name);
  const safeEmail = escapeHtml(email);
  const safeMessage = escapeHtml(message);

  return `<!DOCTYPE html>
<html lang="hu">
<body style="margin:0;padding:0;background:#faf9f7">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#faf9f7;margin:0;padding:0">
    <tr>
      <td align="center" style="padding:32px 16px">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:560px;background:#ffffff;border-radius:6px;overflow:hidden;border:1px solid rgba(43,82,58,0.12)">
          <tr>
            <td style="background:#51735e;padding:28px 32px;text-align:center">
              <p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-size:22px;line-height:1.3;color:#ffffff;letter-spacing:0.02em">Fatime Beauty Nails</p>
              <p style="margin:10px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:0.14em;text-transform:uppercase;color:#c3b78e">Új üzenet a weboldalról</p>
            </td>
          </tr>
          <tr>
            <td style="height:3px;background:#c3b78e;font-size:0;line-height:0">&nbsp;</td>
          </tr>
          <tr>
            <td style="padding:28px 32px 8px;font-family:Arial,Helvetica,sans-serif;color:#2b523a">
              <p style="margin:0 0 20px;font-size:15px;line-height:1.65;color:rgba(43,82,58,0.78)">Új kapcsolatfelvételi üzenet érkezett a weboldalon keresztül.</p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px">
                <tr>
                  <td style="padding:14px 16px;background:#faf9f7;border-radius:6px;border:1px solid rgba(43,82,58,0.10)">
                    <p style="margin:0 0 10px;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#c3b78e;font-family:Arial,Helvetica,sans-serif">Név</p>
                    <p style="margin:0 0 16px;font-size:16px;line-height:1.4;color:#2b523a;font-family:Georgia,'Times New Roman',serif">${safeName}</p>
                    <p style="margin:0 0 10px;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#c3b78e;font-family:Arial,Helvetica,sans-serif">E-mail</p>
                    <p style="margin:0 0 16px;font-size:15px;line-height:1.4;color:#2b523a;font-family:Arial,Helvetica,sans-serif"><a href="mailto:${safeEmail}" style="color:#2b523a;text-decoration:underline">${safeEmail}</a></p>
                    <p style="margin:0 0 10px;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#c3b78e;font-family:Arial,Helvetica,sans-serif">Nyelv</p>
                    <p style="margin:0;font-size:15px;line-height:1.4;color:#2b523a;font-family:Arial,Helvetica,sans-serif">${langLabel}</p>
                  </td>
                </tr>
              </table>
              <p style="margin:0 0 10px;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#c3b78e;font-family:Arial,Helvetica,sans-serif">Üzenet</p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="padding:16px 18px;background:#faf9f7;border-left:3px solid #c3b78e;border-radius:0 6px 6px 0">
                    <p style="margin:0;font-size:15px;line-height:1.7;color:#2b523a;font-family:Arial,Helvetica,sans-serif;white-space:pre-wrap">${safeMessage}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:24px 32px 28px;font-family:Arial,Helvetica,sans-serif;text-align:center">
              <p style="margin:0;font-size:12px;line-height:1.6;color:rgba(43,82,58,0.55)">Fatime Beauty Nails · Frasnacht (TG)<br />Ez az üzenet a weboldal kapcsolatfelvételi űrlapjáról érkezett.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
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
