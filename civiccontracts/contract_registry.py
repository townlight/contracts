"""Deterministic contract registry helpers for Townlight Contracts v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "Townlight Contracts provides contract-repository support only. Staff own every decision; "
    "the module does not interpret legal obligations, approve renewals, provide legal advice, "
    "execute contracts, or replace the contract system of record."
)


@dataclass(frozen=True)
class ContractRecord:
    contract_id: str
    vendor_name: str
    contract_type: str
    registry_notes: tuple[str, ...]
    disclaimer: str = DISCLAIMER


def register_contract_stub(
    *, contract_id: str, vendor_name: str, contract_type: str
) -> ContractRecord:
    """Return a deterministic registry stub without storing official records."""

    kind = contract_type.strip().casefold()
    notes = [
        "Attach executed agreement, amendments, insurance certificates, and source file links.",
        "Confirm department owner, renewal authority, and public-records classification.",
    ]
    if "software" in kind or "saas" in kind:
        notes.append("Flag data-processing, security, and termination clauses for staff/legal review.")
    if "construction" in kind or "public works" in kind:
        notes.append("Flag bonding, retainage, and change-order language for staff/legal review.")
    return ContractRecord(
        contract_id=contract_id.strip() or "unassigned-contract",
        vendor_name=vendor_name.strip() or "Unnamed vendor",
        contract_type=contract_type.strip() or "general",
        registry_notes=tuple(notes),
    )
