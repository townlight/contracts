from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from townlight_contracts.contract_registry import ContractRecord, register_contract_stub
from townlight_contracts.renewal_visibility import summarize_renewal_visibility


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
    schema="townlight_contracts",
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
    schema="townlight_contracts",
)


@dataclass(frozen=True)
class StoredRenewalSummary:
    contract_id: str
    renewal_terms: str
    department_notes: str
    renewal_status: str
    visibility_items: tuple[str, ...]
    staff_review_required: bool
    created_at: datetime


class ContractRegistryRepository:
    """SQLAlchemy-backed contract registry and renewal visibility records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"townlight_contracts": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                schemas = set(sa.inspect(connection).get_schema_names())
                if "civiccontracts" in schemas:
                    raise RuntimeError("Migrate the legacy PostgreSQL schema before opening townlight_contracts.")
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS townlight_contracts"))
        metadata.create_all(self.engine)

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
