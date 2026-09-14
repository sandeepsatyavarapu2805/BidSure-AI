from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.bids.models import BidStatus


class BidCreate(BaseModel):
    tender_id: UUID
    quotation: Decimal | None = Field(default=None, ge=0)


class BidUpdate(BaseModel):
    quotation: Decimal | None = Field(default=None, ge=0)


class BidResponse(BaseModel):
    id: UUID
    tender_id: UUID
    organization_id: UUID
    quotation: Decimal | None
    status: BidStatus
    submitted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
