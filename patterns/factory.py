"""
Factory pattern implementation for quiz application.

This module provides the QuestionFactory class for creating different
types of questions using the Factory pattern.
"""

from typing import List, Any, Optional
from models.question import Question


class QuestionFactory:
    """
    Factory class for creating different types of questions.
    
    Implements the Factory pattern to create questions of various types
    including multiple choice, true/false, and short answer questions.
    """
    
    def __init__(self):
        """Initialize the question factory."""
        self.supported_types = ["mcq", "true_false", "short_answer"]
    
    def create_question(self, question_type: str, text: str, correct_answer: Any,
                       points: int = 1, options: Optional[List[str]] = None,
                       explanation: Optional[str] = None) -> Question:
        """
        Create a question of the specified type.
        
        Args:
            question_type (str): Type of question to create
            text (str): Question text
            correct_answer (Any): Correct answer
            points (int): Points for correct answer
            options (Optional[List[str]]): Options for MCQ questions
            explanation (Optional[str]): Explanation for the answer
            
        Returns:
            Question: Created question object
            
        Raises:
            ValueError: If question type is not supported
        """
        try:
            if question_type not in self.supported_types:
                raise ValueError(f"Unsupported question type: {question_type}")
            
            # Create question based on type
            if question_type == "mcq":
                return self._create_mcq_question(text, correct_answer, points, options, explanation)
            
            elif question_type == "true_false":
                return self._create_true_false_question(text, correct_answer, points, explanation)
            
            elif question_type == "short_answer":
                return self._create_short_answer_question(text, correct_answer, points, explanation)
            
            else:
                raise ValueError(f"Question type '{question_type}' not implemented")
                
        except Exception as e:
            print(f"Error creating question: {e}")
            raise
    
    def _create_mcq_question(self, text: str, correct_answer: Any, points: int,
                           options: Optional[List[str]], explanation: Optional[str]) -> Question:
        """
        Create a multiple choice question.
        
        Args:
            text (str): Question text
            correct_answer (Any): Correct answer
            points (int): Points for correct answer
            options (Optional[List[str]]): Available options
            explanation (Optional[str]): Explanation for the answer
            
        Returns:
            Question: MCQ question object
        """
        try:
            if not options:
                raise ValueError("MCQ questions require options")
            
            if correct_answer not in options:
                raise ValueError("Correct answer must be one of the provided options")
            
            return Question(
                text=text,
                question_type="mcq",
                correct_answer=correct_answer,
                points=points,
                options=options,
                explanation=explanation
            )
        except Exception as e:
            print(f"Error creating MCQ question: {e}")
            raise
    
    def _create_true_false_question(self, text: str, correct_answer: Any, points: int,
                                  explanation: Optional[str]) -> Question:
        """
        Create a true/false question.
        
        Args:
            text (str): Question text
            correct_answer (Any): Correct answer (True or False)
            points (int): Points for correct answer
            explanation (Optional[str]): Explanation for the answer
            
        Returns:
            Question: True/False question object
        """
        try:
            if not isinstance(correct_answer, bool):
                raise ValueError("True/False questions must have boolean correct answer")
            
            return Question(
                text=text,
                question_type="true_false",
                correct_answer=correct_answer,
                points=points,
                explanation=explanation
            )
        except Exception as e:
            print(f"Error creating True/False question: {e}")
            raise
    
    def _create_short_answer_question(self, text: str, correct_answer: Any, points: int,
                                    explanation: Optional[str]) -> Question:
        """
        Create a short answer question.
        
        Args:
            text (str): Question text
            correct_answer (Any): Correct answer (string)
            points (int): Points for correct answer
            explanation (Optional[str]): Explanation for the answer
            
        Returns:
            Question: Short answer question object
        """
        try:
            if not isinstance(correct_answer, str):
                raise ValueError("Short answer questions must have string correct answer")
            
            return Question(
                text=text,
                question_type="short_answer",
                correct_answer=correct_answer,
                points=points,
                explanation=explanation
            )
        except Exception as e:
            print(f"Error creating short answer question: {e}")
            raise
    
    def create_sample_questions(self) -> List[Question]:
        """
        Create a list of sample questions for testing.
        
        Returns:
            List[Question]: List of sample questions
        """
        try:
            questions = []
            
            # Sample MCQ question
            mcq_question = self.create_question(
                question_type="mcq",
                text="What is the capital of France?",
                correct_answer="Paris",
                points=10,
                options=["London", "Berlin", "Paris", "Madrid"],
                explanation="Paris is the capital and largest city of France."
            )
            questions.append(mcq_question)
            
            # Sample True/False question
            tf_question = self.create_question(
                question_type="true_false",
                text="The Earth is flat.",
                correct_answer=False,
                points=5,
                explanation="The Earth is approximately spherical, not flat."
            )
            questions.append(tf_question)
            
            # Sample Short Answer question
            sa_question = self.create_question(
                question_type="short_answer",
                text="What is the chemical symbol for gold?",
                correct_answer="Au",
                points=8,
                explanation="Au comes from the Latin word 'aurum' meaning gold."
            )
            questions.append(sa_question)
            
            return questions
            
        except Exception as e:
            print(f"Error creating sample questions: {e}")
            return []
    
    def get_supported_types(self) -> List[str]:
        """
        Get list of supported question types.
        
        Returns:
            List[str]: List of supported question types
        """
        return self.supported_types.copy()
    
    def add_question_type(self, question_type: str) -> None:
        """
        Add support for a new question type.
        
        Args:
            question_type (str): New question type to support
        """
        try:
            if question_type not in self.supported_types:
                self.supported_types.append(question_type)
                print(f"Added support for question type: {question_type}")
            else:
                print(f"Question type '{question_type}' already supported")
        except Exception as e:
            print(f"Error adding question type: {e}")
