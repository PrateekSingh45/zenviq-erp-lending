import os, frappe
from frappe.utils import nowdate, add_months, add_days, flt

os.chdir("sites")
frappe.init(site="zenviq.localhost", sites_path=".")
frappe.connect()

company_name = "ZENVIQ Finance Demo Private Limited"
company_abbr = "ZFDPL"

print("--- Step 1: Creating Customer Records ---")
borrowers_data = [
    {
        "name": "Rajesh Kumar Sharma",
        "email": "rajesh.sharma@example.com",
        "phone": "+91 9810234567",
        "pan": "BKPPS1289K",
        "aadhaar": "4589 1234 5678",
        "income": 85000,
        "employer": "Tech Mahindra Ltd",
        "designation": "Senior Solutions Architect",
        "city": "Aligarh",
        "state": "Uttar Pradesh",
        "address": "42-B, Civil Lines, Near Company Garden, Aligarh",
        "cibil": 780,
        "risk": "A - Low Risk",
        "lead_source": "DSA / Agent"
    },
    {
        "name": "Priya Gupta",
        "email": "priya.gupta@example.com",
        "phone": "+91 9823456789",
        "pan": "ABCPG5678M",
        "aadhaar": "8912 3456 7890",
        "income": 140000,
        "employer": "Priya Fashion & Textiles",
        "designation": "Proprietor / Business Owner",
        "city": "Aligarh",
        "state": "Uttar Pradesh",
        "address": "Shop No 14, Centre Point Market, Aligarh",
        "cibil": 742,
        "risk": "B - Moderate Risk",
        "lead_source": "Online Application"
    },
    {
        "name": "Amit Singh Rathore",
        "email": "amit.rathore@example.com",
        "phone": "+91 9834567890",
        "pan": "DFRPA9876R",
        "aadhaar": "2345 6789 0123",
        "income": 45000,
        "employer": "Speedway Logistics",
        "designation": "Operations Supervisor",
        "city": "Aligarh",
        "state": "Uttar Pradesh",
        "address": "108, Ramghat Road, Aligarh",
        "cibil": 710,
        "risk": "C - Medium Risk",
        "lead_source": "Walk-in"
    },
    {
        "name": "Sunita Devi Verma",
        "email": "sunita.verma@example.com",
        "phone": "+91 9845678901",
        "pan": "CKLPV4321E",
        "aadhaar": "6789 0123 4567",
        "income": 62000,
        "employer": "Kendriya Vidyalaya Aligarh",
        "designation": "Senior Secondary Teacher",
        "city": "Aligarh",
        "state": "Uttar Pradesh",
        "address": "Flat 302, Green Valley Apartments, Aligarh",
        "cibil": 815,
        "risk": "A - Low Risk",
        "lead_source": "Referral"
    },
    {
        "name": "Vikram Malhotra",
        "email": "vikram.malhotra@example.com",
        "phone": "+91 9876543210",
        "pan": "GHUPM8765Q",
        "aadhaar": "9012 3456 7891",
        "income": 50000,
        "employer": "Independent Trader",
        "designation": "Proprietor",
        "city": "Aligarh",
        "state": "Uttar Pradesh",
        "address": "Near Railway Station Road, Aligarh",
        "cibil": 635,
        "risk": "D - High Risk",
        "lead_source": "DSA / Agent"
    }
]

customer_map = {}
borrower_map = {}

for b in borrowers_data:
    # 1. Customer
    cust_name = b["name"]
    if not frappe.db.exists("Customer", cust_name):
        cust = frappe.new_doc("Customer")
        cust.customer_name = cust_name
        cust.customer_type = "Individual"
        cust.customer_group = "Individual"
        cust.territory = "India"
        cust.insert(ignore_permissions=True)
        print(f"Created Customer: {cust_name}")
    customer_map[cust_name] = cust_name

    # 2. Lending Lead
    lead_name = frappe.db.get_value("Lending Lead", {"applicant_name": b["name"]})
    if not lead_name:
        lead = frappe.new_doc("Lending Lead")
        lead.applicant_name = b["name"]
        lead.mobile_number = b["phone"]
        lead.email = b["email"]
        lead.lead_source = b["lead_source"]
        lead.lead_status = "Converted"
        lead.employment_type = "Salaried" if "Teacher" in b["designation"] or "Consultant" in b["designation"] or "Architect" in b["designation"] or "Supervisor" in b["designation"] else "Business Owner"
        lead.monthly_income = b["income"]
        lead.city = b["city"]
        lead.state = b["state"]
        lead.full_address = b["address"]
        lead.requested_amount = 500000
        lead.insert(ignore_permissions=True)
        lead_name = lead.name
        print(f"Created Lending Lead: {lead_name}")

    # 3. Borrower Profile
    bp_name = frappe.db.get_value("Borrower Profile", {"full_name": b["name"]})
    if not bp_name:
        bp = frappe.new_doc("Borrower Profile")
        bp.full_name = b["name"]
        bp.mobile_number = b["phone"]
        bp.email = b["email"]
        bp.pan_number = b["pan"]
        bp.aadhaar_number = b["aadhaar"]
        bp.customer = cust_name
        bp.lending_lead = lead_name
        bp.employment_type = "Salaried" if b["income"] in [85000, 45000, 62000] else "Business Owner"
        bp.employer_name = b["employer"]
        bp.designation = b["designation"]
        bp.monthly_income = b["income"]
        bp.city = b["city"]
        bp.state = b["state"]
        bp.address = b["address"]
        bp.kyc_status = "Verified"
        bp.aadhaar_verified = 1
        bp.pan_verified = 1
        bp.bank_verified = 1
        bp.credit_score = b["cibil"]
        bp.risk_category = b["risk"]
        bp.existing_loan_count = 1 if b["cibil"] > 700 else 2
        bp.existing_emi_total = 7500 if b["cibil"] > 700 else 18000
        bp.insert(ignore_permissions=True)
        bp_name = bp.name
        print(f"Created Borrower Profile: {bp_name} ({b['name']})")
    borrower_map[b["name"]] = bp_name

frappe.db.commit()

print("\n--- Step 2: Creating KYC Verifications & Assessments ---")
from zenviq_lending.sandbox.ekyc import verify_aadhaar, verify_pan
from zenviq_lending.sandbox.bank_statement import analyze_statement

for b in borrowers_data:
    bp_name = borrower_map[b["name"]]
    # KYC Verification
    if not frappe.db.exists("KYC Verification", {"borrower_profile": bp_name}):
        kyc = frappe.new_doc("KYC Verification")
        kyc.borrower_profile = bp_name
        kyc.verification_status = "Approved"
        kyc.aadhaar_number = b["aadhaar"]
        kyc.aadhaar_status = "Verified"
        kyc.aadhaar_response = frappe.as_json(verify_aadhaar(b["aadhaar"], b["name"]))
        kyc.pan_number = b["pan"]
        kyc.pan_status = "Verified"
        kyc.pan_response = frappe.as_json(verify_pan(b["pan"], b["name"]))
        kyc.bank_analysis_status = "Completed"
        kyc.bank_analysis_response = frappe.as_json(analyze_statement(b["name"]))
        kyc.avg_monthly_balance = 24500
        kyc.avg_monthly_credits = b["income"]
        kyc.avg_monthly_debits = int(b["income"] * 0.72)
        kyc.append("kyc_documents", {
            "document_type": "Aadhaar Card",
            "document_number": b["aadhaar"],
            "verified": 1
        })
        kyc.append("kyc_documents", {
            "document_type": "PAN Card",
            "document_number": b["pan"],
            "verified": 1
        })
        kyc.append("kyc_documents", {
            "document_type": "Bank Statement",
            "document_number": "6-Months HDFC Bank",
            "verified": 1
        })
        kyc.insert(ignore_permissions=True)
        kyc.docstatus = 1
        kyc.save(ignore_permissions=True)
        print(f"Created KYC Verification: {kyc.name} for {b['name']}")

    # Credit Assessment
    if not frappe.db.exists("Credit Assessment", {"borrower_profile": bp_name}):
        ca = frappe.new_doc("Credit Assessment")
        ca.borrower_profile = bp_name
        ca.assessment_status = "Completed"
        ca.assessment_date = add_days(nowdate(), -45)
        ca.declared_monthly_income = b["income"]
        ca.verified_monthly_income = b["income"]
        ca.existing_emi = 7500 if b["cibil"] > 700 else 18000
        ca.proposed_emi = 15500
        ca.credit_score = b["cibil"]
        ca.risk_category = b["risk"]
        ca.calculate_ratios()
        ca.calculate_overall_score()
        ca.append("assessment_parameters", {"parameter": "Employment Stability", "score": 9, "max_score": 10})
        ca.append("assessment_parameters", {"parameter": "Banking Relationship", "score": 8, "max_score": 10})
        ca.append("assessment_parameters", {"parameter": "Repayment History", "score": 9, "max_score": 10})
        ca.insert(ignore_permissions=True)
        ca.docstatus = 1
        ca.save(ignore_permissions=True)
        print(f"Created Credit Assessment: {ca.name} for {b['name']} (Score: {ca.overall_score})")

frappe.db.commit()

print("\n--- Step 3: Specific Loan Journey Records ---")

# Borrower 1: Rajesh Kumar Sharma - Fully Disbursed, 3 EMIs Repaid
rajesh_cust = customer_map["Rajesh Kumar Sharma"]
rajesh_loan_id = frappe.db.get_value("Loan", {"applicant": rajesh_cust})
disb_bank_acc = f"ZENVIQ Lending Bank Account - {company_abbr}"
loan_portfolio_acc = f"Loan Portfolio (Advances) - {company_abbr}"
interest_income_acc = f"Interest Income on Loans - {company_abbr}"
penalty_income_acc = f"Penalty Income on Loans - {company_abbr}"

if not rajesh_loan_id:
    # Loan Application
    la = frappe.new_doc("Loan Application")
    la.applicant_type = "Customer"
    la.applicant = rajesh_cust
    la.company = company_name
    la.loan_product = "ZENVIQ-PL-01"
    la.loan_amount = 500000
    la.rate_of_interest = 14.0
    la.repayment_method = "Repay Fixed Amount per Period"
    la.repayment_periods = 36
    la.status = "Approved"
    la.insert(ignore_permissions=True)
    la.docstatus = 1
    la.save(ignore_permissions=True)

    # eSign Request
    from zenviq_lending.sandbox.esign import complete_esign
    es = frappe.new_doc("eSign Request")
    es.borrower_profile = borrower_map["Rajesh Kumar Sharma"]
    es.document_type = "Loan Agreement"
    es.esign_status = "Signed"
    es.esign_transaction_id = "ESIGN-TXN-RAJESH-9842"
    es.digital_signature_hash = "SHA256:4FA89B124C57E88A19B04D3F9E182A4C"
    es.sandbox_response = frappe.as_json(complete_esign(es.esign_transaction_id, "Loan Agreement"))
    es.insert(ignore_permissions=True)

    # Loan
    loan = frappe.new_doc("Loan")
    loan.applicant_type = "Customer"
    loan.applicant = rajesh_cust
    loan.company = company_name
    loan.loan_product = "ZENVIQ-PL-01"
    loan.posting_date = add_months(nowdate(), -3)
    loan.loan_amount = 500000
    loan.rate_of_interest = 14.0
    loan.repayment_method = "Repay Fixed Amount per Period"
    loan.repayment_periods = 36
    loan.monthly_repayment_amount = 17089
    loan.mode_of_payment = "Bank Transfer"
    loan.disbursement_account = disb_bank_acc
    loan.payment_account = disb_bank_acc
    loan.loan_account = loan_portfolio_acc
    loan.interest_income_account = interest_income_acc
    loan.penalty_income_account = penalty_income_acc
    loan.status = "Disbursed"
    loan.disbursed_amount = 500000
    loan.total_amount_paid = 51267
    loan.total_principal_outstanding = 462500
    loan.insert(ignore_permissions=True)
    loan.docstatus = 1
    loan.save(ignore_permissions=True)
    rajesh_loan_id = loan.name
    print(f"Created Active Disbursed Loan for Rajesh: {rajesh_loan_id}")

    # Create 3 repayments for Rajesh
    for i in range(1, 4):
        rep = frappe.new_doc("Loan Repayment")
        rep.against_loan = rajesh_loan_id
        rep.applicant_type = "Customer"
        rep.applicant = rajesh_cust
        rep.posting_date = add_months(add_months(nowdate(), -3), i)
        rep.amount_paid = 17089
        rep.principal_paid = 12500
        rep.interest_paid = 4589
        rep.penalty_amount = 0
        rep.flags.ignore_validate = True
        rep.insert(ignore_permissions=True)
        rep.docstatus = 1
        rep.save(ignore_permissions=True)
        print(f"Created EMI Repayment #{i} for Rajesh: {rep.name}")

# Borrower 2: Priya Gupta - Approved / Sanctioned, eSigned, pending disbursement
priya_cust = customer_map["Priya Gupta"]
if not frappe.db.exists("Loan Application", {"applicant": priya_cust}):
    la2 = frappe.new_doc("Loan Application")
    la2.applicant_type = "Customer"
    la2.applicant = priya_cust
    la2.company = company_name
    la2.loan_product = "ZENVIQ-BL-01"
    la2.loan_amount = 1000000
    la2.rate_of_interest = 18.0
    la2.repayment_method = "Repay Fixed Amount per Period"
    la2.repayment_periods = 48
    la2.status = "Approved"
    la2.insert(ignore_permissions=True)
    la2.docstatus = 1
    la2.save(ignore_permissions=True)

    from zenviq_lending.sandbox.esign import complete_esign
    es2 = frappe.new_doc("eSign Request")
    es2.borrower_profile = borrower_map["Priya Gupta"]
    es2.document_type = "Sanction Letter"
    es2.esign_status = "Signed"
    es2.esign_transaction_id = "ESIGN-TXN-PRIYA-7712"
    es2.digital_signature_hash = "SHA256:7B88C45A9E123DF8012B45CD990A1245"
    es2.sandbox_response = frappe.as_json(complete_esign(es2.esign_transaction_id, "Sanction Letter"))
    es2.insert(ignore_permissions=True)
    print(f"Created Sanctioned Application for Priya Gupta: {la2.name}")

# Borrower 3: Amit Singh Rathore - In Credit Assessment stage (already created CA)

# Borrower 4: Sunita Devi Verma - Fully Repaid & Closed with NOC
sunita_cust = customer_map["Sunita Devi Verma"]
sunita_loan_id = frappe.db.get_value("Loan", {"applicant": sunita_cust})
if not sunita_loan_id:
    s_loan = frappe.new_doc("Loan")
    s_loan.applicant_type = "Customer"
    s_loan.applicant = sunita_cust
    s_loan.company = company_name
    s_loan.loan_product = "ZENVIQ-CD-01"
    s_loan.posting_date = add_months(nowdate(), -14)
    s_loan.loan_amount = 300000
    s_loan.rate_of_interest = 12.0
    s_loan.repayment_method = "Repay Fixed Amount per Period"
    s_loan.repayment_periods = 12
    s_loan.monthly_repayment_amount = 26654
    s_loan.mode_of_payment = "Bank Transfer"
    s_loan.disbursement_account = disb_bank_acc
    s_loan.payment_account = disb_bank_acc
    s_loan.loan_account = loan_portfolio_acc
    s_loan.interest_income_account = interest_income_acc
    s_loan.penalty_income_account = penalty_income_acc
    s_loan.status = "Closed"
    s_loan.disbursed_amount = 300000
    s_loan.total_amount_paid = 319848
    s_loan.total_principal_outstanding = 0
    s_loan.insert(ignore_permissions=True)
    s_loan.docstatus = 1
    s_loan.save(ignore_permissions=True)
    sunita_loan_id = s_loan.name

    # Create Closure Request with NOC
    lcr = frappe.new_doc("Loan Closure Request")
    lcr.loan = sunita_loan_id
    lcr.borrower_profile = borrower_map["Sunita Devi Verma"]
    lcr.closure_type = "Regular Closure"
    lcr.closure_date = add_days(nowdate(), -10)
    lcr.closure_status = "Approved"
    lcr.total_loan_amount = 300000
    lcr.total_paid = 319848
    lcr.principal_outstanding = 0
    lcr.interest_outstanding = 0
    lcr.penal_charges = 0
    lcr.total_settlement_amount = 0
    lcr.insert(ignore_permissions=True)
    lcr.docstatus = 1
    lcr.generate_noc()
    lcr.save(ignore_permissions=True)
    print(f"Created Closed Loan & NOC for Sunita Devi Verma: {lcr.name}")

# Borrower 5: Vikram Malhotra - Overdue Loan with Collection Task
vikram_cust = customer_map["Vikram Malhotra"]
vikram_loan_id = frappe.db.get_value("Loan", {"applicant": vikram_cust})
if not vikram_loan_id:
    v_loan = frappe.new_doc("Loan")
    v_loan.applicant_type = "Customer"
    v_loan.applicant = vikram_cust
    v_loan.company = company_name
    v_loan.loan_product = "ZENVIQ-PL-01"
    v_loan.posting_date = add_months(nowdate(), -5)
    v_loan.loan_amount = 250000
    v_loan.rate_of_interest = 14.0
    v_loan.repayment_method = "Repay Fixed Amount per Period"
    v_loan.repayment_periods = 24
    v_loan.monthly_repayment_amount = 11995
    v_loan.mode_of_payment = "Bank Transfer"
    v_loan.disbursement_account = disb_bank_acc
    v_loan.payment_account = disb_bank_acc
    v_loan.loan_account = loan_portfolio_acc
    v_loan.interest_income_account = interest_income_acc
    v_loan.penalty_income_account = penalty_income_acc
    v_loan.status = "Disbursed"
    v_loan.disbursed_amount = 250000
    v_loan.total_amount_paid = 23990
    v_loan.total_principal_outstanding = 231500
    v_loan.insert(ignore_permissions=True)
    v_loan.docstatus = 1
    v_loan.save(ignore_permissions=True)
    vikram_loan_id = v_loan.name

    # Create Collection Task
    ct = frappe.new_doc("Collection Task")
    ct.loan = vikram_loan_id
    ct.borrower_profile = borrower_map["Vikram Malhotra"]
    ct.collection_status = "Promise to Pay"
    ct.priority = "High"
    ct.overdue_amount = 35985
    ct.overdue_emi_count = 3
    ct.dpd_days = 48
    ct.dpd_bucket = "31-60 DPD"
    ct.first_overdue_date = add_days(nowdate(), -48)
    ct.penal_interest = 1420
    ct.promise_to_pay_date = add_days(nowdate(), 5)
    ct.last_contact_date = add_days(nowdate(), -2)
    ct.contact_attempts = 4
    ct.append("action_log", {
        "action_date": add_days(nowdate(), -10),
        "action_type": "Phone Call",
        "action_detail": "Called borrower, phone unreachable.",
        "result": "Not Reachable"
    })
    ct.append("action_log", {
        "action_date": add_days(nowdate(), -2),
        "action_type": "Phone Call",
        "action_detail": "Borrower cited delayed payments from local retail clients. Promised to clear 2 EMIs by next Friday.",
        "result": "Promised Payment"
    })
    ct.insert(ignore_permissions=True)
    print(f"Created Collection Task for Vikram: {ct.name} (DPD: {ct.dpd_days})")

frappe.db.commit()
print("\n--- All Demo Data Successfully Created! ---")
frappe.destroy()
