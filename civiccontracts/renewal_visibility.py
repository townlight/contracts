"""Renewal visibility helpers for Townlight Contracts v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenewalSummary:
    contract_id: str
    renewal_status: str
    visibility_items: tuple[str, ...]
    staff_review_required: bool


def summarize_renewal_visibility(
    *, contract_id: str, renewal_terms: str, department_notes: str = ""
) -> RenewalSummary:
    """Summarize renewal visibility without approving a renewal."""

    terms = renewal_terms.casefold()
    status = "needs-staff-review"
    if "no renewal" in terms:
        status = "no-renewal-language-detected"
    elif "automatic" in terms:
        status = "automatic-renewal-review-required"
    items = [
        "Confirm renewal authority and notice deadline.",
        "Confirm budget availability and department performance notes.",
        "Confirm public-records and source-file links.",
    ]
    if department_notes.strip():
        items.append("Department notes supplied; preserve them with the renewal review packet.")
    return RenewalSummary(
        contract_id=contract_id.strip() or "unassigned-contract",
        renewal_status=status,
        visibility_items=tuple(items),
        staff_review_required=True,
    )
