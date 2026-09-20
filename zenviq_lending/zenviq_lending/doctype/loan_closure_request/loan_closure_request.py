import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
import hashlib
import time


class LoanClosureRequest(Document):
    def validate(self):
        self.calculate_settlement()

    def on_submit(self):
        if self.closure_status not in ["Approved", "Completed"]:
            frappe.throw("Closure must be Approved before submission")

    def calculate_settlement(self):
        self.total_settlement_amount = (
            (self.principal_outstanding or 0) +
            (self.interest_outstanding or 0) +
            (self.penal_charges or 0) +
            (self.foreclosure_charges or 0)
        )

    @frappe.whitelist()
    def generate_noc(self):
        """Generate NOC for closed loan"""
        if self.closure_status not in ["Approved", "Completed"]:
            frappe.throw("Closure must be approved first")

        self.noc_generated = 1
        self.noc_date = nowdate()
        self.noc_number = f"NOC-{self.name}-{int(time.time())}"
        self.cibil_updated = 1
        self.closure_status = "Completed"
        self.save(ignore_permissions=True)

        frappe.msgprint(f"NOC Generated: {self.noc_number} (Sandbox)", alert=True)
        return self.noc_number
