"""
Quiz Manager service for quiz application.

This module handles the core quiz flow including loading questions,
starting quizzes, checking answers, and managing quiz state.
"""

from typing import List, Dict, Any, Optional
from models.question import Question
from models.user import User
from utils.timer import Timer
from patterns.observer import Subject, Observer


class QuizManager(Subject, Observer):
    """
    Manages the overall quiz flow and state.
    
    Handles loading questions, starting quizzes, checking answers,
    and managing the quiz lifecycle. Implements both Subject and Observer
    patterns for notifications and time expiration handling.
    """
    
    def __init__(self):
        """Initialize the quiz manager with default state."""
        super().__init__()
        self.questions: List[Question] = []
        self.current_question_index: int = 0
        self.current_user: Optional[User] = None
        self.timer: Optional[Timer] = None
        self.quiz_active: bool = False
        self.quiz_duration: int = 300  # 5 minutes default
    
    def load_questions(self, questions: List[Question]) -> None:
        """
        Load questions for the quiz.
        
        Args:
            questions (List[Question]): List of questions to load
        """
        if not questions:
            raise ValueError("Questions list cannot be empty")
        self.questions = questions
        self.current_question_index = 0
        print(f"Loaded {len(questions)} questions")
        # Notify observers of question load
        self.notify({
            'type': 'questions_loaded',
            'count': len(questions)
        })
    
    def start_quiz(self, user: User, duration: Optional[int] = None) -> bool:
        """
        Start a new quiz session.
        
        Args:
            user (User): The user taking the quiz
            duration (Optional[int]): Quiz duration in seconds
            
        Returns:
            bool: True if quiz started successfully, False otherwise
        """
        if not self.questions:
            raise ValueError("No questions loaded")
        if not user:
            raise ValueError("User is required")
        self.current_user = user
        self.current_question_index = 0
        self.quiz_active = True
        # Set quiz duration
        if duration:
            self.quiz_duration = duration
        # Initialize timer
        self.timer = Timer(self.quiz_duration)
        self.timer.attach(self)
        self.timer.start()
        # Reset user score for new quiz
        user.start_new_quiz()
        print(f"Quiz started for user: {user.name}")
        # Notify observers of quiz start
        self.notify({
            'type': 'quiz_started',
            'user': user.name,
            'duration': self.quiz_duration
        })
        return True
    
    def get_current_question(self) -> Optional[Question]:
        """
        Get the current question.
        
        Returns:
            Optional[Question]: Current question or None if no questions
        """
        try:
            if not self.questions or self.current_question_index >= len(self.questions):
                return None
            return self.questions[self.current_question_index]
        except Exception as e:
            print(f"Error getting current question: {e}")
            return None
    
    def submit_answer(self, answer: Any) -> Dict[str, Any]:
        """
        Submit an answer for the current question.
        
        Args:
            answer (Any): The user's answer
            
        Returns:
            Dict[str, Any]: Result containing correctness and score
        """
        try:
            if not self.quiz_active:
                raise ValueError("No active quiz")
            
            if self.timer and self.timer.is_time_up():
                self.end_quiz()
                return {
                    'correct': False,
                    'points_earned': 0,
                    'error': 'Time is up! Quiz ended.'
                }
            
            current_question = self.get_current_question()
            if not current_question:
                raise ValueError("No current question")
            
            # Check if answer is correct
            is_correct = current_question.check_answer(answer)
            points_earned = current_question.points if is_correct else 0
            
            # Update user score
            if self.current_user:
                self.current_user.add_points(points_earned)
            
            result = {
                'correct': is_correct,
                'points_earned': points_earned,
                'correct_answer': current_question.get_correct_answer(),
                'explanation': current_question.explanation,
                'current_score': self.current_user.current_score if self.current_user else 0
            }
            
            # Move to next question
            self.next_question()
            
            # Notify observers of answer submission
            self.notify({
                'type': 'answer_submitted',
                'correct': is_correct,
                'points': points_earned,
                'current_score': self.current_user.current_score if self.current_user else 0
            })
            
            return result
        except Exception as e:
            print(f"Error submitting answer: {e}")
            return {
                'correct': False,
                'points_earned': 0,
                'error': str(e)
            }
    
    def next_question(self) -> bool:
        """
        Move to the next question.
        
        Returns:
            bool: True if moved to next question, False if quiz is complete
        """
        try:
            self.current_question_index += 1
            
            if self.current_question_index >= len(self.questions):
                self.end_quiz()
                return False
            
            # Notify observers of question change
            self.notify({
                'type': 'question_change',
                'question_number': self.current_question_index + 1,
                'total_questions': len(self.questions)
            })
            
            return True
        except Exception as e:
            print(f"Error moving to next question: {e}")
            return False
    
    def end_quiz(self) -> Dict[str, Any]:
        """
        End the current quiz session.
        
        Returns:
            Dict[str, Any]: Quiz results summary
        """
        try:
            if not self.quiz_active:
                print("[⚠️] Quiz already ended — returning final results.")
                total_questions = len(self.questions)
                answered_questions = min(self.current_question_index, total_questions)
                score = self.current_user.current_score if self.current_user else 0
                return {
                    'total_questions': total_questions,
                    'answered_questions': answered_questions,
                    'final_score': score,
                    'user_name': self.current_user.name if self.current_user else 'Unknown',
                    'elapsed_time': self.timer.get_elapsed_time() if self.timer else 0
                }
            
            self.quiz_active = False
            
            # Stop timer if running
            if self.timer:
                self.timer.stop()
            
            # Complete quiz for user
            if self.current_user:
                self.current_user.complete_quiz()
            
            # Calculate results
            total_questions = len(self.questions)
            answered_questions = min(self.current_question_index, total_questions)
            score = self.current_user.current_score if self.current_user else 0
            
            results = {
                'total_questions': total_questions,
                'answered_questions': answered_questions,
                'final_score': score,
                'user_name': self.current_user.name if self.current_user else 'Unknown',
                'elapsed_time': self.timer.get_elapsed_time() if self.timer else 0
            }
            
            print(f"Quiz ended. Final score: {score}")
            
            # Notify observers of quiz completion
            self.notify({
                'type': 'quiz_complete',
                'results': results
            })
            
            return results
        except Exception as e:
            print(f"Error ending quiz: {e}")
            return {}
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle updates from observed subjects (e.g., Timer).
        
        Args:
            subject (Subject): The subject that sent the update
            data (Any): Data sent by the subject
        """
        try:
            if isinstance(data, dict) and data.get("time_expired") is True:
                if self.quiz_active:
                    print("\n⏰ Time is up! Automatically ending quiz...")
                    self.end_quiz()
        except Exception as e:
            print(f"Error handling timer update: {e}")
    
    def get_quiz_progress(self) -> Dict[str, Any]:
        """
        Get current quiz progress information.
        
        Returns:
            Dict[str, Any]: Progress information
        """
        try:
            if not self.quiz_active:
                return {'active': False}
            
            if self.timer and self.timer.is_time_expired():
                self.quiz_active = False
                return {'active': False, 'error': 'Time is up'}
            
            remaining_time = self.timer.get_remaining_time() if self.timer else 0
            
            return {
                'active': True,
                'current_question': self.current_question_index + 1,
                'total_questions': len(self.questions),
                'remaining_time': remaining_time,
                'current_score': self.current_user.current_score if self.current_user else 0
            }
        except Exception as e:
            print(f"Error getting quiz progress: {e}")
            return {'active': False, 'error': str(e)} 