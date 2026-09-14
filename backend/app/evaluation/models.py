import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    UNABLE_TO_EVALUATE = "UNABLE_TO_EVALUATE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bid_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=False)
    checkpoint_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("checkpoints.id"), nullable=False)

    applicability_status: Mapped[str | None] = mapped_column(String(50))

    system_status: Mapped[ComplianceStatus] = mapped_column(
        Enum(ComplianceStatus, name="compliance_status"), nullable=False
    )

    system_reason_code: Mapped[str | None] = mapped_column(String(100))
    system_explanation: Mapped[str | None] = mapped_column(Text)

    evaluated_value: Mapped[str | None] = mapped_column(String(250))
    normalized_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))

    rule_type: Mapped[str | None] = mapped_column(String(100))
    rule_snapshot: Mapped[dict | None] = mapped_column(JSON)

    match_confidence: Mapped[float | None] = mapped_column(Float)
    interpretation_confidence: Mapped[float | None] = mapped_column(Float)

    contradiction_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    entity_mismatch_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    processing_error_code: Mapped[str | None] = mapped_column(String(100))

    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)