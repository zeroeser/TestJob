from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mptt import mptt_sessionmaker

from app.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = mptt_sessionmaker(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
