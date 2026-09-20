import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, date_diff


class CollectionTask(Document):
    def validate(self):
        self.update_dpd_bucket()
        self.update_priority()

    def update_dpd_bucket(self):
        if self.dpd_days is not None:
            if self.dpd_days <= 0:
                self.dpd_bucket = "0 DPD"
            elif self.dpd_days <= 30:
                self.dpd_bucket = "1-30 DPD"
            elif self.dpd_days <= 60:
                self.dpd_bucket = "31-60 DPD"
            elif self.dpd_days <= 90:
                self.dpd_bucket = "61-90 DPD"
            else:
                self.dpd_bucket = "90+ DPD (NPA)"

    def update_priority(self):
        if self.dpd_days and self.dpd_days > 90:
            self.priority = "Critical"
        elif self.dpd_days and self.dpd_days > 60:
            self.priority = "High"
        elif self.dpd_days and self.dpd_days > 30:
            self.priority = "Medium"
        else:
            self.priority = "Low"

    @frappe.whitelist()
    def log_action(self, action_type, action_detail, result=""):
        self.append("action_log", {
            "action_date": nowdate(),
            "action_type": action_type,
            "action_detail": action_detail,
            "action_by": frappe.session.user,
            "result": result,
        })
        self.contact_attempts = (self.contact_attempts or 0) + 1
        self.last_contact_date = nowdate()
        self.save(ignore_permissions=True)
