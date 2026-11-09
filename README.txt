Townlight Contracts
============

Townlight Contracts is the Townlight module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

Current state: v0.2.0 contract repository foundation plus registry persistence release. It ships deterministic sample helpers, optional database-backed contract registry and renewal visibility records, and an accessible public sample UI at /townlight_contracts, aligned to townlight-core==1.3.0.dev2.

Not shipped: live contract management platforms, official legal interpretation, legal advice, live LLM calls, contract execution workflows, or contract system-of-record integrations.

API surface:
- GET /
- GET /health
- GET /townlight_contracts
- POST /api/v1/townlight_contracts/registry
- GET /api/v1/townlight_contracts/registry/{contract_id}
- POST /api/v1/townlight_contracts/clauses/lookup
- POST /api/v1/townlight_contracts/expirations
- POST /api/v1/townlight_contracts/renewals/summary
- GET /api/v1/townlight_contracts/renewals/{contract_id}
- POST /api/v1/townlight_contracts/export

Optional persistence: set TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL to enable SQLAlchemy-backed contract registry and renewal visibility records. Without it, Townlight Contracts remains deterministic and stateless.

License: code AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments (see LICENSE and LICENSE-EXCEPTION.md); documentation CC BY 4.0.
