import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class BidStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_PRELIMINARY_REVIEW = "UNDER_PRELIMINARY_REVIEW"
    REVIEWED = "REVIEWED"


class Bid(TimestampMixin, Base):
    __tablename__ = "bids"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    quotation: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))

    status: Mapped[BidStatus] = mapped_column(
        Enum(BidStatus, name="bid_status"),
        default=BidStatus.DRAFT,
        nullable=False,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))