import argparse
import getpass

from sqlalchemy import select

from app.auth.security import hash_password
from app.db.session import SessionLocal
from app.users.models import User, UserRole


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a BidSure AI application user."
    )

    parser.add_argument("username")
    parser.add_argument(
        "role",
        choices=[role.value for role in UserRole],
    )

    args = parser.parse_args()

    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        raise SystemExit("Passwords do not match.")

    if len(password) < 12:
        raise SystemExit(
            "Password must contain at least 12 characters."
        )

    with SessionLocal() as db:
        existing = db.scalar(
            select(User).where(
                User.username == args.username
            )
        )

        if existing is not None:
            raise SystemExit("User already exists.")

        user = User(
            username=args.username,
            password_hash=hash_password(password),
            role=UserRole(args.role),
            is_active=True,
        )

        db.add(user)
        db.commit()

        print(
            f"Created user '{args.username}' "
            f"with role '{args.role}'."
        )


if __name__ == "__main__":
    main()