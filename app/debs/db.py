from typing import AsyncGenerator

from app.db.session import SessionLocal


async def get_db() -> AsyncGenerator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()
