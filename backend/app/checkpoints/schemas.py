from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.checkpoints.models import RequirementClass, ValidationMethod


class CheckpointCreate(BaseModel):
    original_text: str
    normalized_requirement: str
    category: str | None = None
    requirement_class: RequirementClass
    validation_method: ValidationMethod
    operator: str | None = None
    threshold_value: Decimal | None = None
    threshold_unit: str | None = None
    expected_evidence_type: str | None = None
    applicability_definition: str | None = None
    validity_definition: str | None = None
    sequence_number: int


class CheckpointUpdate(BaseModel):
    normalized_requirement: str | None = None
    category: str | None = None
    requirement_class: RequirementClass | None = None
    validation_method: ValidationMethod | None = None
    operator: str | None = None
    threshold_value: Decimal | None = None
    threshold_unit: str | None = None
    expected_evidence_type: str | None = None
    applicability_definition: str | None = None
    validity_definition: str | None = None
    sequence_number: int | None = None


class CheckpointResponse(BaseModel):
    id: UUID
    tender_id: UUID
    original_text: str
    normalized_requirement: str
    category: str | None
    requirement_class: RequirementClass
    validation_method: ValidationMethod
    operator: str | None
    threshold_value: Decimal | None
    threshold_unit: str | None
    expected_evidence_type: str | None
    sequence_number: int
    is_confirmed: bool

    model_config = ConfigDict(from_attributes=True)