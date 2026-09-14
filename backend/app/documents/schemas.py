from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.documents.models import (
    DocumentOwnerType,
    DocumentProcessingStatus,
    DocumentRole,
)


class DocumentResponse(BaseModel):
    id: UUID
    owner_type: DocumentOwnerType
    owner_id: UUID
    document_role: DocumentRole
    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    sha256: str
    storage_key: str
    processing_status: DocumentProcessingStatus
    uploaded_by: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)