"""
finance_sdk/sample_usage.py

Sample showing how to use the auto-generated Python SDK after running:

    npm install -g @openapitools/openapi-generator-cli
    openapi-generator-cli generate \
        -i http://localhost:8000/openapi.json \
        -g python \
        -o finance_sdk

Install the generated SDK first:
    pip install -e finance_sdk/

Then run this file:
    python finance_sdk/sample_usage.py
"""

# ── After SDK generation, uncomment and run the lines below ──────────────────
#
# from finance_sdk.api.transactions_api import TransactionsApi
# from finance_sdk.api.budget_api import BudgetApi
# from finance_sdk.api.dashboard_api import DashboardApi
# from finance_sdk import ApiClient, Configuration
#
# config = Configuration(host="http://localhost:8000")
# client = ApiClient(configuration=config)
#
# # ── Transactions ──────────────────────────────────────────────────────────
# tx_api = TransactionsApi(client)
#
# # Add a transaction
# from finance_sdk.models import TransactionCreate
# new_tx = tx_api.add_transaction_transactions_post(
#     TransactionCreate(amount=500, description="Zomato order", transaction_type="expense")
# )
# print("Created:", new_tx)
#
# # List all transactions
# all_tx = tx_api.list_transactions_transactions_get()
# for tx in all_tx:
#     print(f"  [{tx.id}] {tx.description} - {tx.category} - ₹{abs(tx.amount)}")
#
# # Get summary
# summary = tx_api.get_summary_transactions_summary_get()
# print("Summary:", summary)
#
# # ── Dashboard ─────────────────────────────────────────────────────────────
# dash_api = DashboardApi(client)
# dashboard = dash_api.get_dashboard_dashboard_get()
# print(f"Balance: ₹{dashboard.balance:,.2f}")
# print(f"Top spending: {dashboard.top_spending_category}")
#
# # ── Budget ────────────────────────────────────────────────────────────────
# budget_api = BudgetApi(client)
# from finance_sdk.models import BudgetCreate
# budget_api.set_budget_budget_post(BudgetCreate(category="Food", monthly_limit=3000))
# status = budget_api.budget_status_budget_status_get()
# for s in status:
#     exceeded = "⚠ EXCEEDED" if s.exceeded else "OK"
#     print(f"  {s.category}: ₹{s.current_spending} / ₹{s.monthly_limit} [{exceeded}]")

# ── Fallback: raw requests demo (no SDK generation required) ─────────────────
import requests

BASE = "http://localhost:8000"

def demo():
    print("=== FinanceOS SDK Demo (raw requests) ===\n")

    # Add transaction
    resp = requests.post(f"{BASE}/transactions/", json={
        "amount": 1200,
        "description": "Pizza delivery",
        "transaction_type": "expense",
        "note": "Weekend treat"
    })
    if resp.status_code == 201:
        tx = resp.json()
        print(f"✓ Added: {tx['description']} → {tx['category']} (₹{abs(tx['amount'])})")
    else:
        print(f"✗ Add failed: {resp.json()}")

    # Dashboard
    dash = requests.get(f"{BASE}/dashboard").json()
    print(f"\nDashboard:")
    print(f"  Income:       ₹{dash['total_income']:,.0f}")
    print(f"  Expenses:     ₹{dash['total_expenses']:,.0f}")
    print(f"  Balance:      ₹{dash['balance']:,.0f}")
    print(f"  Transactions: {dash['total_transactions']}")
    print(f"  Top category: {dash['top_spending_category']}")

    # Budget status
    status = requests.get(f"{BASE}/budget/status").json()
    if status:
        print(f"\nBudget status:")
        for s in status:
            flag = "⚠ EXCEEDED" if s["exceeded"] else "✓ OK"
            print(f"  {s['category']}: ₹{s['current_spending']} / ₹{s['monthly_limit']} [{flag}]")


if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("Backend not running. Start it with: uvicorn main:app --reload")
