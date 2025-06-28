"""
Question management module for the quiz application.

This module handles question objects and implements the Factory pattern
for creating different types of questions (MCQ, True/False, etc.).
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict


class Question(ABC):
    """
    Abstract base class for quiz questions.
    
    This class defines the interface that all question types must implement.
    Questions can be multiple choice, true/false, short answer, etc.
    """
    
    def __init__(self, text: str, points: int = 1):
        """
        Initialize a question.
        
        Args:
            text (str): The question text
            points (int): Points awarded for correct answer
        """
        self.text = text
        self.points = points
    
    @abstractmethod
    def check_answer(self, user_answer: Any) -> bool:
        """
        Check if the user's answer is correct.
        
        Args:
            user_answer (Any): The user's submitted answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        pass
    
    @abstractmethod
    def get_correct_answer(self) -> Any:
        """
        Get the correct answer for this question.
        
        Returns:
            Any: The correct answer
        """
        pass
    
    @abstractmethod
    def display_question(self) -> str:
        """
        Get a formatted display string for the question.
        
        Returns:
            str: Formatted question text
        """
        pass


class MultipleChoiceQuestion(Question):
    """
    Multiple choice question implementation.
    
    Represents a question with multiple options where only one is correct.
    """
    
    def __init__(self, text: str, options: List[str], correct_answer: str, points: int = 1):
        """
        Initialize a multiple choice question.
        
        Args:
            text (str): The question text
            options (List[str]): Available answer options
            correct_answer (str): The correct answer (must be in options)
            points (int): Points awarded for correct answer
        """
        super().__init__(text, points)
        self.options = options
        self.correct_answer = correct_answer
    
    def check_answer(self, user_answer: Any) -> bool:
        """
        Check if the user's answer is correct.
        
        Args:
            user_answer (Any): The user's submitted answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        return user_answer == self.correct_answer
    
    def get_correct_answer(self) -> Any:
        """
        Get the correct answer for this question.
        
        Returns:
            str: The correct answer
        """
        return self.correct_answer
    
    def display_question(self) -> str:
        """
        Get a formatted display string for the question.
        
        Returns:
            str: Formatted question text with options
        """
        display = f"Question: {self.text}\n"
        display += "Options:\n"
        for i, option in enumerate(self.options, 1):
            display += f"  {i}. {option}\n"
        display += f"Points: {self.points}"
        return display


class TrueFalseQuestion(Question):
    """
    True/False question implementation.
    
    Represents a question with only True or False as possible answers.
    """
    
    def __init__(self, text: str, correct_answer: bool, points: int = 1):
        """
        Initialize a true/false question.
        
        Args:
            text (str): The question text
            correct_answer (bool): The correct answer (True or False)
            points (int): Points awarded for correct answer
        """
        super().__init__(text, points)
        self.correct_answer = correct_answer
    
    def check_answer(self, user_answer: Any) -> bool:
        """
        Check if the user's answer is correct.
        
        Args:
            user_answer (Any): The user's submitted answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        return user_answer == self.correct_answer
    
    def get_correct_answer(self) -> Any:
        """
        Get the correct answer for this question.
        
        Returns:
            bool: The correct answer
        """
        return self.correct_answer
    
    def display_question(self) -> str:
        """
        Get a formatted display string for the question.
        
        Returns:
            str: Formatted question text with True/False options
        """
        display = f"Question: {self.text}\n"
        display += "Options:\n"
        display += "  1. True\n"
        display += "  2. False\n"
        display += f"Points: {self.points}"
        return display


class ShortAnswerQuestion(Question):
    """
    Short answer question implementation.
    
    Represents a question where the user provides a text answer
    that is matched case-insensitively.
    """
    
    def __init__(self, text: str, correct_answer: str, points: int = 1):
        """
        Initialize a short answer question.
        
        Args:
            text (str): The question text
            correct_answer (str): The correct answer (case-insensitive matching)
            points (int): Points awarded for correct answer
        """
        super().__init__(text, points)
        self.correct_answer = correct_answer
    
    def check_answer(self, user_answer: Any) -> bool:
        """
        Check if the user's answer is correct (case-insensitive).
        
        Args:
            user_answer (Any): The user's submitted answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        if not isinstance(user_answer, str):
            return False
        return user_answer.strip().lower() == self.correct_answer.strip().lower()
    
    def get_correct_answer(self) -> Any:
        """
        Get the correct answer for this question.
        
        Returns:
            str: The correct answer
        """
        return self.correct_answer
    
    def display_question(self) -> str:
        """
        Get a formatted display string for the question.
        
        Returns:
            str: Formatted question text
        """
        display = f"Question: {self.text}\n"
        display += "Enter your answer:\n"
        display += f"Points: {self.points}"
        return display


class QuestionFactory:
    """
    Factory class for creating different types of questions.
    
    Implements the Factory pattern to create questions of various types
    including multiple choice, true/false, and other question formats.
    """
    
    def __init__(self):
        """Initialize the question factory."""
        self.supported_types = ["mcq", "true_false", "short_answer"]
    
    def create_question(self, question_type: str, text: str, correct_answer: Any,
                       points: int = 1, options: Optional[List[str]] = None) -> Question:
        """
        Create a question of the specified type.
        
        Args:
            question_type (str): Type of question to create
            text (str): Question text
            correct_answer (Any): Correct answer
            points (int): Points for correct answer
            options (Optional[List[str]]): Options for MCQ questions
            
        Returns:
            Question: Created question object
            
        Raises:
            ValueError: If question type is not supported
        """
        if question_type == "mcq":
            if not options:
                raise ValueError("MCQ questions require options")
            return MultipleChoiceQuestion(text, options, correct_answer, points)
        
        elif question_type == "true_false":
            if not isinstance(correct_answer, bool):
                raise ValueError("True/False questions must have boolean correct answer")
            return TrueFalseQuestion(text, correct_answer, points)
        
        elif question_type == "short_answer":
            if not isinstance(correct_answer, str):
                raise ValueError("Short answer questions must have string correct answer")
            return ShortAnswerQuestion(text, correct_answer, points)
        
        else:
            raise ValueError(f"Unsupported question type: {question_type}")
    
    def get_supported_types(self) -> List[str]:
        """
        Get list of supported question types.
        
        Returns:
            List[str]: List of supported question types
        """
        return self.supported_types.copy() 