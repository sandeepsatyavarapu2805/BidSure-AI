from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import AuthSession
from app.auth.schemas import LoginRequest, LoginResponse, UserResponse
from app.auth.security import hash_session_token
from app.auth.service import (
    authenticate_user,
    create_auth_session,
    revoke_auth_session,
)
from app.config import settings
from app.db.session import get_db
from app.users.models import User


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = authenticate_user(
        db,
        payload.username,
        payload.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    _, raw_token = create_auth_session(db, user)

    response.set_cookie(
        key=settings.session_cookie_name,
        value=raw_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.session_ttl_hours * 3600,
    )

    return LoginResponse(
        user=UserResponse.model_validate(user)
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> None:
    raw_token = request.cookies.get(settings.session_cookie_name)

    if raw_token:
        auth_session = db.scalar(
            select(AuthSession).where(
                AuthSession.token_hash
                == hash_session_token(raw_token)
            )
        )

        if (
            auth_session is not None
            and auth_session.revoked_at is None
        ):
            revoke_auth_session(db, auth_session)

    response.delete_cookie(
        key=settings.session_cookie_name,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    user: User = Depends(get_current_user),
) -> User:
    return user