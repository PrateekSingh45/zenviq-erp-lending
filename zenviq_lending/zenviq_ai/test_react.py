import frappe
from zenviq_lending.zenviq_ai.api.chat import generate_change_plan
import json

def run():
    frappe.conf.developer_mode = 1
    frappe.set_user('Administrator')

    try:
        print('Starting ReAct prompt...')
        result = generate_change_plan('Create a Query Report showing exactly the Disbursed Amount for each Loan Product for Loans created this month. Inspect the Loan schema to get the exact database fieldnames before writing the SQL!')
        print(json.dumps(result, indent=2))
    except Exception as e:
        print('Error:', e)
        
