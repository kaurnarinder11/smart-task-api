# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base, get_db
import app.models  # noqa: F401 — registers User/Task with Base before create_all
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# StaticPool reuses a single connection so in-memory tables survive across sessions
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Shared session for the whole test run so module-level auth setup persists
_shared_session = TestingSessionLocal()

def override_get_db():
    yield _shared_session

# Apply immediately so module-level code in test files also uses the test DB
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    yield _shared_session
    _shared_session.rollback()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    _shared_session.close()
    Base.metadata.drop_all(bind=engine)
