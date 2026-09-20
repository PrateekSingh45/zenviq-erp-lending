import frappe
from frappe.model.document import Document


class KYCVerification(Document):
    def validate(self):
        self.update_overall_status()

    def on_submit(self):
        self.update_borrower_kyc_status()

    def update_overall_status(self):
        if self.aadhaar_status == "Verified" and self.pan_status == "Verified":
            self.verification_status = "Approved"
            self.verified_by = frappe.session.user
            self.verified_on = frappe.utils.now()
        elif self.aadhaar_status == "Failed" or self.pan_status == "Failed":
            self.verification_status = "Rejected"
        elif self.aadhaar_status != "Not Started" or self.pan_status != "Not Started":
            self.verification_status = "In Progress"

    def update_borrower_kyc_status(self):
        if self.borrower_profile and self.verification_status == "Approved":
            bp = frappe.get_doc("Borrower Profile", self.borrower_profile)
            bp.aadhaar_verified = 1 if self.aadhaar_status == "Verified" else 0
            bp.pan_verified = 1 if self.pan_status == "Verified" else 0
            bp.bank_verified = 1 if self.bank_analysis_status == "Completed" else 0
            bp.save(ignore_permissions=True)

    @frappe.whitelist()
    def run_aadhaar_ekyc(self):
        from zenviq_lending.sandbox.ekyc import verify_aadhaar
        result = verify_aadhaar(self.aadhaar_number, self.borrower_name)
        self.aadhaar_status = "Verified" if result.get("verified") else "Failed"
        self.aadhaar_response = frappe.as_json(result)
        self.save(ignore_permissions=True)
        return result

    @frappe.whitelist()
    def run_pan_verification(self):
        from zenviq_lending.sandbox.ekyc import verify_pan
        result = verify_pan(self.pan_number, self.borrower_name)
        self.pan_status = "Verified" if result.get("verified") else "Failed"
        self.pan_response = frappe.as_json(result)
        self.save(ignore_permissions=True)
        return result

    @frappe.whitelist()
    def analyze_bank_statement(self):
        from zenviq_lending.sandbox.bank_statement import analyze_statement
        result = analyze_statement(self.borrower_name)
        self.bank_analysis_status = "Completed"
        self.avg_monthly_balance = result.get("avg_monthly_balance", 0)
        self.avg_monthly_credits = result.get("avg_monthly_credits", 0)
        self.avg_monthly_debits = result.get("avg_monthly_debits", 0)
        self.bank_analysis_response = frappe.as_json(result)
        self.save(ignore_permissions=True)
        return result
