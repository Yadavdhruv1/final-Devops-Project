"""
FinPilot Backend - SQLAlchemy Models
"""
import enum
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    Enum as SQLEnum, Text, CheckConstraint
)
from app.database import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(str, enum.Enum):
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SHOPPING = "shopping"
    TRAVEL = "travel"
    INSURANCE = "insurance"
    SAVINGS = "savings"
    OTHER = "other"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False, index=True)
    category = Column(SQLEnum(Category), nullable=False, index=True)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0", name="positive_amount"),
    )


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(SQLEnum(Category), nullable=False, unique=True)
    monthly_limit = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("monthly_limit > 0", name="positive_budget_limit"),
        CheckConstraint("month >= 1 AND month <= 12", name="valid_month"),
    )
