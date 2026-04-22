"""
routes/dashboard.py - Dashboard, budget, and recurring transaction endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Response, HTTPException
from sqlalchemy.orm import Session
from app import utils
from app import crud
from app import schemas
from app.database import get_db

# ── Dashboard ─────────────────────────────────────────────────────────────────
dashboard_router = APIRouter(tags=["Dashboard"])


from typing import Optional
from fastapi import Query

@dashboard_router.get("/dashboard", response_model=schemas.DashboardOut)
def get_dashboard(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Return financial KPIs and recent activity."""
    return crud.get_dashboard(db, month, year)


# ── Budget ────────────────────────────────────────────────────────────────────
budget_router = APIRouter(prefix="/budget", tags=["Budget"])


@budget_router.post("/", response_model=schemas.BudgetOut, status_code=201)
def set_budget(data: schemas.BudgetCreate, db: Session = Depends(get_db)):
    """Create or update a monthly budget for a category."""
    return crud.create_budget(db, data)


@budget_router.get("/status", response_model=List[schemas.BudgetStatus])
def budget_status(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Return spending vs budget for each configured category."""
    return crud.get_budget_status(db, month, year)


# ── Recurring ─────────────────────────────────────────────────────────────────
recurring_router = APIRouter(prefix="/recurring", tags=["Recurring"])


@recurring_router.post("/", response_model=schemas.RecurringOut, status_code=201)
def create_recurring(data: schemas.RecurringCreate, db: Session = Depends(get_db)):
    """Create a recurring transaction template."""
    from app import scheduler
    rec = crud.create_recurring(db, data)
    # Immediately trigger processing so past-due items deduct instantly
    scheduler.process_recurring_transactions(db)
    # Refresh the local instance in case the scheduler bumped its next_due_date
    db.refresh(rec)
    return rec


@recurring_router.get("/", response_model=List[schemas.RecurringOut])
def list_recurring(db: Session = Depends(get_db)):
    """List all recurring transaction templates."""
    return crud.get_recurring(db)


@recurring_router.delete("/{rec_id}", status_code=204)
def delete_recurring(rec_id: int, db: Session = Depends(get_db)):
    """Cancel a recurring transaction template."""
    from fastapi import HTTPException
    success = crud.delete_recurring(db, rec_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recurring transaction not found.")
    return None

# ── Savings ──────────────────────────────────────────────────────────────────
savings_router = APIRouter(prefix="/savings", tags=["Savings"])

@savings_router.post("/", response_model=schemas.SavingGoalOut, status_code=201)
def create_saving_goal(data: schemas.SavingGoalCreate, db: Session = Depends(get_db)):
    return crud.create_saving_goal(db, data)

@savings_router.get("/", response_model=List[schemas.SavingGoalOut])
def list_saving_goals(db: Session = Depends(get_db)):
    return crud.get_saving_goals(db)

@savings_router.patch("/{goal_id}/add", response_model=schemas.SavingGoalOut)
def add_to_saving_goal(goal_id: int, data: schemas.SavingGoalAdd, db: Session = Depends(get_db)):
    return crud.add_to_saving_goal(db, goal_id, data.amount)

@savings_router.post("/deposit", response_model=schemas.SavingsTransactionOut)
def deposit_to_savings(data: schemas.SavingsTransactionCreate, db: Session = Depends(get_db)):
    return crud.deposit_to_savings(db, data)

@savings_router.post("/withdraw", response_model=schemas.SavingsTransactionOut)
def withdraw_from_savings(data: schemas.SavingsTransactionCreate, db: Session = Depends(get_db)):
    return crud.withdraw_from_savings(db, data)

@savings_router.get("/history", response_model=List[schemas.SavingsTransactionOut])
def get_savings_history(db: Session = Depends(get_db)):
    return crud.get_savings_history(db)

@savings_router.get("/balance", response_model=schemas.SavingsBalanceOut)
def get_savings_balance(db: Session = Depends(get_db)):
    return {"balance": crud.get_savings_balance(db)}

# ── Optimization & Gamification Endpoints ────────────────────────────────────

@dashboard_router.get("/optimization", response_model=List[schemas.OptimizationRecommendation])
def get_optimization_advice(db: Session = Depends(get_db)):
    return crud.get_optimization_advisor(db)

@dashboard_router.get("/gamification", response_model=schemas.GamificationStatus)
def get_gamification_stats(db: Session = Depends(get_db)):
    return crud.get_gamification_status(db)

# ── CSV & PDF Reports ───────────────────────────────────────────────────────

@dashboard_router.post("/csv/import")
def import_transactions_csv(
    file: UploadFile = File(...), 
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        contents = file.file.read()
        records = utils.parse_csv_stream(contents, month=month, year=year)
        count = crud.bulk_create_transactions(db, records)
        return {"message": f"Successfully imported {count} transactions."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV Import failed: {str(e)}")

@dashboard_router.get("/report/pdf")
def download_pdf_report(db: Session = Depends(get_db)):
    dashboard_data = crud.get_dashboard(db)
    summary_data = crud.get_summary(db)
    savings_data = crud.get_saving_goals(db)
    
    pdf_bytes = utils.generate_pdf_report(dashboard_data, summary_data, savings_data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Financial_Report.pdf"}
    )
