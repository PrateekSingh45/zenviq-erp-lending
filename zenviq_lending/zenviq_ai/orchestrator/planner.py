import frappe
from ..providers.gemini import GeminiProvider
from ..providers.openai import OpenAIProvider
from ..schemas.change_plan import ChangePlan, ChangeOperation
from ..tools import registry
from ..policy.risk_engine import RiskEngine
from ..policy.permission_engine import PermissionEngine
import json

class Planner:
    def __init__(self, user: str):
        self.user = user
        self.settings = frappe.get_single('AI Settings')
        if not self.settings.enabled:
            raise Exception('ZENVIQ AI is disabled.')
            
        api_key = self.settings.get_password('api_key')
        
        if self.settings.provider == 'Gemini':
            model = self.settings.model or 'gemini-1.5-pro'
            self.provider = GeminiProvider(api_key=api_key, model_name=model)
        elif self.settings.provider == 'OpenAI':
            model = self.settings.model or 'gpt-4o'
            self.provider = OpenAIProvider(api_key=api_key, model_name=model)
        else:
            raise NotImplementedError(f'Provider {self.settings.provider} is not currently implemented.')

    def create_plan(self, prompt: str) -> ChangePlan:
        context = {
            'user': self.user,
            'roles': frappe.get_roles(self.user),
            'environment': 'production' if not self.settings.developer_mode else 'development'
        }
        
        all_tools = registry.get_all_tools()
        tools_manifest = [
            {
                'name': t.name,
                'description': t.description,
                'schema': t.schema
            } for t in all_tools
        ]
        
        plan_json_str = self.provider.generate_plan(prompt, context, tools_manifest)
        
        plan_json_str = plan_json_str.strip()
        if plan_json_str.startswith('```json'):
            plan_json_str = plan_json_str[7:]
        if plan_json_str.startswith('```'):
            plan_json_str = plan_json_str[3:]
        if plan_json_str.endswith('```'):
            plan_json_str = plan_json_str[:-3]
        plan_json_str = plan_json_str.strip()
        
        plan_dict = json.loads(plan_json_str)
        
        for op in plan_dict.get('operations', []):
            if isinstance(op.get('parameters'), str):
                try:
                    op['parameters'] = json.loads(op['parameters'])
                except:
                    op['parameters'] = {}

        plan = ChangePlan(**plan_dict)
        
        actual_risk = RiskEngine.evaluate_risk(plan)
        if plan.risk_level != actual_risk:
            plan.warnings.append(f'Risk level upgraded from {plan.risk_level} to {actual_risk} by Policy Engine.')
            plan.risk_level = actual_risk
            
        plan.requires_approval = RiskEngine.requires_approval(plan.risk_level)
        
        for op in plan.operations:
            tool = registry.get_tool(op.tool)
            if not PermissionEngine.user_has_tool_permission(self.user, tool.required_permissions):
                plan.warnings.append(f'User lacks permission to execute {op.tool}.')
                
        return plan
