from typing import List, Dict, Any
from ..schemas.change_plan import ChangePlan
from ..tools.registry import registry

class RiskEngine:
    
    @staticmethod
    def evaluate_risk(plan: ChangePlan) -> str:
        """
        Determines the maximum risk level of a given change plan.
        It evaluates the tools being called against the environment.
        """
        highest_risk = "GREEN"
        
        for op in plan.operations:
            tool = registry.get_tool(op.tool)
            risk = tool.risk_classification
            
            if risk == "RED":
                return "RED"
            elif risk == "YELLOW":
                highest_risk = "YELLOW"
                
        return highest_risk

    @staticmethod
    def requires_approval(risk_level: str) -> bool:
        # Based on Phase 1 rules
        if risk_level in ["YELLOW", "RED"]:
            return True
        return False
