import frappe
def run():
    frappe.conf.developer_mode = 1
    valid_query = 'SELECT branch, SUM(CASE WHEN days_past_due > 30 THEN (loan_amount - total_principal_paid) ELSE 0 END) / NULLIF(SUM(loan_amount - total_principal_paid), 0) * 100 AS par_30 FROM  WHERE status = \\'Disbursed\\' GROUP BY branch'
    frappe.db.set_value('Report', 'Branch-wise PAR 30', 'query', valid_query)
    frappe.db.commit()
