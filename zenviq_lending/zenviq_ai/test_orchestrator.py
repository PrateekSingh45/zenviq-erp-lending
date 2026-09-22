import frappe
from zenviq_lending.zenviq_ai.api.chat import generate_change_plan
import json

def run():
    frappe.conf.developer_mode = 1
    frappe.set_user('Administrator')

    try:
        result = generate_change_plan('Show branch-wise PAR 30 for the last six months.')
        print(json.dumps(result, indent=2))
    except Exception as e:
        print('Error:', e)
        
