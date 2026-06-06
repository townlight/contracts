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


def test_get_contract_uses_default_local_persistence(monkeypatch) -> None:
    monkeypatch.delenv("CIVICCONTRACTS_REGISTRY_DB_URL", raising=False)
    _dispose_registry_repository()

    created = client.post(
        "/api/v1/civiccontracts/registry",
        json={
            "contract_id": "ct-2026-001",
            "vendor_name": "Acme Software",
            "contract_type": "software subscription",
        },
    )
    fetched = client.get("/api/v1/civiccontracts/registry/ct-2026-001")

    assert created.status_code == 200
    assert fetched.status_code == 200
    assert fetched.json()["vendor_name"] == "Acme Software"


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


def test_procurement_handoff_contract_draft_persists_and_queues_review() -> None:
    created = client.post(
        "/api/v1/civiccontracts/drafts/from-procurement",
        json={
            "contract_id": "ct-2026-002",
            "vendor_name": "Apex Construction",
            "contract_type": "public works construction",
            "procurement_packet_id": "rfp-2026-bridge",
            "award_packet_id": "award-2026-bridge",
            "source_module": "civicprocure",
            "source_title": "Bridge repair award",
            "terms_summary": "Construction award with bonding and retainage review.",
        },
    )
    payload = created.json()
    fetched = client.get(f"/api/v1/civiccontracts/drafts/{payload['draft_id']}")

    assert created.status_code == 200
    assert payload["vendor_name"] == "Apex Construction"
    assert payload["source_module"] == "civicprocure"
    assert payload["staff_review_id"].startswith("contract-review-")
    assert any("Route draft" in item for item in payload["review_items"])
    assert fetched.status_code == 200
    assert fetched.json()["award_packet_id"] == "award-2026-bridge"


def test_staff_review_queue_requires_key_and_returns_items(monkeypatch) -> None:
    monkeypatch.setenv("CIVICCONTRACTS_STAFF_API_KEY", "local-contracts-key")
    created = client.post(
        "/api/v1/civiccontracts/drafts/from-procurement",
        json={
            "contract_id": "ct-2026-003",
            "vendor_name": "Acme Software",
            "contract_type": "software subscription",
            "award_packet_id": "award-2026-software",
        },
    )

    denied = client.get("/api/v1/civiccontracts/staff/reviews")
    allowed = client.get(
        "/api/v1/civiccontracts/staff/reviews",
        headers={
            "X-CivicContracts-Role": "staff",
            "X-CivicContracts-Staff-Key": "local-contracts-key",
        },
    )

    assert created.status_code == 200
    assert denied.status_code in {401, 403}
    assert allowed.status_code == 200
    assert allowed.json()["visibility"] == "staff_only"
    assert allowed.json()["items"][0]["contract_id"] == "ct-2026-003"
