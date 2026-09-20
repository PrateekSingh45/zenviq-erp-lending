import frappe

def execute(filters=None):
    columns = [
        {"label": "Disbursement ID", "fieldname": "name", "fieldtype": "Link", "options": "Loan Disbursement", "width": 140},
        {"label": "Loan ID", "fieldname": "against_loan", "fieldtype": "Link", "options": "Loan", "width": 140},
        {"label": "Applicant", "fieldname": "applicant", "fieldtype": "Data", "width": 170},
        {"label": "Disbursement Date", "fieldname": "disbursement_date", "fieldtype": "Date", "width": 120},
        {"label": "Disbursed Amount (INR)", "fieldname": "disbursed_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]
    
    disbs = frappe.get_all("Loan Disbursement", fields=["name", "against_loan", "applicant", "disbursement_date", "disbursed_amount", "docstatus"])
    data = []
    for d in disbs:
        data.append({
            "name": d.name,
            "against_loan": d.against_loan,
            "applicant": d.applicant,
            "disbursement_date": d.disbursement_date,
            "disbursed_amount": d.disbursed_amount,
            "status": "Disbursed" if d.docstatus == 1 else "Draft"
        })
    return columns, data
