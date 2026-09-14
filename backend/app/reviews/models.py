import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.evaluation.models import ComplianceStatus


class ReviewerDecisionType(str, enum.Enum):
    CONFIRM = "CONFIRM"
    OVERRIDE = "OVERRIDE"


class ReviewerDecision(Base):
    __tablename__ = "reviewer_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    evaluation_result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_results.id"),
        nullable=False,
    )

    system_status_snapshot: Mapped[ComplianceStatus] = mapped_column(
        Enum(ComplianceStatus, name="compliance_status", create_type=False),
        nullable=False,
    )

    reviewer_status: Mapped[ComplianceStatus] = mapped_column(
        Enum(ComplianceStatus, name="compliance_status", create_type=False),
        nullable=False,
    )

    decision_type: Mapped[ReviewerDecisionType] = mapped_column(
        Enum(ReviewerDecisionType, name="reviewer_decision_type"),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(Text, nullable=False)

    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)