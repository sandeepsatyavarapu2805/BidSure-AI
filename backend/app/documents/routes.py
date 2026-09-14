from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.bids.models import Bid, BidStatus
from app.db.session import get_db
from app.documents.models import (
    Document,
    DocumentOwnerType,
    DocumentProcessingStatus,
    DocumentRole,
)
from app.documents.schemas import DocumentResponse
from app.documents.service import validate_upload
from app.organizations.models import Organization
from app.storage.local import LocalFileStorage
from app.tenders.models import Tender, TenderStatus
from app.users.models import User, UserRole


router = APIRouter(tags=["documents"])

storage = LocalFileStorage()


@router.post(
    "/tenders/{tender_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
async def upload_tender_document(
    tender_id: UUID,
    document_role: DocumentRole = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(
        require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)
    ),
    db: Session = Depends(get_db),
):
    tender = db.get(Tender, tender_id)

    if tender is None:
        raise HTTPException(404, "Tender not found.")

    if tender.status != TenderStatus.DRAFT:
        raise HTTPException(409, "Documents can only be added to DRAFT tenders.")

    if user.role != UserRole.ADMIN and tender.created_by != user.id:
        raise HTTPException(403, "Not authorized for this tender.")

    content, stored_filename, sha256 = await validate_upload(file)

    key = f"tenders/{tender.id}/{stored_filename}"
    storage.save(key, content)

    document = Document(
        owner_type=DocumentOwnerType.TENDER,
        owner_id=tender.id,
        document_role=document_role,
        original_filename=Path(file.filename or "upload").name,
        stored_filename=stored_filename,
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        sha256=sha256,
        storage_key=key,
        processing_status=DocumentProcessingStatus.PENDING,
        uploaded_by=user.id,
        created_at=datetime.now(timezone.utc),
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.post(
    "/bids/{bid_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
async def upload_bid_document(
    bid_id: UUID,
    document_role: DocumentRole = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(require_roles(UserRole.BIDDER)),
    db: Session = Depends(get_db),
):
    bid = db.get(Bid, bid_id)

    if bid is None:
        raise HTTPException(404, "Bid not found.")

    if bid.status != BidStatus.DRAFT:
        raise HTTPException(409, "Only DRAFT bids accept uploads.")

    organization = db.get(Organization, bid.organization_id)

    if organization is None or organization.owner_user_id != user.id:
        raise HTTPException(403, "Not authorized for this bid.")

    content, stored_filename, sha256 = await validate_upload(file)

    key = f"bids/{bid.id}/{stored_filename}"
    storage.save(key, content)

    document = Document(
        owner_type=DocumentOwnerType.BID,
        owner_id=bid.id,
        document_role=document_role,
        original_filename=Path(file.filename or "upload").name,
        stored_filename=stored_filename,
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        sha256=sha256,
        storage_key=key,
        processing_status=DocumentProcessingStatus.PENDING,
        uploaded_by=user.id,
        created_at=datetime.now(timezone.utc),
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document