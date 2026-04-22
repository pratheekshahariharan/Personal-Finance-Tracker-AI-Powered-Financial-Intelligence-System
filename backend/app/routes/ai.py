"""
routes/ai.py - AI powered Financial Assistant and OCR features
"""
import os
import json
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import logging

from app import crud
from app.database import get_db

router = APIRouter(prefix="/ai", tags=["AI Integration"])

# Helper to get high-precision Gemini client
def get_gemini_client():
    import os
    import logging
    
    # Correct path: .env is in backend/.env
    # Current file is in backend/app/routes/ai.py
    # So we need to go up three levels
    current_dir = os.path.dirname(os.path.abspath(__file__)) # .../app/routes
    app_dir = os.path.dirname(current_dir) # .../app
    backend_dir = os.path.dirname(app_dir) # .../backend
    env_path = os.path.join(backend_dir, ".env")
    
    key = os.getenv("GEMINI_API_KEY")
    
    if not key and os.path.exists(env_path):
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        os.environ["GEMINI_API_KEY"] = key
                        break
        except Exception as e:
            logging.error(f"Manual .env parse error: {e}")

    if not key:
        return None, f"Key not found (checked {env_path} and environment)"
        
    try:
        from google import genai
        client = genai.Client(api_key=key)
        return client, None
    except Exception as e:
        return None, str(e)


class ChatRequest(BaseModel):
    message: str
    month: Optional[int] = None
    year: Optional[int] = None


@router.post("/chat")
@router.post("/chatbot/query")
def chat_assistant(data: ChatRequest, db: Session = Depends(get_db)):
    """
    NLP Financial Assistant.
    Provides context-aware insights based on user transactions for a specific period.
    """
    message = data.message
    m, y = data.month, data.year

    # Get period-specific user context
    dashboard = crud.get_dashboard(db, month=m, year=y)
    summary = crud.get_summary(db, month=m, year=y)
    savings = crud.get_saving_goals(db)
    budgets = crud.get_budget_status(db, month=m, year=y)
    recurring = crud.get_recurring(db)
    
    period_label = f"{m}/{y}" if m and y else "All Time / Current"

    context_str = f"""
    Current Financial Window: {period_label}
    Monthly Net: {dashboard['monthly_income'] - dashboard['monthly_expenses']}
    Monthly Income: {dashboard['monthly_income']}
    Monthly Expenses: {dashboard['monthly_expenses']}
    Carried Forward Savings: {dashboard['carried_savings']}
    Total Absolute Balance (excluding goal-locked cash): {dashboard['balance']}

    Active Savings Goals: {[f"{s.name}: {s.current_amount}/{s.target_amount}" for s in savings]}
    Active Budgets (for {period_label}): {[f"{b['category']}: {b['current_spending']}/{b['monthly_limit']}" for b in budgets]}
    Recurring Subscriptions: {[f"{r.description}: {r.amount}" for r in recurring]}
    Top Spending Category in {period_label}: {dashboard['top_spending_category']}
    """

    prompt = f"""
    You are an expert "Financial Co-Pilot" inside a premium personal finance app. 
    You are NOT a simple list-maker. Your job is to analyze the user's finances holistically and provide proactive, natural, and actionable advice.

    Here is the exact state of the user's wealth:
    {context_str}
    
    When answering the user:
    1. NEVER just repeat the raw data. Analyze it. (e.g., instead of "You have a Netflix subscription", say "I noticed you're spending ₹799 on Netflix. Do you use it enough to justify the cost?")
    2. Be proactive and specific. Suggest precise actions (cancelling a subscription, moving money to a savings goal, reallocating a budget).
    3. Keep your tone natural, premium, empathetic, and highly intelligent.
    4. Format your responses elegantly in markdown (use bullet points or bold text sparingly for emphasis).
    
    User Query: {message}
    """

    client, error_msg = get_gemini_client()
    if client:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt,
            )
            return {"response": response.text}
        except Exception as e:
            logging.error(f"AI Error: {str(e)}")
            return {"response": f"I encountered an error: {str(e)}"}
    else:
        return {"response": f"Offline Mode: {error_msg}. Please ensure your API key is correct in backend/.env and restart the server."}


@router.post("/receipt")
def parse_receipt(file: UploadFile = File(...)):
    """
    Receipt OCR that extracts transaction amount and description.
    Uses local EasyOCR (Tensor-based) as primary, with Gemini as fallback.
    """
    try:
        contents = file.file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the uploaded file.")

    # 1. Try High-Performance Gemini OCR first (Faster & More Accurate)
    client, error_msg = get_gemini_client()
    if client:
        try:
            from google.genai import types
            
            prompt = """Extract the transaction amount and the vendor name from this receipt.
            Rules:
            1. 'amount' must be a float (look for the final 'Total' amount).
            2. 'description' must be a string (vendor name found at the top).
            3. Return ONLY valid JSON with keys: 'amount' and 'description'.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[
                    types.Part.from_bytes(data=contents, mime_type=file.content_type or "image/jpeg"),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            parsed = json.loads(response.text)
            return {
                "amount": parsed.get("amount", 0.0),
                "description": parsed.get("description", "Unknown Vendor"),
                "date": parsed.get("date", None),
                "method": "gemini_ai_v2"
            }
        except Exception as e:
            logging.error(f"Gemini OCR Error: {e}")
            # Fall through to local OCR

    # 2. Local Fallback: Tensor-based OCR (EasyOCR)
    try:
        from app.ocr_utils import extract_receipt_data
        local_result = extract_receipt_data(contents)
        
        return {
            "amount": local_result["amount"],
            "description": local_result["description"],
            "date": None,
            "method": "local_tensor_ocr"
        }
    except Exception as e:
        logging.error(f"Local OCR Error: {e}")
        raise HTTPException(status_code=500, detail="Both AI and Local OCR failed.")

    # Mock response if everything fails
    return {
        "amount": 0.0,
        "description": "OCR Failed (No API Key & Local Error)",
        "date": "2024-01-01",
        "is_mock": true
    }
