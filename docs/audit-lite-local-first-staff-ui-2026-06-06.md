# Audit Lite - CivicContracts local-first staff runtime
**Date:** 2026-06-06
**Scope:** CivicContracts default local persistence, procurement handoff contract drafts, staff review queue, staff UI, integration contracts, dependency alignment, docs, and tests.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice to the full module gate. CivicContracts now works as a local-first standalone module: it creates and retrieves contract registry records, renewal summaries, CivicProcure handoff contract drafts, and staff review queue items without requiring an external database. Staff queue routes use the CivicCore staff-key gate, and the module exposes suite integration contracts for installer verification.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

No findings.

## What's working
- `civiccontracts.main` now exposes `/ready`, `/api/v1/civiccontracts/readiness`, `/civiccontracts/staff`, `/api/v1/civiccontracts/integration-contracts`, procurement handoff draft endpoints, and staff review queue endpoints.
- `civiccontracts.persistence` now creates default local SQLite-backed schema for registry, renewal, contract draft, and staff review records through `CIVICCONTRACTS_DATA_DIR`.
- Staff-only queue routes use `CIVICCONTRACTS_STAFF_API_KEY` and `X-CivicContracts-Staff-Key` through CivicCore `staff_key_gate`.
- The placeholder-import guard now permits the real CivicCore v1.2.0 auth dependency while still failing forbidden placeholder imports.
- README, user manual, docs landing page, and changelog now describe the local-first/staff runtime and suite handoff boundaries.
- Behavioral tests passed: `python -m pytest -q`, `bash scripts/verify-release.sh`, and `python -m py_compile civiccontracts/main.py civiccontracts/persistence.py civiccontracts/public_ui.py`.

## Watch items

Full stage gate still needs a browser walkthrough and audit-full over the finished module, then umbrella pinning and clean-machine proof after the active CivicGrants gate clears.

## Escalation recommendation

No escalation needed for this slice. Continue with the full module gate and umbrella installer integration after this commit.
