"""Initial schema - transactions and budgets

Revision ID: 001_initial
Revises: None
Create Date: 2026-10-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create transaction type enum
    transaction_type = sa.Enum(
        "income", "expense",
        name="transactiontype",
        create_type=True,
    )

    # Create category enum
    category = sa.Enum(
        "salary", "freelance", "investment",
        "food", "transport", "housing", "utilities",
        "entertainment", "healthcare", "education",
        "shopping", "travel", "insurance", "savings", "other",
        name="category",
        create_type=True,
    )

    # Create transactions table
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False, index=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("type", transaction_type, nullable=False, index=True),
        sa.Column("category", category, nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("amount > 0", name="positive_amount"),
    )

    # Create budgets table
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("category", category, nullable=False, unique=True),
        sa.Column("monthly_limit", sa.Float(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("monthly_limit > 0", name="positive_budget_limit"),
        sa.CheckConstraint("month >= 1 AND month <= 12", name="valid_month"),
    )


def downgrade() -> None:
    op.drop_table("budgets")
    op.drop_table("transactions")
    sa.Enum(name="category").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="transactiontype").drop(op.get_bind(), checkfirst=True)
