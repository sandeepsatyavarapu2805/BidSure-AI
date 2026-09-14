from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.tenders.models import Tender, TenderStatus
from app.tenders.schemas import TenderCreate, TenderResponse, TenderUpdate
from app.users.models import User, UserRole


router = APIRouter(prefix="/tenders", tags=["tenders"])


@router.post("", response_model=TenderResponse, status_code=201)
def create_tender(
    payload: TenderCreate,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    tender = Tender(created_by=user.id, **payload.model_dump())
    db.add(tender)
    db.commit()
    db.refresh(tender)
    return tender


@router.get("", response_model=list[TenderResponse])
def list_tenders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role == UserRole.BIDDER:
        return list(db.scalars(select(Tender).where(Tender.status == TenderStatus.OPEN)).all())

    return list(db.scalars(select(Tender)).all())


@router.patch("/{tender_id}", response_model=TenderResponse)
def update_tender(
    tender_id: UUID,
    payload: TenderUpdate,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    tender = db.get(Tender, tender_id)

    if tender is None:
        raise HTTPException(404, "Tender not found.")

    if tender.status != TenderStatus.DRAFT:
        raise HTTPException(409, "Only DRAFT tenders can be edited.")

    if user.role != UserRole.ADMIN and tender.created_by != user.id:
        raise HTTPException(403, "Not authorized for this tender.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tender, field, value)

    db.commit()
    db.refresh(tender)
    return tender


@router.post("/{tender_id}/open", response_model=TenderResponse)
def open_tender(
    tender_id: UUID,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    tender = db.get(Tender, tender_id)

    if tender is None:
        raise HTTPException(404, "Tender not found.")

    if tender.status != TenderStatus.DRAFT:
        raise HTTPException(409, "Only DRAFT tenders can be opened.")

    if user.role != UserRole.ADMIN and tender.created_by != user.id:
        raise HTTPException(403, "Not authorized for this tender.")

    tender.status = TenderStatus.OPEN
    tender.checkpoint_set_frozen_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(tender)
    return tender