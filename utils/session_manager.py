import logging
from typing import Dict, List, Any
from datetime import datetime
from models.schemas import SessionData

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        
    def get_or_create_session(self, session_id: str) -> SessionData:
        """Get existing session or create new one"""
        if session_id not in self.sessions:
            logger.info(f"Creating new session: {session_id}")
            self.sessions[session_id] = SessionData(
                session_id=session_id,
                history=[],
                created_at=datetime.now().isoformat(),
                last_accessed=datetime.now().isoformat()
            )
        else:
            self.sessions[session_id].last_accessed = datetime.now().isoformat()
            
        return self.sessions[session_id]
        
    def update_session_history(self, session_id: str, history: List[Dict[str, Any]]):
        """Update session conversation history"""
        if session_id in self.sessions:
            self.sessions[session_id].history = history
            self.sessions[session_id].last_accessed = datetime.now().isoformat()
            logger.info(f"Updated history for session: {session_id}")
        
    def get_session_count(self) -> int:
        """Get total number of active sessions"""
        return len(self.sessions)
