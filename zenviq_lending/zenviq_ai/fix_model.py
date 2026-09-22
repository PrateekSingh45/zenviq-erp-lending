import frappe

def run():
    frappe.conf.developer_mode = 1
    
    settings = frappe.get_single('AI Settings')
    settings.model = 'gemini-3.6-flash'
    settings.save(ignore_permissions=True)
    frappe.db.commit()
    print('Updated AI Settings model to gemini-3.6-flash')
    
