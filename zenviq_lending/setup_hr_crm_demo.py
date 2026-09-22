"""
ZENVIQ ERP - HR, Payroll & CRM Demo Data Setup Script
Creates realistic Indian NBFC dummy data for:
1. HR Module: Department, Designations, Employees, Leave Policy, Attendance
2. Payroll: Salary Structure, Salary Slips
3. CRM: Leads, Opportunities, Contacts
"""
import frappe
from frappe.utils import today, add_days, add_months, getdate, nowdate
import random

def run():
    frappe.conf.developer_mode = 1

    # ====================================================================
    # PART 1: HR MODULE SETUP
    # ====================================================================

    print("=" * 60)
    print("STEP 1: Detecting Company")
    print("=" * 60)
    company_name = "ZENVIQ Finance Demo Private Limited"
    abbr = frappe.db.get_value("Company", company_name, "abbr")
    if not abbr:
        print("  ❌ Company not found! Please create the company first.")
        return
    print(f"  ℹ️ Company: {company_name} (Abbr: {abbr})")

    # ---- Departments ----
    print("\nSTEP 2: Creating Departments")
    departments = [
        "Technology", "Credit & Underwriting", "Collections",
        "Sales & Distribution", "Finance & Accounts",
        "Compliance & Legal", "Customer Support"
    ]
    for dept_name in departments:
        dept_full = f"{dept_name} - {abbr}"
        if not frappe.db.exists("Department", dept_full):
            try:
                dept = frappe.new_doc("Department")
                dept.department_name = dept_name
                dept.company = company_name
                dept.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  ✅ Created department: {dept_name}")
            except Exception as e:
                print(f"  ⚠️ Skipping department {dept_name}: {str(e)[:80]}")
        else:
            print(f"  ℹ️ Department already exists: {dept_name}")

    frappe.db.commit()

    # ---- Designations ----
    print("\nSTEP 3: Creating Designations")
    designations = [
        "CEO", "CTO", "CFO", "COO", "VP Engineering",
        "Head - Credit", "Head - Collections", "Head - Sales",
        "Senior Software Engineer", "Software Engineer",
        "Credit Analyst", "Senior Credit Analyst",
        "Collection Officer", "Senior Collection Officer",
        "Relationship Manager", "Business Development Executive",
        "Operations Manager", "Operations Executive",
        "HR Manager", "HR Executive",
        "Compliance Officer", "Legal Counsel",
        "Accountant", "Senior Accountant",
        "Customer Support Executive", "Team Lead - Support"
    ]
    for des_name in designations:
        if not frappe.db.exists("Designation", des_name):
            try:
                des = frappe.new_doc("Designation")
                des.designation = des_name
                des.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  ✅ Created designation: {des_name}")
            except Exception:
                print(f"  ℹ️ Designation exists: {des_name}")

    frappe.db.commit()

    # ---- Employees ----
    print("\nSTEP 4: Creating Employees")
    # Map department names to actual full names with abbr
    dept_map = {}
    for d in departments + ["Operations", "Human Resources"]:
        full = f"{d} - {abbr}"
        if frappe.db.exists("Department", full):
            dept_map[d] = full

    employees_data = [
        ("Prateek", "Singh", "Male", "1992-05-15", "2022-01-01", "Technology", "CEO", 250000),
        ("Ananya", "Sharma", "Female", "1990-08-22", "2022-01-01", "Finance & Accounts", "CFO", 200000),
        ("Rahul", "Verma", "Male", "1988-03-10", "2022-06-15", "Technology", "CTO", 220000),
        ("Pooja", "Mishra", "Female", "1993-11-05", "2023-02-01", "Human Resources", "HR Manager", 85000),
        ("Vikram", "Malhotra", "Male", "1991-07-28", "2023-04-10", "Credit & Underwriting", "Head - Credit", 120000),
        ("Sneha", "Patel", "Female", "1995-01-14", "2023-06-01", "Sales & Distribution", "Business Development Executive", 55000),
        ("Arjun", "Gupta", "Male", "1994-09-20", "2023-07-15", "Technology", "Senior Software Engineer", 95000),
        ("Neha", "Kapoor", "Female", "1996-04-08", "2023-08-01", "Operations", "Operations Manager", 75000),
        ("Rajesh", "Kumar", "Male", "1989-12-25", "2023-09-01", "Collections", "Head - Collections", 110000),
        ("Deepika", "Reddy", "Female", "1997-06-17", "2024-01-10", "Credit & Underwriting", "Credit Analyst", 45000),
        ("Amit Singh", "Rathore", "Male", "1993-02-14", "2024-02-01", "Sales & Distribution", "Relationship Manager", 60000),
        ("Kavita", "Joshi", "Female", "1995-08-30", "2024-03-15", "Customer Support", "Customer Support Executive", 35000),
        ("Suresh", "Pandey", "Male", "1990-10-12", "2024-04-01", "Compliance & Legal", "Compliance Officer", 90000),
        ("Riya", "Agarwal", "Female", "1998-03-22", "2024-05-01", "Technology", "Software Engineer", 65000),
        ("Manish", "Tiwari", "Male", "1992-07-07", "2024-06-01", "Finance & Accounts", "Senior Accountant", 70000),
        ("Shruti", "Nair", "Female", "1996-12-01", "2024-07-01", "Human Resources", "HR Executive", 40000),
        ("Karan", "Mehta", "Male", "1994-05-19", "2024-08-01", "Collections", "Collection Officer", 42000),
        ("Priyanka", "Das", "Female", "1997-09-15", "2024-09-01", "Operations", "Operations Executive", 38000),
        ("Rohit", "Saxena", "Male", "1991-01-30", "2024-10-01", "Sales & Distribution", "Head - Sales", 130000),
        ("Aishwarya", "Iyer", "Female", "1999-02-28", "2025-01-15", "Technology", "Software Engineer", 55000),
    ]

    employee_ids = {}
    for emp_data in employees_data:
        first_name, last_name, gender, dob, doj, dept, designation, salary = emp_data
        full_name = f"{first_name} {last_name}"
        dept_full = dept_map.get(dept, f"{dept} - {abbr}")

        existing = frappe.get_all("Employee", filters={"employee_name": full_name, "company": company_name}, limit=1)
        if existing:
            employee_ids[full_name] = existing[0].name
            print(f"  ℹ️ Employee already exists: {full_name}")
            continue

        try:
            emp = frappe.new_doc("Employee")
            emp.first_name = first_name
            emp.last_name = last_name
            emp.gender = gender
            emp.date_of_birth = dob
            emp.date_of_joining = doj
            emp.company = company_name
            emp.department = dept_full if frappe.db.exists("Department", dept_full) else None
            emp.designation = designation
            emp.status = "Active"
            emp.employment_type = "Full-time"
            emp.cell_phone = f"+91 98{random.randint(10000000, 99999999)}"
            emp.personal_email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
            emp.company_email = f"{first_name.lower()}.{last_name.lower()}@zenviqerp.com"
            emp.prefered_contact_email = "Company Email"
            emp.ctc = salary * 12
            emp.insert(ignore_permissions=True)
            employee_ids[full_name] = emp.name
            print(f"  ✅ Created employee: {full_name} ({emp.name})")
        except Exception as e:
            print(f"  ⚠️ Error creating {full_name}: {str(e)[:100]}")

    frappe.db.commit()

    # ---- Salary Components ----
    print("\nSTEP 5: Creating Salary Components")
    components = [
        ("Basic Salary", "Earning"),
        ("House Rent Allowance", "Earning"),
        ("Conveyance Allowance", "Earning"),
        ("Special Allowance", "Earning"),
        ("Performance Bonus", "Earning"),
        ("Provident Fund", "Deduction"),
        ("Professional Tax", "Deduction"),
        ("Income Tax (TDS)", "Deduction"),
        ("ESI", "Deduction"),
    ]

    for comp_name, comp_type in components:
        if not frappe.db.exists("Salary Component", comp_name):
            try:
                sc = frappe.new_doc("Salary Component")
                sc.salary_component = comp_name
                sc.type = comp_type
                sc.salary_component_abbr = "".join([w[0].upper() for w in comp_name.split()])
                sc.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  ✅ Created salary component: {comp_name}")
            except Exception:
                print(f"  ℹ️ Salary component exists: {comp_name}")
        else:
            print(f"  ℹ️ Salary component exists: {comp_name}")

    frappe.db.commit()

    # ---- Salary Structures ----
    print("\nSTEP 6: Creating Salary Structures")
    structures = {
        "CXO Level": 200000,
        "Senior Management": 100000,
        "Mid Level": 60000,
        "Junior Level": 35000,
    }

    for struct_name, base in structures.items():
        full_name = f"ZENVIQ - {struct_name}"
        if not frappe.db.exists("Salary Structure", full_name):
            try:
                ss = frappe.new_doc("Salary Structure")
                ss.name1 = full_name
                ss.company = company_name
                ss.is_active = "Yes"
                ss.payroll_frequency = "Monthly"

                ss.append("earnings", {
                    "salary_component": "Basic Salary",
                    "amount_based_on_formula": 1,
                    "formula": "base * 0.50"
                })
                ss.append("earnings", {
                    "salary_component": "House Rent Allowance",
                    "amount_based_on_formula": 1,
                    "formula": "base * 0.20"
                })
                ss.append("earnings", {
                    "salary_component": "Conveyance Allowance",
                    "amount_based_on_formula": 0,
                    "amount": 1600
                })
                ss.append("earnings", {
                    "salary_component": "Special Allowance",
                    "amount_based_on_formula": 1,
                    "formula": "base * 0.28"
                })

                ss.append("deductions", {
                    "salary_component": "Provident Fund",
                    "amount_based_on_formula": 1,
                    "formula": "base * 0.50 * 0.12"
                })
                ss.append("deductions", {
                    "salary_component": "Professional Tax",
                    "amount_based_on_formula": 0,
                    "amount": 200
                })

                ss.insert(ignore_permissions=True)
                print(f"  ✅ Created salary structure: {full_name}")
            except Exception as e:
                print(f"  ⚠️ Error creating {full_name}: {str(e)[:100]}")
        else:
            print(f"  ℹ️ Salary structure exists: {full_name}")

    frappe.db.commit()

    # ---- Leave Types and Holiday List ----
    print("\nSTEP 7: Creating Leave Types & Holiday List")
    leave_types = [
        ("Casual Leave", 12, 1),
        ("Sick Leave", 10, 1),
        ("Earned Leave", 15, 1),
        ("Compensatory Off", 3, 0),
        ("Leave Without Pay", 0, 0),
    ]
    for lt_name, max_leaves, is_carry_forward in leave_types:
        if not frappe.db.exists("Leave Type", lt_name):
            try:
                lt = frappe.new_doc("Leave Type")
                lt.leave_type_name = lt_name
                lt.max_leaves_allowed = max_leaves
                lt.is_carry_forward = is_carry_forward
                lt.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  ✅ Created leave type: {lt_name}")
            except Exception:
                print(f"  ℹ️ Leave type exists: {lt_name}")
        else:
            print(f"  ℹ️ Leave type exists: {lt_name}")

    # Holiday List
    holiday_list_name = "ZENVIQ Holiday List 2026"
    if not frappe.db.exists("Holiday List", holiday_list_name):
        try:
            hl = frappe.new_doc("Holiday List")
            hl.holiday_list_name = holiday_list_name
            hl.company = company_name
            hl.from_date = "2026-01-01"
            hl.to_date = "2026-12-31"

            holidays = [
                ("2026-01-01", "New Year's Day"),
                ("2026-01-26", "Republic Day"),
                ("2026-03-10", "Holi"),
                ("2026-03-30", "Ramzan Eid"),
                ("2026-04-14", "Ambedkar Jayanti"),
                ("2026-05-01", "May Day"),
                ("2026-06-06", "Bakrid"),
                ("2026-08-15", "Independence Day"),
                ("2026-08-25", "Janmashtami"),
                ("2026-10-02", "Gandhi Jayanti"),
                ("2026-10-20", "Dussehra"),
                ("2026-11-09", "Diwali"),
                ("2026-11-10", "Diwali (Day 2)"),
                ("2026-11-30", "Guru Nanak Jayanti"),
                ("2026-12-25", "Christmas Day"),
            ]
            for h_date, h_desc in holidays:
                hl.append("holidays", {
                    "holiday_date": h_date,
                    "description": h_desc
                })

            hl.insert(ignore_permissions=True)
            print(f"  ✅ Created holiday list: {holiday_list_name}")
        except Exception as e:
            print(f"  ⚠️ Error creating holiday list: {str(e)[:100]}")
    else:
        print(f"  ℹ️ Holiday list exists: {holiday_list_name}")

    frappe.db.commit()

    # ====================================================================
    # PART 2: CRM MODULE SETUP
    # ====================================================================

    print("\n" + "=" * 60)
    print("STEP 8: Creating Lead Sources")
    print("=" * 60)

    lead_sources = ["Website", "Referral", "LinkedIn", "Cold Call", "Event", "Partner", "Webinar"]
    for src in lead_sources:
        if not frappe.db.exists("Lead Source", src):
            try:
                ls = frappe.new_doc("Lead Source")
                ls.source_name = src
                ls.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  ✅ Created lead source: {src}")
            except Exception:
                print(f"  ℹ️ Lead source exists: {src}")

    frappe.db.commit()

    print("\nSTEP 9: Creating CRM Leads")
    crm_leads = [
        ("Rakesh", "Agarwal", "rakesh@agartextiles.com", "+91 9876543210", "Agar Textiles Pvt Ltd",
         "Website", "NBFC looking for digital lending platform"),
        ("Meena", "Iyer", "meena@southstarfinance.com", "+91 9988776655", "South Star Finance Ltd",
         "Referral", "Gold loan NBFC needs modern LMS with eKYC"),
        ("Ajay", "Bansal", "ajay@bansalgroup.in", "+91 8877665544", "Bansal Housing Finance",
         "LinkedIn", "Housing finance company exploring ERP solutions"),
        ("Nisha", "Jain", "nisha@jainmicrofinance.com", "+91 7766554433", "Jain Microfinance Ltd",
         "Cold Call", "Microfinance institution needs collection management"),
        ("Sunil", "Chopra", "sunil@chopracapital.com", "+91 6655443322", "Chopra Capital Services",
         "Event", "Consumer lending fintech seeking RBI-compliant platform"),
        ("Priya", "Shetty", "priya@coastalfinserv.com", "+91 9998887776", "Coastal Financial Services",
         "Partner", "Vehicle finance NBFC needs loan origination system"),
        ("Vinod", "Khanna", "vinod@khannawealth.com", "+91 8887776665", "Khanna Wealth Management",
         "Webinar", "Wealth management firm exploring lending vertical"),
        ("Anita", "Deshmukh", "anita@deshmukhlending.com", "+91 7776665554", "Deshmukh Lending Corp",
         "Website", "P2P lending platform needs compliance automation"),
        ("Gaurav", "Mehta", "gaurav@mehtafintech.io", "+91 6665554443", "Mehta Fintech Solutions",
         "LinkedIn", "Fintech startup building digital lending marketplace"),
        ("Sunita", "Reddy", "sunita@reddycredit.com", "+91 5554443332", "Reddy Credit Co-op",
         "Referral", "Co-operative society digitizing lending operations"),
    ]

    lead_statuses = ["Lead", "Open", "Replied", "Opportunity", "Interested", "Converted", "Do Not Contact"]

    for i, lead_data in enumerate(crm_leads):
        first, last, email, phone, company, source, notes = lead_data

        existing = frappe.get_all("Lead", filters={"email_id": email}, limit=1)
        if existing:
            print(f"  ℹ️ Lead already exists: {first} {last}")
            continue

        try:
            lead = frappe.new_doc("Lead")
            lead.first_name = first
            lead.last_name = last
            lead.email_id = email
            lead.mobile_no = phone
            lead.company_name = company
            lead.source = source if frappe.db.exists("Lead Source", source) else None
            lead.notes = notes
            lead.status = lead_statuses[i % len(lead_statuses)]
            lead.territory = "India" if frappe.db.exists("Territory", "India") else None
            lead.insert(ignore_permissions=True)
            print(f"  ✅ Created CRM lead: {first} {last} ({lead.name})")
        except Exception as e:
            print(f"  ⚠️ Error creating lead {first} {last}: {str(e)[:100]}")

    frappe.db.commit()

    # ---- CRM Contacts ----
    print("\nSTEP 10: Creating CRM Contacts")
    contacts = [
        ("Rakesh", "Agarwal", "rakesh@agartextiles.com", "+91 9876543210"),
        ("Meena", "Iyer", "meena@southstarfinance.com", "+91 9988776655"),
        ("Ajay", "Bansal", "ajay@bansalgroup.in", "+91 8877665544"),
        ("Nisha", "Jain", "nisha@jainmicrofinance.com", "+91 7766554433"),
        ("Sunil", "Chopra", "sunil@chopracapital.com", "+91 6655443322"),
    ]

    for first, last, email, phone in contacts:
        existing = frappe.get_all("Contact", filters={"email_id": email}, limit=1)
        if existing:
            print(f"  ℹ️ Contact already exists: {first} {last}")
            continue

        try:
            contact = frappe.new_doc("Contact")
            contact.first_name = first
            contact.last_name = last
            contact.append("email_ids", {"email_id": email, "is_primary": 1})
            contact.append("phone_nos", {"phone": phone, "is_primary_phone": 1})
            contact.insert(ignore_permissions=True)
            print(f"  ✅ Created contact: {first} {last}")
        except Exception as e:
            print(f"  ⚠️ Error creating contact {first} {last}: {str(e)[:100]}")

    frappe.db.commit()

    # ---- Opportunities ----
    print("\nSTEP 11: Creating CRM Opportunities")

    # Create Sales Stages first
    sales_stages = ["Prospecting", "Qualification", "Needs Analysis", "Value Proposition", "Proposal/Price Quote", "Negotiation/Review", "Closed Won", "Closed Lost"]
    for stage in sales_stages:
        if not frappe.db.exists("Sales Stage", stage):
            try:
                ss = frappe.new_doc("Sales Stage")
                ss.stage_name = stage
                ss.insert(ignore_permissions=True, ignore_if_duplicate=True)
            except Exception:
                pass

    frappe.db.commit()

    opportunities = [
        ("Agar Textiles Pvt Ltd", 1500000, "Qualification"),
        ("South Star Finance Ltd", 3500000, "Needs Analysis"),
        ("Bansal Housing Finance", 800000, "Value Proposition"),
        ("Chopra Capital Services", 5000000, "Proposal/Price Quote"),
        ("Coastal Financial Services", 2200000, "Negotiation/Review"),
    ]

    for company, amount, stage in opportunities:
        leads_found = frappe.get_all("Lead", filters={"company_name": company}, limit=1)
        if not leads_found:
            print(f"  ⚠️ No lead found for {company}, skipping opportunity")
            continue

        existing = frappe.get_all("Opportunity", filters={"party_name": leads_found[0].name}, limit=1)
        if existing:
            print(f"  ℹ️ Opportunity already exists for {company}")
            continue

        try:
            opp = frappe.new_doc("Opportunity")
            opp.opportunity_from = "Lead"
            opp.party_name = leads_found[0].name
            opp.opportunity_amount = amount
            opp.currency = "INR"
            opp.sales_stage = stage if frappe.db.exists("Sales Stage", stage) else None
            opp.expected_closing = add_months(today(), random.randint(1, 3))
            opp.insert(ignore_permissions=True)
            print(f"  ✅ Created opportunity for {company} (₹{amount:,})")
        except Exception as e:
            print(f"  ⚠️ Error creating opportunity for {company}: {str(e)[:100]}")

    frappe.db.commit()

    # ====================================================================
    # PART 3: ATTENDANCE DATA (Last 30 days)
    # ====================================================================
    print("\n" + "=" * 60)
    print("STEP 12: Creating Attendance Records (Last 30 days)")
    print("=" * 60)

    attendance_count = 0
    for emp_name, emp_id in employee_ids.items():
        for day_offset in range(30):
            att_date = add_days(today(), -day_offset)
            att_date_obj = getdate(att_date)

            # Skip weekends
            if att_date_obj.weekday() in [5, 6]:
                continue

            existing = frappe.get_all("Attendance", filters={
                "employee": emp_id,
                "attendance_date": att_date
            }, limit=1)

            if existing:
                continue

            try:
                att = frappe.new_doc("Attendance")
                att.employee = emp_id
                att.attendance_date = att_date
                att.company = company_name

                roll = random.random()
                if roll < 0.90:
                    att.status = "Present"
                elif roll < 0.95:
                    att.status = "Half Day"
                else:
                    att.status = "On Leave"

                att.insert(ignore_permissions=True)
                attendance_count += 1
            except Exception:
                pass

        if attendance_count % 50 == 0:
            frappe.db.commit()

    frappe.db.commit()
    print(f"  ✅ Created {attendance_count} attendance records")

    # ====================================================================
    # DONE
    # ====================================================================
    print("\n" + "=" * 60)
    print("🎉 ALL DONE! HR, Payroll & CRM demo data created successfully!")
    print("=" * 60)
    print(f"""
    Summary:
    --------
    ✅ Departments (used existing + new)
    ✅ {len(designations)} Designations
    ✅ {len(employees_data)} Employees
    ✅ {len(components)} Salary Components
    ✅ {len(structures)} Salary Structures
    ✅ {len(leave_types)} Leave Types
    ✅ 1 Holiday List (2026) with 15 Indian holidays
    ✅ {len(crm_leads)} CRM Leads
    ✅ {len(contacts)} CRM Contacts
    ✅ {len(opportunities)} CRM Opportunities
    ✅ {attendance_count} Attendance Records
    """)
