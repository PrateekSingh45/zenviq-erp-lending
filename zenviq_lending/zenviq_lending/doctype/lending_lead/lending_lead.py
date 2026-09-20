import frappe
from frappe.model.document import Document


class LendingLead(Document):
    def validate(self):
        if self.mobile_number and len(self.mobile_number.replace('+', '').replace(' ', '').replace('-', '')) < 10:
            frappe.throw("Mobile number must be at least 10 digits")

    @frappe.whitelist()
    def convert_to_borrower(self):
        """Convert this lead to a Borrower Profile and optionally a Loan Application"""
        if self.lead_status == "Converted":
            frappe.throw("This lead is already converted")

        # Create Borrower Profile
        borrower = frappe.new_doc("Borrower Profile")
        borrower.full_name = self.applicant_name
        borrower.mobile_number = self.mobile_number
        borrower.email = self.email
        borrower.employment_type = self.employment_type
        borrower.monthly_income = self.monthly_income
        borrower.city = self.city
        borrower.state = self.state
        borrower.pincode = self.pincode
        borrower.address = self.full_address
        borrower.lending_lead = self.name
        borrower.insert(ignore_permissions=True)

        self.lead_status = "Converted"
        self.borrower_profile = borrower.name
        self.save(ignore_permissions=True)

        frappe.msgprint(f"Borrower Profile {borrower.name} created successfully", alert=True)
        return borrower.name
