from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel
import frappe

class Tool(BaseModel):
    name: str
    description: str
    schema: Dict[str, Any]
    required_permissions: list[str]
    risk_classification: str # GREEN, YELLOW, RED
    
    # In Pydantic models, Callable fields need to be handled carefully or excluded from validation
    class Config:
        arbitrary_types_allowed = True

    def validate(self, params: Dict[str, Any], user: str) -> bool:
        """Validates if the user and parameters are allowed for this tool"""
        return True

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the tool and returns the result"""
        raise NotImplementedError
        
    def verify(self, params: Dict[str, Any]) -> bool:
        """Verifies if the tool executed successfully"""
        return True
        
    def get_rollback_payload(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Returns data needed to rollback this operation"""
        return None
