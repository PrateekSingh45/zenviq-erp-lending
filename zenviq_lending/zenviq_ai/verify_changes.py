import frappe

def run():
    frappe.conf.developer_mode = 1
    
    # Check Custom Field
    cf = frappe.db.exists('Custom Field', {'dt': 'User', 'fieldname': 'retirement_date'})
    print(f'Custom Field exists: {cf}')
    if cf:
        print(frappe.get_doc('Custom Field', cf).as_dict())
        
    # Check Server Script
    scripts = frappe.get_all('Server Script', filters={'reference_doctype': 'Loan Application'}, fields=['name', 'script'])
    for s in scripts:
        print(f'\nServer Script: {s.name}\nScript:\n{s.script}')

