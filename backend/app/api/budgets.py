"""
FinPilot Backend - Budget API Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    BudgetCreate, BudgetUpdate, BudgetResponse, BudgetWithSpending,
)
from app.services import budget_service

router = APIRouter(prefix="/api/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse, status_code=201)
def create_budget(payload: BudgetCreate, db: Session = Depends(get_db)):
    """Create a new monthly budget for a category."""
    try:
        return budget_service.create_budget(
            db=db,
            category=payload.category,
            monthly_limit=payload.monthly_limit,
            month=payload.month,
            year=payload.year,
        )
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail=f"Budget for category '{payload.category.value}' already exists"
            )
        raise


@router.get("/", response_model=list[BudgetResponse])
def list_budgets(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020, le=2100),
    db: Session = Depends(get_db),
):
    """List all budgets, optionally filtered by month/year."""
    return budget_service.list_budgets(db, month=month, year=year)


@router.get("/spending", response_model=list[BudgetWithSpending])
def get_budgets_with_spending(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2100),
    db: Session = Depends(get_db),
):
    """Get budgets with actual spending for a month."""
    return budget_service.get_budgets_with_spending(db, month=month, year=year)


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get a specific budget by ID."""
    budget = budget_service.get_budget(db, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
):
    """Update a budget by ID."""
    update_data = payload.model_dump(exclude_unset=True)
    budget = budget_service.update_budget(db, budget_id, **update_data)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.delete("/{budget_id}", status_code=204)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    """Delete a budget by ID."""
    deleted = budget_service.delete_budget(db, budget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Budget not found")
    return None
