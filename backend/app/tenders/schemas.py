from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.tenders.models import TenderStatus


class TenderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    description: str | None = None
    category: str | None = None
    procurement_type: str | None = None
    quantity: int | None = Field(default=None, ge=1)
    estimated_value: Decimal | None = Field(default=None, ge=0)
    submission_deadline: datetime | None = None


class TenderUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=250)
    description: str | None = None
    category: str | None = None
    procurement_type: str | None = None
    quantity: int | None = Field(default=None, ge=1)
    estimated_value: Decimal | None = Field(default=None, ge=0)
    submission_deadline: datetime | None = None


class TenderResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    category: str | None
    procurement_type: str | None
    quantity: int | None
    estimated_value: Decimal | None
    submission_deadline: datetime | None
    status: TenderStatus
    created_by: UUID
    checkpoint_set_frozen_at: datetime | None

    model_config = ConfigDict(from_attributes=True)