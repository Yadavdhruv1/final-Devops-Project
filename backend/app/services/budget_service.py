"""
FinPilot Backend - Budget Service Layer
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models import Budget, Transaction, TransactionType, Category


def create_budget(db: Session, category: Category, monthly_limit: float,
                  month: int, year: int) -> Budget:
    """Create a new budget."""
    budget = Budget(
        category=category,
        monthly_limit=monthly_limit,
        month=month,
        year=year
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budget(db: Session, budget_id: int) -> Optional[Budget]:
    """Get a single budget by ID."""
    return db.query(Budget).filter(Budget.id == budget_id).first()


def list_budgets(db: Session, month: Optional[int] = None,
                 year: Optional[int] = None) -> List[Budget]:
    """List budgets, optionally filtered by month/year."""
    query = db.query(Budget)
    if month:
        query = query.filter(Budget.month == month)
    if year:
        query = query.filter(Budget.year == year)
    return query.order_by(Budget.category).all()


def update_budget(db: Session, budget_id: int, **kwargs) -> Optional[Budget]:
    """Update a budget by ID."""
    budget = get_budget(db, budget_id)
    if not budget:
        return None

    for key, value in kwargs.items():
        if value is not None:
            setattr(budget, key, value)

    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget_id: int) -> bool:
    """Delete a budget by ID."""
    budget = get_budget(db, budget_id)
    if not budget:
        return False
    db.delete(budget)
    db.commit()
    return True


def get_budgets_with_spending(db: Session, month: int, year: int) -> list:
    """Get budgets with actual spending for a given month/year."""
    budgets = list_budgets(db, month=month, year=year)
    result = []

    for budget in budgets:
        spent = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.category == budget.category,
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year
        ).scalar()

        spent = float(spent)
        remaining = max(0, budget.monthly_limit - spent)
        pct = round((spent / budget.monthly_limit) * 100, 2) if budget.monthly_limit > 0 else 0

        result.append({
            "id": budget.id,
            "category": budget.category,
            "monthly_limit": budget.monthly_limit,
            "month": budget.month,
            "year": budget.year,
            "created_at": budget.created_at,
            "updated_at": budget.updated_at,
            "spent": round(spent, 2),
            "remaining": round(remaining, 2),
            "percentage_used": pct,
        })

    return result
