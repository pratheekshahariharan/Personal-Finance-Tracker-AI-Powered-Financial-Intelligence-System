"""
crud.py - Database CRUD helpers used by route handlers.
"""
import csv
import io
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.categorizer import auto_categorize, validate_category_type


# ── Transactions ─────────────────────────────────────────────────────────────

def create_transaction(db: Session, data: schemas.TransactionCreate) -> models.Transaction:
    category = auto_categorize(data.description)
    validate_category_type(category, data.transaction_type)

    # Duplicate detection: same amount + description within 5 minutes
    cutoff = datetime.utcnow() - timedelta(minutes=5)
    lookup_amount = -data.amount if data.transaction_type == "expense" else data.amount
    duplicate = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.amount == lookup_amount,
            func.lower(models.Transaction.description) == data.description.lower(),
            models.Transaction.timestamp >= cutoff,
        )
        .first()
    )
    if duplicate:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Duplicate transaction detected within 5 minutes.")

    # Store expenses as negative values
    stored_amount = -data.amount if data.transaction_type == "expense" else data.amount

    tx = models.Transaction(
        amount=stored_amount,
        description=data.description,
        transaction_type=data.transaction_type,
        category=category,
        auto_tagged=True,
        note=data.note,
        timestamp=data.timestamp if data.timestamp else datetime.utcnow(),
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_transactions(
    db: Session,
    month: Optional[int] = None,
    year: Optional[int] = None,
    category: Optional[str] = None,
    transaction_type: Optional[str] = None,
    search: Optional[str] = None,
):
    q = db.query(models.Transaction)
    if month:
        q = q.filter(extract("month", models.Transaction.timestamp) == month)
    if year:
        q = q.filter(extract("year", models.Transaction.timestamp) == year)
    if category:
        q = q.filter(models.Transaction.category == category)
    if transaction_type:
        q = q.filter(models.Transaction.transaction_type == transaction_type)
    if search:
        q = q.filter(models.Transaction.description.ilike(f"%{search}%"))
    return q.order_by(models.Transaction.timestamp.desc()).all()


def get_transaction(db: Session, tx_id: int) -> Optional[models.Transaction]:
    return db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()


def delete_transaction(db: Session, tx_id: int) -> bool:
    tx = get_transaction(db, tx_id)
    if not tx:
        return False
    db.delete(tx)
    db.commit()
    return True


def bulk_delete_transactions(db: Session, tx_ids: list[int]) -> int:
    count = db.query(models.Transaction).filter(models.Transaction.id.in_(tx_ids)).delete(synchronize_session=False)
    db.commit()
    return count


def reclassify_transaction(db: Session, tx_id: int, category: str) -> Optional[models.Transaction]:
    tx = get_transaction(db, tx_id)
    if not tx:
        return None
    tx.category = category
    tx.auto_tagged = False
    db.commit()
    db.refresh(tx)
    return tx


def get_summary(db: Session, month: Optional[int] = None, year: Optional[int] = None):
    """Period-specific summary grouped by category; expenses shown as positive."""
    q = db.query(
        func.strftime("%Y-%m", models.Transaction.timestamp).label("month"),
        models.Transaction.category,
        func.sum(models.Transaction.amount).label("total"),
    )
    
    if month:
        q = q.filter(extract("month", models.Transaction.timestamp) == month)
    if year:
        q = q.filter(extract("year", models.Transaction.timestamp) == year)
        
    rows = q.group_by(func.strftime("%Y-%m", models.Transaction.timestamp), models.Transaction.category).all()
    
    return [
        {"month": r.month, "category": r.category, "total": r.total}
        for r in rows
    ]


def get_dashboard(db: Session, month: Optional[int] = None, year: Optional[int] = None) -> dict:
    txs = db.query(models.Transaction).all()
    
    # Metrics anchored to target date
    now = datetime.utcnow()
    target_month = month if month is not None else now.month
    target_year = year if year is not None else now.year
    
    # Calculate balance *at the end* of target month for true Time Travel
    from calendar import monthrange
    _, last_day = monthrange(target_year, target_month)
    end_of_period = datetime(target_year, target_month, last_day, 23, 59, 59)
    
    income = sum(t.amount for t in txs if t.transaction_type == "income" and t.timestamp <= end_of_period)
    expenses = sum(-t.amount for t in txs if t.transaction_type == "expense" and t.timestamp <= end_of_period)

    # Historical Savings Balance at end of period
    total_savings = get_savings_balance(db, as_of=end_of_period)

    # Top spending category for that month
    spending_row = (
        db.query(
            models.Transaction.category,
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(
            models.Transaction.transaction_type == "expense",
            extract("month", models.Transaction.timestamp) == target_month,
            extract("year", models.Transaction.timestamp) == target_year,
        )
        .group_by(models.Transaction.category)
        .order_by(func.sum(models.Transaction.amount))
        .first()
    )
    top_cat = spending_row.category if spending_row else "None"

    recent = (
        db.query(models.Transaction)
        .filter(models.Transaction.timestamp <= end_of_period)
        .order_by(models.Transaction.timestamp.desc())
        .limit(5)
        .all()
    )


    # Monthly Metrics (Current Pulse)
    m_inc = sum(t.amount for t in txs if t.transaction_type == "income" 
                and t.timestamp.month == target_month and t.timestamp.year == target_year)
    m_exp = sum(-t.amount for t in txs if t.transaction_type == "expense" 
                and t.timestamp.month == target_month and t.timestamp.year == target_year)
    
    # Retained savings up to the *previous* month
    try:
        first_of_month = datetime(target_year, target_month, 1)
        inc_before = sum(t.amount for t in txs if (t.transaction_type == "income" and t.timestamp < first_of_month))
        exp_before = sum(abs(t.amount) for t in txs if (t.transaction_type == "expense" and t.timestamp < first_of_month))
        carried = inc_before - exp_before
    except Exception:
        carried = 0

    return {
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "total_savings": round(total_savings, 2),
        "monthly_income": round(m_inc, 2),
        "monthly_expenses": round(m_exp, 2),
        "carried_savings": round(carried, 2),
        "total_transactions": len(txs),
        "top_spending_category": top_cat,
        "recent_activity": recent,
    }


def export_csv(db: Session) -> str:
    txs = db.query(models.Transaction).order_by(models.Transaction.timestamp.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "description", "amount", "transaction_type", "category", "auto_tagged", "timestamp", "note"])
    for t in txs:
        writer.writerow([t.id, t.description, t.amount, t.transaction_type, t.category, t.auto_tagged, t.timestamp, t.note])
    return output.getvalue()


# ── Budgets ──────────────────────────────────────────────────────────────────

def create_budget(db: Session, data: schemas.BudgetCreate) -> models.Budget:
    existing = db.query(models.Budget).filter(models.Budget.category == data.category).first()
    if existing:
        existing.monthly_limit = data.monthly_limit
        db.commit()
        db.refresh(existing)
        return existing
    budget = models.Budget(category=data.category, monthly_limit=data.monthly_limit)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budget_status(db: Session, month: Optional[int] = None, year: Optional[int] = None):
    budgets = db.query(models.Budget).all()
    now = datetime.utcnow()
    target_month = month if month is not None else now.month
    target_year = year if year is not None else now.year
    
    from calendar import monthrange
    _, total_days = monthrange(target_year, target_month)
    
    # If viewing current month, use today's day; otherwise use total days
    is_current = (target_month == now.month and target_year == now.year)
    days_passed = now.day if is_current else total_days
    days_left = (total_days - now.day) if is_current else 0

    result = []
    for b in budgets:
        spent_row = (
            db.query(func.sum(models.Transaction.amount))
            .filter(
                models.Transaction.category == b.category,
                models.Transaction.transaction_type == "expense",
                extract("month", models.Transaction.timestamp) == target_month,
                extract("year", models.Transaction.timestamp) == target_year,
            )
            .scalar()
        )
        spent = -(spent_row or 0)
        
        # Predictive calculation: (Spent / Days Passed) * Total Days
        projected = (spent / days_passed) * total_days if days_passed > 0 else 0
        
        result.append({
            "category": b.category,
            "monthly_limit": b.monthly_limit,
            "current_spending": round(spent, 2),
            "projected_spending": round(projected, 2),
            "days_left": days_left,
            "exceeded": spent > b.monthly_limit,
        })
    return result


# ── Recurring ────────────────────────────────────────────────────────────────

def create_recurring(db: Session, data: schemas.RecurringCreate) -> models.RecurringTransaction:
    category = auto_categorize(data.description)
    rec = models.RecurringTransaction(
        description=data.description,
        amount=data.amount,
        transaction_type=data.transaction_type,
        category=category,
        frequency=data.frequency,
        next_due_date=data.next_due_date,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def get_recurring(db: Session):
    return db.query(models.RecurringTransaction).all()


def delete_recurring(db: Session, rec_id: int) -> bool:
    rec = db.query(models.RecurringTransaction).filter(models.RecurringTransaction.id == rec_id).first()
    if not rec:
        return False
    db.delete(rec)
    db.commit()
    return True

# ── Savings ──────────────────────────────────────────────────────────────────

def create_saving_goal(db: Session, data: schemas.SavingGoalCreate):
    from fastapi import HTTPException
    existing = db.query(models.SavingGoal).filter(models.SavingGoal.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Saving goal with this name already exists")
    sg = models.SavingGoal(name=data.name, target_amount=data.target_amount)
    db.add(sg)
    db.commit()
    db.refresh(sg)
    return sg

def get_saving_goals(db: Session):
    return db.query(models.SavingGoal).all()

def add_to_saving_goal(db: Session, goal_id: int, amount: float):
    from fastapi import HTTPException
    sg = db.query(models.SavingGoal).filter(models.SavingGoal.id == goal_id).first()
    if not sg:
        raise HTTPException(status_code=404, detail="Saving goal not found.")
    sg.current_amount += amount
    db.commit()
    db.refresh(sg)
    return sg

# ── New Savings Features ─────────────────────────────────────────────────────

def get_savings_balance(db: Session, as_of: datetime = None) -> float:
    # Source of truth: sum of all savings transactions
    deposit_query = db.query(func.sum(models.SavingsTransaction.amount)).filter(models.SavingsTransaction.type == "deposit")
    withdraw_query = db.query(func.sum(models.SavingsTransaction.amount)).filter(models.SavingsTransaction.type == "withdrawal")
    
    if as_of:
        deposit_query = deposit_query.filter(models.SavingsTransaction.timestamp <= as_of)
        withdraw_query = withdraw_query.filter(models.SavingsTransaction.timestamp <= as_of)
        
    deposit_sum = deposit_query.scalar() or 0.0
    withdraw_sum = withdraw_query.scalar() or 0.0
    return deposit_sum - withdraw_sum

def deposit_to_savings(db: Session, data: schemas.SavingsTransactionCreate) -> models.SavingsTransaction:
    # 1. Prepare Savings Transaction
    tx = models.SavingsTransaction(
        type="deposit",
        amount=data.amount,
        reason=data.reason,
        goal_id=data.goal_id,
        timestamp=datetime.utcnow()
    )
    db.add(tx)
    
    # 2. Update Goal Progress (Manual update to avoid nested commits)
    goal_name = ""
    if data.goal_id:
        goal = db.query(models.SavingGoal).filter(models.SavingGoal.id == data.goal_id).first()
        if goal:
            goal.current_amount += data.amount
            goal_name = f" ({goal.name})"
        else:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Saving goal not found.")
        
    # 3. Create shadow transaction for metrics
    shadow_tx = models.Transaction(
        amount=-data.amount, # Expense
        description=f"Savings Deposit{goal_name}",
        transaction_type="expense",
        category="Savings",
        auto_tagged=False,
        timestamp=tx.timestamp
    )
    db.add(shadow_tx)

    db.commit()
    db.refresh(tx)
    return tx

def withdraw_from_savings(db: Session, data: schemas.SavingsTransactionCreate) -> models.SavingsTransaction:
    balance = get_savings_balance(db)
    if data.amount > balance:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Insufficient savings balance")
    
    # 1. Prepare Withdrawal Transaction
    tx = models.SavingsTransaction(
        type="withdrawal",
        amount=data.amount,
        reason=data.reason,
        goal_id=data.goal_id,
        timestamp=datetime.utcnow()
    )
    db.add(tx)

    # 2. Update Goal Progress (Manual update to avoid nested commits)
    goal_name = ""
    if data.goal_id:
        goal = db.query(models.SavingGoal).filter(models.SavingGoal.id == data.goal_id).first()
        if not goal:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Saving goal not found.")
        if goal.current_amount < data.amount:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=f"Insufficient funds in goal: {goal.name}")
        
        goal.current_amount -= data.amount
        goal_name = f" ({goal.name})"

    # 3. Create shadow transaction for metrics
    shadow_tx = models.Transaction(
        amount=data.amount, # Positive amount in 'expense' column reduces total expenditure
        description=f"Savings Withdrawal{goal_name}",
        transaction_type="expense",
        category="Savings",
        auto_tagged=False,
        timestamp=tx.timestamp
    )
    db.add(shadow_tx)

    db.commit()
    db.refresh(tx)
    return tx

def get_savings_history(db: Session) -> list[models.SavingsTransaction]:
    return db.query(models.SavingsTransaction).order_by(models.SavingsTransaction.timestamp.desc()).all()

# ── Expansion Features (Optimization, Gamification, Bulk) ────────────────────

def get_optimization_advisor(db: Session):
    """Detect overlapping subscriptions and calculate potential savings."""
    recs = []
    
    # 1. Global Analysis
    all_subs = db.query(models.RecurringTransaction).filter(models.RecurringTransaction.transaction_type == "expense").all()
    if all_subs:
        total_monthly = sum(s.amount for s in all_subs)
        recs.append(schemas.OptimizationRecommendation(
            category="Global Audit",
            count=len(all_subs),
            potential_monthly_savings=0.0,
            message=f"I've analyzed all your {len(all_subs)} active subscriptions. You are spending ₹{total_monthly:,.0f} every month."
        ))

    # 2. Redundancy Analysis (Group by category)
    from sqlalchemy import func
    groups = (
        db.query(models.RecurringTransaction.category, func.count(models.RecurringTransaction.id).label("count"))
        .group_by(models.RecurringTransaction.category)
        .having(func.count(models.RecurringTransaction.id) > 1)
        .all()
    )

    for cat, count in groups:
        subs = db.query(models.RecurringTransaction).filter(models.RecurringTransaction.category == cat).all()
        # Find the one to keep (cheapest for advisor logic or just first)
        subs_sorted = sorted(subs, key=lambda x: x.amount)
        potential_savings = sum(s.amount for s in subs_sorted[:-1]) 
        
        recs.append(schemas.OptimizationRecommendation(
            category=cat,
            count=count,
            potential_monthly_savings=potential_savings,
            message=f"You have {count} subscriptions for {cat}. Cancelling redundant ones could save you ₹{potential_savings} monthly!"
        ))
    return recs

def get_gamification_status(db: Session):
    """(Deprecated) Returns an empty status as gamification features were removed."""
    return schemas.GamificationStatus(
        streak_days=0,
        badges=[],
        savings_progress=0.0
    )

def bulk_create_transactions(db: Session, records: list):
    count = 0
    errors = 0
    for r in records:
        try:
            # Re-use create_transaction logic for categorization
            schemas_obj = schemas.TransactionCreate(**r)
            create_transaction(db, schemas_obj)
            count += 1
        except Exception as e:
            import logging
            logging.error(f"Bulk import row failed: {e}")
            errors += 1
            continue
    return count
