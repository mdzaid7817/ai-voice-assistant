import logging
from typing import List, Dict, Any, Tuple
import google.generativeai as genai
from models.schemas import LLMResponse

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str, model_name: str = 'gemini-1.5-flash'):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def get_response(self, user_input: str, history: List[Dict[str, Any]]) -> Tuple[LLMResponse, List[Dict[str, Any]]]:
        try:
            logger.info(f"Processing LLM request: {user_input[:50]}...")
            chat = self.model.start_chat(history=history)
            response = chat.send_message(user_input)
            logger.info(f"LLM response generated: {response.text[:50]}...")
            return LLMResponse(text=response.text), chat.history
        except Exception as e:
            logger.error(f"LLM Service error: {str(e)}")
            raise
