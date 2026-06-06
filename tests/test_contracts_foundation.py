from datetime import date

from fastapi.testclient import TestClient

from civiccontracts.clause_lookup import lookup_clause_topics
from civiccontracts.contract_registry import register_contract_stub
from civiccontracts.expiration_tracker import build_expiration_plan
from civiccontracts.main import app
from civiccontracts.records_export import build_contract_records_export
from civiccontracts.renewal_visibility import summarize_renewal_visibility


client = TestClient(app)


def test_contract_registry_flags_owner_and_boundary() -> None:
    result = register_contract_stub(
        contract_id="ct-2026-001",
        vendor_name="Acme Software",
        contract_type="software subscription",
    )
    assert result.vendor_name == "Acme Software"
    assert any("data-processing" in note for note in result.registry_notes)
    assert "does not interpret legal obligations" in result.disclaimer


def test_clause_lookup_flags_public_records_language() -> None:
    result = lookup_clause_topics(
        query="public records",
        contract_text="Confidential pricing and indemnification language appears here.",
    )
    assert "Indemnification" in result.matched_topics
    assert "Confidentiality / public records" in result.matched_topics
    assert result.staff_review_required is True


def test_expiration_plan_builds_review_reminders() -> None:
    result = build_expiration_plan(
        contract_id="ct-2026-001",
        expiration_date=date(2026, 12, 31),
    )
    assert result.contract_id == "ct-2026-001"
    assert len(result.reminders) == 4
    assert "verify dates" in result.staff_note


def test_renewal_visibility_flags_automatic_renewal() -> None:
    result = summarize_renewal_visibility(
        contract_id="ct-2026-001",
        renewal_terms="Automatic one-year renewal unless notice is given.",
        department_notes="Vendor performance acceptable.",
    )
    assert result.renewal_status == "automatic-renewal-review-required"
    assert result.staff_review_required is True
    assert any("Department notes supplied" in item for item in result.visibility_items)


def test_records_export_preserves_contract_context() -> None:
    result = build_contract_records_export(title="Software agreement", contract_id="ct-2026-001")
    assert result.contract_id == "ct-2026-001"
    assert "Preserve executed agreement" in result.checklist[0]
    assert "retention schedule" in result.retention_note


def test_contract_support_apis_success_shape() -> None:
    registry = client.post(
        "/api/v1/civiccontracts/registry",
        json={
            "contract_id": "ct-2026-001",
            "vendor_name": "Acme Software",
            "contract_type": "software subscription",
        },
    )
    clauses = client.post(
        "/api/v1/civiccontracts/clauses/lookup",
        json={
            "query": "public records",
            "contract_text": "Confidential pricing and indemnification language appears here.",
        },
    )
    expirations = client.post(
        "/api/v1/civiccontracts/expirations",
        json={"contract_id": "ct-2026-001", "expiration_date": "2026-12-31"},
    )
    renewals = client.post(
        "/api/v1/civiccontracts/renewals/summary",
        json={
            "contract_id": "ct-2026-001",
            "renewal_terms": "Automatic one-year renewal unless notice is given.",
            "department_notes": "Vendor performance acceptable.",
        },
    )
    export = client.post(
        "/api/v1/civiccontracts/export",
        json={"title": "Software agreement", "contract_id": "ct-2026-001"},
    )
    assert registry.status_code == 200
    assert registry.json()["vendor_name"] == "Acme Software"
    assert clauses.status_code == 200
    assert "Indemnification" in clauses.json()["matched_topics"]
    assert expirations.status_code == 200
    assert len(expirations.json()["reminders"]) == 4
    assert renewals.status_code == 200
    assert renewals.json()["renewal_status"] == "automatic-renewal-review-required"
    assert export.status_code == 200
    assert export.json()["contract_id"] == "ct-2026-001"


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civiccontracts")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "v0.1.1 contract repository foundation" in text
    assert "does not interpret legal obligations" in text
    assert "contract system of record" in text


def test_staff_ui_route_is_accessible_and_uses_safe_dom_updates() -> None:
    response = client.get("/civiccontracts/staff")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<main id="main" tabindex="-1">' in text
    assert "Contract draft review" in text
    assert "/api/v1/civiccontracts/drafts/from-procurement" in text
    assert "/api/v1/civiccontracts/staff/reviews" in text
    assert "textContent" in text
    assert "innerHTML" not in text
