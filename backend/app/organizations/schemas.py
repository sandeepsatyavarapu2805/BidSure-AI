from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    legal_name: str | None = Field(default=None, max_length=250)
    organization_type: str | None = Field(default=None, max_length=100)
    registration_number: str | None = Field(default=None, max_length=100)

    years_of_operation: int | None = Field(default=None, ge=0)
    completed_projects: int | None = Field(default=None, ge=0)
    relevant_experience_years: int | None = Field(default=None, ge=0)

    turnover: Decimal | None = Field(default=None, ge=0)

    is_oem: bool = False


class OrganizationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    legal_name: str | None = Field(default=None, max_length=250)
    organization_type: str | None = Field(default=None, max_length=100)
    registration_number: str | None = Field(default=None, max_length=100)

    years_of_operation: int | None = Field(default=None, ge=0)
    completed_projects: int | None = Field(default=None, ge=0)
    relevant_experience_years: int | None = Field(default=None, ge=0)

    turnover: Decimal | None = Field(default=None, ge=0)

    is_oem: bool | None = None


class OrganizationResponse(BaseModel):
    id: UUID
    owner_user_id: UUID

    name: str
    legal_name: str | None
    organization_type: str | None
    registration_number: str | None

    years_of_operation: int | None
    completed_projects: int | None
    relevant_experience_years: int | None

    turnover: Decimal | None

    is_oem: bool

    model_config = ConfigDict(from_attributes=True)