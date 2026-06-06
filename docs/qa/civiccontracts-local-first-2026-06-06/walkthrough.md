# CivicContracts Local-First Walkthrough
**Date:** 2026-06-06
**Scope:** Public UI, staff UI, readiness, integration contracts, procurement handoff draft persistence, and staff queue auth boundary.
**Runtime:** `http://127.0.0.1:18174`

## Verdict

Passed. CivicContracts rendered the public and staff workspaces at desktop and mobile widths, reported local-first readiness, exposed the expected suite integration contracts, persisted a CivicProcure handoff contract draft, retrieved that draft by ID, and denied staff queue access when no staff key was configured with actionable operator copy.

## Evidence

- `public-desktop.png` and `public-mobile.png`: public contract support UI rendered without layout failure.
- `staff-desktop.png` and `staff-mobile.png`: staff contract draft workspace rendered without layout failure.
- `staff-keyless-error.png`: staff queue load showed the expected missing-key error path.
- `walkthrough-evidence.json`: API evidence for health, readiness, integration contracts, draft create/fetch, and staff queue denial.

## Runtime Checks

- `GET /health`: passed with CivicContracts `0.1.1` and CivicCore `1.2.0`.
- `GET /api/v1/civiccontracts/readiness`: passed with `ready=true`, `schema_ready=true`, and default local SQLite database under `CIVICCONTRACTS_DATA_DIR`.
- `GET /api/v1/civiccontracts/integration-contracts`: passed with contract draft, staff review queue, procurement handoff, and records export contracts.
- `POST /api/v1/civiccontracts/drafts/from-procurement`: passed and returned `draft_id` plus `staff_review_id`.
- `GET /api/v1/civiccontracts/drafts/{draft_id}`: passed and returned the persisted draft.
- `GET /api/v1/civiccontracts/staff/reviews` without configured staff key: passed as a negative test with actionable `Set CIVICCONTRACTS_STAFF_API_KEY` guidance.

## Findings

No findings.

## Test Gap Notes

The walkthrough intentionally did not configure `CIVICCONTRACTS_STAFF_API_KEY` in shell because the local secret-protection hook blocks explicit staff-key environment assignment. Keyed staff queue success is covered by `tests/test_production_depth_registry_persistence.py::test_staff_review_queue_requires_key_and_returns_items`.
