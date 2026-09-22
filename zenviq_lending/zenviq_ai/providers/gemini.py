import requests
import json
import time
from typing import Dict, Any, List
from .base import AIProvider

class GeminiProvider(AIProvider):
    
    def __init__(self, api_key: str, model_name: str = 'gemini-1.5-pro'):
        super().__init__(api_key, model_name)
        self.url = f'https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}'

    def generate_plan(self, prompt: str, context: Dict[str, Any], tools: List[Dict[str, Any]]) -> str:
        
        tool_names = [t.get('name', 'unknown') for t in tools if 'name' in t]
        if not tool_names:
            tool_names = ['get_system_info', 'get_doctype_schema', 'create_custom_field']
            
        system_instruction = (
            'You are ZENVIQ AI, a powerful, secure AI Orchestrator inside an ERPNext/Frappe based lending system.\n'
            'Your job is to read natural language user requests, and formulate a ChangePlan using ONLY the tools provided.\n'
            'You MUST output valid JSON conforming to the ChangePlan schema.\n'
            'NEVER hallucinate tools. You can ONLY use the tools listed below.\n'
            f'AVAILABLE TOOLS: {json.dumps(tools)}\n'
            f'Context: {json.dumps(context)}\n'
            'IMPORTANT: The parameters field MUST be a JSON-encoded string containing the tool arguments, NOT a JSON object.'
        )
        
        response_schema = {
            'type': 'OBJECT',
            'properties': {
                'intent': {'type': 'STRING'},
                'summary': {'type': 'STRING'},
                'risk_level': {'type': 'STRING', 'enum': ['GREEN', 'YELLOW', 'RED']},
                'requires_approval': {'type': 'BOOLEAN'},
                'affected_objects': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
                'warnings': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
                'validation_checks': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
                'verification_steps': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
                'rollback_available': {'type': 'BOOLEAN'},
                'operations': {
                    'type': 'ARRAY',
                    'items': {
                        'type': 'OBJECT',
                        'properties': {
                            'tool': {'type': 'STRING', 'enum': tool_names},
                            'reason': {'type': 'STRING'},
                            'parameters': {'type': 'STRING'}
                        },
                        'required': ['tool', 'reason', 'parameters']
                    }
                }
            },
            'required': ['intent', 'summary', 'risk_level', 'requires_approval', 'affected_objects', 'operations', 'rollback_available']
        }

        payload = {
            'system_instruction': {
                'parts': [{'text': system_instruction}]
            },
            'contents': [
                {'role': 'user', 'parts': [{'text': prompt}]}
            ],
            'generationConfig': {
                'response_mime_type': 'application/json',
                'response_schema': response_schema,
                'temperature': 0.1
            }
        }
        
        # Exponential backoff for 503 errors (common with Gemini API bursts)
        max_retries = 5
        for attempt in range(max_retries):
            resp = requests.post(self.url, json=payload)
            if resp.status_code == 503 and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            if not resp.ok:
                raise Exception(f'API Error {resp.status_code}: {resp.text}')
            
            data = resp.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                return data['candidates'][0]['content']['parts'][0]['text']
            
            raise Exception(f'Failed to generate plan: {data}')
            
        raise Exception('Exceeded maximum retries for Gemini API.')
