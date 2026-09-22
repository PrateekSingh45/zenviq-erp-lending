import frappe
import json
from ..tools.registry import registry

@frappe.whitelist()
def rollback_change_plan(request_id: str):
    request_doc = frappe.get_doc('AI Change Request', request_id)
    
    if request_doc.status != 'Completed':
        return {'status': 'error', 'message': 'Only Completed requests can be rolled back.'}
        
    ops_to_rollback = reversed(request_doc.operations)
    
    for op in ops_to_rollback:
        if op.execution_status != 'Success':
            continue
            
        try:
            params = json.loads(op.parameters)
        except:
            params = {}
            
        if op.tool_name == 'create_custom_field':
            dt = params.get('dt')
            fieldname = params.get('fieldname')
            cf_name = frappe.db.get_value('Custom Field', {'dt': dt, 'fieldname': fieldname})
            if cf_name:
                frappe.delete_doc('Custom Field', cf_name, ignore_permissions=True)
                frappe.clear_cache(doctype=dt)
                op.rollback_status = 'Success'
                
        elif op.tool_name == 'create_server_script':
            name = params.get('name')
            if frappe.db.exists('Server Script', name):
                frappe.delete_doc('Server Script', name, ignore_permissions=True)
                frappe.clear_cache()
                op.rollback_status = 'Success'
                
        elif op.tool_name == 'modify_field_property':
            doctype_name = params.get('doctype_name')
            fieldname = params.get('fieldname')
            property = params.get('property')
            ps_name = frappe.db.get_value('Property Setter', {'doc_type': doctype_name, 'field_name': fieldname, 'property': property})
            if ps_name:
                frappe.delete_doc('Property Setter', ps_name, ignore_permissions=True)
                frappe.clear_cache(doctype=doctype_name)
                op.rollback_status = 'Success'
                
        elif op.tool_name == 'create_document':
            try:
                doc_dict = json.loads(params.get('doc_json'))
                doctype_name = params.get('doctype_name')
                doc_name = doc_dict.get('name') or doc_dict.get('report_name') or doc_dict.get('workflow_name')
                if not doc_name:
                    # Try to find by filtering
                    docs = frappe.get_all(doctype_name, filters=doc_dict, limit=1)
                    if docs:
                        doc_name = docs[0].name
                if doc_name and frappe.db.exists(doctype_name, doc_name):
                    frappe.delete_doc(doctype_name, doc_name, ignore_permissions=True)
                    op.rollback_status = 'Success'
                else:
                    op.rollback_status = 'Failed'
            except Exception as e:
                op.rollback_status = f'Failed: {str(e)}'
                
    request_doc.status = 'Rolled Back'
    request_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {'status': 'success'}
