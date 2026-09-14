from app.auth.security import (
    generate_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)


def test_password_hashing():
    password = "VeryStrongPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_session_token_generation_and_hashing():
    token = generate_session_token()
    token_hash = hash_session_token(token)

    assert token
    assert token_hash
    assert token != token_hash
    assert hash_session_token(token) == token_hash