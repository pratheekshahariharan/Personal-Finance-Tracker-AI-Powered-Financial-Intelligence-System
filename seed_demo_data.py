import sqlite3
from datetime import datetime, date

# Path to the database
DB_PATH = r"d:\finance-tracker\backend\finance.db"

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Cleaning existing data...")
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM budgets")
    cursor.execute("DELETE FROM saving_goals")
    cursor.execute("DELETE FROM recurring_transactions")
    cursor.execute("DELETE FROM savings_transactions")
    
    # Commit deletions
    conn.commit()

    curr_month = "2026-04" # Consistent with system time
    today = "2026-04-22"

    print("Seeding new transactions...")
    transactions = [
        # (amount, description, type, category, timestamp)
        (95000.0, "Monthly Salary - AUMNE AI", "income", "Salary", f"{curr_month}-01 09:00:00"),
        (-28000.0, "Residential Rent - April", "expense", "Housing", f"{curr_month}-01 10:00:00"),
        (-4200.0, "Reliance Fresh Groceries", "expense", "Food", f"{curr_month}-05 14:30:00"),
        (-850.0, "Uber Ride to Office", "expense", "Transport", f"{curr_month}-08 08:45:00"),
        (-2400.0, "Saturday Dinner - The Social", "expense", "Food", f"{curr_month}-12 20:00:00"),
        (-12500.0, "Amazon - Noise-Cancelling Headphones", "expense", "Shopping", f"{curr_month}-15 11:20:00"),
        (-1200.0, "PVR Cinemas - Movie Night", "expense", "Entertainment", f"{curr_month}-18 18:00:00"),
        (-650.0, "Zomato - Late Night Snack", "expense", "Food", f"{curr_month}-21 23:15:00"),
        (-3350.0, "Monthly Fuel Refill", "expense", "Transport", f"{curr_month}-05 17:00:00"),
    ]
    
    for t in transactions:
        cursor.execute("""
            INSERT INTO transactions (amount, description, transaction_type, category, auto_tagged, timestamp)
            VALUES (?, ?, ?, ?, 1, ?)
        """, t)

    print("Seeding budgets...")
    # Add a budget that is nearly exceeded
    # Total Food spending above is 4200 + 2400 + 650 = 7250
    # Let's set Food limit to 7000 to trigger the warning
    budgets = [
        ("Food", 7000.0),
        ("Transport", 5000.0),
        ("Shopping", 15000.0),
        ("Entertainment", 5000.0)
    ]
    for b in budgets:
        cursor.execute("INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)", b)

    print("Seeding saving goals...")
    goals = [
        ("Laptop Fund", 180000.0, 12000.0),
        ("Emergency Fund", 200000.0, 45000.0)
    ]
    for g in goals:
        cursor.execute("INSERT INTO saving_goals (name, target_amount, current_amount) VALUES (?, ?, ?)", g)

    print("Seeding recurring transactions...")
    recurring = [
        ("Netflix Premium", -799.0, "expense", "Entertainment", "monthly", f"{curr_month}-28"),
        ("Spotify Family Plan", -199.0, "expense", "Entertainment", "monthly", f"{curr_month}-25")
    ]
    for r in recurring:
        cursor.execute("""
            INSERT INTO recurring_transactions (description, amount, transaction_type, category, frequency, next_due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print("Database polished for demo successfully!")

if __name__ == "__main__":
    seed()
