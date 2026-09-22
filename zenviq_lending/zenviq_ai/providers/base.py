from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    
    @abstractmethod
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def generate_plan(self, prompt: str, context: Dict[str, Any], tools: List[Dict[str, Any]]) -> str:
        """
        Sends the prompt to the AI with tools and context, and returns the generated ChangePlan JSON string.
        """
        pass
