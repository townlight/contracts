"""Configure explicit credentials for existing authorized workflow tests."""
import pytest

@pytest.fixture(autouse=True)
def configured_contracts_staff_key(monkeypatch):
    monkeypatch.setenv("TOWNLIGHT_CONTRACTS_STAFF_API_KEY", "test-only-key")
