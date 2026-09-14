import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bid_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bids.id", ondelete="CASCADE"), nullable=False, index=True
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )

    page_number: Mapped[int | None]
    section_reference: Mapped[str | None] = mapped_column(String(200))
    evidence_type: Mapped[str | None] = mapped_column(String(100))

    raw_text: Mapped[str | None] = mapped_column(Text)
    normalized_text: Mapped[str | None] = mapped_column(Text)

    value_text: Mapped[str | None] = mapped_column(String(250))
    normalized_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    unit: Mapped[str | None] = mapped_column(String(50))

    date_value: Mapped[date | None] = mapped_column(Date)
    identifier_value: Mapped[str | None] = mapped_column(String(200))
    organization_name: Mapped[str | None] = mapped_column(String(250))

    extraction_method: Mapped[str | None] = mapped_column(String(100))
    extraction_confidence: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CheckpointEvidenceLink(Base):
    __tablename__ = "checkpoint_evidence_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoints.id", ondelete="CASCADE"), nullable=False
    )

    evidence_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evidence_items.id", ondelete="CASCADE"), nullable=False
    )

    match_method: Mapped[str | None] = mapped_column(String(100))
    match_score: Mapped[float | None] = mapped_column(Float)

    is_system_suggested: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_reviewer_confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)