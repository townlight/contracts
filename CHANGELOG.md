# Changelog

## 0.2.0

- Renamed the distribution to `townlight-contracts` and the import package to `townlight_contracts`.
- Aligned with the Townlight Core version used by the Windows suite.


All notable changes to CivicContracts will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed contract registry and renewal visibility records via `CIVICCONTRACTS_REGISTRY_DB_URL`.
- Contract registry and renewal visibility retrieval endpoints for persisted records.

### Changed

- Aligned CivicContracts to `civiccore==0.3.0`.
- Updated current-facing docs, release gate, CI wheel install, health/version tests, and browser QA evidence for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- FastAPI package/runtime foundation pinned to `civiccore==0.2.0`.
- contract registry helper using deterministic sample data.
- clause lookup helper with staff-verification boundary.
- expiration tracking helper with review-required boundary.
- renewal visibility helper.
- Public-records export checklist for contract records.
- Accessible public sample UI at `/civiccontracts` with browser QA coverage.
- Release gate: tests, docs, placeholder import guard, Ruff, and build artifact checks.

### Not Shipped

- live contract management platforms, official legal interpretation decisions, legal advice, live LLM calls, contract execution workflows, and contract system-of-record integrations.
