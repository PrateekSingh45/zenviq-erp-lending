import frappe
import json
from typing import Dict, Any, Optional
from .base import Tool
from .registry import registry

class CreateDocumentTool(Tool):
    def __init__(self):
        super().__init__(
            name='create_document',
            description='Creates any Frappe Document (e.g. Workflow, Report, Notification). You must provide the full JSON payload for the document including child tables.',
            schema={
                'type': 'object',
                'properties': {
                    'doctype_name': {'type': 'string', 'description': 'The DocType of the document to create'},
                    'doc_json': {'type': 'string', 'description': 'JSON encoded string of the document properties and child tables'}
                },
                'required': ['doctype_name', 'doc_json']
            },
            required_permissions=['System Manager'],
            risk_classification='YELLOW'
        )

    def validate(self, params: Dict[str, Any], user: str) -> bool:
        if not frappe.db.exists('DocType', params.get('doctype_name')):
            frappe.throw(f"DocType {params.get('doctype_name')} does not exist.")
        return True

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        doc_dict = json.loads(params.get('doc_json'))
        doc_dict['doctype'] = params.get('doctype_name')
        doc = frappe.get_doc(doc_dict)
        doc.insert(ignore_permissions=True)
        return {'status': 'success', 'name': doc.name}

    def verify(self, params: Dict[str, Any]) -> bool:
        return True

    def get_rollback_payload(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # In order to rollback, we need to know the document name that was created.
        # Since we don't have the return value here, we can extract it from the doc_json if it was provided,
        # otherwise rollback.py will handle it by searching for the document.
        doc_dict = json.loads(params.get('doc_json'))
        return {
            'doctype_name': params.get('doctype_name'),
            'doc_name': doc_dict.get('name') or doc_dict.get('report_name') or doc_dict.get('workflow_name') or doc_dict.get('subject')
        }

registry.register(CreateDocumentTool())
