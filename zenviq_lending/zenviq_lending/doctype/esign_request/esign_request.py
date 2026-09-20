import frappe
from frappe.model.document import Document


class ESignRequest(Document):
    @frappe.whitelist()
    def send_otp(self):
        """Simulate sending OTP for Aadhaar eSign"""
        from zenviq_lending.sandbox.esign import send_esign_otp
        result = send_esign_otp(self.borrower_name, self.document_type)
        self.esign_status = "OTP Sent"
        self.otp_sent_at = frappe.utils.now()
        self.esign_transaction_id = result.get("transaction_id")
        self.sandbox_response = frappe.as_json(result)
        self.save(ignore_permissions=True)
        frappe.msgprint("OTP sent to registered Aadhaar mobile (Sandbox)", alert=True)
        return result

    @frappe.whitelist()
    def complete_esign(self):
        """Simulate completing eSign after OTP verification"""
        from zenviq_lending.sandbox.esign import complete_esign
        result = complete_esign(self.esign_transaction_id, self.document_type)
        self.esign_status = "Signed"
        self.signed_at = frappe.utils.now()
        self.digital_signature_hash = result.get("signature_hash")
        self.sandbox_response = frappe.as_json(result)
        self.save(ignore_permissions=True)
        frappe.msgprint("Document signed successfully (Sandbox)", alert=True)
        return result
eSignRequest = ESignRequest
