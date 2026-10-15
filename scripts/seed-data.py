"""
FinPilot - Seed Sample Financial Data
Usage: python scripts/seed-data.py
Requires DATABASE_URL environment variable.
"""
import os
import sys
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, engine, Base
from app.models import Transaction, Budget, TransactionType, Category

INCOME_CATEGORIES = [Category.SALARY, Category.FREELANCE, Category.INVESTMENT]
EXPENSE_CATEGORIES = [
    Category.FOOD, Category.TRANSPORT, Category.HOUSING, Category.UTILITIES,
    Category.ENTERTAINMENT, Category.HEALTHCARE, Category.SHOPPING, Category.TRAVEL,
]

INCOME_TITLES = [
    ("Monthly Salary", 4500, 6000),
    ("Freelance Project", 500, 2000),
    ("Investment Dividend", 100, 800),
]

EXPENSE_TITLES = {
    Category.FOOD: [("Grocery Shopping", 50, 200), ("Restaurant Dinner", 20, 80), ("Coffee Shop", 5, 15)],
    Category.TRANSPORT: [("Gas Station", 30, 70), ("Uber Ride", 10, 35), ("Bus Pass", 40, 60)],
    Category.HOUSING: [("Monthly Rent", 1200, 1800), ("Home Repair", 50, 300)],
    Category.UTILITIES: [("Electric Bill", 60, 150), ("Internet Bill", 40, 80), ("Water Bill", 20, 50)],
    Category.ENTERTAINMENT: [("Movie Tickets", 15, 40), ("Streaming Service", 10, 20), ("Concert", 50, 150)],
    Category.HEALTHCARE: [("Doctor Visit", 30, 150), ("Pharmacy", 10, 60)],
    Category.SHOPPING: [("Clothing", 30, 200), ("Electronics", 50, 500), ("Home Decor", 20, 100)],
    Category.TRAVEL: [("Flight Ticket", 200, 800), ("Hotel Stay", 80, 250)],
}


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(Transaction).count()
        if existing > 0:
            print(f"Database already has {existing} transactions. Skipping seed.")
            return

        transactions = []
        today = date.today()

        # Generate 6 months of data
        for month_offset in range(6):
            month_start = today.replace(day=1) - timedelta(days=30 * month_offset)

            # Income
            for title, low, high in INCOME_TITLES:
                txn_date = month_start + timedelta(days=random.randint(0, 27))
                transactions.append(Transaction(
                    title=title,
                    amount=round(random.uniform(low, high), 2),
                    type=TransactionType.INCOME,
                    category=random.choice(INCOME_CATEGORIES),
                    description=f"Auto-generated sample data",
                    date=txn_date,
                ))

            # Expenses (5-10 per month)
            for _ in range(random.randint(5, 10)):
                cat = random.choice(EXPENSE_CATEGORIES)
                title, low, high = random.choice(EXPENSE_TITLES[cat])
                txn_date = month_start + timedelta(days=random.randint(0, 27))
                transactions.append(Transaction(
                    title=title,
                    amount=round(random.uniform(low, high), 2),
                    type=TransactionType.EXPENSE,
                    category=cat,
                    description=f"Auto-generated sample data",
                    date=txn_date,
                ))

        db.add_all(transactions)

        # Add sample budgets for current month
        budgets = [
            Budget(category=Category.FOOD, monthly_limit=500, month=today.month, year=today.year),
            Budget(category=Category.TRANSPORT, monthly_limit=200, month=today.month, year=today.year),
            Budget(category=Category.ENTERTAINMENT, monthly_limit=150, month=today.month, year=today.year),
            Budget(category=Category.SHOPPING, monthly_limit=300, month=today.month, year=today.year),
        ]
        db.add_all(budgets)
        db.commit()

        print(f"✅ Seeded {len(transactions)} transactions and {len(budgets)} budgets")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
