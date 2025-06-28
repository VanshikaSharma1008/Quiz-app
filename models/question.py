"""
Question model for quiz application.

This module contains the Question class that represents different types
of quiz questions including multiple choice, true/false, and more.
"""

from typing import List, Any, Optional


class Question:
    """
    Represents a quiz question with various types and formats.
    
    Attributes:
        text (str): The question text
        question_type (str): Type of question (mcq, true_false, etc.)
        options (List[str]): Available options for MCQ questions
        correct_answer (Any): The correct answer
        points (int): Points awarded for correct answer
        explanation (Optional[str]): Explanation for the answer
    """
    
    def __init__(self, text: str, question_type: str, correct_answer: Any, 
                 points: int = 1, options: Optional[List[str]] = None, 
                 explanation: Optional[str] = None):
        """
        Initialize a new question.
        
        Args:
            text (str): The question text
            question_type (str): Type of question (mcq, true_false, etc.)
            correct_answer (Any): The correct answer
            points (int): Points awarded for correct answer
            options (Optional[List[str]]): Available options for MCQ questions
            explanation (Optional[str]): Explanation for the answer
        """
        self.text = text
        self.question_type = question_type
        self.correct_answer = correct_answer
        self.points = points
        self.options = options or []
        self.explanation = explanation
        
        # Validate question based on type
        self._validate_question()
    
    def _validate_question(self) -> None:
        """Validate question data based on question type."""
        try:
            if not self.text.strip():
                raise ValueError("Question text cannot be empty")
            
            if self.points < 0:
                raise ValueError("Points cannot be negative")
            
            if self.question_type == "mcq":
                if not self.options:
                    raise ValueError("MCQ questions must have options")
                if len(self.options) < 2:
                    raise ValueError("MCQ questions must have at least 2 options")
                if self.correct_answer not in self.options:
                    raise ValueError("Correct answer must be one of the options")
            
            elif self.question_type == "true_false":
                if not isinstance(self.correct_answer, bool):
                    raise ValueError("True/False questions must have boolean correct answer")
                if self.options:
                    raise ValueError("True/False questions should not have options")
            
            elif self.question_type == "short_answer":
                if not isinstance(self.correct_answer, str):
                    raise ValueError("Short answer questions must have string correct answer")
                if self.options:
                    raise ValueError("Short answer questions should not have options")
            
            else:
                raise ValueError(f"Unsupported question type: {self.question_type}")
                
        except Exception as e:
            raise ValueError(f"Validation failed: {e}") from e

    
    def check_answer(self, user_answer: str | bool) -> bool:

                """
        Check if the user's answer is correct.

        Args:
            user_answer (str | bool): The answer provided by the user.
                - For 'mcq': a string matching one of the options.
                - For 'true_false': a boolean.
                - For 'short_answer': a string (case-insensitive match).

        Returns:
            bool: True if the answer is correct, False otherwise.

        Raises:
            RuntimeError: If an unexpected error occurs during comparison.

        Examples:
            >>> q = Question("2 + 2?", "mcq", "4", options=["3", "4", "5"])
            >>> q.check_answer("4")
            True
        """
        try:
            if self.question_type == "mcq":
                return user_answer == self.correct_answer
            
            elif self.question_type == "true_false":
                return user_answer == self.correct_answer
            
            elif self.question_type == "short_answer":
                # Case-insensitive string comparison for short answers
                if isinstance(user_answer, str) and isinstance(self.correct_answer, str):
                    return user_answer.strip().lower() == self.correct_answer.strip().lower()
                return user_answer == self.correct_answer
            
            else:
                return user_answer == self.correct_answer
                
        except Exception as e:
            raise RuntimeError(f"Answer check failed: {e}") from e
    
    def get_correct_answer(self) -> Any:
        """
        Get the correct answer for this question.
        
        Returns:
            Any: The correct answer
        """
        return self.correct_answer
    
    def get_options(self) -> List[str]:
        """
        Get the available options for this question.
        
        Returns:
            List[str]: List of options, empty for non-MCQ questions
        """
        return self.options.copy() if self.options else []
    
    def display_question(self) -> str:
        """
        Get a formatted display string for the question.
        
        Returns:
            str: Formatted question text
        """
        try:
            display = f"Question: {self.text}\n"
            
            if self.question_type == "mcq" and self.options:
                display += "Options:\n"
                for i, option in enumerate(self.options, 1):
                    display += f"  {i}. {option}\n"
            
            elif self.question_type == "true_false":
                display += "Options:\n  1. True\n  2. False\n"
            
            display += f"Points: {self.points}"
            return display
            
        except Exception as e:
            print(f"Error displaying question: {e}")
            return self.text
    
    def __str__(self) -> str:
        """Return string representation of the question."""
        return f"Question(type={self.question_type}, text='{self.text[:50]}...', points={self.points})"
