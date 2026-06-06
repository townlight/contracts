"""FastAPI runtime foundation for CivicContracts."""

import os
from datetime import date
from pathlib import Path

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import staff_key_gate
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from civiccontracts import __version__
from civiccontracts.clause_lookup import lookup_clause_topics
from civiccontracts.contract_registry import register_contract_stub
from civiccontracts.expiration_tracker import build_expiration_plan
from civiccontracts.persistence import (
    ContractRegistryRepository,
    StaffReviewQueueItem,
    StoredContractDraft,
    StoredRenewalSummary,
)
from civiccontracts.public_ui import render_public_lookup_page, render_staff_page
from civiccontracts.records_export import build_contract_records_export
from civiccontracts.renewal_visibility import summarize_renewal_visibility


app = FastAPI(
    title="CivicContracts",
    version=__version__,
    description="Contract repository, clause lookup, expiration tracking, renewal visibility, and public-records-aware export support for CivicSuite.",
)

_registry_repository: ContractRegistryRepository | None = None
_registry_db_url: str | None = None
_require_staff_key = staff_key_gate("CIVICCONTRACTS_STAFF_API_KEY", "X-CivicContracts-Staff-Key")


class ContractRegistryRequest(BaseModel):
    contract_id: str = Field(..., min_length=1, max_length=160)
    vendor_name: str = Field(..., min_length=1, max_length=500)
    contract_type: str = Field(..., min_length=1, max_length=255)


class ClauseLookupRequest(BaseModel):
    query: str
    contract_text: str


class ExpirationRequest(BaseModel):
    contract_id: str
    expiration_date: date


class RenewalRequest(BaseModel):
    contract_id: str
    renewal_terms: str
    department_notes: str = ""


class RecordsExportRequest(BaseModel):
    contract_id: str
    title: str
    format: str = "markdown"


class ContractDraftRequest(BaseModel):
    contract_id: str = Field(..., min_length=1, max_length=160)
    vendor_name: str = Field(..., min_length=1, max_length=500)
    contract_type: str = Field(..., min_length=1, max_length=255)
    procurement_packet_id: str = Field(default="", max_length=255)
    award_packet_id: str = Field(default="", max_length=255)
    source_module: str = Field(default="civicprocure", max_length=160)
    source_title: str = Field(default="", max_length=500)
    terms_summary: str = Field(default="", max_length=8000)


class StaffReviewCreateRequest(BaseModel):
    draft_id: str = Field(..., min_length=1, max_length=160)
    contract_id: str = Field(..., min_length=1, max_length=160)
    title: str = Field(..., min_length=1, max_length=500)
    reason: str = Field(..., min_length=1, max_length=1000)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicContracts",
        "version": __version__,
        "status": "contract repository foundation plus registry persistence",
        "message": (
            "CivicContracts package, API foundation, sample contract registry, clause lookup, "
            "expiration tracking helper, renewal visibility helper, optional database-backed contract "
            "registry and renewal visibility records, local-first contract draft records, staff review "
            "queues, CivicProcure award handoff support, integration contracts, public-records export "
            "checklist, and public/staff UI foundations are online; live contract management platforms, official legal interpretation, "
            "legal advice, live LLM calls, contract execution workflows, and contract system-of-record "
            "integrations are not implemented yet."
        ),
        "next_step": "Open /civiccontracts/staff for contract draft intake and staff review queues.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civiccontracts",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/ready")
def ready() -> dict[str, object]:
    return _readiness_payload()


@app.get("/api/v1/civiccontracts/readiness")
def readiness() -> dict[str, object]:
    return _readiness_payload()


@app.get("/civiccontracts", response_class=HTMLResponse)
def public_civiccontracts_page() -> str:
    """Return the public sample contract repository support UI."""

    return render_public_lookup_page()


@app.get("/civiccontracts/staff", response_class=HTMLResponse)
def staff_civiccontracts_page() -> str:
    """Return the staff contract drafting and review queue UI."""

    return render_staff_page()


@app.get("/api/v1/civiccontracts/integration-contracts")
def integration_contracts() -> dict[str, object]:
    """Return suite-visible integration contracts for installer and downstream checks."""

    return {
        "module": "civiccontracts",
        "version": __version__,
        "contracts": [
            {
                "name": "civiccontracts.contract_draft.v1",
                "endpoint": "/api/v1/civiccontracts/drafts/from-procurement",
                "method": "POST",
                "boundary": "Creates staff-review contract drafts; it does not execute contracts or provide legal advice.",
            },
            {
                "name": "civiccontracts.staff_review_queue.v1",
                "endpoint": "/api/v1/civiccontracts/staff/reviews",
                "method": "GET",
                "requires_staff_key": True,
                "boundary": "Staff-only queue for draft review before signature, agenda action, or publication.",
            },
            {
                "name": "civiccontracts.procurement_handoff.v1",
                "endpoint": "/api/v1/civiccontracts/drafts/from-procurement",
                "method": "POST",
                "source_module": "civicprocure",
                "boundary": "Consumes CivicProcure award/RFP identifiers without making award or legal decisions.",
            },
            {
                "name": "civiccontracts.records_export.v1",
                "endpoint": "/api/v1/civiccontracts/export",
                "method": "POST",
                "boundary": "Builds records export checklists; it does not publish or redact records.",
            },
        ],
        "downstream_ready_for": [
            "civicprocure award packet contract routing",
            "civicclerk agenda contract approvals",
            "civicrecords-ai contract file retention",
            "civiclegal counsel review queue",
        ],
    }


@app.post("/api/v1/civiccontracts/registry")
def contract_registry(request: ContractRegistryRequest) -> dict[str, object]:
    result = _register_contract(
        contract_id=request.contract_id,
        vendor_name=request.vendor_name,
        contract_type=request.contract_type,
    )
    return result.__dict__


@app.get("/api/v1/civiccontracts/registry/{contract_id}")
def get_contract_registry(contract_id: str) -> dict[str, object]:
    stored = _get_registry_repository().get_contract(contract_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Contract registry record not found.",
                "fix": "Use a contract_id returned by POST /api/v1/civiccontracts/registry.",
            },
        )
    return stored.__dict__


@app.post("/api/v1/civiccontracts/drafts/from-procurement")
def draft_from_procurement(request: ContractDraftRequest) -> dict[str, object]:
    stored = _get_registry_repository().create_contract_draft(
        contract_id=request.contract_id,
        vendor_name=request.vendor_name,
        contract_type=request.contract_type,
        procurement_packet_id=request.procurement_packet_id,
        award_packet_id=request.award_packet_id,
        source_module=request.source_module,
        source_title=request.source_title,
        terms_summary=request.terms_summary,
    )
    review = _get_registry_repository().create_staff_review_queue_item(
        draft_id=stored.draft_id,
        contract_id=stored.contract_id,
        title=stored.source_title,
        reason="Contract draft requires staff/legal review before signature, agenda routing, or publication.",
        created_by="staff",
    )
    return _stored_contract_draft_response(stored, staff_review=review)


@app.get("/api/v1/civiccontracts/drafts/{draft_id}")
def get_contract_draft(draft_id: str) -> dict[str, object]:
    stored = _get_registry_repository().get_contract_draft(draft_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Contract draft record not found.",
                "fix": "Use a draft_id returned by POST /api/v1/civiccontracts/drafts/from-procurement.",
            },
        )
    return _stored_contract_draft_response(stored)


@app.post("/api/v1/civiccontracts/clauses/lookup")
def clause_lookup(request: ClauseLookupRequest) -> dict[str, object]:
    return lookup_clause_topics(
        query=request.query,
        contract_text=request.contract_text,
    ).__dict__


@app.post("/api/v1/civiccontracts/expirations")
def expiration_plan(request: ExpirationRequest) -> dict[str, object]:
    return build_expiration_plan(
        contract_id=request.contract_id,
        expiration_date=request.expiration_date,
    ).__dict__


@app.post("/api/v1/civiccontracts/renewals/summary")
def renewal_summary(request: RenewalRequest) -> dict[str, object]:
    if _registry_database_url() is not None:
        stored = _get_registry_repository().create_renewal_summary(
            contract_id=request.contract_id,
            renewal_terms=request.renewal_terms,
            department_notes=request.department_notes,
        )
        return _stored_renewal_response(stored)

    result = summarize_renewal_visibility(
        contract_id=request.contract_id,
        renewal_terms=request.renewal_terms,
        department_notes=request.department_notes,
    )
    return result.__dict__


@app.get("/api/v1/civiccontracts/renewals/{contract_id}")
def get_renewal_summary(contract_id: str) -> dict[str, object]:
    stored = _get_registry_repository().get_renewal_summary(contract_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Renewal visibility record not found.",
                "fix": "Use a contract_id returned by POST /api/v1/civiccontracts/renewals/summary.",
            },
        )
    return _stored_renewal_response(stored)


@app.post("/api/v1/civiccontracts/export")
def records_export(request: RecordsExportRequest) -> dict[str, object]:
    return build_contract_records_export(
        contract_id=request.contract_id,
        title=request.title,
        format=request.format,
    ).__dict__


@app.post("/api/v1/civiccontracts/staff/reviews")
def create_staff_review(
    request: StaffReviewCreateRequest,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    item = _get_registry_repository().create_staff_review_queue_item(
        draft_id=request.draft_id,
        contract_id=request.contract_id,
        title=request.title,
        reason=request.reason,
        created_by="staff",
    )
    return _staff_review_payload(item)


@app.get("/api/v1/civiccontracts/staff/reviews")
def list_staff_reviews(
    status: str | None = None,
    _staff_principal: object = Depends(_require_staff_key),
) -> dict[str, object]:
    return {
        "visibility": "staff_only",
        "items": [
            _staff_review_payload(item)
            for item in _get_registry_repository().list_staff_review_queue_items(status=status)
        ],
    }


def _registry_database_url() -> str:
    configured = os.environ.get("CIVICCONTRACTS_REGISTRY_DB_URL")
    if configured:
        return configured
    data_dir = Path(os.environ.get("CIVICCONTRACTS_DATA_DIR", Path.cwd() / "data")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite+pysqlite:///{(data_dir / 'civiccontracts-registry.db').as_posix()}"


def _uses_default_registry_database() -> bool:
    return not os.environ.get("CIVICCONTRACTS_REGISTRY_DB_URL")


def _get_registry_repository() -> ContractRegistryRepository:
    global _registry_db_url, _registry_repository
    db_url = _registry_database_url()
    if _registry_repository is None or db_url != _registry_db_url:
        _dispose_registry_repository()
        _registry_db_url = db_url
        _registry_repository = ContractRegistryRepository(db_url=db_url)
    return _registry_repository


def _dispose_registry_repository() -> None:
    global _registry_repository
    if _registry_repository is not None:
        _registry_repository.engine.dispose()
        _registry_repository = None


def _register_contract(*, contract_id: str, vendor_name: str, contract_type: str):
    if _registry_database_url() is None:
        return register_contract_stub(
            contract_id=contract_id,
            vendor_name=vendor_name,
            contract_type=contract_type,
        )
    return _get_registry_repository().register_contract(
        contract_id=contract_id,
        vendor_name=vendor_name,
        contract_type=contract_type,
    )


def _stored_renewal_response(stored: StoredRenewalSummary) -> dict[str, object]:
    return {
        "contract_id": stored.contract_id,
        "renewal_terms": stored.renewal_terms,
        "department_notes": stored.department_notes,
        "renewal_status": stored.renewal_status,
        "visibility_items": list(stored.visibility_items),
        "staff_review_required": stored.staff_review_required,
        "created_at": stored.created_at.isoformat(),
    }


def _stored_contract_draft_response(
    stored: StoredContractDraft, *, staff_review: StaffReviewQueueItem | None = None
) -> dict[str, object]:
    return {
        "draft_id": stored.draft_id,
        "contract_id": stored.contract_id,
        "vendor_name": stored.vendor_name,
        "contract_type": stored.contract_type,
        "procurement_packet_id": stored.procurement_packet_id,
        "award_packet_id": stored.award_packet_id,
        "source_module": stored.source_module,
        "source_title": stored.source_title,
        "terms_summary": stored.terms_summary,
        "review_items": list(stored.review_items),
        "disclaimer": stored.disclaimer,
        "staff_review_id": None if staff_review is None else staff_review.review_id,
        "created_at": stored.created_at.isoformat(),
        "updated_at": stored.updated_at.isoformat(),
        "boundary": (
            "CivicContracts drafts support staff review only; they do not execute contracts, "
            "provide legal advice, approve procurement awards, publish records, or update a contract system of record."
        ),
    }


def _staff_review_payload(item: StaffReviewQueueItem) -> dict[str, object]:
    return {
        "review_id": item.review_id,
        "draft_id": item.draft_id,
        "contract_id": item.contract_id,
        "title": item.title,
        "reason": item.reason,
        "status": item.status,
        "assigned_to": item.assigned_to,
        "resolution": item.resolution,
        "created_by": item.created_by,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "visibility": "staff_only",
        "boundary": (
            "Staff review queues support contract drafting and routing only; they do not execute "
            "contracts, provide legal advice, approve awards, or update a system of record."
        ),
    }


def _readiness_payload() -> dict[str, object]:
    db_url = _registry_database_url()
    repository = _get_registry_repository()
    schema_status = repository.schema_status()
    blockers: list[str] = []
    if not schema_status.ready:
        blockers.append("Initialize the CivicContracts local registry database schema.")
    ready_for_public_use = not blockers
    return {
        "status": "ready" if ready_for_public_use else "not-ready",
        "ready": ready_for_public_use,
        "registry_database_configured": True,
        "registry_database_url": db_url,
        "using_default_local_database": _uses_default_registry_database(),
        "schema_ready": schema_status.ready,
        "schema_version": schema_status.schema_version,
        "expected_schema_version": schema_status.expected_schema_version,
        "blockers": blockers,
    }
