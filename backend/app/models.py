"""
models.py - SQLAlchemy ORM models for all database tables.
"""
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False)           # negative for expenses
    description = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)  # "income" | "expense"
    category = Column(String, default="Other")
    auto_tagged = Column(Boolean, default=True)
    timestamp = Column(DateTime, server_default=func.now())
    note = Column(String, nullable=True)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String, nullable=False, unique=True)
    monthly_limit = Column(Float, nullable=False)


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    category = Column(String, default="Other")
    frequency = Column(String, nullable=False)   # daily, weekly, monthly
    next_due_date = Column(Date, nullable=True)


class SavingGoal(Base):
    __tablename__ = "saving_goals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)


class SavingsTransaction(Base):
    __tablename__ = "savings_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, nullable=False)  # "deposit" | "withdrawal"
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    goal_id = Column(Integer, nullable=True) # Optional link to a specific SavingGoal
    timestamp = Column(DateTime, server_default=func.now())
