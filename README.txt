Townlight Contracts
============

Townlight Contracts is the Townlight module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

Current state: v0.1.1 contract repository foundation plus registry persistence release. It ships deterministic sample helpers, optional database-backed contract registry and renewal visibility records, and an accessible public sample UI at /civiccontracts, aligned to civiccore==0.3.0.

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

Optional persistence: set CIVICCONTRACTS_REGISTRY_DB_URL to enable SQLAlchemy-backed contract registry and renewal visibility records. Without it, Townlight Contracts remains deterministic and stateless.

License: code AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments (see LICENSE and LICENSE-EXCEPTION.md); documentation CC BY 4.0.
