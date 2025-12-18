"""
Interview service for managing interview sessions
"""
import asyncio
import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta
import os

# Import the agents from the parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from agents import InterviewAgents


class InterviewSession:
    """Represents an active interview session"""
    
    def __init__(self, session_id: str, technology: str, position: str):
        self.session_id = session_id
        self.technology = technology
        self.position = position
        self.agents = InterviewAgents(technology, position)
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.current_question_number = 0
        self.current_question = None
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'technology': self.technology,
            'position': self.position,
            'current_question_number': self.current_question_number,
            'questions_answered': len(self.agents.interview_history),
            'average_score': round(sum(self.agents.scores) / len(self.agents.scores), 2) if self.agents.scores else 0,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat()
        }


class InterviewService:
    """Service for managing interview sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.session_timeout = timedelta(hours=2)  # Sessions expire after 2 hours
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session.last_activity > self.session_timeout
        ]
        for sid in expired:
            del self.sessions[sid]
    
    def create_session(self, technology: str, position: str) -> str:
        """Create a new interview session"""
        self._cleanup_expired_sessions()
        
        session_id = str(uuid.uuid4())
        session = InterviewSession(session_id, technology, position)
        self.sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get an interview session by ID"""
        session = self.sessions.get(session_id)
        if session:
            session.last_activity = datetime.now()
        return session
    
    async def start_interview(self, session_id: str) -> Dict:
        """Start an interview and get the first question"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.current_question_number = 1
        question = await session.agents.get_next_question(1)
        session.current_question = question
        
        return {
            'session_id': session_id,
            'question_number': 1,
            'question': question
        }
    
    async def submit_answer(self, session_id: str, answer: str) -> Dict:
        """Submit an answer and get feedback and score"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        if not session.current_question:
            raise ValueError("No active question")
        
        # Process the answer
        result = await session.agents.process_answer(
            session.current_question,
            answer,
            session.current_question_number
        )
        
        return {
            'session_id': session_id,
            'question_number': result['question_number'],
            'question': result['question'],
            'answer': result['answer'],
            'feedback': result['feedback'],
            'score': result['score'],
            'score_details': result['score_details']
        }
    
    async def get_next_question(self, session_id: str) -> Dict:
        """Get the next question"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.current_question_number += 1
        question = await session.agents.get_next_question(session.current_question_number)
        session.current_question = question
        
        return {
            'session_id': session_id,
            'question_number': session.current_question_number,
            'question': question
        }
    
    async def end_interview(self, session_id: str) -> Dict:
        """End the interview and get summary"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.is_active = False
        summary = await session.agents.get_overall_summary()
        
        return {
            'session_id': session_id,
            'technology': session.technology,
            'position': session.position,
            'summary': summary
        }
    
    def get_session_info(self, session_id: str) -> Dict:
        """Get session information"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        return session.to_dict()
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# Global service instance
interview_service = InterviewService()

