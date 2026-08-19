from datetime import datetime, timezone

from app.core.celery import celery_app
from app.core.database import SessionLocal
from app.models.refresh_token import RefreshToken
from app.models.user import User


@celery_app.task
def cleanup_expired_refresh_tokens():
    db = SessionLocal()

    try:
        db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.now(timezone.utc)
        ).delete()

        db.commit()

    finally:
        db.close()