"""Static public UI shell for CivicContracts v0.1.1."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicContracts sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicContracts Contract Repository Support</title>
<style>
  :root { --ink:#18212b; --muted:#56606a; --paper:#f8fbff; --blue:#284f73; --green:#2f654c; --gold:#d7aa45; --line:#c7d4e2; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#f5f9ff,#eef8f0); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.18em; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.5rem,7vw,5.4rem); line-height:.98; letter-spacing:-.05em; }
  .lede { max-width:840px; font-size:clamp(1.1rem,2.4vw,1.45rem); line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:999px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:28px; background:rgba(255,255,255,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:-.03em; }
  h2 { margin:0 0 14px; font-size:clamp(1.8rem,4vw,3rem); }
  p, li { line-height:1.65; }
  textarea, button { width:100%; border:1px solid #b9c6cc; border-radius:16px; padding:.85rem 1rem; font:inherit; }
  textarea { background:#f7f8fb; color:var(--ink); }
  button { width:fit-content; min-width:190px; border:0; background:var(--blue); color:white; font-weight:900; cursor:default; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:18px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header,main,footer{margin:0;max-width:390px;width:100%;padding-left:24px;padding-right:24px}header{padding-top:34px}h1{font-size:clamp(2.2rem,11vw,3rem)}.card{grid-column:span 12;padding:20px;border-radius:22px}button{width:100%} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicContracts public sample</p>
  <h1>Keep contract obligations visible before they become emergencies.</h1>
  <p class="lede">CivicContracts demonstrates contract repository support: registry stubs, clause topic lookup, expiration reminders, renewal visibility, and public-records-aware export checklists without interpreting legal obligations.</p>
  <p><span class="badge">v0.1.1 contract repository foundation</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Sample contract registry</p>
      <h2 id="lookup-title">Software subscription agreement</h2>
      <textarea aria-label="Sample contract notes" rows="4">Agreement includes renewal language, insurance terms, confidentiality language, and data-processing obligations.</textarea>
      <button type="button">Draft sample contract file</button>
      <div class="result" role="status" aria-live="polite">
        <h3>Staff review packet</h3>
        <ul><li>Attach executed agreement, amendments, insurance certificates, and source file links.</li><li>Flag renewal, termination, insurance, indemnification, and public-records topics.</li><li>Create 180/120/90/30-day expiration reminders.</li></ul>
      </div>
    </article>
    <article class="card"><p class="kicker">Clause lookup</p><h2>Topics, not advice</h2><div class="result"><p>CivicContracts can flag common clause topics, but staff and legal counsel interpret the contract.</p></div></article>
    <article class="card"><p class="kicker">Renewals</p><h2>Visibility first</h2><div class="result"><p>Renewal helpers surface authority, notice deadlines, budget context, and department notes for staff review.</p></div></article>
    <article class="card"><p class="kicker">Records export</p><h2>Preserve provenance</h2><div class="result"><p>Exports preserve agreements, amendments, renewal notes, expiration reminders, public-records review notes, and retention classification.</p></div></article>
    <article class="card large"><p class="kicker">Boundary</p><h2>No official legal interpretation</h2><div class="result warning"><p>CivicContracts does not interpret legal obligations, approve renewals, provide legal advice, call live LLMs, execute contracts, or replace the contract system of record.</p></div></article>
  </section>
</main>
<footer><p>CivicContracts is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""


def render_staff_page() -> str:
    """Render the staff-facing CivicContracts draft and review queue page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicContracts Staff Workspace</title>
<style>
  :root { --ink:#18212b; --muted:#5a6470; --paper:#f8fbff; --blue:#284f73; --green:#2f654c; --gold:#d7aa45; --line:#c7d4e2; --warn:#9c4e32; }
  * { box-sizing:border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:#f5f8fb; }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1180px, calc(100% - 32px)); margin:0 auto; }
  header { padding:34px 0 18px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.14em; font-weight:800; font-size:.78rem; }
  h1 { margin:.2rem 0 .6rem; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.1rem,5vw,4.6rem); line-height:1; }
  .lede { max-width:860px; color:#31404a; font-size:1.08rem; line-height:1.55; }
  .grid { display:grid; grid-template-columns:390px minmax(0,1fr); gap:18px; align-items:start; }
  .panel { min-width:0; padding:22px; border:1px solid var(--line); border-radius:8px; background:var(--paper); box-shadow:0 12px 32px rgba(35,43,50,.08); }
  h2 { margin:0 0 14px; font-size:1.35rem; }
  label { display:block; margin:.85rem 0 .35rem; font-weight:800; }
  input, textarea, button { width:100%; border:1px solid #b8c6c0; border-radius:8px; padding:.78rem .9rem; font:inherit; }
  textarea { min-height:110px; resize:vertical; }
  button { margin-top:14px; border:0; background:var(--blue); color:white; font-weight:900; cursor:pointer; }
  button.secondary { background:var(--green); }
  button:disabled { opacity:.65; cursor:wait; }
  .status { margin-top:14px; padding:14px; border-left:5px solid var(--green); background:white; border-radius:8px; line-height:1.55; }
  .warning { border-left-color:var(--warn); background:#fff8f4; }
  .review-list { display:grid; gap:12px; }
  .review { padding:14px; border:1px solid var(--line); border-radius:8px; background:white; }
  .meta { color:var(--muted); font-size:.9rem; }
  footer { padding:32px 0 48px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:820px) { header,main,footer{width:100%;padding-left:20px;padding-right:20px}.grid{grid-template-columns:1fr}.panel{padding:18px} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicContracts staff</p>
  <h1>Contract draft review</h1>
  <p class="lede">Create local contract drafts from procurement packet identifiers, queue staff/legal review, and preserve export context before signature, agenda action, publication, or system-of-record updates.</p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-label="CivicContracts staff workspace">
    <form id="draft-form" class="panel">
      <h2>Create draft from procurement</h2>
      <label for="staff-key">Staff API key</label>
      <input id="staff-key" type="password" autocomplete="off">
      <label for="contract-id">Contract ID</label>
      <input id="contract-id" value="ct-2026-local">
      <label for="vendor-name">Vendor name</label>
      <input id="vendor-name" value="Acme Software">
      <label for="contract-type">Contract type</label>
      <input id="contract-type" value="software subscription">
      <label for="award-packet-id">CivicProcure award packet ID</label>
      <input id="award-packet-id" value="award-2026-local">
      <label for="terms-summary">Terms summary</label>
      <textarea id="terms-summary">One-year software subscription with renewal, data-processing, insurance, and public-records review notes.</textarea>
      <button id="create-button" type="submit">Create contract draft</button>
      <button id="load-button" class="secondary" type="button">Load review queue</button>
      <div id="form-status" class="status" role="status" aria-live="polite">Ready.</div>
    </form>
    <section class="panel" aria-labelledby="queue-title">
      <h2 id="queue-title">Open contract reviews</h2>
      <div id="queue" class="review-list" aria-live="polite"></div>
    </section>
  </section>
</main>
<footer><p>CivicContracts keeps contract draft work local. Staff and counsel remain responsible for contract interpretation, signatures, approvals, publication, and system-of-record updates.</p></footer>
<script>
  const form = document.querySelector("#draft-form");
  const keyInput = document.querySelector("#staff-key");
  const createButton = document.querySelector("#create-button");
  const loadButton = document.querySelector("#load-button");
  const statusBox = document.querySelector("#form-status");
  const queue = document.querySelector("#queue");

  function setStatus(kind, message) {
    statusBox.className = `status ${kind}`;
    statusBox.textContent = message;
  }

  function headers() {
    return {
      "Content-Type": "application/json",
      "X-CivicContracts-Role": "staff",
      "X-CivicContracts-Staff-Key": keyInput.value.trim()
    };
  }

  function field(id) {
    return document.querySelector(id).value.trim();
  }

  function renderQueue(items) {
    queue.replaceChildren();
    if (!items.length) {
      const empty = document.createElement("p");
      empty.textContent = "No contract review items yet.";
      queue.appendChild(empty);
      return;
    }
    for (const item of items) {
      const card = document.createElement("article");
      card.className = "review";
      const title = document.createElement("h3");
      title.textContent = item.title || "Untitled contract review";
      const reason = document.createElement("p");
      reason.textContent = item.reason || "Review required.";
      const meta = document.createElement("p");
      meta.className = "meta";
      meta.textContent = `${item.status || "open"} / ${item.contract_id || "no contract id"} / ${item.review_id || "no review id"}`;
      card.append(title, reason, meta);
      queue.appendChild(card);
    }
  }

  async function loadQueue() {
    setStatus("", "Loading staff queue.");
    const response = await fetch("/api/v1/civiccontracts/staff/reviews", { headers: headers() });
    const payload = await response.json();
    if (!response.ok) {
      const detail = payload.detail || {};
      setStatus("warning", detail.fix || detail.message || "Queue load failed.");
      return;
    }
    renderQueue(Array.isArray(payload.items) ? payload.items : []);
    setStatus("", "Staff queue loaded.");
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    createButton.disabled = true;
    setStatus("", "Creating local contract draft and staff review item.");
    try {
      const response = await fetch("/api/v1/civiccontracts/drafts/from-procurement", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contract_id: field("#contract-id"),
          vendor_name: field("#vendor-name"),
          contract_type: field("#contract-type"),
          award_packet_id: field("#award-packet-id"),
          source_module: "civicprocure",
          source_title: `${field("#vendor-name")} ${field("#contract-type")}`,
          terms_summary: field("#terms-summary")
        })
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        setStatus("warning", detail.fix || detail.message || "Contract draft failed.");
        return;
      }
      setStatus("", `Created contract draft ${payload.draft_id || "pending"} and review ${payload.staff_review_id || "pending"}.`);
      await loadQueue();
    } catch {
      setStatus("warning", "The local CivicContracts API did not respond. Check service logs and retry.");
    } finally {
      createButton.disabled = false;
    }
  });

  loadButton.addEventListener("click", () => {
    loadQueue().catch(() => setStatus("warning", "The local CivicContracts API did not respond."));
  });
</script>
</body>
</html>
"""
