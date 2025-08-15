import logging
import requests
from models.schemas import TTSResponse

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.murf.ai/v1/speech/generate"
        self.default_voice = "en-US-natalie"
        
    async def text_to_speech(self, text: str, voice_id: str = None) -> TTSResponse:
        """Convert text to speech using Murf AI"""
        try:
            logger.info(f"Generating TTS for text: {text[:50]}...")
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.api_key
            }
            
            payload = {
                "text": text,
                "voiceId": voice_id or self.default_voice,
                "format": "MP3",
                "volume": "100%"
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            audio_url = response_data.get("audioFile")
            
            if not audio_url:
                raise Exception("No audio URL in response")
                
            logger.info("TTS generation successful")
            return TTSResponse(audio_url=audio_url)
            
        except Exception as e:
            logger.error(f"TTS Service error: {str(e)}")
            raise e
