"""
FinPilot Backend - Transaction API Routes
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TransactionType, Category
from app.schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    TransactionListResponse,
)
from app.services import transaction_service

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new financial transaction."""
    return transaction_service.create_transaction(
        db=db,
        title=payload.title,
        amount=payload.amount,
        type=payload.type,
        category=payload.category,
        description=payload.description,
        txn_date=payload.date,
    )


@router.get("/", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: Optional[TransactionType] = None,
    category: Optional[Category] = None,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    """List transactions with optional filtering and pagination."""
    transactions, total = transaction_service.list_transactions(
        db=db,
        page=page,
        per_page=per_page,
        type_filter=type,
        category_filter=category,
        search=search,
        start_date=start_date,
        end_date=end_date,
    )
    return TransactionListResponse(
        transactions=transactions,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID."""
    txn = transaction_service.get_transaction(db, transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Update a transaction by ID."""
    update_data = payload.model_dump(exclude_unset=True)
    if "date" in update_data:
        update_data["date"] = update_data.pop("date")

    txn = transaction_service.update_transaction(db, transaction_id, **update_data)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction by ID."""
    deleted = transaction_service.delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None
