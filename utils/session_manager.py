import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class SessionManager:
    """Manages user sessions and interview progress."""
    
    def __init__(self):
        """Initialize the session manager."""
        self.sessions = {}
        self.session_timeout = 3600  # 1 hour
    
    def create_session(self, user_profile: Dict) -> str:
        """
        Create a new interview session.
        
        Args:
            user_profile: User profile information
            
        Returns:
            Session ID
        """
        import uuid
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            'user_profile': user_profile,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'questions_asked': 0,
            'current_question': None,
            'responses': [],
            'scores': [],
            'categories_covered': set(),
            'difficulty_level': 'beginner',
            'session_complete': False
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found/expired
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session has expired
        if self._is_session_expired(session):
            self.delete_session(session_id)
            return None
        
        # Update last activity
        session['last_activity'] = datetime.now()
        return session
    
    def update_session(self, session_id: str, updates: Dict) -> bool:
        """
        Update session information.
        
        Args:
            session_id: Session identifier
            updates: Dictionary of updates to apply
            
        Returns:
            True if successful, False otherwise
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        
        for key, value in updates.items():
            if key in session:
                session[key] = value
        
        session['last_activity'] = datetime.now()
        return True
    
    def add_response(self, session_id: str, question: str, response: str, evaluation: Dict) -> bool:
        """
        Add a response to the session.
        
        Args:
            session_id: Session identifier
            question: The question that was asked
            response: User's response
            evaluation: AI evaluation of the response
            
        Returns:
            True if successful, False otherwise
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        
        response_data = {
            'question': question,
            'response': response,
            'evaluation': evaluation,
            'timestamp': datetime.now().isoformat()
        }
        
        session['responses'].append(response_data)
        session['scores'].append(evaluation.get('score', 5))
        session['questions_asked'] += 1
        session['last_activity'] = datetime.now()
        
        # Update difficulty based on performance
        self._adjust_difficulty(session)
        
        return True
    
    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """
        Get a summary of the session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary or None if not found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        scores = session['scores']
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total_questions': session['questions_asked'],
            'average_score': round(avg_score, 2),
            'categories_covered': list(session['categories_covered']),
            'difficulty_level': session['difficulty_level'],
            'session_duration': self._get_session_duration(session),
            'responses': session['responses']
        }
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False otherwise
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        return len(expired_sessions)
    
    def _is_session_expired(self, session: Dict) -> bool:
        """Check if a session has expired."""
        last_activity = session['last_activity']
        if isinstance(last_activity, str):
            last_activity = datetime.fromisoformat(last_activity)
        
        return datetime.now() - last_activity > timedelta(seconds=self.session_timeout)
    
    def _get_session_duration(self, session: Dict) -> int:
        """Get session duration in minutes."""
        created_at = session['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        duration = datetime.now() - created_at
        return int(duration.total_seconds() / 60)
    
    def _adjust_difficulty(self, session: Dict) -> None:
        """Adjust difficulty level based on recent performance."""
        if len(session['scores']) < 3:
            return
        
        # Look at last 3 scores
        recent_scores = session['scores'][-3:]
        avg_recent_score = sum(recent_scores) / len(recent_scores)
        
        current_difficulty = session['difficulty_level']
        
        if avg_recent_score >= 8 and current_difficulty == 'beginner':
            session['difficulty_level'] = 'intermediate'
        elif avg_recent_score >= 8 and current_difficulty == 'intermediate':
            session['difficulty_level'] = 'advanced'
        elif avg_recent_score <= 4 and current_difficulty == 'advanced':
            session['difficulty_level'] = 'intermediate'
        elif avg_recent_score <= 4 and current_difficulty == 'intermediate':
            session['difficulty_level'] = 'beginner' 