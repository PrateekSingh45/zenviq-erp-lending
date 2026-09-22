import frappe
import random

def run():
    company_name = 'ZENVIQ Finance Demo Private Limited'
    existing = frappe.get_all('Employee', filters={'employee_name': 'Amit Singh Rathore', 'company': company_name}, limit=1)
    if existing:
        print('Already exists')
        return
    emp = frappe.new_doc('Employee')
    emp.first_name = 'Amit Singh'
    emp.last_name = 'Rathore'
    emp.gender = 'Male'
    emp.date_of_birth = '1993-02-14'
    emp.date_of_joining = '2024-02-01'
    emp.company = company_name
    emp.status = 'Active'
    emp.employment_type = 'Full-time'
    emp.cell_phone = f'+91 98{random.randint(10000000, 99999999)}'
    emp.personal_email = 'amitsingh.rathore@gmail.com'
    emp.company_email = 'amitsingh.rathore@zenviqerp.com'
    emp.prefered_contact_email = 'Company Email'
    emp.ctc = 60000 * 12
    emp.flags.ignore_validate = True
    emp.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f'Created: {emp.name}')
