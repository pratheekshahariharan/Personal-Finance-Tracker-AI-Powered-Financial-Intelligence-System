"""
categorizer.py - Keyword-based auto-categorization and cross-type validation.
"""
from fastapi import HTTPException

# ── Keyword → Category mapping ────────────────────────────────────────────────
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Food": ["mcdonald", "pizza", "zomato", "swiggy", "cafe", "restaurant",
             "burger", "kfc", "domino", "starbucks", "dunkin", "subway", "biryani", "food"],
    "Transport": ["uber", "ola", "bus", "metro", "train", "fuel", "petrol",
                  "rapido", "auto", "taxi", "cab", "flight", "airline"],
    "Shopping": ["amazon", "flipkart", "mall", "myntra", "meesho", "nykaa",
                 "ajio", "store", "market", "purchase", "shopping"],
    "Housing": ["rent", "electricity", "water bill", "maintenance", "gas",
                "broadband", "wifi", "internet bill"],
    "Entertainment": ["movie", "netflix", "spotify", "prime", "youtube",
                      "disney", "hotstar", "concert", "gaming", "steam"],
    "Healthcare": ["hospital", "clinic", "medicine", "pharmacy", "doctor",
                   "lab", "test", "health"],
    "Education": ["course", "udemy", "college", "school", "book", "tutorial",
                  "certification", "fee", "tuition"],
    "Salary": ["salary", "bonus", "freelance", "stipend", "paycheck",
               "commission", "income", "wage"],
}

# ── Categories that logically belong to only one transaction type ─────────────
INCOME_ONLY = {"Salary"}
EXPENSE_ONLY = {"Transport", "Shopping", "Housing", "Entertainment",
                "Healthcare", "Education"}


def auto_categorize(description: str) -> str:
    """Return the best matching category for a description, or 'Other'."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return category
    return "Other"


def validate_category_type(category: str, transaction_type: str) -> None:
    """
    Raise HTTP 400 if a transaction's category contradicts its type.

    Examples:
        "Rent" as income  → error
        "Salary" as expense → error
    """
    if category in INCOME_ONLY and transaction_type == "expense":
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category}' cannot be classified as 'expense'. "
                   f"This looks like income."
        )
    if category in EXPENSE_ONLY and transaction_type == "income":
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category}' cannot be classified as 'income'. "
                   f"This looks like an expense."
        )
