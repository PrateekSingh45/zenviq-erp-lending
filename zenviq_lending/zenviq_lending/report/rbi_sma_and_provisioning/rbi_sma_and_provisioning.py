import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"fieldname": "borrower_name", "label": "Borrower Name", "fieldtype": "Data", "width": 180},
        {"fieldname": "pan_number", "label": "PAN Number", "fieldtype": "Data", "width": 140},
        {"fieldname": "loan_account", "label": "Loan Account", "fieldtype": "Link", "options": "Loan", "width": 220},
        {"fieldname": "sanction_amount", "label": "Sanction Amt", "fieldtype": "Currency", "width": 140},
        {"fieldname": "principal_os", "label": "Principal O/S", "fieldtype": "Currency", "width": 140},
        {"fieldname": "overdue", "label": "Overdue", "fieldtype": "Currency", "width": 140},
        {"fieldname": "dpd", "label": "DPD", "fieldtype": "Int", "width": 80},
        {"fieldname": "classification", "label": "Classification", "fieldtype": "Data", "width": 180},
        {"fieldname": "prov_rate", "label": "Prov. Rate (%)", "fieldtype": "Percent", "width": 130},
        {"fieldname": "prov_amount", "label": "Prov. Amount", "fieldtype": "Currency", "width": 140}
    ]

    data = []
    
    loans = frappe.get_all("Loan", fields=["name", "applicant_name", "loan_amount", "status"])
    
    for loan in loans:
        pan = ""
        borrowers = frappe.get_all("Borrower Profile", filters={"full_name": loan.applicant_name}, fields=["pan_number"], limit=1)
        if borrowers:
            pan = borrowers[0].pan_number
            
        collection = frappe.get_all("Collection Task", filters={"loan": loan.name}, fields=["dpd_days", "overdue_amount"], limit=1)
        dpd = 0
        overdue = 0
        if collection:
            dpd = collection[0].dpd_days or 0
            overdue = collection[0].overdue_amount or 0
            
        classification = "Standard"
        prov_rate = 0.4
        
        if dpd == 0:
            classification = "Standard"
        elif 1 <= dpd <= 30:
            classification = "SMA-0"
        elif 31 <= dpd <= 60:
            classification = "SMA-1"
        elif 61 <= dpd <= 90:
            classification = "SMA-2"
        elif 91 <= dpd <= 365:
            classification = "Sub-Standard (NPA)"
            prov_rate = 15.0
        elif dpd > 365:
            classification = "Doubtful (NPA)"
            prov_rate = 25.0
            
        outstanding = flt(loan.loan_amount)
        if dpd == 0 and loan.status != "Closed":
            outstanding = outstanding * 0.8
            
        if loan.status == "Closed":
            outstanding = 0
            overdue = 0
            dpd = 0
            classification = "Closed / Satisfied"
            prov_rate = 0
            
        prov_amount = (outstanding * prov_rate) / 100
        
        data.append({
            "borrower_name": loan.applicant_name,
            "pan_number": pan,
            "loan_account": loan.name,
            "sanction_amount": loan.loan_amount,
            "principal_os": outstanding,
            "overdue": overdue,
            "dpd": dpd,
            "classification": classification,
            "prov_rate": prov_rate,
            "prov_amount": prov_amount
        })

    return columns, data
