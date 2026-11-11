import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database.models import Base
from database import store


@pytest.fixture
def sandbox_db(monkeypatch):
    """Every test uses an isolated in-memory database; no user data is touched."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    monkeypatch.setattr(store, "Session", sessionmaker(bind=engine, expire_on_commit=False))
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()
