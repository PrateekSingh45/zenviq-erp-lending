import requests
import json
from typing import Dict, Any, List
from .base import AIProvider
import frappe

class OpenAIProvider(AIProvider):
    
    def __init__(self, api_key: str, model_name: str = 'gpt-4o'):
        super().__init__(api_key, model_name)
        self.url = 'https://api.openai.com/v1/chat/completions'

    def generate_plan(self, prompt: str, context: Dict[str, Any], tools_manifest: List[Dict[str, Any]]) -> str:
        from ..tools.registry import registry
        
        green_tools = []
        for t in registry.get_all_tools():
            if getattr(t, 'risk_classification', 'RED') == 'GREEN':
                green_tools.append(t)
                
        openai_tools = []
        for t in green_tools:
            openai_tools.append({
                'type': 'function',
                'function': {
                    'name': t.name,
                    'description': t.description,
                    'parameters': t.schema
                }
            })
            
        all_tool_names = [t['name'] for t in tools_manifest]
        
        system_instruction = (
            'You are ZENVIQ AI, a powerful, secure AI Orchestrator inside an ERPNext/Frappe based lending system.\n'
            'You are currently in the AGENTIC LOOP PHASE.\n'
            'You have access to safe exploration tools (functions) like get_doctype_schema or get_system_info.\n'
            '1. ALWAYS use these exploration tools FIRST if you do not know the exact Frappe schema (e.g. column names for reports, fields to modify).\n'
            '2. Once you have all the information, you MUST output a raw JSON ChangePlan matching the schema below.\n'
            '3. NEVER output markdown or text around the JSON. Your final output MUST be purely the JSON ChangePlan.\n\n'
            f'ALL AVAILABLE TOOLS AND THEIR SCHEMAS FOR THE FINAL PLAN: {json.dumps(tools_manifest)}\n'
            f'Context: {json.dumps(context)}\n\n'
            'CHANGE PLAN SCHEMA (FINAL OUTPUT):\n'
            '{\n'
            '  "intent": "string",\n'
            '  "summary": "string",\n'
            '  "risk_level": "GREEN | YELLOW | RED",\n'
            '  "requires_approval": boolean,\n'
            '  "affected_objects": ["string"],\n'
            '  "warnings": ["string"],\n'
            '  "validation_checks": ["string"],\n'
            '  "verification_steps": ["string"],\n'
            '  "rollback_available": boolean,\n'
            '  "operations": [\n'
            '    {\n'
            f'      "tool": "MUST BE ONE OF: {all_tool_names}",\n'
            '      "reason": "string",\n'
            '      "parameters": "JSON-ENCODED STRING OF TOOL ARGUMENTS MATCHING THE TOOL SCHEMA (e.g. \"{\\\"name\\\":\\\"val\\\"}\")"\n'
            '    }\n'
            '  ]\n'
            '}\n'
        )
        
        messages = [
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': prompt}
        ]
        
        max_turns = 5
        for turn in range(max_turns):
            payload = {
                'model': self.model_name,
                'temperature': 0.1,
                'messages': messages,
            }
            if openai_tools:
                payload['tools'] = openai_tools
                
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            resp = requests.post(self.url, json=payload, headers=headers)
            if not resp.ok:
                raise Exception(f'OpenAI API Error {resp.status_code}: {resp.text}')
                
            data = resp.json()
            message = data['choices'][0]['message']
            
            messages.append(message)
            
            if message.get('tool_calls'):
                for tool_call in message['tool_calls']:
                    function_name = tool_call['function']['name']
                    try:
                        arguments = json.loads(tool_call['function']['arguments'])
                        tool = registry.get_tool(function_name)
                        result = tool.execute(arguments)
                        result_str = json.dumps(result)
                    except json.JSONDecodeError:
                        result_str = json.dumps({'error': 'Invalid JSON passed to arguments'})
                    except Exception as e:
                        result_str = json.dumps({'error': str(e)})
                        
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call['id'],
                        'name': function_name,
                        'content': result_str
                    })
            else:
                return message.get('content', '{}')
                
        raise Exception('Max ReAct turns reached without outputting a plan.')
