from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.db.session import get_db
from app.organizations.models import Organization
from app.organizations.schemas import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.users.models import User, UserRole


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.get(
    "/me",
    response_model=OrganizationResponse,
)
def get_my_organization(
    current_user: User = Depends(
        require_roles(UserRole.BIDDER)
    ),
    db: Session = Depends(get_db),
) -> Organization:
    organization = db.scalar(
        select(Organization).where(
            Organization.owner_user_id == current_user.id
        )
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization profile not found.",
        )

    return organization


@router.post(
    "/me",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_organization(
    payload: OrganizationCreate,
    current_user: User = Depends(
        require_roles(UserRole.BIDDER)
    ),
    db: Session = Depends(get_db),
) -> Organization:
    existing = db.scalar(
        select(Organization).where(
            Organization.owner_user_id == current_user.id
        )
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization profile already exists.",
        )

    organization = Organization(
        owner_user_id=current_user.id,
        **payload.model_dump(),
    )

    db.add(organization)
    db.commit()
    db.refresh(organization)

    return organization


@router.patch(
    "/me",
    response_model=OrganizationResponse,
)
def update_my_organization(
    payload: OrganizationUpdate,
    current_user: User = Depends(
        require_roles(UserRole.BIDDER)
    ),
    db: Session = Depends(get_db),
) -> Organization:
    organization = db.scalar(
        select(Organization).where(
            Organization.owner_user_id == current_user.id
        )
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization profile not found.",
        )

    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(organization, field, value)

    db.commit()
    db.refresh(organization)

    return organization