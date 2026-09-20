from datetime import datetime
import random

def analyze_statement(borrower_name=None, bank_name="State Bank of India"):
    monthly_credits = random.randint(62000, 78000)
    monthly_debits = int(monthly_credits * random.uniform(0.68, 0.78))
    avg_bal = random.randint(18000, 29000)
    
    return {
        "status": "COMPLETED",
        "mode": "SANDBOX",
        "analyzer": "ZENVIQ Statement AI Engine (Sandbox)",
        "borrower_name": borrower_name or "Borrower",
        "bank_detected": bank_name,
        "statement_period": "Past 6 Months",
        "metrics": {
            "avg_monthly_balance": avg_bal,
            "avg_monthly_credits": monthly_credits,
            "avg_monthly_debits": monthly_debits,
            "net_monthly_savings": monthly_credits - monthly_debits,
            "cheque_ecs_bounces": 0,
            "salary_detected": True,
            "regular_salary_day": 1,
            "salary_employer": "Zenviq Infotech Solutions"
        },
        "avg_monthly_balance": avg_bal,
        "avg_monthly_credits": monthly_credits,
        "avg_monthly_debits": monthly_debits,
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "Automated simulated bank statement analytics for demonstration."
    }
