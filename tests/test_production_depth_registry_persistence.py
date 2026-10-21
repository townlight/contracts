from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civiccontracts.main import app, _dispose_registry_repository
from civiccontracts.persistence import ContractRegistryRepository


client = TestClient(app)


def test_repository_persists_contract_and_renewal_summary(tmp_path: Path) -> None:
    db_path = tmp_path / "civiccontracts.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = ContractRegistryRepository(db_url=db_url)
    contract = repository.register_contract(
        contract_id="ct-2026-001",
        vendor_name="Acme Software",
        contract_type="software subscription",
    )
    renewal = repository.create_renewal_summary(
        contract_id="ct-2026-001",
        renewal_terms="Automatic one-year renewal unless notice is given.",
        department_notes="Vendor performance acceptable.",
    )
    repository.engine.dispose()

    reloaded = ContractRegistryRepository(db_url=db_url)
    stored_contract = reloaded.get_contract(contract.contract_id)
    stored_renewal = reloaded.get_renewal_summary(renewal.contract_id)
    reloaded.engine.dispose()

    assert stored_contract is not None
    assert stored_contract.vendor_name == "Acme Software"
    assert stored_renewal is not None
    assert stored_renewal.renewal_status == "automatic-renewal-review-required"
    assert stored_renewal.staff_review_required is True
    db_path.unlink()


def test_registry_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccontracts-api.db"
    monkeypatch.setenv("CIVICCONTRACTS_REGISTRY_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_registry_repository()

    created_contract = client.post(
        "/api/v1/civiccontracts/registry",
        json={
            "contract_id": "ct-2026-001",
            "vendor_name": "Acme Software",
            "contract_type": "software subscription",
        },
    )
    fetched_contract = client.get("/api/v1/civiccontracts/registry/ct-2026-001")
    created_renewal = client.post(
        "/api/v1/civiccontracts/renewals/summary",
        json={
            "contract_id": "ct-2026-001",
            "renewal_terms": "Automatic one-year renewal unless notice is given.",
            "department_notes": "Vendor performance acceptable.",
        },
    )
    fetched_renewal = client.get("/api/v1/civiccontracts/renewals/ct-2026-001")

    _dispose_registry_repository()
    monkeypatch.delenv("CIVICCONTRACTS_REGISTRY_DB_URL")

    assert created_contract.status_code == 200
    assert fetched_contract.status_code == 200
    assert fetched_contract.json()["vendor_name"] == "Acme Software"
    assert created_renewal.status_code == 200
    assert fetched_renewal.status_code == 200
    assert fetched_renewal.json()["renewal_status"] == "automatic-renewal-review-required"
    db_path.unlink()


def test_get_contract_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICCONTRACTS_REGISTRY_DB_URL", raising=False)
    _dispose_registry_repository()

    response = client.get("/api/v1/civiccontracts/registry/ct-2026-001")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "Townlight Contracts registry persistence is not configured."
    assert "Set CIVICCONTRACTS_REGISTRY_DB_URL" in detail["fix"]


def test_get_renewal_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccontracts-missing.db"
    monkeypatch.setenv("CIVICCONTRACTS_REGISTRY_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_registry_repository()

    response = client.get("/api/v1/civiccontracts/renewals/missing")

    _dispose_registry_repository()
    monkeypatch.delenv("CIVICCONTRACTS_REGISTRY_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Renewal visibility record not found."
    assert "POST /api/v1/civiccontracts/renewals/summary" in detail["fix"]
    db_path.unlink()
