import frappe
from typing import Dict, Any, Optional
from .base import Tool
from .registry import registry

class GetSystemInfoTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_system_info",
            description="Get basic system info and installed apps",
            schema={
                "type": "object",
                "properties": {},
                "required": []
            },
            required_permissions=["System Manager"],
            risk_classification="GREEN"
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        apps = frappe.get_installed_apps()
        return {
            "version": frappe.__version__,
            "installed_apps": apps,
            "site": frappe.local.site
        }

class GetDoctypeSchemaTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_doctype_schema",
            description="Get the schema (fields, properties) of a Frappe DocType",
            schema={
                "type": "object",
                "properties": {
                    "doctype": {"type": "string", "description": "Name of the DocType"}
                },
                "required": ["doctype"]
            },
            required_permissions=["System Manager"],
            risk_classification="GREEN"
        )
        
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        dt = params.get("doctype")
        if not frappe.db.exists("DocType", dt):
            return {"error": f"DocType {dt} does not exist."}
            
        meta = frappe.get_meta(dt)
        fields = []
        for f in meta.fields:
            fields.append({
                "fieldname": f.fieldname,
                "label": f.label,
                "fieldtype": f.fieldtype,
                "options": f.options,
                "reqd": f.reqd,
                "hidden": f.hidden
            })
            
        custom_fields = frappe.get_all("Custom Field", filters={"dt": dt}, fields=["fieldname", "label", "fieldtype", "options", "reqd", "hidden"])
        for cf in custom_fields:
            fields.append(cf)
            
        return {
            "name": dt,
            "module": meta.module,
            "is_submittable": meta.is_submittable,
            "istable": meta.istable,
            "custom": meta.custom,
            "fields": fields
        }

# Register tools
registry.register(GetSystemInfoTool())
registry.register(GetDoctypeSchemaTool())
