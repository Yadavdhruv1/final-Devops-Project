"""
FinPilot Backend - Pydantic Schemas
"""
from datetime import date as date_type, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models import TransactionType, Category


# ─── Transaction Schemas ───


class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Monthly Salary"])
    amount: float = Field(..., gt=0, examples=[5000.00])
    type: TransactionType = Field(..., examples=["income"])
    category: Category = Field(..., examples=["salary"])
    description: Optional[str] = Field(None, max_length=500, examples=["October salary payment"])
    date: date_type = Field(default_factory=date_type.today)


class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[Category] = None
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[date_type] = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: float
    type: TransactionType
    category: Category
    description: Optional[str]
    date: date_type
    created_at: datetime
    updated_at: datetime


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    per_page: int


# ─── Budget Schemas ───


class BudgetCreate(BaseModel):
    category: Category = Field(..., examples=["food"])
    monthly_limit: float = Field(..., gt=0, examples=[500.00])
    month: int = Field(..., ge=1, le=12, examples=[10])
    year: int = Field(..., ge=2020, le=2100, examples=[2026])


class BudgetUpdate(BaseModel):
    monthly_limit: Optional[float] = Field(None, gt=0)
    month: Optional[int] = Field(None, ge=1, le=12)
    year: Optional[int] = Field(None, ge=2020, le=2100)


class BudgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: Category
    monthly_limit: float
    month: int
    year: int
    created_at: datetime
    updated_at: datetime


class BudgetWithSpending(BudgetResponse):
    spent: float = 0.0
    remaining: float = 0.0
    percentage_used: float = 0.0


# ─── Analytics Schemas ───


class CategorySummary(BaseModel):
    category: str
    total: float
    count: int
    percentage: float


class MonthlySummary(BaseModel):
    month: int
    year: int
    total_income: float
    total_expenses: float
    net_savings: float
    transaction_count: int


class DashboardOverview(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    transaction_count: int
    expense_by_category: List[CategorySummary]
    income_by_category: List[CategorySummary]
    monthly_trend: List[MonthlySummary]
    recent_transactions: List[TransactionResponse]


# ─── Health Schemas ───


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    details: Optional[str] = None
