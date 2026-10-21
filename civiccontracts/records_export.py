"""Public-records-aware export helpers for Townlight Contracts v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractRecordsExport:
    contract_id: str
    title: str
    format: str
    checklist: tuple[str, ...]
    retention_note: str


def build_contract_records_export(
    *, contract_id: str, title: str, format: str = "markdown"
) -> ContractRecordsExport:
    """Build a deterministic export checklist for contract records."""

    return ContractRecordsExport(
        contract_id=contract_id.strip() or "unassigned-contract",
        title=title.strip() or "Untitled contract export",
        format=format,
        checklist=(
            "Preserve executed agreement, amendments, exhibits, and insurance records.",
            "Preserve source file link, renewal notes, expiration reminders, and owner metadata.",
            "Preserve public-records review notes and any redaction/withholding basis supplied by staff.",
            "Preserve retention classification and export manifest.",
        ),
        retention_note="Keep contract records according to municipal retention schedule and contract terms.",
    )
