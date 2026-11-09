<a id="townlight_contracts-user-manual"></a>

# Townlight Contracts User Manual

## For Non-Technical Users

Townlight Contracts helps city staff keep contract records, clause topics, expiration dates, renewal notes, public-records review notes, and export manifests organized. It can create a sample contract registry stub, flag clause topics, build expiration reminders, summarize renewal visibility, and assemble a public-records export checklist.

## In the Windows suite

Register executed agreements, store their signed PDFs, and track staff-entered renewal deadlines. Install the [signed Townlight Windows beta 1.8.0.1](https://github.com/townlight/townlight/releases/tag/townlight-windows-v1.8.0.1) and select the full profile. See the [staff operating guide](https://townlight.github.io/manuals/windows-staff-workflows.html#contracts). The package examples below describe the standalone development interface.

Current state: `0.2.0` contract repository foundation plus registry persistence release. Townlight Contracts can optionally save contract registry and renewal visibility records when IT configures `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL`. Townlight Contracts does not provide official legal interpretation, legal advice, live contract management platforms, live LLM calls, contract execution workflows, renewal approvals, or contract system-of-record updates. Staff own every decision.

## For IT and Technical Staff

Townlight Contracts is a FastAPI Python package pinned to `townlight-core==1.3.0.dev2`. The current runtime exposes:

- `GET /`
- `GET /health`
- `GET /townlight_contracts`
- `POST /api/v1/townlight_contracts/registry`
- `GET /api/v1/townlight_contracts/registry/{contract_id}`
- `POST /api/v1/townlight_contracts/clauses/lookup`
- `POST /api/v1/townlight_contracts/expirations`
- `POST /api/v1/townlight_contracts/renewals/summary`
- `GET /api/v1/townlight_contracts/renewals/{contract_id}`
- `POST /api/v1/townlight_contracts/export`

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

Set `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL` to enable local SQLAlchemy-backed contract registry and renewal visibility records. If the variable is not set, Townlight Contracts keeps deterministic stateless behavior and retrieval endpoints return actionable configuration guidance.

## Architecture

```mermaid
flowchart LR
  Staff["Clerk / legal / finance / department managers"] --> Townlight Contracts["Townlight Contracts"]
  Townlight Contracts --> CivicCore["Townlight Core 1.3.0.dev2"]
  Townlight Contracts -. future file links .-> CivicRecords["CivicRecords AI v1.4.0"]
  Townlight Contracts --> Export["Public-records export checklist"]
```

Townlight Contracts depends on Townlight Core. Townlight Core does not depend on Townlight Contracts. Townlight Contracts v0.2.0 uses deterministic sample contract data plus optional local registry persistence; live contract management platforms, Townlight Records file links, staff review queues, and production contract-system integrations are future work.

## Upgrading standalone PostgreSQL data

Stop the old service and back up its PostgreSQL database. In the same database,
verify that the old schema exists and the new schema does not. As the schema
owner, run the following in a transaction, then start the upgraded service
and check that existing records are present. The operation keeps the tables
and data in the same database. SQLite files require no schema rename.

```sql
BEGIN;
ALTER SCHEMA civiccontracts RENAME TO townlight_contracts;
COMMIT;
```
