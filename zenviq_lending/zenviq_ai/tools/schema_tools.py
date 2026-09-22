import frappe
from typing import Dict, Any, Optional
from .base import Tool
from .registry import registry

class CreateCustomFieldTool(Tool):
    def __init__(self):
        super().__init__(
            name='create_custom_field',
            description='Creates a new custom field on a DocType.',
            schema={
                'type': 'object',
                'properties': {
                    'dt': {'type': 'string', 'description': 'The Target DocType'},
                    'fieldname': {'type': 'string', 'description': 'The database field name (snake_case)'},
                    'label': {'type': 'string', 'description': 'Human readable label'},
                    'fieldtype': {'type': 'string', 'description': 'Data type, e.g. Data, Int, Date, Select, Check'},
                    'reqd': {'type': 'integer', 'description': '1 if mandatory, 0 otherwise'},
                    'options': {'type': 'string', 'description': 'Options for Select or Link fields'}
                },
                'required': ['dt', 'fieldname', 'label', 'fieldtype']
            },
            required_permissions=['System Manager'],
            risk_classification='YELLOW'
        )

    def validate(self, params: Dict[str, Any], user: str) -> bool:
        if not frappe.db.exists('DocType', params.get('dt')):
            frappe.throw(f'DocType {params.get("dt")} does not exist.')
        
        existing = frappe.db.exists('Custom Field', {'dt': params.get('dt'), 'fieldname': params.get('fieldname')})
        if existing:
            frappe.throw(f'Custom Field {params.get("fieldname")} already exists on {params.get("dt")}.')
        return True

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        from frappe.custom.doctype.custom_field.custom_field import create_custom_field
        
        field_args = {k: v for k, v in params.items() if k != 'dt'}
        if 'insert_after' in field_args and field_args['insert_after'] == 'last_field':
            del field_args['insert_after'] # Fix AI hallucination issue
            
        create_custom_field(params.get('dt'), field_args)
        return {'status': 'success'}

    def verify(self, params: Dict[str, Any]) -> bool:
        return bool(frappe.db.exists('Custom Field', {'dt': params.get('dt'), 'fieldname': params.get('fieldname')}))

    def get_rollback_payload(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {'dt': params.get('dt'), 'fieldname': params.get('fieldname')}


class ModifyFieldPropertyTool(Tool):
    def __init__(self):
        super().__init__(
            name='modify_field_property',
            description='Modifies a property (like mandatory/reqd, hidden, read_only, etc) of an existing field in a DocType safely using Property Setter.',
            schema={
                'type': 'object',
                'properties': {
                    'doctype_name': {'type': 'string', 'description': 'The Target DocType'},
                    'fieldname': {'type': 'string', 'description': 'The field name to modify'},
                    'property': {'type': 'string', 'description': 'The property to change (e.g. reqd, hidden, options, label)'},
                    'value': {'type': 'string', 'description': 'The new value for the property (e.g. \"1\" for true, \"0\" for false)'}
                },
                'required': ['doctype_name', 'fieldname', 'property', 'value']
            },
            required_permissions=['System Manager'],
            risk_classification='YELLOW'
        )

    def validate(self, params: Dict[str, Any], user: str) -> bool:
        if not frappe.db.exists('DocType', params.get('doctype_name')):
            frappe.throw(f'DocType {params.get("doctype_name")} does not exist.')
        return True

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        from frappe.custom.doctype.property_setter.property_setter import make_property_setter
        make_property_setter(
            params.get('doctype_name'),
            params.get('fieldname'),
            params.get('property'),
            params.get('value'),
            'Check' if params.get('value') in ['0', '1'] else 'Data'
        )
        return {'status': 'success'}

    def verify(self, params: Dict[str, Any]) -> bool:
        return True

    def get_rollback_payload(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {
            'doctype_name': params.get('doctype_name'),
            'fieldname': params.get('fieldname'),
            'property': params.get('property')
        }

registry.register(CreateCustomFieldTool())
registry.register(ModifyFieldPropertyTool())
