import frappe

def execute(filters=None):
    columns = [
        {"label": "Loan ID", "fieldname": "loan", "fieldtype": "Link", "options": "Loan", "width": 130},
        {"label": "Borrower", "fieldname": "borrower_name", "fieldtype": "Data", "width": 180},
        {"label": "DPD Days", "fieldname": "dpd_days", "fieldtype": "Int", "width": 90},
        {"label": "Classification", "fieldname": "classification", "fieldtype": "Data", "width": 130},
        {"label": "Outstanding Principal", "fieldname": "overdue_amount", "fieldtype": "Currency", "width": 140},
        {"label": "Penal Interest", "fieldname": "penal_interest", "fieldtype": "Currency", "width": 130},
        {"label": "Provision Required (15%)", "fieldname": "provision", "fieldtype": "Currency", "width": 140},
        {"label": "Recovery Status", "fieldname": "collection_status", "fieldtype": "Data", "width": 120}
    ]
    
    tasks = frappe.get_all("Collection Task", filters={"dpd_days": [">=", 90]}, fields=["loan", "borrower_name", "dpd_days", "overdue_amount", "penal_interest", "collection_status"])
    data = []
    for t in tasks:
        overdue = t.overdue_amount or 0
        data.append({
            "loan": t.loan,
            "borrower_name": t.borrower_name,
            "dpd_days": t.dpd_days,
            "classification": "Sub-Standard (NPA)" if t.dpd_days < 180 else "Doubtful NPA",
            "overdue_amount": overdue,
            "penal_interest": t.penal_interest or 0,
            "provision": round(overdue * 0.15, 2),
            "collection_status": t.collection_status
        })
    return columns, data
