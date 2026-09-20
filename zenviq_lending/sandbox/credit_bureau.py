from datetime import datetime, date
import random

def fetch_credit_report(pan_number, full_name=None, dob=None):
    pan = (pan_number or "ABCDE1234F").upper().strip()
    score = random.randint(720, 785)
    
    return {
        "status": "SUCCESS",
        "mode": "SANDBOX",
        "bureau": "TransUnion CIBIL (Sandbox Simulator)",
        "pan": pan,
        "name": full_name or "Rajesh Kumar Sharma",
        "score": score,
        "score_band": "Excellent" if score >= 750 else "Good",
        "report_date": date.today().strftime("%Y-%m-%d"),
        "report_id": f"CIBIL-SBX-{random.randint(1000000, 9999999)}",
        "summary": {
            "total_accounts": 3,
            "active_accounts": 2,
            "closed_accounts": 1,
            "total_sanctioned_amount": 450000,
            "current_balance": 115000,
            "total_emi": 8500,
            "overdue_accounts": 0,
            "overdue_amount": 0,
            "recent_inquiries_30d": 1,
            "credit_age_months": 38
        },
        "accounts": [
            {
                "institution": "HDFC Bank Ltd",
                "account_type": "Auto Loan",
                "sanctioned_amount": 300000,
                "current_balance": 65000,
                "monthly_emi": 6200,
                "status": "Active",
                "payment_history_36m": "000/000/000/000/000/000 (No DPD)"
            },
            {
                "institution": "State Bank of India",
                "account_type": "Consumer Loan",
                "sanctioned_amount": 50000,
                "current_balance": 0,
                "monthly_emi": 0,
                "status": "Closed / Settled in Full",
                "payment_history_36m": "000/000/000/000"
            },
            {
                "institution": "ICICI Bank Ltd",
                "account_type": "Credit Card",
                "credit_limit": 100000,
                "current_balance": 18000,
                "monthly_emi": 2300,
                "status": "Active",
                "payment_history_36m": "000/000/000/000/000/000"
            }
        ],
        "disclaimer": "Simulated Credit Bureau report for ZENVIQ Individual Lending POC."
    }
