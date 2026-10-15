"""
FinPilot Backend - Analytics API Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TransactionType
from app.schemas import DashboardOverview, CategorySummary, MonthlySummary
from app.services import transaction_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardOverview)
def get_dashboard(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020, le=2100),
    db: Session = Depends(get_db),
):
    """Get dashboard overview with totals, category breakdowns, and trends."""
    totals = transaction_service.get_totals(db)
    expense_by_cat = transaction_service.get_category_summary(
        db, TransactionType.EXPENSE, month=month, year=year
    )
    income_by_cat = transaction_service.get_category_summary(
        db, TransactionType.INCOME, month=month, year=year
    )
    monthly_trend = transaction_service.get_monthly_trend(db, limit=6)
    recent, _ = transaction_service.list_transactions(db, page=1, per_page=5)

    return DashboardOverview(
        total_income=totals["total_income"],
        total_expenses=totals["total_expenses"],
        net_balance=totals["net_balance"],
        transaction_count=totals["transaction_count"],
        expense_by_category=expense_by_cat,
        income_by_category=income_by_cat,
        monthly_trend=monthly_trend,
        recent_transactions=recent,
    )


@router.get("/categories/expenses", response_model=list[CategorySummary])
def get_expense_categories(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020, le=2100),
    db: Session = Depends(get_db),
):
    """Get expense breakdown by category."""
    return transaction_service.get_category_summary(
        db, TransactionType.EXPENSE, month=month, year=year
    )


@router.get("/categories/income", response_model=list[CategorySummary])
def get_income_categories(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020, le=2100),
    db: Session = Depends(get_db),
):
    """Get income breakdown by category."""
    return transaction_service.get_category_summary(
        db, TransactionType.INCOME, month=month, year=year
    )


@router.get("/trends", response_model=list[MonthlySummary])
def get_monthly_trends(
    limit: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
):
    """Get monthly income/expense trends."""
    return transaction_service.get_monthly_trend(db, limit=limit)
