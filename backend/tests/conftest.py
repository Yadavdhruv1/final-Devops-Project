"""
FinPilot Test Configuration — conftest.py

Uses an isolated SQLite in-memory database to avoid polluting production data.
Provides a FastAPI TestClient that overrides the database dependency.
"""
import os
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Use SQLite in-memory for test isolation (no PostgreSQL required in CI)
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency with test database."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create all tables before each test and drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client():
    """Provide a FastAPI test client with overridden database."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_transaction():
    """Sample transaction data for testing."""
    return {
        "title": "Monthly Salary",
        "amount": 5000.00,
        "type": "income",
        "category": "salary",
        "description": "October salary payment",
        "date": "2026-10-15",
    }


@pytest.fixture
def sample_expense():
    """Sample expense data for testing."""
    return {
        "title": "Grocery Shopping",
        "amount": 150.50,
        "type": "expense",
        "category": "food",
        "description": "Weekly groceries",
        "date": "2026-10-14",
    }


@pytest.fixture
def sample_budget():
    """Sample budget data for testing."""
    return {
        "category": "food",
        "monthly_limit": 500.00,
        "month": 10,
        "year": 2026,
    }
