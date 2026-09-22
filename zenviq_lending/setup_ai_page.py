import frappe

def run():
    frappe.conf.developer_mode = 1
    
    if not frappe.db.exists('Page', 'zenviq_ai_chat'):
        doc = frappe.get_doc({
            'doctype': 'Page',
            'page_name': 'zenviq_ai_chat',
            'title': 'ZENVIQ AI',
            'module': 'ZENVIQ AI',
            'standard': 'Yes',
            'roles': [
                {'role': 'System Manager'}
            ]
        })
        doc.insert(ignore_permissions=True)
        print('Created Page: zenviq_ai_chat')
    else:
        print('Page already exists.')
        
    frappe.db.commit()

