import frappe
from ..orchestrator.planner import Planner
import traceback

@frappe.whitelist()
def generate_change_plan(prompt: str):
    frappe.only_for('System Manager')
    try:
        user = frappe.session.user
        planner = Planner(user)
        plan = planner.create_plan(prompt)
        
        request_doc = frappe.get_doc({
            'doctype': 'AI Change Request',
            'user': user,
            'prompt': prompt,
            'intent': plan.intent,
            'risk_level': plan.risk_level,
            'status': 'Awaiting Approval' if plan.requires_approval else 'Completed',
            'operations': [
                {
                    'tool_name': op.tool,
                    'reason': op.reason,
                    'parameters': frappe.as_json(op.parameters)
                } for op in plan.operations
            ]
        })
        request_doc.insert(ignore_permissions=True)
        
        return {
            'status': 'success',
            'request_id': request_doc.name,
            'plan': plan.dict()
        }
    except Exception as e:
        frappe.log_error(title='AI Orchestrator Error', message=traceback.format_exc())
        return {'status': 'error', 'message': str(e)}

@frappe.whitelist()
def apply_change_plan(request_id: str):
    frappe.only_for('System Manager')
    request_doc = frappe.get_doc('AI Change Request', request_id)
    
    if request_doc.status not in ['Awaiting Approval', 'Failed']:
        return {'status': 'error', 'message': f'Cannot apply plan in status: {request_doc.status}'}
        
    from ..tools.registry import registry
    
    for op in request_doc.operations:
        tool = registry.get_tool(op.tool_name)
        params = frappe.parse_json(op.parameters)
        
        try:
            result = tool.execute(params)
            op.execution_status = 'Success'
            op.execution_log = frappe.as_json(result)
        except Exception as e:
            op.execution_status = 'Failed'
            op.execution_log = str(e)
            request_doc.status = 'Failed'
            request_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {'status': 'error', 'message': f'Operation {op.tool_name} failed: {str(e)}'}
            
    request_doc.status = 'Completed'
    request_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {'status': 'success'}
