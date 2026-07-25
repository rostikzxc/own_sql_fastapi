from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


# ==========================
# Refresh Token Repository
# ==========================

def create(
    db: Session,
    user_id: int,
    token_hash: str,
    expires_at
):
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token


def get_by_hash(
    db: Session,
    token_hash: str
):
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash)
        .first()
    )


def revoke(
    db: Session,
    token_hash: str
):
    refresh_token = get_by_hash(
        db,
        token_hash
    )

    if not refresh_token:
        return None

    refresh_token.revoked = True

    db.commit()
    db.refresh(refresh_token)

    return refresh_token