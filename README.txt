
## Shared meeting imports · Windows 1.8.1.1

Windows 1.8.1.1 adds shared meeting imports for 31 source families, with 34 supported source/format pairs. Installed Windows Sandbox checks exercised preview, save and durable readback using public captures and fixtures, plus the documented Townlight handoffs. These checks do not establish automatic discovery on every live portal or a complete retest of every module.

[All 31 sources, formats and handoffs](https://townlight.github.io/manuals/meeting-imports.html) · [Installed acceptance](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/ACCEPTANCE-Windows-1.8.1.1.md).

Windows 1.8.1.1 has fresh-install acceptance. An in-place upgrade to 1.8.1.1 was not exercised. The previous Windows 1.8.0.1 release tested upgrade from 1.7.2.1; that result applies to 1.8.0.1. Before an existing-city evaluation, back up city data and settings, close Townlight, keep the existing %LOCALAPPDATA%\CivicSuite profile, and use the same Windows account. Keep the prior installer and a restore path. Station continues to use its separately configured service.

The accepted MSI contains Townlight Runtime 0.3.1 and Meetings 1.0.6 distributions. Its health version strings still report Runtime 0.3.0 and Meetings 1.0.5. Default-branch source corrects those display strings; the signed MSI and its exact build source remain unchanged.

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
