import frappe

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
