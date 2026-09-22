import frappe

def run():
    abbr = frappe.db.get_value('Company', 'ZENVIQ Finance Demo Private Limited', 'abbr')
    depts = frappe.get_all('Department', filters={'company': 'ZENVIQ Finance Demo Private Limited'}, pluck='name')
    print(f'ABBR={abbr}')
    print(f'EXISTING_DEPTS={depts}')
