import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

def generate_pdf_report(dashboard_data: dict, summary_data: list, savings_data: list) -> bytes:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, "Personal Finance Tracker")
    p.setFont("Helvetica", 14)
    p.drawString(50, height - 70, f"Financial Health Statement - {datetime.utcnow().strftime('%B %Y')}")

    # Metrics
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 120, "At a Glance Overview")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 150, f"Total Income: INR {dashboard_data['total_income']}")
    p.drawString(50, height - 170, f"Total Expenses: INR {dashboard_data['total_expenses']}")
    p.drawString(50, height - 190, f"Net Balance: INR {dashboard_data['balance']}")
    p.drawString(50, height - 210, f"Total Savings Goal Achieved: INR {dashboard_data['total_savings']}")
    
    # Financial Health Analyzer (AI-like rule)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 260, "Financial Health Analysis")
    p.setFont("Helvetica", 11)
    if dashboard_data['total_income'] > 0:
        ratio = (dashboard_data['total_expenses'] / dashboard_data['total_income']) * 100
        if ratio > 80:
            msg = "Warning: High spend ratio. You are spending over 80% of your income."
        else:
            msg = f"Healthy: You are successfully saving {100-ratio:.1f}% of your monthly income!"
    else:
        msg = "Notice: Insufficient top-level income data to compute ratios."
    
    p.drawString(50, height - 280, msg)

    # Top Spends
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 330, "Top Spend Categories")
    p.setFont("Helvetica", 11)
    
    y = height - 350
    for s in summary_data[:5]:
        p.drawString(50, y, f"- {s['category']}: INR {s['total']}")
        y -= 20

    # Draw bottom border
    p.line(50, 50, width - 50, 50)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 35, "Generated automatically by Personal Finance Tracker OS")

    p.showPage()
    p.save()
    return buffer.getvalue()


def parse_csv_stream(file_content: bytes, month: int = None, year: int = None):
    df = pd.read_csv(io.BytesIO(file_content))
    records = []
    
    # Use current year/month as fallback if none provided
    now = datetime.now()
    target_year = year if year else now.year
    target_month = month if month else now.month

    for _, row in df.iterrows():
        try:
            # Construct a date for this record. Default to 1st of the month if overriding.
            record_date = datetime(target_year, target_month, 1)
            
            records.append({
                "description": str(row.get('description', 'Unknown')),
                "amount": abs(float(row.get('amount', 0))),
                "transaction_type": "expense" if str(row.get('type', '')).lower() == 'expense' else "income",
                "note": str(row.get('note', '')),
                "timestamp": record_date
            })
        except:
            continue
    return records
