import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Repayment ID", "fieldname": "name", "fieldtype": "Link", "options": "Loan Repayment", "width": 140},
        {"label": "Loan ID", "fieldname": "against_loan", "fieldtype": "Link", "options": "Loan", "width": 140},
        {"label": "Borrower", "fieldname": "applicant", "fieldtype": "Data", "width": 180},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
        {"label": "Principal Paid", "fieldname": "principal_amount_paid", "fieldtype": "Currency", "width": 120},
        {"label": "Interest Paid", "fieldname": "total_interest_paid", "fieldtype": "Currency", "width": 120},
        {"label": "Penalty Paid", "fieldname": "total_penalty_paid", "fieldtype": "Currency", "width": 110},
        {"label": "Total Amount Paid", "fieldname": "amount_paid", "fieldtype": "Currency", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]
    
    repayments = frappe.get_all("Loan Repayment", fields=["name", "against_loan", "applicant", "posting_date", "principal_amount_paid", "total_interest_paid", "total_penalty_paid", "amount_paid", "docstatus"])
    data = []
    for r in repayments:
        data.append({
            "name": r.name,
            "against_loan": r.against_loan,
            "applicant": r.applicant,
            "posting_date": r.posting_date,
            "principal_amount_paid": r.principal_amount_paid,
            "total_interest_paid": r.total_interest_paid,
            "total_penalty_paid": r.total_penalty_paid or 0,
            "amount_paid": r.amount_paid,
            "status": "Submitted" if r.docstatus == 1 else ("Cancelled" if r.docstatus == 2 else "Draft")
        })
    return columns, data
