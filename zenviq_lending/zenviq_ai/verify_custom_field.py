import frappe
def run():
    frappe.conf.developer_mode = 1
    fields = frappe.get_all('Custom Field', filters={'dt': 'Lending Lead'}, fields=['name', 'fieldname', 'insert_after'])
    print(fields)
    
