import frappe

def create_it():
    frappe.conf.developer_mode = 1
    if not frappe.db.exists('Report', 'RBI SMA and Provisioning'):
        doc = frappe.new_doc('Report')
        doc.report_name = 'RBI SMA and Provisioning'
        doc.ref_doctype = 'Loan'
        doc.report_type = 'Script Report'
        doc.is_standard = 'Yes'
        doc.module = 'ZENVIQ Lending'
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Report created!')
    else:
        print('Report already exists')
