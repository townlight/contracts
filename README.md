<a id="townlight_contracts"></a>

# Townlight Contracts

Townlight Contracts is the Townlight module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

## In the Windows suite

Register executed agreements, store their signed PDFs, and track staff-entered renewal deadlines. Install the [signed Townlight Windows beta 1.8.0.1](https://github.com/townlight/townlight/releases/tag/townlight-windows-v1.8.0.1) and select the full profile. See the [staff operating guide](https://townlight.github.io/manuals/windows-staff-workflows.html#contracts). The package examples below describe the standalone development interface.

Current state: **v0.2.0 contract repository foundation plus registry persistence release**. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample contract registry, clause topic lookup, expiration tracking helper, renewal visibility helper, optional database-backed contract registry and renewal visibility records, public-records export checklist, and accessible public sample UI at `/townlight_contracts`, aligned to `townlight-core==1.3.0.dev2`. It does **not** ship live contract management platforms, official legal interpretation, legal advice, live LLM calls, contract execution workflows, or contract system-of-record integrations.

<a id="what-townlight_contracts-does"></a>

## What Townlight Contracts Does

- Create sample contract registry stubs and review notes.
- Persist contract registry and renewal visibility records when `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL` is configured.
- Flag common clause topics for staff/legal review.
- Build expiration reminder plans.
- Summarize renewal visibility without approving renewals.
- Produce public-records-aware export checklists.
- Demonstrate a public contract-support UI at `/townlight_contracts`.

<a id="what-townlight_contracts-does-not-do"></a>

## What Townlight Contracts Does Not Do

- It does not interpret legal obligations.
- It does not approve renewals or execute contracts.
- It does not provide legal advice.
- It does not call live LLMs in v0.2.0.
- It does not replace a contract system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and Townlight Core versions.
- `GET /townlight_contracts` returns the accessible public sample UI.
- `POST /api/v1/townlight_contracts/registry` returns a sample contract registry stub.
- `GET /api/v1/townlight_contracts/registry/{contract_id}` retrieves a persisted contract registry record when `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL` is configured.
- `POST /api/v1/townlight_contracts/clauses/lookup` returns clause topic flags.
- `POST /api/v1/townlight_contracts/expirations` returns expiration reminders.
- `POST /api/v1/townlight_contracts/renewals/summary` returns renewal visibility items.
- `GET /api/v1/townlight_contracts/renewals/{contract_id}` retrieves a persisted renewal visibility record when `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL` is configured.
- `POST /api/v1/townlight_contracts/export` returns a public-records export checklist.

## Optional Persistence

Set `TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL` to enable local SQLAlchemy-backed contract registry and renewal visibility records.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. See [LICENSE](LICENSE) and [LICENSE-EXCEPTION.md](LICENSE-EXCEPTION.md).
Documentation is CC BY 4.0.
