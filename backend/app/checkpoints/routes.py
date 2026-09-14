from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.checkpoints.models import Checkpoint
from app.checkpoints.schemas import CheckpointCreate, CheckpointResponse, CheckpointUpdate
from app.db.session import get_db
from app.tenders.models import Tender, TenderStatus
from app.users.models import User, UserRole


router = APIRouter(tags=["checkpoints"])


def editable_tender(db: Session, tender_id: UUID, user: User) -> Tender:
    tender = db.get(Tender, tender_id)

    if tender is None:
        raise HTTPException(404, "Tender not found.")

    if user.role != UserRole.ADMIN and tender.created_by != user.id:
        raise HTTPException(403, "Not authorized for this tender.")

    if tender.status != TenderStatus.DRAFT or tender.checkpoint_set_frozen_at is not None:
        raise HTTPException(409, "Checkpoint set is frozen.")

    return tender


@router.post(
    "/tenders/{tender_id}/checkpoints",
    response_model=CheckpointResponse,
    status_code=201,
)
def create_checkpoint(
    tender_id: UUID,
    payload: CheckpointCreate,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    editable_tender(db, tender_id, user)

    checkpoint = Checkpoint(
        tender_id=tender_id,
        confirmed_by=user.id,
        confirmed_at=datetime.now(timezone.utc),
        is_confirmed=True,
        **payload.model_dump(),
    )

    db.add(checkpoint)
    db.commit()
    db.refresh(checkpoint)
    return checkpoint


@router.get(
    "/tenders/{tender_id}/checkpoints",
    response_model=list[CheckpointResponse],
)
def list_checkpoints(
    tender_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(
        UserRole.BUYER_REVIEWER,
        UserRole.ADMIN,
        UserRole.BIDDER,
    )),
):
    tender = db.get(Tender, tender_id)

    if tender is None:
        raise HTTPException(404, "Tender not found.")

    if user.role == UserRole.BIDDER and tender.status != TenderStatus.OPEN:
        raise HTTPException(403, "Tender is not open.")

    return list(
        db.scalars(
            select(Checkpoint)
            .where(Checkpoint.tender_id == tender_id)
            .order_by(Checkpoint.sequence_number)
        ).all()
    )


@router.patch(
    "/tenders/{tender_id}/checkpoints/{checkpoint_id}",
    response_model=CheckpointResponse,
)
def update_checkpoint(
    tender_id: UUID,
    checkpoint_id: UUID,
    payload: CheckpointUpdate,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    editable_tender(db, tender_id, user)

    checkpoint = db.get(Checkpoint, checkpoint_id)

    if checkpoint is None or checkpoint.tender_id != tender_id:
        raise HTTPException(404, "Checkpoint not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(checkpoint, field, value)

    db.commit()
    db.refresh(checkpoint)
    return checkpoint


@router.delete(
    "/tenders/{tender_id}/checkpoints/{checkpoint_id}",
    status_code=204,
)
def delete_checkpoint(
    tender_id: UUID,
    checkpoint_id: UUID,
    user: User = Depends(require_roles(UserRole.BUYER_REVIEWER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    editable_tender(db, tender_id, user)

    checkpoint = db.get(Checkpoint, checkpoint_id)

    if checkpoint is None or checkpoint.tender_id != tender_id:
        raise HTTPException(404, "Checkpoint not found.")

    db.delete(checkpoint)
    db.commit()