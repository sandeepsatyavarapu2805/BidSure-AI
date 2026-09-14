from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.bids.models import Bid, BidStatus
from app.bids.schemas import BidCreate, BidResponse, BidUpdate
from app.db.session import get_db
from app.organizations.models import Organization
from app.tenders.models import Tender, TenderStatus
from app.users.models import User, UserRole


router = APIRouter(prefix="/bids", tags=["bids"])


def bidder_org(db: Session, user: User) -> Organization:
    org = db.scalar(
        select(Organization).where(Organization.owner_user_id == user.id)
    )

    if org is None:
        raise HTTPException(409, "Create organization profile first.")

    return org


@router.post("", response_model=BidResponse, status_code=201)
def create_bid(
    payload: BidCreate,
    user: User = Depends(require_roles(UserRole.BIDDER)),
    db: Session = Depends(get_db),
):
    org = bidder_org(db, user)

    tender = db.get(Tender, payload.tender_id)

    if tender is None or tender.status != TenderStatus.OPEN:
        raise HTTPException(409, "Tender is not open for submissions.")

    existing = db.scalar(
        select(Bid).where(
            Bid.tender_id == tender.id,
            Bid.organization_id == org.id,
        )
    )

    if existing:
        raise HTTPException(409, "Bid already exists for this tender.")

    bid = Bid(
        tender_id=tender.id,
        organization_id=org.id,
        quotation=payload.quotation,
    )

    db.add(bid)
    db.commit()
    db.refresh(bid)
    return bid


@router.patch("/{bid_id}", response_model=BidResponse)
def update_bid(
    bid_id: UUID,
    payload: BidUpdate,
    user: User = Depends(require_roles(UserRole.BIDDER)),
    db: Session = Depends(get_db),
):
    org = bidder_org(db, user)
    bid = db.get(Bid, bid_id)

    if bid is None or bid.organization_id != org.id:
        raise HTTPException(404, "Bid not found.")

    if bid.status != BidStatus.DRAFT:
        raise HTTPException(409, "Only DRAFT bids are editable.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(bid, field, value)

    db.commit()
    db.refresh(bid)
    return bid


@router.post("/{bid_id}/submit", response_model=BidResponse)
def submit_bid(
    bid_id: UUID,
    user: User = Depends(require_roles(UserRole.BIDDER)),
    db: Session = Depends(get_db),
):
    org = bidder_org(db, user)
    bid = db.get(Bid, bid_id)

    if bid is None or bid.organization_id != org.id:
        raise HTTPException(404, "Bid not found.")

    if bid.status != BidStatus.DRAFT:
        raise HTTPException(409, "Only DRAFT bids can be submitted.")

    bid.status = BidStatus.SUBMITTED
    bid.submitted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(bid)
    return bid