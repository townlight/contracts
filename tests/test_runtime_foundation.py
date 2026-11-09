from fastapi.testclient import TestClient

import townlight_contracts
from townlight_contracts.main import app


client = TestClient(app)


def test_package_version() -> None:
    assert townlight_contracts.__version__ == "0.2.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "Townlight Contracts"
    assert payload["version"] == "0.2.0"
    assert payload["status"] == "contract repository foundation plus registry persistence"
    assert "database-backed contract registry and renewal visibility records" in payload["message"]
    assert "official legal interpretation" in payload["message"]
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"].startswith("Post-v0.2.0 roadmap")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "townlight_contracts"
    assert payload["version"] == "0.2.0"
    assert payload["townlight_core_version"] == "1.3.0.dev2"
