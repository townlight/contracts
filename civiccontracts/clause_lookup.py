"""Clause lookup helpers for Townlight Contracts v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civiccontracts.contract_registry import DISCLAIMER


@dataclass(frozen=True)
class ClauseLookup:
    query: str
    matched_topics: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str = DISCLAIMER


def lookup_clause_topics(*, query: str, contract_text: str) -> ClauseLookup:
    """Flag common clause topics without providing legal interpretation."""

    haystack = f"{query} {contract_text}".casefold()
    topics: list[str] = []
    if "renew" in haystack:
        topics.append("Renewal / extension")
    if "terminat" in haystack:
        topics.append("Termination")
    if "indemn" in haystack:
        topics.append("Indemnification")
    if "insurance" in haystack:
        topics.append("Insurance")
    if "confidential" in haystack or "public record" in haystack:
        topics.append("Confidentiality / public records")
    if not topics:
        topics.append("No common clause topic detected; staff must review the contract text.")
    return ClauseLookup(
        query=query.strip() or "general clause lookup",
        matched_topics=tuple(topics),
        staff_review_required=True,
    )
