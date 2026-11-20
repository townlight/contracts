"""Standalone staff APIs must fail closed, independent of Windows session auth."""
import pytest
from fastapi.testclient import TestClient
from townlight_contracts.main import app

client = TestClient(app)
ROUTES = [(next(iter(r.methods)), r.path) for r in app.routes if r.path.startswith('/api/v1/')]

@pytest.mark.parametrize('method,path', ROUTES)
def test_staff_auth_missing_configuration(monkeypatch, method, path):
    monkeypatch.delenv('TOWNLIGHT_CONTRACTS_STAFF_API_KEY', raising=False)
    response = client.request(method, path, json={} if method == 'POST' else None)
    assert response.status_code == 503
    assert response.json()['detail']['message'] == 'Staff API key auth is not configured.'

@pytest.mark.parametrize('method,path', ROUTES)
@pytest.mark.parametrize('headers', [{}, {'X-Townlight-Contracts-Staff-Key':'wrong','X-Townlight-Contracts-Role':'staff'}, {'X-Townlight-Contracts-Staff-Key':'test-only-key','X-Townlight-Contracts-Role':'resident'}])
def test_staff_auth_rejects_untrusted_requests(monkeypatch, method, path, headers):
    monkeypatch.setenv('TOWNLIGHT_CONTRACTS_STAFF_API_KEY', 'test-only-key')
    response = client.request(method, path, headers=headers, json={} if method == 'POST' else None)
    assert response.status_code == 403

def test_staff_auth_does_not_hide_public_health(monkeypatch):
    monkeypatch.delenv('TOWNLIGHT_CONTRACTS_STAFF_API_KEY', raising=False)
    assert client.get('/health').status_code == 200
