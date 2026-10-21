"""Expiration tracking helpers for Townlight Contracts v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class ExpirationPlan:
    contract_id: str
    expiration_date: date
    reminders: tuple[str, ...]
    staff_note: str


def build_expiration_plan(*, contract_id: str, expiration_date: date) -> ExpirationPlan:
    """Create deterministic reminder dates for staff review."""

    reminders = (
        f"{expiration_date - timedelta(days=180)}: confirm renewal path and contract owner.",
        f"{expiration_date - timedelta(days=120)}: gather department performance notes.",
        f"{expiration_date - timedelta(days=90)}: prepare renewal, rebid, or closeout recommendation.",
        f"{expiration_date - timedelta(days=30)}: verify governing-body or delegated approval status.",
    )
    return ExpirationPlan(
        contract_id=contract_id.strip() or "unassigned-contract",
        expiration_date=expiration_date,
        reminders=reminders,
        staff_note="Staff must verify dates against the executed contract and amendments.",
    )
