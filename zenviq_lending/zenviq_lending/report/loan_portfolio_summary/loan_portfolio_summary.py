import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Loan ID", "fieldname": "loan_id", "fieldtype": "Link", "options": "Loan", "width": 140},
        {"label": "Borrower", "fieldname": "borrower", "fieldtype": "Data", "width": 180},
        {"label": "Product", "fieldname": "product", "fieldtype": "Link", "options": "Loan Product", "width": 160},
        {"label": "Sanction Date", "fieldname": "sanction_date", "fieldtype": "Date", "width": 110},
        {"label": "Sanctioned (INR)", "fieldname": "loan_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Disbursed (INR)", "fieldname": "disbursed_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Outstanding Principal", "fieldname": "total_principal_outstanding", "fieldtype": "Currency", "width": 140},
        {"label": "Interest Payable", "fieldname": "total_interest_payable", "fieldtype": "Currency", "width": 130},
        {"label": "Total Repaid", "fieldname": "total_amount_paid", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110}
    ]
    
    loans = frappe.get_all("Loan", fields=["name", "applicant", "loan_product", "posting_date", "loan_amount", "disbursed_amount", "total_principal_paid", "total_interest_payable", "total_amount_paid", "status"])
    data = []
    for l in loans:
        outstanding = flt(l.loan_amount) - flt(l.total_principal_paid) if l.status != "Closed" else 0
        data.append({
            "loan_id": l.name,
            "borrower": l.applicant,
            "product": l.loan_product,
            "sanction_date": l.posting_date,
            "loan_amount": l.loan_amount,
            "disbursed_amount": l.disbursed_amount,
            "total_principal_outstanding": outstanding,
            "total_interest_payable": l.total_interest_payable,
            "total_amount_paid": l.total_amount_paid,
            "status": l.status
        })
    return columns, data
