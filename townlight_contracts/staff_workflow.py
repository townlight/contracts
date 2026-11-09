"""Staff contract register inputs and storage for the desktop suite."""
from datetime import date
from pathlib import PureWindowsPath
from typing import Annotated

import sqlalchemy as sa
from pydantic import Base64Bytes, BaseModel, ConfigDict, Field, model_validator

from townlight_contracts.persistence import contract_registry_records, metadata

ShortText = Annotated[str, Field(min_length=1, max_length=255)]

agreements = sa.Table(
    "staff_agreements", metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("title", sa.String(255), nullable=False),
    sa.Column("vendor_name", sa.String(255), nullable=False),
    sa.Column("owner", sa.String(255), nullable=False),
    sa.Column("start_date", sa.Date),
    sa.Column("expiration_date", sa.Date),
    sa.Column("renewal_due", sa.Date),
    sa.Column("document_name", sa.String(255)),
    sa.Column("document_content", sa.LargeBinary),
    sa.Column("procurement_id", sa.Uuid, unique=True),
    sa.Column("status", sa.String(20), nullable=False),
    sa.CheckConstraint(
        "(status = 'draft' AND document_content IS NULL) OR "
        "(status = 'signed' AND document_content IS NOT NULL AND "
        "start_date IS NOT NULL AND expiration_date IS NOT NULL AND renewal_due IS NOT NULL)",
        name="staff_agreement_lifecycle",
    ),
    schema=contract_registry_records.schema,
)


class SignedAgreement(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: ShortText
    vendor_name: ShortText
    owner: ShortText
    start_date: date
    expiration_date: date
    renewal_due: date
    document_name: ShortText
    document_content: Base64Bytes = Field(max_length=8 * 1024 * 1024)

    @model_validator(mode="after")
    def validate_dates(self):
        if not self.start_date <= self.renewal_due <= self.expiration_date:
            raise ValueError("The renewal deadline must fall between the start and expiration dates.")
        name = PureWindowsPath(self.document_name)
        if name.name != self.document_name or ":" in self.document_name or name.suffix.lower() != ".pdf":
            raise ValueError("Choose a PDF with a plain file name.")
        if not self.document_content.startswith(b"%PDF-"):
            raise ValueError("The selected file is not a PDF.")
        return self
