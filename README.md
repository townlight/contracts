<a id="civiccontracts"></a>

# Townlight Contracts

Townlight Contracts is the Townlight module for central contract registry support, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware exports.

Current state: **v0.1.1 contract repository foundation plus registry persistence release**. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic sample contract registry, clause topic lookup, expiration tracking helper, renewal visibility helper, optional database-backed contract registry and renewal visibility records, public-records export checklist, and accessible public sample UI at `/civiccontracts`, aligned to `civiccore==0.3.0`. It does **not** ship live contract management platforms, official legal interpretation, legal advice, live LLM calls, contract execution workflows, or contract system-of-record integrations.

<a id="what-civiccontracts-does"></a>

## What Townlight Contracts Does

- Create sample contract registry stubs and review notes.
- Persist contract registry and renewal visibility records when `CIVICCONTRACTS_REGISTRY_DB_URL` is configured.
- Flag common clause topics for staff/legal review.
- Build expiration reminder plans.
- Summarize renewal visibility without approving renewals.
- Produce public-records-aware export checklists.
- Demonstrate a public contract-support UI at `/civiccontracts`.

<a id="what-civiccontracts-does-not-do"></a>

## What Townlight Contracts Does Not Do

- It does not interpret legal obligations.
- It does not approve renewals or execute contracts.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.1.
- It does not replace a contract system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and Townlight Core versions.
- `GET /civiccontracts` returns the accessible public sample UI.
- `POST /api/v1/civiccontracts/registry` returns a sample contract registry stub.
- `GET /api/v1/civiccontracts/registry/{contract_id}` retrieves a persisted contract registry record when `CIVICCONTRACTS_REGISTRY_DB_URL` is configured.
- `POST /api/v1/civiccontracts/clauses/lookup` returns clause topic flags.
- `POST /api/v1/civiccontracts/expirations` returns expiration reminders.
- `POST /api/v1/civiccontracts/renewals/summary` returns renewal visibility items.
- `GET /api/v1/civiccontracts/renewals/{contract_id}` retrieves a persisted renewal visibility record when `CIVICCONTRACTS_REGISTRY_DB_URL` is configured.
- `POST /api/v1/civiccontracts/export` returns a public-records export checklist.

## Optional Persistence

Set `CIVICCONTRACTS_REGISTRY_DB_URL` to enable local SQLAlchemy-backed contract registry and renewal visibility records.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. See [LICENSE](LICENSE) and [LICENSE-EXCEPTION.md](LICENSE-EXCEPTION.md).
Documentation is CC BY 4.0.
