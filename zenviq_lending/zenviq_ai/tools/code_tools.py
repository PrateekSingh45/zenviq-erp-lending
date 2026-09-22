import frappe
from typing import Dict, Any, Optional
from .base import Tool
from .registry import registry

class CreateServerScriptTool(Tool):
    def __init__(self):
        super().__init__(
            name="create_server_script",
            description="Creates a Python Server Script in Frappe to enforce validation rules, logic, or calculations.",
            schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the script (e.g. 'Loan Validation')"},
                    "script_type": {"type": "string", "description": "Usually 'DocType Event'"},
                    "reference_doctype": {"type": "string", "description": "The DocType this script runs on"},
                    "doctype_event": {"type": "string", "description": "e.g., 'Before Save', 'Before Insert', 'On Update'"},
                    "script": {"type": "string", "description": "The Python code block. Variables available: doc, frappe."}
                },
                "required": ["name", "script_type", "reference_doctype", "doctype_event", "script"]
            },
            required_permissions=["System Manager", "Administrator"],
            risk_classification="RED" # Code injection is highest risk
        )

    def validate(self, params: Dict[str, Any], user: str) -> bool:
        if frappe.db.exists("Server Script", params.get("name")):
            frappe.throw(f"Server Script {params.get('name')} already exists.")
        return True

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        doc = frappe.get_doc({
            "doctype": "Server Script",
            "name": params.get("name"),
            "script_type": params.get("script_type"),
            "reference_doctype": params.get("reference_doctype"),
            "doctype_event": params.get("doctype_event"),
            "script": params.get("script")
        })
        doc.insert(ignore_permissions=True)
        return {"name": doc.name}

    def verify(self, params: Dict[str, Any]) -> bool:
        return frappe.db.exists("Server Script", params.get("name"))

    def get_rollback_payload(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {"name": params.get("name")}

registry.register(CreateServerScriptTool())
