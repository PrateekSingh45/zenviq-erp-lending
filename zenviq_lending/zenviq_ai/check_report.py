import frappe
def run():
    doc = frappe.get_doc('Report', 'Branch-wise PAR 30')
    print(doc.as_dict())
