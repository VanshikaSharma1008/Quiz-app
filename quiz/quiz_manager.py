"""
Quiz manager module for the quiz application.

This module handles quiz state management, timing, scoring, and implements
the Singleton pattern to ensure only one quiz manager instance exists.
"""

import time
import threading
from typing import List, Dict, Any, Optional
from .questions import Question
from .observer import Subject


class QuizManager(Subject):
    """
    Singleton class for managing quiz state and operations.
    
    This class handles quiz initialization, question progression,
    scoring, timing, and state management. Implements the Singleton
    pattern to ensure only one instance exists.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure only one instance of QuizManager exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(QuizManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the quiz manager (only once)."""
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.questions: List[Question] = []
            self.current_question_index: int = 0
            self.current_user: Optional[str] = None
            self.quiz_active: bool = False
            self.quiz_duration: int = 300  # 5 minutes default
            self.start_time: Optional[float] = None
            self.current_score: int = 0
            self._lock = threading.Lock()
            self._initialized = True
    
    def load_questions(self, questions: List[Question]) -> None:
        """
        Load questions for the quiz.
        
        Args:
            questions (List[Question]): List of questions to load
        """
        with self._lock:
            if not questions:
                raise ValueError("Questions list cannot be empty")
            self.questions = questions
            self.current_question_index = 0
            self.notify({'type': 'questions_loaded', 'count': len(questions)})
    
    def start_quiz(self, user_name: str, duration: Optional[int] = None) -> bool:
        """
        Start a new quiz session.
        
        Args:
            user_name (str): Name of the user taking the quiz
            duration (Optional[int]): Quiz duration in seconds
            
        Returns:
            bool: True if quiz started successfully, False otherwise
        """
        with self._lock:
            if not self.questions:
                raise ValueError("No questions loaded")
            
            self.current_user = user_name
            self.current_question_index = 0
            self.quiz_active = True
            self.current_score = 0
            
            if duration:
                self.quiz_duration = duration
            
            self.start_time = time.time()
            self.notify({
                'type': 'quiz_started',
                'user': user_name,
                'duration': self.quiz_duration
            })
            return True
    
    def get_current_question(self) -> Optional[Question]:
        """
        Get the current question.
        
        Returns:
            Optional[Question]: Current question or None if no questions
        """
        with self._lock:
            if not self.questions or self.current_question_index >= len(self.questions):
                return None
            return self.questions[self.current_question_index]
    
    def submit_answer(self, answer: Any) -> Dict[str, Any]:
        """
        Submit an answer for the current question.
        
        Args:
            answer (Any): The user's answer
            
        Returns:
            Dict[str, Any]: Result containing correctness and score
        """
        with self._lock:
            if not self.quiz_active:
                raise ValueError("No active quiz")
            
            current_question = self.get_current_question()
            if not current_question:
                raise ValueError("No current question")
            
            is_correct = current_question.check_answer(answer)
            points_earned = current_question.points if is_correct else 0
            self.current_score += points_earned
            
            result = {
                'correct': is_correct,
                'points_earned': points_earned,
                'correct_answer': current_question.get_correct_answer(),
                'current_score': self.current_score
            }
            
            # Notify observers about answer result
            self.notify({
                'type': 'answer_submitted',
                'correct': is_correct,
                'points': points_earned,
                'current_score': self.current_score
            })
            self.next_question()
            
            return result
    
    def next_question(self) -> bool:
        """
        Move to the next question.
        
        Returns:
            bool: True if moved to next question, False if quiz is complete
        """
        with self._lock:
            self.current_question_index += 1
            
            if self.current_question_index >= len(self.questions):
                self.end_quiz()
                return False
            
            self.notify({
                'type': 'question_change',
                'question_number': self.current_question_index + 1,
                'total_questions': len(self.questions)
            })
            
            return True
    
    def end_quiz(self) -> Dict[str, Any]:
        """
        End the current quiz session.
        
        Returns:
            Dict[str, Any]: Quiz results summary
        """
        with self._lock:
            if not self.quiz_active:
                raise ValueError("No active quiz to end")
            
            self.quiz_active = False
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            
            results = {
                'user_name': self.current_user,
                'final_score': self.current_score,
                'total_questions': len(self.questions),
                'answered_questions': self.current_question_index,
                'elapsed_time': elapsed_time
            }
            
            # Notify observers about quiz ending
            self.notify("Quiz has ended.")
            
            self.notify({
                'type': 'quiz_complete',
                'results': results
            })
            
            return results
    
    def get_quiz_progress(self) -> Dict[str, Any]:
        """
        Get current quiz progress information.
        
        Returns:
            Dict[str, Any]: Progress information
        """
        with self._lock:
            if not self.quiz_active:
                return {'active': False}
            
            remaining_time = max(0, self.quiz_duration - (time.time() - self.start_time))
            
            return {
                'active': True,
                'current_question': self.current_question_index + 1,
                'total_questions': len(self.questions),
                'remaining_time': remaining_time,
                'current_score': self.current_score
            }
    
    def get_remaining_time(self) -> int:
        """
        Get the remaining time in seconds.
        
        Returns:
            int: Remaining time in seconds, 0 if expired
        """
        with self._lock:
            if not self.quiz_active or not self.start_time:
                return 0
            
            remaining = max(0, int(self.quiz_duration - (time.time() - self.start_time)))
            return remaining
    
    def is_time_expired(self) -> bool:
        """
        Check if the quiz time has expired.
        
        Returns:
            bool: True if time has expired, False otherwise
        """
        expired = self.get_remaining_time() == 0
        if expired and self.quiz_active:
            self.notify("⏰ Time is up!")
        return expired 