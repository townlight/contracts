from fastapi.testclient import TestClient

import civiccontracts
from civiccontracts.main import app


client = TestClient(app)


def test_package_version_is_011() -> None:
    assert civiccontracts.__version__ == "0.1.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicContracts"
    assert payload["version"] == "0.1.1"
    assert payload["status"] == "contract repository foundation plus registry persistence"
    assert "local-first contract draft records" in payload["message"]
    assert "official legal interpretation" in payload["message"]
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"].startswith("Open /civiccontracts/staff")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiccontracts"
    assert payload["version"] == "0.1.1"
    assert payload["civiccore_version"] == "1.2.0"


def test_readiness_is_green_with_default_local_database() -> None:
    response = client.get("/api/v1/civiccontracts/readiness")
    assert response.status_code == 200
    payload = response.json()

    assert payload["ready"] is True
    assert payload["schema_ready"] is True
    assert payload["using_default_local_database"] is True
    assert payload["registry_database_configured"] is True


def test_integration_contracts_advertise_suite_handoffs() -> None:
    response = client.get("/api/v1/civiccontracts/integration-contracts")
    assert response.status_code == 200
    payload = response.json()
    contracts = {contract["name"] for contract in payload["contracts"]}

    assert "civiccontracts.contract_draft.v1" in contracts
    assert "civiccontracts.staff_review_queue.v1" in contracts
    assert "civiccontracts.procurement_handoff.v1" in contracts
    assert "civiccontracts.records_export.v1" in contracts
    assert "civicprocure award packet contract routing" in payload["downstream_ready_for"]
