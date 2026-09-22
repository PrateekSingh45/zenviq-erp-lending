import frappe
def run():
    frappe.conf.developer_mode = 1
    props = frappe.get_all('Property Setter', filters={'doc_type': 'Lending Lead', 'field_name': 'email', 'property': 'reqd'}, fields=['name', 'value'])
    print('Property Setters for email reqd:', props)
    
