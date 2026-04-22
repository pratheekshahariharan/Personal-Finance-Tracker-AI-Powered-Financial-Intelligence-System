"""
scheduler.py - Polls Recurring Transactions to execute them on their due dates.
"""
import asyncio
import logging
from datetime import date, timedelta
from calendar import monthrange
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, crud, schemas
from app.categorizer import auto_categorize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, monthrange(year, month)[1])
    return date(year, month, day)

def process_recurring_transactions(db: Session = None):
    """Finds all due recurring transactions and executes them."""
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
        
    try:
        today = date.today()
        # Find all recurring transactions that are due (or past due)
        due_items = db.query(models.RecurringTransaction).filter(
            models.RecurringTransaction.next_due_date <= today
        ).all()

        for rec in due_items:
            while rec.next_due_date and rec.next_due_date <= today:
                # 1. Create the real transaction
                category = auto_categorize(rec.description)
                stored_amount = -rec.amount if rec.transaction_type == "expense" else rec.amount
                
                # Check for duplicates so we don't accidentally run it multiple times 
                # (e.g. if the server runs multiple threads or restarts rapidly)
                from datetime import datetime
                # Just assume the runtime is now
                now = datetime.utcnow()
                
                tx = models.Transaction(
                    amount=stored_amount,
                    description=f"{rec.description} (Auto-Billed)",
                    transaction_type=rec.transaction_type,
                    category=category,
                    auto_tagged=True,
                    note=f"Automatically generated from Recurring Template ID {rec.id}",
                    timestamp=now
                )
                db.add(tx)
                
                # 2. Increment the next due date
                if rec.frequency == "daily":
                    rec.next_due_date += timedelta(days=1)
                elif rec.frequency == "weekly":
                    rec.next_due_date += timedelta(days=7)
                elif rec.frequency == "monthly":
                    rec.next_due_date = add_months(rec.next_due_date, 1)
                else:
                    # Fallback just in case
                    rec.next_due_date += timedelta(days=30)
                
                # Commit exactly when successful
                db.commit()
                logger.info(f"Auto-billed '{rec.description}' for {-stored_amount if stored_amount < 0 else stored_amount}.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing recurring transactions: {e}")
    finally:
        if should_close:
            db.close()

async def recurring_task_loop():
    """Background loop to periodically check system."""
    logger.info("Recurring transaction background task started.")
    while True:
        process_recurring_transactions()
        # Sleep for 1 hour before checking again
        await asyncio.sleep(3600)
