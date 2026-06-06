CivicContracts
============

CivicContracts is the CivicSuite module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

Current state: v0.1.1 local-first contract drafting and registry runtime. It ships deterministic sample helpers, default local SQLite-backed contract registry, renewal visibility records, contract drafts, staff review queues, integration contracts, an accessible public sample UI at /civiccontracts, and a staff workspace at /civiccontracts/staff, aligned to the published CivicCore v1.2.0 release wheel.

Not shipped: live contract management platforms, official legal interpretation, legal advice, live LLM calls, contract execution workflows, or contract system-of-record integrations.

API surface:
- GET /
- GET /health
- GET /civiccontracts
- POST /api/v1/civiccontracts/registry
- GET /api/v1/civiccontracts/registry/{contract_id}
- POST /api/v1/civiccontracts/clauses/lookup
- POST /api/v1/civiccontracts/expirations
- POST /api/v1/civiccontracts/renewals/summary
- GET /api/v1/civiccontracts/renewals/{contract_id}
- POST /api/v1/civiccontracts/export

Optional persistence: set CIVICCONTRACTS_REGISTRY_DB_URL to enable SQLAlchemy-backed contract registry and renewal visibility records. Without it, CivicContracts remains deterministic and stateless.

License: code Apache License 2.0; documentation CC BY 4.0.
