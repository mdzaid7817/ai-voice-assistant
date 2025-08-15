# services/stt_service.py
import logging
from typing import BinaryIO
import assemblyai as aai
from models.schemas import TranscriptionResult

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        aai.settings.api_key = api_key
        self.transcriber = aai.Transcriber()

    async def transcribe_audio(self, audio_file: BinaryIO) -> TranscriptionResult:
        """Transcribe audio file to text using AssemblyAI"""
        try:
            logger.info("Starting audio transcription")
            transcript = self.transcriber.transcribe(audio_file)

            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                raise Exception(f"Transcription failed: {transcript.error}")

            if not transcript.text:
                logger.warning("No speech detected in audio")
                raise Exception("No speech detected")

            logger.info(f"Transcription successful: {transcript.text[:50]}...")
            confidence = getattr(transcript, "confidence", None)
            return TranscriptionResult(text=transcript.text, confidence=confidence)

        except Exception as e:
            logger.error(f"STT Service error: {str(e)}")
            raise
