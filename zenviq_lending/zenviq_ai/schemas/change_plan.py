from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChangeOperation(BaseModel):
    tool: str = Field(..., description="The name of the tool to execute")
    reason: str = Field(..., description="Reason for this specific operation")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters to pass to the tool")
    before_state: Optional[Dict[str, Any]] = Field(None, description="Expected state before execution")
    expected_after_state: Optional[Dict[str, Any]] = Field(None, description="Expected state after execution")

class ChangePlan(BaseModel):
    intent: str = Field(..., description="Detected user intent")
    summary: str = Field(..., description="Human-readable summary of what will change")
    risk_level: str = Field(..., description="GREEN, YELLOW, or RED")
    requires_approval: bool = Field(..., description="True if human approval is required")
    affected_objects: List[str] = Field(default_factory=list, description="List of DocTypes or records affected")
    operations: List[ChangeOperation] = Field(default_factory=list, description="Ordered list of operations to perform")
    warnings: List[str] = Field(default_factory=list, description="Any warnings about this plan")
    validation_checks: List[str] = Field(default_factory=list, description="Pre-execution checks")
    verification_steps: List[str] = Field(default_factory=list, description="Post-execution verification steps")
    rollback_available: bool = Field(True, description="Whether this plan can be safely rolled back")
