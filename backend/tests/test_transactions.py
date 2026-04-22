import pytest
from datetime import datetime, timedelta

def test_create_transaction(client):
    response = client.post(
        "/transactions/",
        json={"amount": 100.0, "description": "McDonalds Lunch", "transaction_type": "expense"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == -100.0  # Expenses stored as negative
    assert data["category"] == "Food"  # Auto-categorized

def test_duplicate_detection(client):
    # Add first transaction
    client.post(
        "/transactions/",
        json={"amount": 50.0, "description": "Duplicate Test", "transaction_type": "expense"}
    )
    # Try adding same transaction immediately
    response = client.post(
        "/transactions/",
        json={"amount": 50.0, "description": "Duplicate Test", "transaction_type": "expense"}
    )
    assert response.status_code == 409
    assert "Duplicate transaction detected" in response.json()["detail"]

def test_invalid_transaction_type(client):
    # Rent should not be income (enforced by categorizer)
    response = client.post(
        "/transactions/",
        json={"amount": 1000.0, "description": "Rent Payment", "transaction_type": "income"}
    )
    assert response.status_code == 400
    assert "cannot be classified as 'income'" in response.json()["detail"].lower()

def test_budget_projection(client):
    # Set a budget for Food
    client.post("/budget/", json={"category": "Food", "monthly_limit": 1000.0})
    
    # Add an expense
    client.post(
        "/transactions/",
        json={"amount": 200.0, "description": "Pizza Hut", "transaction_type": "expense"}
    )
    
    response = client.get("/budget/status")
    assert response.status_code == 200
    budgets = response.json()
    food_budget = next(b for b in budgets if b["category"] == "Food")
    
    assert food_budget["current_spending"] == 200.0
    assert food_budget["projected_spending"] >= 200.0
    assert "days_left" in food_budget
