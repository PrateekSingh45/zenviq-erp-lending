import frappe
def run():
    frappe.conf.developer_mode = 1
    scripts = frappe.get_all('Server Script', filters={'reference_doctype': 'Lending Lead'}, fields=['name', 'script'])
    for s in scripts:
        print(s)
    
