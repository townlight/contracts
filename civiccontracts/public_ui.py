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
<footer><p>CivicContracts is part of the AGPL-3.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""
