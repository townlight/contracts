from __future__ import annotations

import pytest

import civiccontracts.main as main_module


@pytest.fixture(autouse=True)
def isolated_civiccontracts_runtime_data(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Keep default local-first runtime data isolated per test."""

    monkeypatch.setenv("CIVICCONTRACTS_DATA_DIR", str(tmp_path / "runtime-data"))
    yield
    main_module._dispose_registry_repository()
    main_module._registry_db_url = None
