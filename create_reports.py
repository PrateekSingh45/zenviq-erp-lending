import os, json

BASE_DIR = "/workspace/development/frappe-bench/apps/zenviq_lending/zenviq_lending/zenviq_lending"
REPORTS_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORTS_DIR, exist_ok=True)
with open(os.path.join(REPORTS_DIR, "__init__.py"), "w") as f:
    f.write("")

reports = [
    {
        "name": "Loan Portfolio Summary",
        "folder": "loan_portfolio_summary",
        "ref_doctype": "Loan",
        "execute_code": """import frappe

def execute(filters=None):
    columns = [
        {"label": "Loan ID", "fieldname": "loan_id", "fieldtype": "Link", "options": "Loan", "width": 140},
        {"label": "Borrower", "fieldname": "borrower", "fieldtype": "Data", "width": 180},
        {"label": "Product", "fieldname": "product", "fieldtype": "Link", "options": "Loan Product", "width": 160},
        {"label": "Sanction Date", "fieldname": "sanction_date", "fieldtype": "Date", "width": 110},
        {"label": "Sanctioned (INR)", "fieldname": "loan_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Disbursed (INR)", "fieldname": "disbursed_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Outstanding Principal", "fieldname": "total_principal_outstanding", "fieldtype": "Currency", "width": 140},
        {"label": "Interest Accrued", "fieldname": "total_interest_payable", "fieldtype": "Currency", "width": 130},
        {"label": "Total Repaid", "fieldname": "total_amount_paid", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110}
    ]
    
    loans = frappe.get_all("Loan", fields=["name", "applicant_name", "loan_product", "posting_date", "loan_amount", "disbursed_amount", "total_principal_outstanding", "total_interest_payable", "total_amount_paid", "status"])
    data = []
    for l in loans:
        data.append({
            "loan_id": l.name,
            "borrower": l.applicant_name,
            "product": l.loan_product,
            "sanction_date": l.posting_date,
            "loan_amount": l.loan_amount,
            "disbursed_amount": l.disbursed_amount,
            "total_principal_outstanding": l.total_principal_outstanding,
            "total_interest_payable": l.total_interest_payable,
            "total_amount_paid": l.total_amount_paid,
            "status": l.status
        })
    return columns, data
"""
    },
    {
        "name": "EMI Collection Report",
        "folder": "emi_collection_report",
        "ref_doctype": "Loan Repayment",
        "execute_code": """import frappe

def execute(filters=None):
    columns = [
        {"label": "Repayment ID", "fieldname": "name", "fieldtype": "Link", "options": "Loan Repayment", "width": 140},
        {"label": "Loan ID", "fieldname": "against_loan", "fieldtype": "Link", "options": "Loan", "width": 140},
        {"label": "Borrower", "fieldname": "applicant", "fieldtype": "Data", "width": 180},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
        {"label": "Principal Paid", "fieldname": "principal_paid", "fieldtype": "Currency", "width": 120},
        {"label": "Interest Paid", "fieldname": "interest_paid", "fieldtype": "Currency", "width": 120},
        {"label": "Penalty Paid", "fieldname": "penalty_amount", "fieldtype": "Currency", "width": 110},
        {"label": "Total Amount Paid", "fieldname": "amount_paid", "fieldtype": "Currency", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]
    
    repayments = frappe.get_all("Loan Repayment", fields=["name", "against_loan", "applicant", "posting_date", "principal_paid", "interest_paid", "penalty_amount", "amount_paid", "docstatus"])
    data = []
    for r in repayments:
        data.append({
            "name": r.name,
            "against_loan": r.against_loan,
            "applicant": r.applicant,
            "posting_date": r.posting_date,
            "principal_paid": r.principal_paid,
            "interest_paid": r.interest_paid,
            "penalty_amount": r.penalty_amount or 0,
            "amount_paid": r.amount_paid,
            "status": "Submitted" if r.docstatus == 1 else ("Cancelled" if r.docstatus == 2 else "Draft")
        })
    return columns, data
"""
    },
    {
        "name": "DPD Aging Analysis",
        "folder": "dpd_aging_analysis",
        "ref_doctype": "Collection Task",
        "execute_code": """import frappe

def execute(filters=None):
    columns = [
        {"label": "Collection Task", "fieldname": "name", "fieldtype": "Link", "options": "Collection Task", "width": 130},
        {"label": "Loan ID", "fieldname": "loan", "fieldtype": "Link", "options": "Loan", "width": 130},
        {"label": "Borrower", "fieldname": "borrower_name", "fieldtype": "Data", "width": 170},
        {"label": "DPD Days", "fieldname": "dpd_days", "fieldtype": "Int", "width": 90},
        {"label": "DPD Bucket", "fieldname": "dpd_bucket", "fieldtype": "Data", "width": 120},
        {"label": "Overdue Amount", "fieldname": "overdue_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Overdue EMIs", "fieldname": "overdue_emi_count", "fieldtype": "Int", "width": 100},
        {"label": "Last Contact", "fieldname": "last_contact_date", "fieldtype": "Date", "width": 110},
        {"label": "Promise Date", "fieldname": "promise_to_pay_date", "fieldtype": "Date", "width": 110},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
        {"label": "Status", "fieldname": "collection_status", "fieldtype": "Data", "width": 110}
    ]
    
    tasks = frappe.get_all("Collection Task", fields=["name", "loan", "borrower_name", "dpd_days", "dpd_bucket", "overdue_amount", "overdue_emi_count", "last_contact_date", "promise_to_pay_date", "priority", "collection_status"])
    return columns, tasks
"""
    },
    {
        "name": "Disbursement Register",
        "folder": "disbursement_register",
        "ref_doctype": "Loan Disbursement",
        "execute_code": """import frappe

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
"""
    },
    {
        "name": "NPA and Recovery Report",
        "folder": "npa_and_recovery_report",
        "ref_doctype": "Collection Task",
        "execute_code": """import frappe

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
"""
    },
    {
        "name": "Borrower 360 Ledger",
        "folder": "borrower_360_ledger",
        "ref_doctype": "Borrower Profile",
        "execute_code": """import frappe

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
    loans = frappe.get_all("Loan", fields=["name", "applicant_name", "posting_date", "disbursed_amount", "total_amount_paid", "total_principal_outstanding"])
    for l in loans:
        data.append({
            "date": l.posting_date,
            "reference": l.name,
            "borrower": l.applicant_name,
            "event_type": "Loan Disbursement",
            "debit": l.disbursed_amount,
            "credit": 0,
            "balance": l.disbursed_amount
        })
        if l.total_amount_paid:
            data.append({
                "date": l.posting_date,
                "reference": "PMT-" + l.name,
                "borrower": l.applicant_name,
                "event_type": "EMI Repayment Cumulative",
                "debit": 0,
                "credit": l.total_amount_paid,
                "balance": l.total_principal_outstanding
            })
    return columns, data
"""
    }
]

for r in reports:
    r_dir = os.path.join(REPORTS_DIR, r["folder"])
    os.makedirs(r_dir, exist_ok=True)
    with open(os.path.join(r_dir, "__init__.py"), "w") as f:
        f.write("")
    
    report_json = {
        "add_total_row": 1,
        "columns": [],
        "creation": "2026-09-06 23:45:00.000000",
        "disable_prepared_report": 0,
        "disabled": 0,
        "docstatus": 0,
        "doctype": "Report",
        "is_standard": "Yes",
        "modified": "2026-09-06 23:45:00.000000",
        "module": "ZENVIQ Lending",
        "name": r["name"],
        "prepared_report": 0,
        "ref_doctype": r["ref_doctype"],
        "report_name": r["name"],
        "report_type": "Script Report",
        "roles": [
            {"role": "Lending Officer"},
            {"role": "Credit Analyst"},
            {"role": "Loan Approver"},
            {"role": "Collections Officer"},
            {"role": "Branch Manager Lending"},
            {"role": "Lending Admin"},
            {"role": "System Manager"}
        ]
    }
    with open(os.path.join(r_dir, r["folder"] + ".json"), "w") as f:
        json.dump(report_json, f, indent=2)
    
    with open(os.path.join(r_dir, r["folder"] + ".py"), "w") as f:
        f.write(r["execute_code"])
        
    js_content = 'frappe.query_reports["' + r["name"] + '"] = {\n    "filters": []\n};\n'
    with open(os.path.join(r_dir, r["folder"] + ".js"), "w") as f:
        f.write(js_content)
    
    print("Created report:", r["name"])

print("All 6 reports generated successfully!")
