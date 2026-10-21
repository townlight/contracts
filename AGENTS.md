<a id="civiccontracts-agent-contract"></a>

# Townlight Contracts Agent Contract

## Source of Truth

- Upstream suite spec: `townlight/townlight/docs/CivicSuiteUnifiedSpec.md`, especially the Townlight Contracts catalog entry and suite-wide non-negotiables.
- Townlight Contracts supports central contract registry stubs, clause topic lookup, expiration tracking, renewal visibility, and public-records-aware export checklists.
- Staff own every decision.

## Hard Boundaries

- Townlight Contracts never interprets legal obligations, approves renewals, executes contracts, provides legal advice, or updates a contract system of record.
- Townlight Contracts v0.1.1 must not call live LLMs or live contract management platforms.
- Clause lookups, renewal visibility, and records exports must be marked staff-review-required where applicable.
- Townlight Contracts depends on Townlight Core; Townlight Core must never depend on Townlight Contracts.
- Townlight Contracts may reference Townlight Procurement and Townlight Records concepts only through released contracts or deterministic sample data in v0.1.1.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
