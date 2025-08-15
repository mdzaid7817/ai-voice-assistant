import logging
import os
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Path as FastAPIPath, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from models.schemas import ChatResponse, ErrorResponse
from services.stt_service import STTService
from services.llm_service import LLMService
from services.tts_service import TTSService
from utils.session_manager import SessionManager

# Load environment variables
load_dotenv()

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Voice Assistant",
    description="A conversational AI voice assistant with STT, LLM, and TTS capabilities",
    version="1.0.0"
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services
def initialize_services():
    """Initialize all external services"""
    try:
        # Get API keys
        assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        murf_key = os.getenv("MURF_API_KEY")
        
        if not all([assemblyai_key, gemini_key, murf_key]):
            missing = []
            if not assemblyai_key: missing.append("ASSEMBLYAI_API_KEY")
            if not gemini_key: missing.append("GEMINI_API_KEY")
            if not murf_key: missing.append("MURF_API_KEY")
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        # Initialize services
        stt_service = STTService(assemblyai_key)
        llm_service = LLMService(gemini_key)
        tts_service = TTSService(murf_key)
        session_manager = SessionManager()
        
        logger.info("All services initialized successfully")
        return stt_service, llm_service, tts_service, session_manager
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise e

# Initialize services
try:
    stt_service, llm_service, tts_service, session_manager = initialize_services()
except Exception as e:
    logger.error("Application startup failed")
    stt_service = llm_service = tts_service = session_manager = None

@app.get("/")
async def home(request: Request):
    """Serve the main application UI"""
    logger.info("Serving main application page")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/agent/chat/{session_id}", response_model=ChatResponse)
async def agent_chat(
    session_id: str = FastAPIPath(..., description="Unique session identifier"),
    audio_file: UploadFile = File(...)
):
    """Handle conversational chat with voice input and output"""
    fallback_audio_path = "static/fallback.mp3"
    
    # Check if services are available
    if not all([stt_service, llm_service, tts_service, session_manager]):
        logger.error("Services not properly initialized")
        return FileResponse(
            fallback_audio_path, 
            media_type="audio/mpeg", 
            headers={"X-Error": "true"}
        )
    
    try:
        logger.info(f"Processing chat request for session: {session_id}")
        
        # Step 1: Speech to Text
        transcription = await stt_service.transcribe_audio(audio_file.file)
        user_input = transcription.text
        logger.info(f"User input transcribed: {user_input[:100]}...")
        
        # Step 2: Get session and chat history
        session = session_manager.get_or_create_session(session_id)
        
        # Step 3: Get LLM response
        llm_response, updated_history = await llm_service.get_response(
            user_input, 
            session.history
        )
        
        # Step 4: Update session history
        session_manager.update_session_history(session_id, updated_history)
        
        # Step 5: Convert response to speech
        tts_response = await tts_service.text_to_speech(llm_response.text)
        
        logger.info(f"Chat request completed successfully for session: {session_id}")
        
        return JSONResponse(content={
            "audio_url": tts_response.audio_url,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return FileResponse(
            fallback_audio_path,
            media_type="audio/mpeg",
            headers={"X-Error": "true"}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    services_status = {
        "stt_service": stt_service is not None,
        "llm_service": llm_service is not None,
        "tts_service": tts_service is not None,
        "session_manager": session_manager is not None
    }
    
    return {
        "status": "healthy" if all(services_status.values()) else "unhealthy",
        "services": services_status,
        "active_sessions": session_manager.get_session_count() if session_manager else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
