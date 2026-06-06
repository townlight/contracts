from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civiccontracts.contract_registry import ContractRecord, register_contract_stub
from civiccontracts.renewal_visibility import summarize_renewal_visibility


metadata = sa.MetaData()

contract_registry_records = sa.Table(
    "contract_registry_records",
    metadata,
    sa.Column("contract_id", sa.String(160), primary_key=True),
    sa.Column("vendor_name", sa.String(500), nullable=False),
    sa.Column("contract_type", sa.String(255), nullable=False),
    sa.Column("registry_notes", sa.JSON(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccontracts",
)

renewal_visibility_records = sa.Table(
    "renewal_visibility_records",
    metadata,
    sa.Column("contract_id", sa.String(160), primary_key=True),
    sa.Column("renewal_terms", sa.Text(), nullable=False),
    sa.Column("department_notes", sa.Text(), nullable=False),
    sa.Column("renewal_status", sa.String(160), nullable=False),
    sa.Column("visibility_items", sa.JSON(), nullable=False),
    sa.Column("staff_review_required", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccontracts",
)

contract_draft_records = sa.Table(
    "contract_draft_records",
    metadata,
    sa.Column("draft_id", sa.String(160), primary_key=True),
    sa.Column("contract_id", sa.String(160), nullable=False),
    sa.Column("vendor_name", sa.String(500), nullable=False),
    sa.Column("contract_type", sa.String(255), nullable=False),
    sa.Column("procurement_packet_id", sa.String(255), nullable=False),
    sa.Column("award_packet_id", sa.String(255), nullable=False),
    sa.Column("source_module", sa.String(160), nullable=False),
    sa.Column("source_title", sa.String(500), nullable=False),
    sa.Column("terms_summary", sa.Text(), nullable=False),
    sa.Column("review_items", sa.JSON(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccontracts",
)

staff_review_queue_records = sa.Table(
    "staff_review_queue_records",
    metadata,
    sa.Column("review_id", sa.String(160), primary_key=True),
    sa.Column("draft_id", sa.String(160), nullable=False),
    sa.Column("contract_id", sa.String(160), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("reason", sa.Text(), nullable=False),
    sa.Column("status", sa.String(120), nullable=False),
    sa.Column("assigned_to", sa.String(255), nullable=True),
    sa.Column("resolution", sa.Text(), nullable=True),
    sa.Column("created_by", sa.String(160), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccontracts",
)


@dataclass(frozen=True)
class SchemaStatus:
    ready: bool
    schema_version: str
    expected_schema_version: str


@dataclass(frozen=True)
class StoredRenewalSummary:
    contract_id: str
    renewal_terms: str
    department_notes: str
    renewal_status: str
    visibility_items: tuple[str, ...]
    staff_review_required: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredContractDraft:
    draft_id: str
    contract_id: str
    vendor_name: str
    contract_type: str
    procurement_packet_id: str
    award_packet_id: str
    source_module: str
    source_title: str
    terms_summary: str
    review_items: tuple[str, ...]
    disclaimer: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class StaffReviewQueueItem:
    review_id: str
    draft_id: str
    contract_id: str
    title: str
    reason: str
    status: str
    assigned_to: str | None
    resolution: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime


class ContractRegistryRepository:
    """SQLAlchemy-backed contract registry and renewal visibility records."""

    expected_schema_version = "civiccontracts-local-first-v1"

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civiccontracts": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civiccontracts"))
        metadata.create_all(self.engine)

    def schema_status(self) -> SchemaStatus:
        try:
            with self.engine.begin() as connection:
                for table in (
                    contract_registry_records,
                    renewal_visibility_records,
                    contract_draft_records,
                    staff_review_queue_records,
                ):
                    connection.execute(sa.select(sa.func.count()).select_from(table)).scalar_one()
        except Exception:
            return SchemaStatus(
                ready=False,
                schema_version="unavailable",
                expected_schema_version=self.expected_schema_version,
            )
        return SchemaStatus(
            ready=True,
            schema_version=self.expected_schema_version,
            expected_schema_version=self.expected_schema_version,
        )

    def register_contract(
        self, *, contract_id: str, vendor_name: str, contract_type: str
    ) -> ContractRecord:
        record = register_contract_stub(
            contract_id=contract_id,
            vendor_name=vendor_name,
            contract_type=contract_type,
        )
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(contract_registry_records.c.contract_id).where(
                    contract_registry_records.c.contract_id == record.contract_id
                )
            ).first()
            values = {
                "contract_id": record.contract_id,
                "vendor_name": record.vendor_name,
                "contract_type": record.contract_type,
                "registry_notes": list(record.registry_notes),
                "disclaimer": record.disclaimer,
                "updated_at": now,
            }
            if exists is None:
                connection.execute(contract_registry_records.insert().values(**values, created_at=now))
            else:
                connection.execute(
                    contract_registry_records.update()
                    .where(contract_registry_records.c.contract_id == record.contract_id)
                    .values(**values)
                )
        return record

    def get_contract(self, contract_id: str) -> ContractRecord | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(contract_registry_records).where(
                    contract_registry_records.c.contract_id == contract_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_contract(row)

    def create_renewal_summary(
        self, *, contract_id: str, renewal_terms: str, department_notes: str = ""
    ) -> StoredRenewalSummary:
        summary = summarize_renewal_visibility(
            contract_id=contract_id,
            renewal_terms=renewal_terms,
            department_notes=department_notes,
        )
        stored = StoredRenewalSummary(
            contract_id=summary.contract_id,
            renewal_terms=renewal_terms,
            department_notes=department_notes,
            renewal_status=summary.renewal_status,
            visibility_items=summary.visibility_items,
            staff_review_required=summary.staff_review_required,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(renewal_visibility_records.c.contract_id).where(
                    renewal_visibility_records.c.contract_id == stored.contract_id
                )
            ).first()
            values = {
                "contract_id": stored.contract_id,
                "renewal_terms": stored.renewal_terms,
                "department_notes": stored.department_notes,
                "renewal_status": stored.renewal_status,
                "visibility_items": list(stored.visibility_items),
                "staff_review_required": stored.staff_review_required,
                "created_at": stored.created_at,
            }
            if exists is None:
                connection.execute(renewal_visibility_records.insert().values(**values))
            else:
                connection.execute(
                    renewal_visibility_records.update()
                    .where(renewal_visibility_records.c.contract_id == stored.contract_id)
                    .values(**values)
                )
        return stored

    def get_renewal_summary(self, contract_id: str) -> StoredRenewalSummary | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(renewal_visibility_records).where(
                    renewal_visibility_records.c.contract_id == contract_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_renewal(row)

    def create_contract_draft(
        self,
        *,
        contract_id: str,
        vendor_name: str,
        contract_type: str,
        procurement_packet_id: str = "",
        award_packet_id: str = "",
        source_module: str = "civicprocure",
        source_title: str = "",
        terms_summary: str = "",
    ) -> StoredContractDraft:
        registry = register_contract_stub(
            contract_id=contract_id,
            vendor_name=vendor_name,
            contract_type=contract_type,
        )
        clean_contract_id = registry.contract_id
        draft_id = _stable_id(
            "contract-draft",
            clean_contract_id,
            registry.vendor_name,
            procurement_packet_id,
            award_packet_id,
            source_title,
        )
        now = datetime.now(UTC)
        review_items = [
            *registry.registry_notes,
            "Confirm procurement award authority, signature authority, insurance, and funding source.",
            "Route draft to staff/legal review before execution or publication.",
        ]
        stored = StoredContractDraft(
            draft_id=draft_id,
            contract_id=clean_contract_id,
            vendor_name=registry.vendor_name,
            contract_type=registry.contract_type,
            procurement_packet_id=procurement_packet_id.strip(),
            award_packet_id=award_packet_id.strip(),
            source_module=source_module.strip() or "civicprocure",
            source_title=source_title.strip() or registry.contract_type,
            terms_summary=terms_summary.strip(),
            review_items=tuple(review_items),
            disclaimer=registry.disclaimer,
            created_at=now,
            updated_at=now,
        )
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(contract_draft_records.c.draft_id).where(
                    contract_draft_records.c.draft_id == stored.draft_id
                )
            ).first()
            values = {
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
                "updated_at": stored.updated_at,
            }
            if exists is None:
                connection.execute(contract_draft_records.insert().values(**values, created_at=now))
            else:
                connection.execute(
                    contract_draft_records.update()
                    .where(contract_draft_records.c.draft_id == stored.draft_id)
                    .values(**values)
                )
        return stored

    def get_contract_draft(self, draft_id: str) -> StoredContractDraft | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(contract_draft_records).where(contract_draft_records.c.draft_id == draft_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_contract_draft(row)

    def create_staff_review_queue_item(
        self,
        *,
        draft_id: str,
        contract_id: str,
        title: str,
        reason: str,
        created_by: str = "staff",
    ) -> StaffReviewQueueItem:
        review_id = _stable_id("contract-review", draft_id, contract_id, reason)
        now = datetime.now(UTC)
        item = StaffReviewQueueItem(
            review_id=review_id,
            draft_id=draft_id,
            contract_id=contract_id,
            title=title.strip() or "Untitled contract review",
            reason=reason.strip() or "Contract staff review required.",
            status="open",
            assigned_to=None,
            resolution=None,
            created_by=created_by.strip() or "staff",
            created_at=now,
            updated_at=now,
        )
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(staff_review_queue_records.c.review_id).where(
                    staff_review_queue_records.c.review_id == item.review_id
                )
            ).first()
            values = {
                "review_id": item.review_id,
                "draft_id": item.draft_id,
                "contract_id": item.contract_id,
                "title": item.title,
                "reason": item.reason,
                "status": item.status,
                "assigned_to": item.assigned_to,
                "resolution": item.resolution,
                "created_by": item.created_by,
                "updated_at": item.updated_at,
            }
            if exists is None:
                connection.execute(staff_review_queue_records.insert().values(**values, created_at=now))
            else:
                connection.execute(
                    staff_review_queue_records.update()
                    .where(staff_review_queue_records.c.review_id == item.review_id)
                    .values(**values)
                )
        return item

    def list_staff_review_queue_items(self, status: str | None = None) -> list[StaffReviewQueueItem]:
        query = sa.select(staff_review_queue_records).order_by(
            staff_review_queue_records.c.updated_at.desc()
        )
        if status:
            query = query.where(staff_review_queue_records.c.status == status)
        with self.engine.begin() as connection:
            rows = connection.execute(query).mappings().all()
        return [_row_to_staff_review(row) for row in rows]


def _row_to_contract(row: object) -> ContractRecord:
    data = dict(row)
    return ContractRecord(
        contract_id=data["contract_id"],
        vendor_name=data["vendor_name"],
        contract_type=data["contract_type"],
        registry_notes=tuple(data["registry_notes"]),
        disclaimer=data["disclaimer"],
    )


def _row_to_renewal(row: object) -> StoredRenewalSummary:
    data = dict(row)
    return StoredRenewalSummary(
        contract_id=data["contract_id"],
        renewal_terms=data["renewal_terms"],
        department_notes=data["department_notes"],
        renewal_status=data["renewal_status"],
        visibility_items=tuple(data["visibility_items"]),
        staff_review_required=data["staff_review_required"],
        created_at=data["created_at"],
    )


def _row_to_contract_draft(row: object) -> StoredContractDraft:
    data = dict(row)
    return StoredContractDraft(
        draft_id=data["draft_id"],
        contract_id=data["contract_id"],
        vendor_name=data["vendor_name"],
        contract_type=data["contract_type"],
        procurement_packet_id=data["procurement_packet_id"],
        award_packet_id=data["award_packet_id"],
        source_module=data["source_module"],
        source_title=data["source_title"],
        terms_summary=data["terms_summary"],
        review_items=tuple(data["review_items"]),
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def _row_to_staff_review(row: object) -> StaffReviewQueueItem:
    data = dict(row)
    return StaffReviewQueueItem(
        review_id=data["review_id"],
        draft_id=data["draft_id"],
        contract_id=data["contract_id"],
        title=data["title"],
        reason=data["reason"],
        status=data["status"],
        assigned_to=data["assigned_to"],
        resolution=data["resolution"],
        created_by=data["created_by"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256("|".join(part.strip() for part in parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"
