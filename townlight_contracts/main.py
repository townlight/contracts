"""FastAPI runtime foundation for Townlight Contracts."""

import os
from datetime import date

from townlight_core import __version__ as TOWNLIGHT_CORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from townlight_contracts import __version__
from townlight_contracts.clause_lookup import lookup_clause_topics
from townlight_contracts.contract_registry import register_contract_stub
from townlight_contracts.expiration_tracker import build_expiration_plan
from townlight_contracts.persistence import ContractRegistryRepository, StoredRenewalSummary
from townlight_contracts.public_ui import render_public_lookup_page
from townlight_contracts.records_export import build_contract_records_export
from townlight_contracts.renewal_visibility import summarize_renewal_visibility


app = FastAPI(
    title='Townlight Contracts',
    version=__version__,
    description='Contract repository, clause lookup, expiration tracking, renewal visibility, and public-records-aware export support for Townlight.',
)

_registry_repository: ContractRegistryRepository | None = None
_registry_db_url: str | None = None


class ContractRegistryRequest(BaseModel):
    contract_id: str
    vendor_name: str
    contract_type: str


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


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "Townlight Contracts",
        "version": __version__,
        "status": "contract repository foundation plus registry persistence",
        "message": (
            "Townlight Contracts package, API foundation, sample contract registry, clause lookup, "
            "expiration tracking helper, renewal visibility helper, optional database-backed contract "
            "registry and renewal visibility records, public-records export checklist, and public UI "
            "foundation are online; live contract management platforms, official legal interpretation, "
            "legal advice, live LLM calls, contract execution workflows, and contract system-of-record "
            "integrations are not implemented yet."
        ),
        "next_step": "Post-v0.2.0 roadmap: local contract catalog configuration, Townlight Records file links, and staff review queues",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "townlight_contracts",
        "version": __version__,
        "townlight_core_version": TOWNLIGHT_CORE_VERSION,
    }


@app.get("/townlight_contracts", response_class=HTMLResponse)
def public_townlight_contracts_page() -> str:
    """Return the public sample contract repository support UI."""

    return render_public_lookup_page()


@app.post("/api/v1/townlight_contracts/registry")
def contract_registry(request: ContractRegistryRequest) -> dict[str, object]:
    result = _register_contract(
        contract_id=request.contract_id,
        vendor_name=request.vendor_name,
        contract_type=request.contract_type,
    )
    return result.__dict__


@app.get("/api/v1/townlight_contracts/registry/{contract_id}")
def get_contract_registry(contract_id: str) -> dict[str, object]:
    if _registry_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Contracts registry persistence is not configured.",
                "fix": "Set TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL to retrieve persisted contract registry records.",
            },
        )
    stored = _get_registry_repository().get_contract(contract_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Contract registry record not found.",
                "fix": "Use a contract_id returned by POST /api/v1/townlight_contracts/registry.",
            },
        )
    return stored.__dict__


@app.post("/api/v1/townlight_contracts/clauses/lookup")
def clause_lookup(request: ClauseLookupRequest) -> dict[str, object]:
    return lookup_clause_topics(
        query=request.query,
        contract_text=request.contract_text,
    ).__dict__


@app.post("/api/v1/townlight_contracts/expirations")
def expiration_plan(request: ExpirationRequest) -> dict[str, object]:
    return build_expiration_plan(
        contract_id=request.contract_id,
        expiration_date=request.expiration_date,
    ).__dict__


@app.post("/api/v1/townlight_contracts/renewals/summary")
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


@app.get("/api/v1/townlight_contracts/renewals/{contract_id}")
def get_renewal_summary(contract_id: str) -> dict[str, object]:
    if _registry_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Contracts registry persistence is not configured.",
                "fix": "Set TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL to retrieve persisted renewal visibility records.",
            },
        )
    stored = _get_registry_repository().get_renewal_summary(contract_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Renewal visibility record not found.",
                "fix": "Use a contract_id returned by POST /api/v1/townlight_contracts/renewals/summary.",
            },
        )
    return _stored_renewal_response(stored)


@app.post("/api/v1/townlight_contracts/export")
def records_export(request: RecordsExportRequest) -> dict[str, object]:
    return build_contract_records_export(
        contract_id=request.contract_id,
        title=request.title,
        format=request.format,
    ).__dict__


def _registry_database_url() -> str | None:
    return os.environ.get("TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL")


def _get_registry_repository() -> ContractRegistryRepository:
    global _registry_db_url, _registry_repository
    db_url = _registry_database_url()
    if db_url is None:
        raise RuntimeError("TOWNLIGHT_CONTRACTS_REGISTRY_DB_URL is not configured.")
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
