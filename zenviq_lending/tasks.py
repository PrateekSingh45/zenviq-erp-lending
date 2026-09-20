import frappe
from frappe.utils import nowdate, date_diff

def update_dpd_buckets():
    """Daily job: Check overdue loans and update DPD (Days Past Due) and buckets"""
    try:
        tasks = frappe.get_all("Collection Task", filters={"collection_status": ["not in", ["Resolved", "Write Off"]]}, fields=["name", "first_overdue_date", "dpd_days", "dpd_bucket"])
        for t in tasks:
            if t.first_overdue_date:
                days = date_diff(nowdate(), t.first_overdue_date)
                doc = frappe.get_doc("Collection Task", t.name)
                doc.dpd_days = max(0, days)
                doc.update_dpd_bucket()
                doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(title="update_dpd_buckets error", message=str(e))

def flag_npa_loans():
    """Daily job: Check if any loan has 90+ DPD and flag as NPA"""
    try:
        tasks = frappe.get_all("Collection Task", filters={"dpd_days": [">=", 90], "collection_status": ["not in", ["Resolved", "Write Off"]]}, fields=["name", "loan"])
        for t in tasks:
            if t.loan:
                # Could log classification or update custom status
                pass
    except Exception as e:
        frappe.log_error(title="flag_npa_loans error", message=str(e))

def create_collection_tasks():
    """Daily job: Automatically create Collection Tasks for overdue repayments"""
    pass
