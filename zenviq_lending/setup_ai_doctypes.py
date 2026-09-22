import frappe

def run():
    frappe.conf.developer_mode = 1
    
    # Create Module Def
    if not frappe.db.exists('Module Def', 'ZENVIQ AI'):
        frappe.get_doc({
            'doctype': 'Module Def',
            'module_name': 'ZENVIQ AI',
            'app_name': 'zenviq_lending'
        }).insert(ignore_if_duplicate=True)
        print('Created Module Def: ZENVIQ AI')

    # Create AI Change Operation (Child Table)
    if not frappe.db.exists('DocType', 'AI Change Operation'):
        doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'AI Change Operation',
            'module': 'ZENVIQ AI',
            'istable': 1,
            'custom': 0,
            'fields': [
                {'fieldname': 'sequence', 'fieldtype': 'Int', 'label': 'Sequence'},
                {'fieldname': 'tool_name', 'fieldtype': 'Data', 'label': 'Tool Name'},
                {'fieldname': 'target', 'fieldtype': 'Data', 'label': 'Target Object'},
                {'fieldname': 'parameters', 'fieldtype': 'Code', 'label': 'Parameters', 'options': 'JSON'},
                {'fieldname': 'before_state', 'fieldtype': 'Code', 'label': 'Before State', 'options': 'JSON'},
                {'fieldname': 'after_state', 'fieldtype': 'Code', 'label': 'After State', 'options': 'JSON'},
                {'fieldname': 'execution_status', 'fieldtype': 'Select', 'label': 'Execution Status', 'options': 'Pending\nSuccess\nFailed\nRolled Back'},
                {'fieldname': 'error_message', 'fieldtype': 'Text', 'label': 'Error Message'},
                {'fieldname': 'rollback_status', 'fieldtype': 'Select', 'label': 'Rollback Status', 'options': 'Not Applicable\nPending\nSuccess\nFailed'}
            ]
        })
        doc.insert(ignore_permissions=True)
        print('Created DocType: AI Change Operation')

    # Create AI Change Request
    if not frappe.db.exists('DocType', 'AI Change Request'):
        doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'AI Change Request',
            'module': 'ZENVIQ AI',
            'custom': 0,
            'naming_rule': 'Expression',
            'autoname': 'AI-REQ-.YYYY.-.#####',
            'fields': [
                {'fieldname': 'request_id', 'fieldtype': 'Data', 'label': 'Request ID', 'unique': 1, 'hidden': 1},
                {'fieldname': 'requested_by', 'fieldtype': 'Link', 'label': 'Requested By', 'options': 'User'},
                {'fieldname': 'prompt', 'fieldtype': 'Text', 'label': 'Prompt'},
                {'fieldname': 'intent', 'fieldtype': 'Data', 'label': 'Detected Intent'},
                {'fieldname': 'risk_level', 'fieldtype': 'Select', 'label': 'Risk Level', 'options': 'GREEN\nYELLOW\nRED'},
                {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status', 'options': 'Draft\nPlanned\nAwaiting Approval\nApproved\nExecuting\nCompleted\nFailed\nRolled Back'},
                {'fieldname': 'requires_approval', 'fieldtype': 'Check', 'label': 'Requires Approval'},
                {'fieldname': 'approved_by', 'fieldtype': 'Link', 'label': 'Approved By', 'options': 'User'},
                {'fieldname': 'approved_at', 'fieldtype': 'Datetime', 'label': 'Approved At'},
                {'fieldname': 'affected_doctypes', 'fieldtype': 'Text', 'label': 'Affected DocTypes'},
                {'fieldname': 'change_plan_json', 'fieldtype': 'Code', 'label': 'Change Plan', 'options': 'JSON'},
                {'fieldname': 'verification_result_json', 'fieldtype': 'Code', 'label': 'Verification Result', 'options': 'JSON'},
                {'fieldname': 'rollback_payload_json', 'fieldtype': 'Code', 'label': 'Rollback Payload', 'options': 'JSON'},
                {'fieldname': 'error_log', 'fieldtype': 'Text', 'label': 'Error Log'},
                {'fieldname': 'model_provider', 'fieldtype': 'Data', 'label': 'Model Provider'},
                {'fieldname': 'model_name', 'fieldtype': 'Data', 'label': 'Model Name'},
                {'fieldname': 'model_response_id', 'fieldtype': 'Data', 'label': 'Model Response ID'},
                {'fieldname': 'operations', 'fieldtype': 'Table', 'label': 'Operations', 'options': 'AI Change Operation'}
            ]
        })
        doc.insert(ignore_permissions=True)
        print('Created DocType: AI Change Request')

    # Create AI Settings (Single)
    if not frappe.db.exists('DocType', 'AI Settings'):
        doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'AI Settings',
            'module': 'ZENVIQ AI',
            'custom': 0,
            'issingle': 1,
            'fields': [
                {'fieldname': 'enabled', 'fieldtype': 'Check', 'label': 'Enable ZENVIQ AI'},
                {'fieldname': 'provider', 'fieldtype': 'Select', 'label': 'AI Provider', 'options': 'Gemini\nOpenAI\nAnthropic', 'default': 'Gemini'},
                {'fieldname': 'model', 'fieldtype': 'Data', 'label': 'Model Name', 'default': 'gemini-1.5-pro'},
                {'fieldname': 'api_key', 'fieldtype': 'Password', 'label': 'API Key'},
                {'fieldname': 'max_tool_calls_per_request', 'fieldtype': 'Int', 'label': 'Max Tool Calls', 'default': 10},
                {'fieldname': 'max_affected_records', 'fieldtype': 'Int', 'label': 'Max Affected Records', 'default': 100},
                {'fieldname': 'allow_auto_execute_green', 'fieldtype': 'Check', 'label': 'Allow Auto-execute Green', 'default': 1},
                {'fieldname': 'require_approval_yellow', 'fieldtype': 'Check', 'label': 'Require Approval Yellow', 'default': 1},
                {'fieldname': 'developer_mode', 'fieldtype': 'Check', 'label': 'Developer Mode'},
                {'fieldname': 'audit_retention_days', 'fieldtype': 'Int', 'label': 'Audit Retention (Days)', 'default': 365}
            ]
        })
        doc.insert(ignore_permissions=True)
        print('Created DocType: AI Settings')

    frappe.db.commit()
    print('Finished setting up AI DocTypes.')

