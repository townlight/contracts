# Changelog

All notable changes to CivicContracts will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Default local SQLite-backed contract registry, renewal visibility, contract draft, and staff review queue persistence via `CIVICCONTRACTS_DATA_DIR`.
- Staff workspace at `/civiccontracts/staff` plus staff-key protected review queue endpoints.
- CivicProcure procurement handoff contract draft endpoint and suite integration-contract metadata.
- CivicCore v1.2.0 release-wheel dependency alignment for staff key gating.

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed contract registry and renewal visibility records via `CIVICCONTRACTS_REGISTRY_DB_URL`.
- Contract registry and renewal visibility retrieval endpoints for persisted records.

### Changed

- Aligned CivicContracts to the published `civiccore v1.2.0` release wheel.
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
