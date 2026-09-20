import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 110},
        {"label": "Reference ID", "fieldname": "reference", "fieldtype": "Data", "width": 140},
        {"label": "Borrower", "fieldname": "borrower", "fieldtype": "Data", "width": 170},
        {"label": "Event Type", "fieldname": "event_type", "fieldtype": "Data", "width": 160},
        {"label": "Debit / Sanctioned", "fieldname": "debit", "fieldtype": "Currency", "width": 130},
        {"label": "Credit / Repaid", "fieldname": "credit", "fieldtype": "Currency", "width": 130},
        {"label": "Running Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 140}
    ]
    
    data = []
    loans = frappe.get_all("Loan", fields=["name", "applicant", "posting_date", "disbursed_amount", "loan_amount", "total_amount_paid", "total_principal_paid", "status"])
    for l in loans:
        data.append({
            "date": l.posting_date,
            "reference": l.name,
            "borrower": l.applicant,
            "event_type": "Loan Disbursement",
            "debit": l.disbursed_amount,
            "credit": 0,
            "balance": l.disbursed_amount
        })
        if l.total_amount_paid:
            balance = flt(l.loan_amount) - flt(l.total_principal_paid) if l.status != "Closed" else 0
            data.append({
                "date": l.posting_date,
                "reference": "PMT-" + l.name,
                "borrower": l.applicant,
                "event_type": "EMI Repayment Cumulative",
                "debit": 0,
                "credit": l.total_amount_paid,
                "balance": balance
            })
    return columns, data
