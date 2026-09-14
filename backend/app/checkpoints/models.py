import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class RequirementClass(str, enum.Enum):
    MANDATORY = "MANDATORY"
    CONDITIONAL = "CONDITIONAL"
    INFORMATIONAL = "INFORMATIONAL"


class ValidationMethod(str, enum.Enum):
    DOCUMENT_PRESENCE = "DOCUMENT_PRESENCE"
    NUMERIC_THRESHOLD = "NUMERIC_THRESHOLD"
    DATE_VALIDITY = "DATE_VALIDITY"
    EXPERIENCE_THRESHOLD = "EXPERIENCE_THRESHOLD"
    PROJECT_COUNT = "PROJECT_COUNT"
    TECHNICAL_NUMERIC = "TECHNICAL_NUMERIC"
    SEMANTIC = "SEMANTIC"
    DECLARATION_PRESENCE = "DECLARATION_PRESENCE"
    ENTITY_CONSISTENCY = "ENTITY_CONSISTENCY"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class Checkpoint(TimestampMixin, Base):
    __tablename__ = "checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_requirement: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str | None] = mapped_column(String(100))

    requirement_class: Mapped[RequirementClass] = mapped_column(
        Enum(RequirementClass, name="requirement_class"),
        nullable=False,
    )

    validation_method: Mapped[ValidationMethod] = mapped_column(
        Enum(ValidationMethod, name="validation_method"),
        nullable=False,
    )

    operator: Mapped[str | None] = mapped_column(String(50))
    threshold_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    threshold_unit: Mapped[str | None] = mapped_column(String(50))

    expected_evidence_type: Mapped[str | None] = mapped_column(String(100))
    applicability_definition: Mapped[str | None] = mapped_column(Text)
    validity_definition: Mapped[str | None] = mapped_column(Text)

    source_document_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    source_page: Mapped[int | None] = mapped_column(Integer)
    source_section: Mapped[str | None] = mapped_column(String(150))

    extraction_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))

    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    confirmed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)