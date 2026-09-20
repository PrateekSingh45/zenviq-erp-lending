import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class BorrowerProfile(Document):
    def validate(self):
        self.validate_pan()
        self.update_kyc_status()

    def validate_pan(self):
        if self.pan_number:
            import re
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', self.pan_number.upper()):
                frappe.throw("PAN Number format is invalid. Expected: ABCDE1234F")
            self.pan_number = self.pan_number.upper()

    def update_kyc_status(self):
        if self.aadhaar_verified and self.pan_verified and self.bank_verified:
            self.kyc_status = "Verified"
            if not self.kyc_verified_on:
                self.kyc_verified_on = frappe.utils.now()
        elif self.aadhaar_verified or self.pan_verified or self.bank_verified:
            self.kyc_status = "In Progress"

    @frappe.whitelist()
    def fetch_credit_score(self):
        """Fetch credit score from sandbox CIBIL integration"""
        from zenviq_lending.sandbox.credit_bureau import fetch_credit_report
        result = fetch_credit_report(self.pan_number, self.full_name, self.date_of_birth)
        self.credit_score = result.get("score", 0)
        self.credit_score_date = nowdate()
        self.existing_loan_count = result.get("active_accounts", 0)
        self.existing_emi_total = result.get("total_emi", 0)
        self.credit_report_sandbox = frappe.as_json(result)

        # Set risk category based on credit score
        score = self.credit_score
        if score >= 750:
            self.risk_category = "A - Low Risk"
        elif score >= 700:
            self.risk_category = "B - Moderate Risk"
        elif score >= 650:
            self.risk_category = "C - Medium Risk"
        elif score >= 600:
            self.risk_category = "D - High Risk"
        else:
            self.risk_category = "E - Very High Risk"

        self.save(ignore_permissions=True)
        frappe.msgprint(f"Credit Score: {self.credit_score} | Risk: {self.risk_category}", alert=True)
        return result

    @frappe.whitelist()
    def run_ekyc_aadhaar(self):
        """Run Aadhaar eKYC via sandbox"""
        from zenviq_lending.sandbox.ekyc import verify_aadhaar
        result = verify_aadhaar(self.aadhaar_number, self.full_name)
        if result.get("verified"):
            self.aadhaar_verified = 1
            self.save(ignore_permissions=True)
            frappe.msgprint("Aadhaar Verified Successfully (Sandbox)", alert=True)
        return result

    @frappe.whitelist()
    def verify_pan(self):
        """Verify PAN via sandbox"""
        from zenviq_lending.sandbox.ekyc import verify_pan
        result = verify_pan(self.pan_number, self.full_name)
        if result.get("verified"):
            self.pan_verified = 1
            self.save(ignore_permissions=True)
            frappe.msgprint("PAN Verified Successfully (Sandbox)", alert=True)
        return result
