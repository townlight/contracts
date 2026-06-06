# CivicContracts

CivicContracts is the CivicSuite module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

Current state: **v0.1.1 local-first contract drafting and registry runtime**. This repo ships a FastAPI package, health/readiness endpoints, documentation gates, deterministic sample contract registry, clause topic lookup, expiration tracking helper, renewal visibility helper, default local SQLite-backed contract registry, procurement handoff contract drafts, staff-only review queues, integration contracts, public-records export checklist, an accessible public sample UI at `/civiccontracts`, and a staff workspace at `/civiccontracts/staff`, aligned to the published CivicCore v1.2.0 release wheel. It does **not** ship live contract management platforms, official legal interpretation, legal advice, live LLM calls, contract execution workflows, executed signatures, or contract system-of-record integrations.

## What CivicContracts Does

- Create sample contract registry stubs and review notes.
- Persist contract registry, renewal visibility, contract draft, and staff review queue records in a default local SQLite database.
- Create review-required contract drafts from CivicProcure award/RFP packet identifiers.
- Expose staff-only contract review queues protected by `CIVICCONTRACTS_STAFF_API_KEY`.
- Flag common clause topics for staff/legal review.
- Build expiration reminder plans.
- Summarize renewal visibility without approving renewals.
- Produce public-records-aware export checklists.
- Demonstrate a public contract-support UI at `/civiccontracts`.
- Demonstrate a staff contract draft workspace at `/civiccontracts/staff`.

## What CivicContracts Does Not Do

- It does not interpret legal obligations.
- It does not approve renewals or execute contracts.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.1.
- It does not replace a contract system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and CivicCore versions.
- `GET /ready` and `GET /api/v1/civiccontracts/readiness` return local database/schema readiness.
- `GET /civiccontracts` returns the accessible public sample UI.
- `GET /civiccontracts/staff` returns the staff draft/review workspace.
- `GET /api/v1/civiccontracts/integration-contracts` returns suite integration contracts.
- `POST /api/v1/civiccontracts/registry` returns a sample contract registry stub.
- `GET /api/v1/civiccontracts/registry/{contract_id}` retrieves a persisted contract registry record.
- `POST /api/v1/civiccontracts/drafts/from-procurement` creates a review-required contract draft from CivicProcure context.
- `GET /api/v1/civiccontracts/drafts/{draft_id}` retrieves a persisted contract draft.
- `POST /api/v1/civiccontracts/clauses/lookup` returns clause topic flags.
- `POST /api/v1/civiccontracts/expirations` returns expiration reminders.
- `POST /api/v1/civiccontracts/renewals/summary` returns renewal visibility items.
- `GET /api/v1/civiccontracts/renewals/{contract_id}` retrieves a persisted renewal visibility record.
- `POST /api/v1/civiccontracts/export` returns a public-records export checklist.
- `GET /api/v1/civiccontracts/staff/reviews` lists staff-only review items.

## Local Persistence

CivicContracts uses `CIVICCONTRACTS_DATA_DIR` for its default local SQLite-backed registry database, or `CIVICCONTRACTS_REGISTRY_DB_URL` when IT needs an explicit SQLAlchemy database URL. Staff routes require `CIVICCONTRACTS_STAFF_API_KEY`, `X-CivicContracts-Role: staff`, and `X-CivicContracts-Staff-Key` matching the configured key.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
