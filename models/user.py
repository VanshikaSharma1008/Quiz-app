"""
User model for quiz application.

This module contains the User class that manages user information
and score tracking during quiz sessions.
"""


class User:
    """
    Represents a user participating in the quiz application.
    
    Attributes:
        name (str): The user's display name
        current_score (int): Current score in the active quiz
        total_score (int): Cumulative score across all quizzes
        quizzes_taken (int): Number of quizzes completed
    """
    
    def __init__(self, name: str):
        """
        Initialize a new user.
        
        Args:
            name (str): The user's display name
        """
        self.name = name
        self.current_score = 0
        self.total_score = 0
        self.quizzes_taken = 0
    
    def start_new_quiz(self) -> None:
        """Reset current score for a new quiz session."""
        self.current_score = 0
    
    def add_points(self, points: int) -> None:
        """
        Add points to the current quiz score.
        
        Args:
            points (int): Points to add to current score
        """
        if points < 0:
            raise ValueError("Points cannot be negative")
        self.current_score += points
    
    def complete_quiz(self) -> None:
        """Mark quiz as completed and update total statistics."""
        self.total_score += self.current_score
        self.quizzes_taken += 1
    
    def get_average_score(self) -> float:
        """
        Calculate average score across all completed quizzes.
        
        Returns:
            float: Average score, or 0.0 if no quizzes taken
        """
        try:
            if self.quizzes_taken == 0:
                return 0.0
            return self.total_score / self.quizzes_taken
        except ZeroDivisionError:
            return 0.0
    
    def __str__(self) -> str:
        """Return string representation of the user."""
        return f"User(name='{self.name}', current_score={self.current_score}, total_score={self.total_score})" 