"""
routes/transactions.py - All /transactions/* endpoints.
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=schemas.TransactionOut, status_code=201)
def add_transaction(data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """Add a new transaction with auto-categorization and duplicate detection."""
    return crud.create_transaction(db, data)


@router.get("/", response_model=List[schemas.TransactionOut])
def list_transactions(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    category: Optional[str] = None,
    transaction_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all transactions with optional filters."""
    return crud.get_transactions(db, month, year, category, transaction_type, search)


@router.get("/summary")
def get_summary(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Monthly summary grouped by category (expenses shown as positive values)."""
    return crud.get_summary(db, month, year)


@router.get("/export")
def export_csv(db: Session = Depends(get_db)):
    """Download all transactions as a CSV file."""
    csv_data = crud.export_csv(db)
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction by ID."""
    deleted = crud.delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found.")


@router.post("/bulk-delete")
def bulk_delete(tx_ids: List[int], db: Session = Depends(get_db)):
    """Delete multiple transactions at once."""
    count = crud.bulk_delete_transactions(db, tx_ids)
    return {"message": f"Successfully deleted {count} transactions."}


@router.patch("/{transaction_id}/reclassify", response_model=schemas.TransactionOut)
def reclassify(
    transaction_id: int,
    data: schemas.ReclassifyRequest,
    db: Session = Depends(get_db),
):
    """Manually override the auto-assigned category."""
    tx = crud.reclassify_transaction(db, transaction_id, data.category)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return tx
