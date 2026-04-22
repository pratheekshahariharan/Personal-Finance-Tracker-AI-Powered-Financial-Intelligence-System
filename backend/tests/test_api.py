"""
tests/test_api.py - Comprehensive backend test suite using pytest + httpx.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# ── In-memory SQLite for tests ────────────────────────────────────────────────
TEST_DB_URL = "sqlite:///./test_finance.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Wipe all tables before each test for isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ── 1. Add valid transaction ──────────────────────────────────────────────────
def test_add_valid_transaction():
    resp = client.post("/transactions/", json={
        "amount": 500,
        "description": "Zomato order",
        "transaction_type": "expense"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["category"] == "Food"
    assert data["amount"] == -500           # stored as negative
    assert data["auto_tagged"] is True


# ── 2. Reject invalid transaction_type ───────────────────────────────────────
def test_reject_invalid_type():
    resp = client.post("/transactions/", json={
        "amount": 100,
        "description": "Test",
        "transaction_type": "gift"
    })
    assert resp.status_code == 422          # pydantic validation error


# ── 3. Reject duplicate transaction ──────────────────────────────────────────
def test_reject_duplicate():
    payload = {"amount": 500, "description": "Uber ride", "transaction_type": "expense"}
    r1 = client.post("/transactions/", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/transactions/", json=payload)
    assert r2.status_code == 409


# ── 4. Auto category assignment ──────────────────────────────────────────────
def test_auto_category_uber():
    resp = client.post("/transactions/", json={
        "amount": 150, "description": "Uber ride", "transaction_type": "expense"
    })
    assert resp.json()["category"] == "Transport"


def test_auto_category_salary():
    resp = client.post("/transactions/", json={
        "amount": 50000, "description": "Monthly Salary", "transaction_type": "income"
    })
    assert resp.json()["category"] == "Salary"


def test_auto_category_other():
    resp = client.post("/transactions/", json={
        "amount": 100, "description": "Random unknown vendor", "transaction_type": "expense"
    })
    assert resp.json()["category"] == "Other"


# ── 5. Cross-type validation ──────────────────────────────────────────────────
def test_rent_as_income_rejected():
    resp = client.post("/transactions/", json={
        "amount": 15000, "description": "Rent payment", "transaction_type": "income"
    })
    assert resp.status_code == 400


def test_salary_as_expense_rejected():
    resp = client.post("/transactions/", json={
        "amount": 50000, "description": "Salary", "transaction_type": "expense"
    })
    assert resp.status_code == 400


# ── 6. Summary endpoint ───────────────────────────────────────────────────────
def test_summary_endpoint():
    client.post("/transactions/", json={
        "amount": 800, "description": "Swiggy order", "transaction_type": "expense"
    })
    resp = client.get("/transactions/summary")
    assert resp.status_code == 200
    summaries = resp.json()
    assert isinstance(summaries, list)
    assert any(s["category"] == "Food" for s in summaries)
    # expenses shown as negative signed values
    for s in summaries:
        if s["category"] == "Food":
            assert s["total"] == -800.0


# ── 7. Delete endpoint ────────────────────────────────────────────────────────
def test_delete_transaction():
    r = client.post("/transactions/", json={
        "amount": 100, "description": "Test delete", "transaction_type": "expense"
    })
    tx_id = r.json()["id"]
    del_resp = client.delete(f"/transactions/{tx_id}")
    assert del_resp.status_code == 204
    # Verify gone
    txs = client.get("/transactions/").json()
    assert all(t["id"] != tx_id for t in txs)


def test_delete_nonexistent():
    resp = client.delete("/transactions/99999")
    assert resp.status_code == 404


# ── 8. Reclassify endpoint ────────────────────────────────────────────────────
def test_reclassify():
    r = client.post("/transactions/", json={
        "amount": 150, "description": "Uber ride", "transaction_type": "expense"
    })
    tx_id = r.json()["id"]
    patch = client.patch(f"/transactions/{tx_id}/reclassify", json={"category": "Travel"})
    assert patch.status_code == 200
    assert patch.json()["category"] == "Travel"
    assert patch.json()["auto_tagged"] is False


# ── 9. Budget exceeded logic ──────────────────────────────────────────────────
def test_budget_exceeded():
    # Set food budget to ₹500
    client.post("/budget/", json={"category": "Food", "monthly_limit": 500})
    # Spend ₹800 on food
    client.post("/transactions/", json={
        "amount": 800, "description": "Zomato order", "transaction_type": "expense"
    })
    status = client.get("/budget/status").json()
    food = next((s for s in status if s["category"] == "Food"), None)
    assert food is not None
    assert food["exceeded"] is True


# ── 10. CSV export ────────────────────────────────────────────────────────────
def test_csv_export():
    client.post("/transactions/", json={
        "amount": 200, "description": "Amazon purchase", "transaction_type": "expense"
    })
    resp = client.get("/transactions/export")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    content = resp.text
    assert "description" in content
    assert "Amazon purchase" in content


# ── 11. Dashboard endpoint ────────────────────────────────────────────────────
def test_dashboard():
    client.post("/transactions/", json={
        "amount": 50000, "description": "Monthly Salary", "transaction_type": "income"
    })
    client.post("/transactions/", json={
        "amount": 1500, "description": "Zomato food", "transaction_type": "expense"
    })
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    d = resp.json()
    assert d["total_income"] == 50000
    assert d["total_expenses"] == 1500
    assert d["balance"] == 48500


# ── 12. CSV Import ────────────────────────────────────────────────────────────
def test_csv_import():
    content = "description,amount,type,note\nNetflix,799,expense,Monthly sub\nFreelance,5000,income,Project X\n"
    files = {"file": ("test.csv", content, "text/csv")}
    resp = client.post("/csv/import?month=4&year=2026", files=files)
    assert resp.status_code == 200
    assert "Successfully imported 2 transactions" in resp.json()["message"]
    
    # Verify they exist
    txs = client.get("/transactions/").json()
    assert any(t["description"] == "Netflix" and t["amount"] == -799 for t in txs)
    assert any(t["description"] == "Freelance" and t["amount"] == 5000 for t in txs)


# ── 13. Savings goals flow ───────────────────────────────────────────────────
def test_savings_goals():
    # Create goal
    client.post("/savings/", json={"name": "Emergency Fund", "target_amount": 10000})
    goals = client.get("/savings/").json()
    goal_id = goals[0]["id"]
    
    # Deposit
    client.post("/savings/deposit", json={"amount": 1000, "reason": "Monthly stash", "goal_id": goal_id})
    
    # Check balance
    bal_res = client.get("/savings/balance").json()
    assert bal_res["balance"] == 1000
    
    # Withdraw
    client.post("/savings/withdraw", json={"amount": 400, "reason": "Emergency", "goal_id": goal_id})
    bal_res2 = client.get("/savings/balance").json()
    assert bal_res2["balance"] == 600
    
    # Check goal state
    goals = client.get("/savings/").json()
    assert goals[0]["current_amount"] == 600


# ── 14. Recurring Transactions ───────────────────────────────────────────────
def test_recurring_transactions():
    # Create recurring template
    client.post("/recurring/", json={
        "description": "Gym",
        "amount": 2000,
        "transaction_type": "expense",
        "frequency": "monthly",
        "next_due_date": "2024-01-01" # past date
    })
    
    # The recurring logic is triggered on POST /recurring in the app code
    # Let's verify a transaction was created for the Gym
    txs = client.get("/transactions/").json()
    assert any("Gym" in t["description"] for t in txs)

