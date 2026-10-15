"""
FinPilot Backend - Transaction Service Layer
"""
from datetime import date
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from app.models import Transaction, TransactionType, Category


def create_transaction(db: Session, title: str, amount: float,
                       type: TransactionType, category: Category,
                       description: Optional[str] = None,
                       txn_date: Optional[date] = None) -> Transaction:
    """Create a new transaction."""
    transaction = Transaction(
        title=title,
        amount=amount,
        type=type,
        category=category,
        description=description,
        date=txn_date or date.today()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    """Get a single transaction by ID."""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def list_transactions(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    type_filter: Optional[TransactionType] = None,
    category_filter: Optional[Category] = None,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Tuple[List[Transaction], int]:
    """List transactions with filtering, search, and pagination."""
    query = db.query(Transaction)

    if type_filter:
        query = query.filter(Transaction.type == type_filter)
    if category_filter:
        query = query.filter(Transaction.category == category_filter)
    if search:
        query = query.filter(Transaction.title.ilike(f"%{search}%"))
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    total = query.count()
    transactions = (
        query.order_by(Transaction.date.desc(), Transaction.id.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return transactions, total


def update_transaction(db: Session, transaction_id: int, **kwargs) -> Optional[Transaction]:
    """Update a transaction by ID."""
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return None

    for key, value in kwargs.items():
        if value is not None:
            setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction_id: int) -> bool:
    """Delete a transaction by ID."""
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return False
    db.delete(transaction)
    db.commit()
    return True


def get_category_summary(
    db: Session, type_filter: TransactionType,
    month: Optional[int] = None, year: Optional[int] = None
) -> list:
    """Get spending/income summary by category."""
    query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).filter(Transaction.type == type_filter)

    if month and year:
        query = query.filter(
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year
        )

    results = query.group_by(Transaction.category).all()
    grand_total = sum(r.total for r in results) or 1

    return [
        {
            "category": r.category.value,
            "total": round(r.total, 2),
            "count": r.count,
            "percentage": round((r.total / grand_total) * 100, 2)
        }
        for r in results
    ]


def get_monthly_trend(db: Session, limit: int = 6) -> list:
    """Get monthly income/expense trend."""
    income_sub = (
        db.query(
            extract("month", Transaction.date).label("month"),
            extract("year", Transaction.date).label("year"),
            func.sum(Transaction.amount).label("total_income"),
        )
        .filter(Transaction.type == TransactionType.INCOME)
        .group_by("year", "month")
        .subquery()
    )

    expense_sub = (
        db.query(
            extract("month", Transaction.date).label("month"),
            extract("year", Transaction.date).label("year"),
            func.sum(Transaction.amount).label("total_expenses"),
            func.count(Transaction.id).label("txn_count"),
        )
        .filter(Transaction.type == TransactionType.EXPENSE)
        .group_by("year", "month")
        .subquery()
    )

    # Simpler approach: query all transactions grouped by month/year
    results = (
        db.query(
            extract("month", Transaction.date).label("month"),
            extract("year", Transaction.date).label("year"),
            func.sum(
                case(
                    (Transaction.type == TransactionType.INCOME, Transaction.amount),
                    else_=0
                )
            ).label("total_income"),
            func.sum(
                case(
                    (Transaction.type == TransactionType.EXPENSE, Transaction.amount),
                    else_=0
                )
            ).label("total_expenses"),
            func.count(Transaction.id).label("transaction_count"),
        )
        .group_by("year", "month")
        .order_by(extract("year", Transaction.date).desc(), extract("month", Transaction.date).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "month": int(r.month),
            "year": int(r.year),
            "total_income": round(float(r.total_income), 2),
            "total_expenses": round(float(r.total_expenses), 2),
            "net_savings": round(float(r.total_income) - float(r.total_expenses), 2),
            "transaction_count": r.transaction_count,
        }
        for r in results
    ]


def get_totals(db: Session) -> dict:
    """Get total income, expenses, and balance."""
    income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.type == TransactionType.INCOME
    ).scalar()

    expenses = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.type == TransactionType.EXPENSE
    ).scalar()

    count = db.query(func.count(Transaction.id)).scalar()

    return {
        "total_income": round(float(income), 2),
        "total_expenses": round(float(expenses), 2),
        "net_balance": round(float(income) - float(expenses), 2),
        "transaction_count": count,
    }
