<a id="civiccontracts-user-manual"></a>

# Townlight Contracts User Manual

## For Non-Technical Users

Townlight Contracts helps city staff keep contract records, clause topics, expiration dates, renewal notes, public-records review notes, and export manifests organized. It can create a sample contract registry stub, flag clause topics, build expiration reminders, summarize renewal visibility, and assemble a public-records export checklist.

Current state: `0.1.1` contract repository foundation plus registry persistence release. Townlight Contracts can optionally save contract registry and renewal visibility records when IT configures `CIVICCONTRACTS_REGISTRY_DB_URL`. Townlight Contracts does not provide official legal interpretation, legal advice, live contract management platforms, live LLM calls, contract execution workflows, renewal approvals, or contract system-of-record updates. Staff own every decision.

## For IT and Technical Staff

Townlight Contracts is a FastAPI Python package pinned to `civiccore==0.3.0`. The current runtime exposes:

- `GET /`
- `GET /health`
- `GET /civiccontracts`
- `POST /api/v1/civiccontracts/registry`
- `GET /api/v1/civiccontracts/registry/{contract_id}`
- `POST /api/v1/civiccontracts/clauses/lookup`
- `POST /api/v1/civiccontracts/expirations`
- `POST /api/v1/civiccontracts/renewals/summary`
- `GET /api/v1/civiccontracts/renewals/{contract_id}`
- `POST /api/v1/civiccontracts/export`

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

Set `CIVICCONTRACTS_REGISTRY_DB_URL` to enable local SQLAlchemy-backed contract registry and renewal visibility records. If the variable is not set, Townlight Contracts keeps deterministic stateless behavior and retrieval endpoints return actionable configuration guidance.

## Architecture

```mermaid
flowchart LR
  Staff["Clerk / legal / finance / department managers"] --> CivicContracts["CivicContracts"]
  CivicContracts --> CivicCore["CivicCore v0.3.0"]
  CivicContracts -. future file links .-> CivicRecords["CivicRecords AI v1.4.0"]
  CivicContracts --> Export["Public-records export checklist"]
```

Townlight Contracts depends on Townlight Core. Townlight Core does not depend on Townlight Contracts. Townlight Contracts v0.1.1 uses deterministic sample contract data plus optional local registry persistence; live contract management platforms, Townlight Records file links, staff review queues, and production contract-system integrations are future work.
