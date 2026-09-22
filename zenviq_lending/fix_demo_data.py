import frappe
from frappe.utils import today, add_days, add_months, getdate
import random

def run():
    frappe.conf.developer_mode = 1
    company_name = 'ZENVIQ Finance Demo Private Limited'
    abbr = frappe.db.get_value('Company', company_name, 'abbr')
    print(f'Company: {company_name} (Abbr: {abbr})')

    # ---- Fix Designations: Re-create them properly ----
    print('\n=== STEP 1: Fixing Designations ===')
    designations = [
        'CEO', 'CTO', 'CFO', 'COO', 'VP Engineering',
        'Head - Credit', 'Head - Collections', 'Head - Sales',
        'Senior Software Engineer', 'Software Engineer',
        'Credit Analyst', 'Senior Credit Analyst',
        'Collection Officer', 'Senior Collection Officer',
        'Relationship Manager', 'Business Development Executive',
        'Operations Manager', 'Operations Executive',
        'HR Manager', 'HR Executive',
        'Compliance Officer', 'Legal Counsel',
        'Accountant', 'Senior Accountant',
        'Customer Support Executive', 'Team Lead - Support'
    ]
    for des_name in designations:
        if not frappe.db.exists('Designation', des_name):
            frappe.get_doc({'doctype': 'Designation', 'designation': des_name}).db_insert(ignore_if_duplicate=True)
            print(f'  + {des_name}')
    frappe.db.commit()
    print('  Done.')

    # ---- Fix Employees ----
    print('\n=== STEP 2: Creating Employees ===')
    dept_map = {}
    for d in frappe.get_all('Department', filters={'company': company_name}, pluck='name'):
        dept_map[d.replace(f' - {abbr}', '')] = d

    employees_data = [
        ('Prateek', 'Singh', 'Male', '1992-05-15', '2022-01-01', 'Technology', 'CEO', 250000),
        ('Ananya', 'Sharma', 'Female', '1990-08-22', '2022-01-01', 'Finance & Accounts', 'CFO', 200000),
        ('Rahul', 'Verma', 'Male', '1988-03-10', '2022-06-15', 'Technology', 'CTO', 220000),
        ('Pooja', 'Mishra', 'Female', '1993-11-05', '2023-02-01', 'Human Resources', 'HR Manager', 85000),
        ('Vikram', 'Malhotra', 'Male', '1991-07-28', '2023-04-10', 'Credit & Underwriting', 'Head - Credit', 120000),
        ('Sneha', 'Patel', 'Female', '1995-01-14', '2023-06-01', 'Sales & Distribution', 'Business Development Executive', 55000),
        ('Arjun', 'Gupta', 'Male', '1994-09-20', '2023-07-15', 'Technology', 'Senior Software Engineer', 95000),
        ('Neha', 'Kapoor', 'Female', '1996-04-08', '2023-08-01', 'Operations', 'Operations Manager', 75000),
        ('Rajesh', 'Kumar', 'Male', '1989-12-25', '2023-09-01', 'Collections', 'Head - Collections', 110000),
        ('Deepika', 'Reddy', 'Female', '1997-06-17', '2024-01-10', 'Credit & Underwriting', 'Credit Analyst', 45000),
        ('Amit Singh', 'Rathore', 'Male', '1993-02-14', '2024-02-01', 'Sales & Distribution', 'Relationship Manager', 60000),
        ('Kavita', 'Joshi', 'Female', '1995-08-30', '2024-03-15', 'Customer Support', 'Customer Support Executive', 35000),
        ('Suresh', 'Pandey', 'Male', '1990-10-12', '2024-04-01', 'Compliance & Legal', 'Compliance Officer', 90000),
        ('Riya', 'Agarwal', 'Female', '1998-03-22', '2024-05-01', 'Technology', 'Software Engineer', 65000),
        ('Manish', 'Tiwari', 'Male', '1992-07-07', '2024-06-01', 'Finance & Accounts', 'Senior Accountant', 70000),
        ('Shruti', 'Nair', 'Female', '1996-12-01', '2024-07-01', 'Human Resources', 'HR Executive', 40000),
        ('Karan', 'Mehta', 'Male', '1994-05-19', '2024-08-01', 'Collections', 'Collection Officer', 42000),
        ('Priyanka', 'Das', 'Female', '1997-09-15', '2024-09-01', 'Operations', 'Operations Executive', 38000),
        ('Rohit', 'Saxena', 'Male', '1991-01-30', '2024-10-01', 'Sales & Distribution', 'Head - Sales', 130000),
        ('Aishwarya', 'Iyer', 'Female', '1999-02-28', '2025-01-15', 'Technology', 'Software Engineer', 55000),
    ]

    employee_ids = {}
    for emp_data in employees_data:
        first_name, last_name, gender, dob, doj, dept, designation, salary = emp_data
        full_name = f'{first_name} {last_name}'

        existing = frappe.get_all('Employee', filters={'employee_name': full_name, 'company': company_name}, limit=1)
        if existing:
            employee_ids[full_name] = existing[0].name
            print(f'  exists: {full_name}')
            continue

        try:
            emp = frappe.new_doc('Employee')
            emp.first_name = first_name
            emp.last_name = last_name
            emp.gender = gender
            emp.date_of_birth = dob
            emp.date_of_joining = doj
            emp.company = company_name
            emp.department = dept_map.get(dept)
            emp.designation = designation if frappe.db.exists('Designation', designation) else None
            emp.status = 'Active'
            emp.employment_type = 'Full-time'
            emp.cell_phone = f'+91 98{random.randint(10000000, 99999999)}'
            emp.personal_email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
            emp.company_email = f'{first_name.lower()}.{last_name.lower()}@zenviqerp.com'
            emp.prefered_contact_email = 'Company Email'
            emp.ctc = salary * 12
            emp.insert(ignore_permissions=True)
            employee_ids[full_name] = emp.name
            print(f'  ✅ {full_name} ({emp.name})')
        except Exception as e:
            print(f'  ❌ {full_name}: {str(e)[:120]}')

    frappe.db.commit()

    # ---- Fix CRM Leads ----
    print('\n=== STEP 3: Creating CRM Leads ===')
    crm_leads = [
        ('Rakesh', 'Agarwal', 'rakesh@agartextiles.com', '+91 9876543210', 'Agar Textiles Pvt Ltd', 'Website'),
        ('Meena', 'Iyer', 'meena@southstarfinance.com', '+91 9988776655', 'South Star Finance Ltd', 'Referral'),
        ('Ajay', 'Bansal', 'ajay@bansalgroup.in', '+91 8877665544', 'Bansal Housing Finance', 'LinkedIn'),
        ('Nisha', 'Jain', 'nisha@jainmicrofinance.com', '+91 7766554433', 'Jain Microfinance Ltd', 'Cold Call'),
        ('Sunil', 'Chopra', 'sunil@chopracapital.com', '+91 6655443322', 'Chopra Capital Services', 'Event'),
        ('Priya', 'Shetty', 'priya@coastalfinserv.com', '+91 9998887776', 'Coastal Financial Services', 'Partner'),
        ('Vinod', 'Khanna', 'vinod@khannawealth.com', '+91 8887776665', 'Khanna Wealth Management', 'Webinar'),
        ('Anita', 'Deshmukh', 'anita@deshmukhlending.com', '+91 7776665554', 'Deshmukh Lending Corp', 'Website'),
        ('Gaurav', 'Mehta', 'gaurav@mehtafintech.io', '+91 6665554443', 'Mehta Fintech Solutions', 'LinkedIn'),
        ('Sunita', 'Reddy', 'sunita@reddycredit.com', '+91 5554443332', 'Reddy Credit Co-op', 'Referral'),
    ]
    statuses = ['Lead', 'Open', 'Replied', 'Opportunity', 'Interested', 'Converted', 'Do Not Contact']

    for i, ld in enumerate(crm_leads):
        first, last, email, phone, company, source = ld
        existing = frappe.get_all('Lead', filters={'email_id': email}, limit=1)
        if existing:
            print(f'  exists: {first} {last}')
            continue
        try:
            lead = frappe.new_doc('Lead')
            lead.first_name = first
            lead.last_name = last
            lead.email_id = email
            lead.mobile_no = phone
            lead.company_name = company
            lead.source = source if frappe.db.exists('Lead Source', source) else None
            lead.status = statuses[i % len(statuses)]
            lead.territory = 'India' if frappe.db.exists('Territory', 'India') else None
            lead.insert(ignore_permissions=True)
            print(f'  ✅ {first} {last} ({lead.name})')
        except Exception as e:
            print(f'  ❌ {first} {last}: {str(e)[:120]}')
    frappe.db.commit()

    # ---- Fix Opportunities ----
    print('\n=== STEP 4: Creating Opportunities ===')
    sales_stages = ['Prospecting', 'Qualification', 'Needs Analysis', 'Value Proposition', 'Proposal/Price Quote', 'Negotiation/Review', 'Closed Won', 'Closed Lost']
    for stage in sales_stages:
        if not frappe.db.exists('Sales Stage', stage):
            frappe.get_doc({'doctype': 'Sales Stage', 'stage_name': stage}).db_insert(ignore_if_duplicate=True)
    frappe.db.commit()

    opportunities = [
        ('Agar Textiles Pvt Ltd', 1500000, 'Qualification'),
        ('South Star Finance Ltd', 3500000, 'Needs Analysis'),
        ('Bansal Housing Finance', 800000, 'Value Proposition'),
        ('Chopra Capital Services', 5000000, 'Proposal/Price Quote'),
        ('Coastal Financial Services', 2200000, 'Negotiation/Review'),
    ]

    for company, amount, stage in opportunities:
        leads_found = frappe.get_all('Lead', filters={'company_name': company}, limit=1)
        if not leads_found:
            print(f'  ⚠️ No lead for {company}')
            continue
        existing = frappe.get_all('Opportunity', filters={'party_name': leads_found[0].name}, limit=1)
        if existing:
            print(f'  exists: {company}')
            continue
        try:
            opp = frappe.new_doc('Opportunity')
            opp.opportunity_from = 'Lead'
            opp.party_name = leads_found[0].name
            opp.opportunity_amount = amount
            opp.currency = 'INR'
            opp.sales_stage = stage if frappe.db.exists('Sales Stage', stage) else None
            opp.expected_closing = add_months(today(), random.randint(1, 3))
            opp.insert(ignore_permissions=True)
            print(f'  ✅ {company} (Rs {amount:,})')
        except Exception as e:
            print(f'  ❌ {company}: {str(e)[:120]}')
    frappe.db.commit()

    # ---- Fix Attendance ----
    print('\n=== STEP 5: Creating Attendance (30 days) ===')
    att_count = 0
    for emp_name, emp_id in employee_ids.items():
        for day_offset in range(30):
            att_date = add_days(today(), -day_offset)
            if getdate(att_date).weekday() in [5, 6]:
                continue
            existing = frappe.get_all('Attendance', filters={'employee': emp_id, 'attendance_date': att_date}, limit=1)
            if existing:
                continue
            try:
                att = frappe.new_doc('Attendance')
                att.employee = emp_id
                att.attendance_date = att_date
                att.company = company_name
                roll = random.random()
                if roll < 0.90:
                    att.status = 'Present'
                elif roll < 0.95:
                    att.status = 'Half Day'
                else:
                    att.status = 'On Leave'
                att.insert(ignore_permissions=True)
                att_count += 1
            except Exception:
                pass
        if att_count % 50 == 0 and att_count > 0:
            frappe.db.commit()
    frappe.db.commit()
    print(f'  ✅ Created {att_count} attendance records')

    print('\n🎉 ALL FIX STEPS COMPLETE!')
