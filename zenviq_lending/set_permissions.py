import frappe

def run():
    doctypes = ['AI Settings', 'AI Change Request', 'AI Change Operation']
    
    for dt in doctypes:
        doc = frappe.get_doc('DocType', dt)
        if not doc.permissions:
            doc.append('permissions', {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1,
                'submit': 0,
                'cancel': 0,
                'amend': 0
            })
            doc.save(ignore_permissions=True)
            print(f'Added System Manager permission to {dt}')
            
    frappe.db.commit()
    frappe.clear_cache()
    print('Permissions updated and cache cleared.')

