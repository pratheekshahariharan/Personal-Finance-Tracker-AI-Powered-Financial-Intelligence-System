"""
schemas.py - Pydantic models for request/response validation.
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, date


# ── Transaction schemas ──────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    amount: float
    description: str
    transaction_type: str  # "income" | "expense"
    note: Optional[str] = None
    timestamp: Optional[datetime] = None

    @field_validator("transaction_type")
    @classmethod
    def validate_type(cls, v):
        if v not in ("income", "expense"):
            raise ValueError("transaction_type must be 'income' or 'expense'")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount must be a positive number")
        return v


class TransactionOut(BaseModel):
    id: int
    amount: float
    description: str
    transaction_type: str
    category: str
    auto_tagged: bool
    timestamp: datetime
    note: Optional[str] = None

    model_config = {"from_attributes": True}


class ReclassifyRequest(BaseModel):
    category: str


# ── Budget schemas ───────────────────────────────────────────────────────────

class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float

    @field_validator("monthly_limit")
    @classmethod
    def validate_limit(cls, v):
        if v <= 0:
            raise ValueError("monthly_limit must be positive")
        return v


class BudgetOut(BaseModel):
    id: int
    category: str
    monthly_limit: float

    model_config = {"from_attributes": True}


class BudgetStatus(BaseModel):
    category: str
    monthly_limit: float
    current_spending: float
    projected_spending: float
    days_left: int
    exceeded: bool


# ── Recurring schemas ────────────────────────────────────────────────────────

class RecurringCreate(BaseModel):
    description: str
    amount: float
    transaction_type: str
    frequency: str          # daily | weekly | monthly
    next_due_date: Optional[date] = None

    @field_validator("transaction_type")
    @classmethod
    def validate_type(cls, v):
        if v not in ("income", "expense"):
            raise ValueError("transaction_type must be 'income' or 'expense'")
        return v

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, v):
        if v not in ("daily", "weekly", "monthly"):
            raise ValueError("frequency must be daily, weekly, or monthly")
        return v


class RecurringOut(BaseModel):
    id: int
    description: str
    amount: float
    transaction_type: str
    category: str
    frequency: str
    next_due_date: Optional[date] = None

    model_config = {"from_attributes": True}


# ── Dashboard schemas ────────────────────────────────────────────────────────

class DashboardOut(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    total_savings: float
    monthly_income: float
    monthly_expenses: float
    carried_savings: float
    total_transactions: int
    top_spending_category: Optional[str]
    recent_activity: List[TransactionOut]


# ── Summary schemas ──────────────────────────────────────────────────────────

class SummaryItem(BaseModel):
    month: str
    category: str
    total: float


# ── Savings schemas ──────────────────────────────────────────────────────────

class SavingGoalCreate(BaseModel):
    name: str
    target_amount: float

    @field_validator("target_amount")
    @classmethod
    def validate_target(cls, v):
        if v <= 0:
            raise ValueError("target_amount must be greater than 0")
        return v


class SavingGoalOut(BaseModel):
    id: int
    name: str
    target_amount: float
    current_amount: float

    model_config = {"from_attributes": True}


class SavingGoalAdd(BaseModel):
    amount: float

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

class SavingsTransactionCreate(BaseModel):
    amount: float
    reason: Optional[str] = None
    goal_id: Optional[int] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

class SavingsTransactionOut(BaseModel):
    id: int
    type: str
    amount: float
    reason: Optional[str]
    goal_id: Optional[int]
    timestamp: datetime

    model_config = {"from_attributes": True}

class SavingsBalanceOut(BaseModel):
    balance: float

# ── Optimization & Gamification ──────────────────────────────────────────

class OptimizationRecommendation(BaseModel):
    category: str
    count: int
    potential_monthly_savings: float
    message: str

class Badge(BaseModel):
    name: str
    icon: str
    description: str
    unlocked: bool

class GamificationStatus(BaseModel):
    streak_days: int
    badges: List[Badge]
    savings_progress: float  # overall savings efficiency
