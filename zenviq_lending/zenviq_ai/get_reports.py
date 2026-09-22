import frappe
def run():
    frappe.conf.developer_mode = 1
    reports = frappe.get_all('Report', filters={'ref_doctype': 'Loan'}, fields=['name'], order_by='creation desc', limit=3)
    for r in reports:
        print(r.name)
