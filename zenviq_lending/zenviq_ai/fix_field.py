import frappe
def run():
    frappe.conf.developer_mode = 1
    cf = frappe.get_doc('Custom Field', 'Lending Lead-retirement_date')
    cf.insert_after = ''  # Clear invalid insert_after value
    cf.save(ignore_permissions=True)
    frappe.db.commit()
    print('Fixed Custom Field')
    
