import frappe
import json
from ..tools import registry

@frappe.whitelist()
def approve_change_plan(request_id: str):
    request_doc = frappe.get_doc('AI Change Request', request_id)
    if request_doc.risk_level == 'RED':
        frappe.only_for('Administrator')
    else:
        frappe.only_for('System Manager')
        
    request_doc.status = 'Approved'
    request_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {'status': 'success'}

@frappe.whitelist()
def apply_change_plan(request_id: str):
    frappe.only_for('System Manager')
    request_doc = frappe.get_doc('AI Change Request', request_id)
    
    if request_doc.status not in ['Approved', 'Planned']:
        return {'status': 'error', 'message': f'Cannot apply plan in state {request_doc.status}'}
        
    for op in request_doc.operations:
        tool = registry.get_tool(op.tool_name)
        params = json.loads(op.parameters)
        
        try:
            tool.validate(params, frappe.session.user)
            tool.execute(params)
            op.execution_status = 'Success'
            if tool.get_rollback_payload:
                op.rollback_payload_json = json.dumps(tool.get_rollback_payload(params))
        except Exception as e:
            op.execution_status = 'Failed'
            op.error_log = str(e)
            request_doc.status = 'Failed'
            request_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {'status': 'error', 'message': f'Operation {op.tool_name} failed: {e}'}
            
    request_doc.status = 'Completed'
    request_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {'status': 'success'}
