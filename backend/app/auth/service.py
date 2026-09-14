from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import AuthSession
from app.auth.security import (
    generate_session_token,
    hash_session_token,
    verify_password,
)
from app.config import settings
from app.users.models import User


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_auth_session(
    db: Session,
    user: User,
) -> tuple[AuthSession, str]:
    now = datetime.now(timezone.utc)

    raw_token = generate_session_token()

    auth_session = AuthSession(
        user_id=user.id,
        token_hash=hash_session_token(raw_token),
        expires_at=now + timedelta(hours=settings.session_ttl_hours),
        created_at=now,
        last_used_at=now,
    )

    db.add(auth_session)
    db.commit()
    db.refresh(auth_session)

    return auth_session, raw_token


def revoke_auth_session(
    db: Session,
    auth_session: AuthSession,
) -> None:
    auth_session.revoked_at = datetime.now(timezone.utc)
    db.commit()