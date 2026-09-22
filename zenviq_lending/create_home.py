import frappe
def create():
    if not frappe.db.exists('Page', 'zenviq_home'):
        doc = frappe.new_doc('Page')
        doc.page_name = 'zenviq_home'
        doc.title = 'ZENVIQ Lending'
        doc.module = 'ZENVIQ Lending'
        doc.standard = 'Yes'
        doc.append('roles', {'role': 'System Manager'})
        doc.append('roles', {'role': 'All'})
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Page created.')
    else:
        print('Page already exists.')
