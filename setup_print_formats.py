import os, frappe

os.chdir("sites")
frappe.init(site="zenviq.localhost", sites_path=".")
frappe.connect()

print("--- Creating ZENVIQ Print Formats ---")

# 1. Sanction Letter
sanction_letter_html = """
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #263238; padding: 25px; line-height: 1.6;">
    <div style="border-bottom: 3px solid #1A237E; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #1A237E; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 1px;">ZENVIQ FINANCE</h1>
            <p style="margin: 2px 0; font-size: 11px; color: #546E7A; font-weight: 600;">ZENVIQ FINANCE DEMO PRIVATE LIMITED | CIN: U65929UP2026PTC198421</p>
            <p style="margin: 0; font-size: 11px; color: #78909C;">Aligarh Main Branch, Civil Lines, Aligarh, Uttar Pradesh - 202001</p>
        </div>
        <div style="text-align: right;">
            <span style="background: #E8EAF6; color: #1A237E; padding: 6px 14px; border-radius: 4px; font-weight: 700; font-size: 12px; border: 1px solid #C5CAE9;">
                SANCTION LETTER
            </span>
            <p style="font-size: 11px; color: #78909C; margin-top: 5px;">Date: {{ frappe.utils.formatdate(doc.posting_date) }}</p>
        </div>
    </div>

    <p style="font-size: 13px; margin-bottom: 20px;">
        <strong>Ref No:</strong> ZENVIQ/SANCT/{{ doc.name }}<br>
        <strong>To:</strong><br>
        <strong>{{ doc.applicant_name or doc.applicant }}</strong><br>
        Customer ID: {{ doc.applicant }}
    </p>

    <div style="background: #E8F5E9; border-left: 4px solid #2E7D32; padding: 12px 15px; margin-bottom: 20px; font-size: 13px; color: #1B5E20;">
        <strong>Sub: In-Principle Sanction of Individual Loan Facility</strong><br>
        Dear Sir/Madam, With reference to your loan application, we are pleased to inform you that ZENVIQ Finance has sanctioned the credit facility on the terms outlined below:
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 13px;">
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; width: 40%; color: #37474F;">Sanctioned Loan Amount</td>
            <td style="padding: 10px; font-weight: 700; color: #1A237E; font-size: 15px;">₹ {{ frappe.utils.fmt_money(doc.loan_amount, currency="INR") }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Loan Product / Type</td>
            <td style="padding: 10px;">{{ doc.loan_product }}</td>
        </tr>
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Rate of Interest</td>
            <td style="padding: 10px; font-weight: 700;">{{ doc.rate_of_interest }}% p.a. (Reducing Balance)</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Repayment Method</td>
            <td style="padding: 10px;">{{ doc.repayment_method or "Repay Fixed Amount per Period (Equated Monthly Installment)" }}</td>
        </tr>
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Monthly EMI Amount</td>
            <td style="padding: 10px; font-weight: 700; color: #2E7D32;">₹ {{ frappe.utils.fmt_money(doc.monthly_repayment_amount, currency="INR") }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Penal Interest / Overdue Rate</td>
            <td style="padding: 10px; color: #C62828;">24.0% p.a. on overdue installments</td>
        </tr>
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; color: #37474F;">Disbursement Mode</td>
            <td style="padding: 10px;">Direct NEFT/RTGS to Borrower Verified Bank Account</td>
        </tr>
    </table>

    <div style="font-size: 11px; color: #546E7A; margin-bottom: 30px; border: 1px solid #ECEFF1; padding: 12px; background: #FAFAFA;">
        <strong>Important Terms & Conditions:</strong><br>
        1. This sanction is valid for 30 days from the date of issue.<br>
        2. Disbursement is subject to execution of Loan Agreement, eSign, and submission of verified eNACH mandate.<br>
        3. All repayments will be auto-debited via NACH/eMandate on the designated EMI due date.
    </div>

    <table style="width: 100%; margin-top: 40px; font-size: 12px;">
        <tr>
            <td style="width: 50%; vertical-align: bottom;">
                <p style="margin: 0; font-weight: 700; color: #1A237E;">For ZENVIQ Finance Demo Pvt Ltd</p>
                <div style="height: 45px;"></div>
                <p style="margin: 0; border-top: 1px solid #90A4AE; width: 80%; padding-top: 5px;">Authorized Credit Signatory</p>
            </td>
            <td style="width: 50%; text-align: right; vertical-align: bottom;">
                <p style="margin: 0; font-weight: 700; color: #37474F;">Borrower Acceptance</p>
                <div style="height: 45px;"></div>
                <p style="margin: 0; border-top: 1px solid #90A4AE; width: 80%; margin-left: 20%; padding-top: 5px;">Signature of {{ doc.applicant_name or doc.applicant }}</p>
            </td>
        </tr>
    </table>
</div>
"""

# 2. Loan Agreement
loan_agreement_html = """
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #263238; padding: 25px; line-height: 1.5; font-size: 12px;">
    <div style="text-align: center; border-bottom: 2px solid #1A237E; padding-bottom: 10px; margin-bottom: 20px;">
        <h2 style="color: #1A237E; margin: 0; font-size: 20px;">ZENVIQ FINANCE DEMO PRIVATE LIMITED</h2>
        <h3 style="margin: 5px 0 0 0; font-size: 14px; color: #37474F; font-weight: 600;">INDIVIDUAL LOAN FACILITY AGREEMENT</h3>
        <p style="margin: 2px 0 0 0; font-size: 10px; color: #78909C;">Agreement Reference: ZENVIQ-AGR-{{ doc.name }} | Date: {{ frappe.utils.formatdate(doc.posting_date) }}</p>
    </div>

    <p>This Loan Agreement ("Agreement") is executed on this <strong>{{ frappe.utils.formatdate(doc.posting_date) }}</strong> by and between:</p>
    
    <p><strong>1. ZENVIQ FINANCE DEMO PRIVATE LIMITED</strong>, an NBFC company having its registered office at Civil Lines, Aligarh, Uttar Pradesh (hereinafter referred to as the <strong>"Lender"</strong>).</p>
    <p>AND</p>
    <p><strong>2. {{ doc.applicant_name or doc.applicant }}</strong>, an individual residing in India, having PAN registered in records (hereinafter referred to as the <strong>"Borrower"</strong>).</p>

    <h4 style="color: #1A237E; border-bottom: 1px solid #C5CAE9; padding-bottom: 4px; margin-top: 15px;">1. PRINCIPAL LOAN TERMS</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
        <tr style="border-bottom: 1px solid #ECEFF1;"><td style="padding: 6px; font-weight: 600; width: 45%;">Sanctioned Loan Amount</td><td style="padding: 6px;">₹ {{ frappe.utils.fmt_money(doc.loan_amount, currency="INR") }}</td></tr>
        <tr style="border-bottom: 1px solid #ECEFF1;"><td style="padding: 6px; font-weight: 600;">Loan Facility Type</td><td style="padding: 6px;">{{ doc.loan_product }}</td></tr>
        <tr style="border-bottom: 1px solid #ECEFF1;"><td style="padding: 6px; font-weight: 600;">Rate of Interest</td><td style="padding: 6px;">{{ doc.rate_of_interest }}% p.a. (Reducing Balance)</td></tr>
        <tr style="border-bottom: 1px solid #ECEFF1;"><td style="padding: 6px; font-weight: 600;">Monthly Equated Installment (EMI)</td><td style="padding: 6px; font-weight: 700;">₹ {{ frappe.utils.fmt_money(doc.monthly_repayment_amount, currency="INR") }}</td></tr>
        <tr style="border-bottom: 1px solid #ECEFF1;"><td style="padding: 6px; font-weight: 600;">Disbursed Amount</td><td style="padding: 6px;">₹ {{ frappe.utils.fmt_money(doc.disbursed_amount, currency="INR") }}</td></tr>
    </table>

    <h4 style="color: #1A237E; border-bottom: 1px solid #C5CAE9; padding-bottom: 4px; margin-top: 15px;">2. REPAYMENT & DEFAULT</h4>
    <p>The Borrower promises to repay the Loan together with applicable interest strictly as per the Amortization Schedule via automated NACH / eMandate debit.</p>
    <p>In case of delayed repayment, penal interest at 24% per annum shall be charged on the overdue sum from due date until actual settlement.</p>

    <h4 style="color: #1A237E; border-bottom: 1px solid #C5CAE9; padding-bottom: 4px; margin-top: 15px;">3. GOVERNING LAW & JURISDICTION</h4>
    <p>This Agreement shall be governed by the laws of India. Courts at Aligarh, Uttar Pradesh shall have exclusive jurisdiction.</p>

    <div style="margin-top: 40px; display: flex; justify-content: space-between;">
        <div style="width: 45%;">
            <p style="margin: 0; font-weight: 700;">Signed for and on behalf of Lender:</p>
            <div style="height: 50px;"></div>
            <p style="margin: 0; border-top: 1px solid #37474F; padding-top: 4px;">Authorized Officer | ZENVIQ Finance</p>
        </div>
        <div style="width: 45%; text-align: right;">
            <p style="margin: 0; font-weight: 700;">Signed by Borrower:</p>
            <div style="height: 50px;"></div>
            <p style="margin: 0; border-top: 1px solid #37474F; padding-top: 4px;">{{ doc.applicant_name or doc.applicant }} [eSigned]</p>
        </div>
    </div>
</div>
"""

# 3. NOC Certificate
noc_html = """
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #263238; padding: 30px; line-height: 1.6;">
    <div style="border-bottom: 3px solid #2E7D32; padding-bottom: 15px; margin-bottom: 25px; text-align: center;">
        <h1 style="color: #1A237E; margin: 0; font-size: 24px; font-weight: 800;">ZENVIQ FINANCE DEMO PRIVATE LIMITED</h1>
        <p style="margin: 3px 0; font-size: 11px; color: #546E7A;">Registered NBFC Entity | CIN: U65929UP2026PTC198421</p>
        <p style="margin: 0; font-size: 11px; color: #78909C;">Aligarh Main Branch, Civil Lines, Aligarh (U.P.)</p>
        <div style="margin-top: 15px;">
            <span style="background: #E8F5E9; color: #2E7D32; padding: 6px 18px; border-radius: 20px; font-weight: 800; font-size: 14px; border: 1px solid #A5D6A7; letter-spacing: 1px;">
                NO OBJECTION & LOAN CLOSURE CERTIFICATE (NOC)
            </span>
        </div>
    </div>

    <p style="font-size: 13px;">
        <strong>Certificate No:</strong> {{ doc.noc_number or doc.name }}<br>
        <strong>Date of Issue:</strong> {{ frappe.utils.formatdate(doc.noc_date or doc.closure_date) }}<br>
        <strong>To Whomsoever It May Concern</strong>
    </p>

    <div style="font-size: 14px; margin: 25px 0; background: #FAFAFA; border: 1px solid #CFD8DC; padding: 18px; border-radius: 4px;">
        This is to certify that <strong>{{ doc.borrower_name }}</strong>, holding Loan Account <strong>{{ doc.loan }}</strong>, has fully settled and cleared all dues towards the credit facility sanctioned by ZENVIQ Finance Demo Private Limited.
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 13px;">
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600; width: 50%;">Loan Reference</td>
            <td style="padding: 10px; font-weight: 700;">{{ doc.loan }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600;">Borrower Name</td>
            <td style="padding: 10px;">{{ doc.borrower_name }}</td>
        </tr>
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600;">Closure Type</td>
            <td style="padding: 10px;">{{ doc.closure_type }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600;">Total Settlement Paid</td>
            <td style="padding: 10px; font-weight: 700; color: #2E7D32;">₹ {{ frappe.utils.fmt_money(doc.total_settlement_amount or doc.total_paid, currency="INR") }}</td>
        </tr>
        <tr style="background: #F5F7FA; border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600;">Outstanding Balance</td>
            <td style="padding: 10px; font-weight: 700; color: #2E7D32;">₹ 0.00 (NIL Dues)</td>
        </tr>
        <tr style="border-bottom: 1px solid #CFD8DC;">
            <td style="padding: 10px; font-weight: 600;">Credit Bureau Update</td>
            <td style="padding: 10px; color: #1565C0;">Updated to CIBIL / Experian as "CLOSED - FULLY SATISFIED"</td>
        </tr>
    </table>

    <p style="font-size: 13px; color: #37474F;">
        ZENVIQ Finance has <strong>NO OBJECTION</strong> to this loan account closure and confirms that no further liabilities, security charges, or obligations remain outstanding against the borrower under this account.
    </p>

    <div style="margin-top: 50px; text-align: right;">
        <p style="margin: 0; font-weight: 700; color: #1A237E;">For ZENVIQ Finance Demo Private Limited</p>
        <div style="height: 50px;"></div>
        <p style="margin: 0; font-weight: 600; color: #37474F;">Authorized Compliance Signatory</p>
        <p style="margin: 0; font-size: 11px; color: #78909C;">Aligarh Main Branch</p>
    </div>
</div>
"""

# 4. EMI Repayment Receipt
receipt_html = """
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #263238; padding: 25px; line-height: 1.6; font-size: 13px;">
    <div style="border-bottom: 2px solid #1A237E; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between;">
        <div>
            <h2 style="color: #1A237E; margin: 0; font-size: 22px;">ZENVIQ FINANCE</h2>
            <p style="margin: 0; font-size: 11px; color: #546E7A;">ZENVIQ Finance Demo Private Limited | Aligarh Branch</p>
        </div>
        <div style="text-align: right;">
            <span style="background: #E8F5E9; color: #2E7D32; padding: 5px 12px; border-radius: 3px; font-weight: 700; font-size: 12px;">
                REPAYMENT RECEIPT
            </span>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: #78909C;">Receipt: {{ doc.name }}</p>
        </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
        <tr>
            <td style="padding: 6px; width: 50%;"><strong>Borrower:</strong> {{ doc.applicant }}</td>
            <td style="padding: 6px; width: 50%; text-align: right;"><strong>Date:</strong> {{ frappe.utils.formatdate(doc.posting_date) }}</td>
        </tr>
        <tr>
            <td style="padding: 6px;"><strong>Against Loan:</strong> {{ doc.against_loan }}</td>
            <td style="padding: 6px; text-align: right;"><strong>Status:</strong> Successful / Received</td>
        </tr>
    </table>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; border: 1px solid #CFD8DC;">
        <tr style="background: #1A237E; color: white;">
            <th style="padding: 8px; text-align: left;">Component</th>
            <th style="padding: 8px; text-align: right;">Amount (INR)</th>
        </tr>
        <tr style="border-bottom: 1px solid #ECEFF1;">
            <td style="padding: 8px;">Principal Amount</td>
            <td style="padding: 8px; text-align: right; font-weight: 600;">₹ {{ frappe.utils.fmt_money(doc.principal_paid, currency="INR") }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #ECEFF1;">
            <td style="padding: 8px;">Interest Amount</td>
            <td style="padding: 8px; text-align: right;">₹ {{ frappe.utils.fmt_money(doc.interest_paid, currency="INR") }}</td>
        </tr>
        {% if doc.penalty_amount %}
        <tr style="border-bottom: 1px solid #ECEFF1;">
            <td style="padding: 8px; color: #C62828;">Penal Charges</td>
            <td style="padding: 8px; text-align: right; color: #C62828;">₹ {{ frappe.utils.fmt_money(doc.penalty_amount, currency="INR") }}</td>
        </tr>
        {% endif %}
        <tr style="background: #F5F7FA; font-weight: 700; font-size: 14px;">
            <td style="padding: 10px; color: #1A237E;">TOTAL REPAID</td>
            <td style="padding: 10px; text-align: right; color: #2E7D32;">₹ {{ frappe.utils.fmt_money(doc.amount_paid, currency="INR") }}</td>
        </tr>
    </table>

    <div style="font-size: 11px; color: #78909C; text-align: center; margin-top: 30px; border-top: 1px solid #ECEFF1; padding-top: 10px;">
        This is a computer generated receipt. Thank you for banking with ZENVIQ Finance.
    </div>
</div>
"""

formats = [
    {"name": "ZENVIQ Loan Sanction Letter", "doctype": "Loan", "html": sanction_letter_html},
    {"name": "ZENVIQ Individual Loan Agreement", "doctype": "Loan", "html": loan_agreement_html},
    {"name": "ZENVIQ No Objection Certificate", "doctype": "Loan Closure Request", "html": noc_html},
    {"name": "ZENVIQ EMI Repayment Receipt", "doctype": "Loan Repayment", "html": receipt_html},
]

for pf in formats:
    if not frappe.db.exists("Print Format", pf["name"]):
        doc = frappe.new_doc("Print Format")
        doc.name = pf["name"]
        doc.doc_type = pf["doctype"]
        doc.module = "ZENVIQ Lending"
        doc.standard = "No"
        doc.custom_format = 1
        doc.html = pf["html"]
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Created Print Format: {pf['name']}")
    else:
        doc = frappe.get_doc("Print Format", pf["name"])
        doc.html = pf["html"]
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"Updated Print Format: {pf['name']}")

print("Print Formats setup completed successfully!")
frappe.destroy()
