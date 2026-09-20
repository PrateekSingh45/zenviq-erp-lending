import frappe
from frappe.model.document import Document


class CreditAssessment(Document):
    def validate(self):
        self.calculate_ratios()
        self.calculate_overall_score()

    def calculate_ratios(self):
        self.total_monthly_income = (self.verified_monthly_income or 0) + (self.other_income or 0)
        if self.total_monthly_income:
            total_obligations = (self.existing_emi or 0) + (self.proposed_emi or 0)
            self.foir = (total_obligations / self.total_monthly_income) * 100
            self.dti_ratio = ((self.existing_emi or 0) / self.total_monthly_income) * 100
            self.net_monthly_surplus = self.total_monthly_income - total_obligations

            # Recommend loan amount based on surplus (max 60 EMIs)
            if self.net_monthly_surplus > 0:
                max_emi = self.total_monthly_income * 0.5 - (self.existing_emi or 0)
                if max_emi > 0:
                    self.loan_amount_recommended = max_emi * 48  # ~4 year tenure

    def calculate_overall_score(self):
        score = 0
        # Credit score component (max 40 points)
        if self.credit_score:
            if self.credit_score >= 750:
                score += 40
            elif self.credit_score >= 700:
                score += 30
            elif self.credit_score >= 650:
                score += 20
            elif self.credit_score >= 600:
                score += 10

        # FOIR component (max 30 points)
        if self.foir:
            if self.foir <= 40:
                score += 30
            elif self.foir <= 50:
                score += 20
            elif self.foir <= 60:
                score += 10

        # Income stability (max 15 points)
        if self.verified_monthly_income and self.declared_monthly_income:
            ratio = self.verified_monthly_income / self.declared_monthly_income
            if ratio >= 0.9:
                score += 15
            elif ratio >= 0.75:
                score += 10
            elif ratio >= 0.5:
                score += 5

        # Parameters (max 15 points from child table)
        if self.assessment_parameters:
            param_score = sum(p.score or 0 for p in self.assessment_parameters)
            param_max = sum(p.max_score or 10 for p in self.assessment_parameters)
            if param_max:
                score += int((param_score / param_max) * 15)

        self.overall_score = min(score, 100)

        # Auto-set recommendation
        if self.overall_score >= 75:
            self.recommendation = "Approve"
        elif self.overall_score >= 60:
            self.recommendation = "Approve with Conditions"
        elif self.overall_score >= 45:
            self.recommendation = "Refer to Committee"
        else:
            self.recommendation = "Reject"
