import enum
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DocumentOwnerType(str, enum.Enum):
    TENDER = "TENDER"
    BID = "BID"
    ORGANIZATION = "ORGANIZATION"


class DocumentRole(str, enum.Enum):
    TENDER_DOCUMENT = "TENDER_DOCUMENT"
    CERTIFICATE = "CERTIFICATE"
    FINANCIAL_DOCUMENT = "FINANCIAL_DOCUMENT"
    TECHNICAL_DATASHEET = "TECHNICAL_DATASHEET"
    WORK_ORDER = "WORK_ORDER"
    COMPLETION_CERTIFICATE = "COMPLETION_CERTIFICATE"
    AUTHORIZATION = "AUTHORIZATION"
    DECLARATION = "DECLARATION"
    OTHER = "OTHER"


class DocumentProcessingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_type: Mapped[DocumentOwnerType] = mapped_column(
        Enum(DocumentOwnerType, name="document_owner_type"),
        nullable=False,
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    document_role: Mapped[DocumentRole] = mapped_column(
        Enum(DocumentRole, name="document_role"),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(150), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

    page_count: Mapped[int | None] = mapped_column(Integer)

    processing_status: Mapped[DocumentProcessingStatus] = mapped_column(
        Enum(DocumentProcessingStatus, name="document_processing_status"),
        default=DocumentProcessingStatus.PENDING,
        nullable=False,
    )

    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(nullable=False)


class DocumentPage(Base):
    __tablename__ = "document_pages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    page_number: Mapped[int] = mapped_column(Integer, nullable=False)

    extraction_method: Mapped[str | None] = mapped_column(String(50))
    raw_text: Mapped[str | None] = mapped_column(Text)
    normalized_text: Mapped[str | None] = mapped_column(Text)
    ocr_confidence: Mapped[float | None] = mapped_column(Float)

    processing_status: Mapped[DocumentProcessingStatus] = mapped_column(
        Enum(
            DocumentProcessingStatus,
            name="document_processing_status",
            create_type=False,
        ),
        default=DocumentProcessingStatus.PENDING,
        nullable=False,
    )

    block_metadata: Mapped[dict | None] = mapped_column(JSON)