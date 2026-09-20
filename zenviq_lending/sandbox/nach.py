from datetime import datetime
import random

def register_mandate(borrower_name, bank_name, account_number, emi_amount):
    umrn = f"ZENVIQ{random.randint(1000000000, 9999999999)}NACH"
    acc = str(account_number or "1234")
    masked = f"XXXXXX{acc[-4:]}"
    return {
        "status": "ACTIVE",
        "mode": "SANDBOX",
        "provider": "NPCI e-NACH Gateway (Sandbox)",
        "umrn": umrn,
        "borrower_name": borrower_name,
        "bank_name": bank_name or "State Bank of India",
        "account_number_masked": masked,
        "max_debit_amount": (emi_amount or 10000) * 2,
        "frequency": "Monthly",
        "first_debit_date": "2026-10-05",
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "Simulated NPCI e-Mandate registration for demonstration."
    }
