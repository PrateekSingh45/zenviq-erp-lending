import frappe
from typing import List

class PermissionEngine:
    
    @staticmethod
    def user_has_tool_permission(user: str, required_roles: List[str]) -> bool:
        """
        Checks if the given user has the roles required to execute the tool.
        """
        if "System Manager" in frappe.get_roles(user):
            return True
            
        user_roles = set(frappe.get_roles(user))
        required = set(required_roles)
        
        # If any of the required roles are present, grant permission
        if user_roles.intersection(required):
            return True
            
        return False
