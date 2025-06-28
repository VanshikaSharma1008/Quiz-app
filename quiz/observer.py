"""
Observer pattern implementation for the quiz application.

This module provides the Observer pattern for handling notifications
when quiz events occur, such as quiz completion, time expiration, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):
    """
    Abstract base class for observers in the Observer pattern.
    
    Observers are notified when subjects they're observing
    experience state changes.
    """
    
    @abstractmethod
    def update(self, subject: 'Subject', data: Any = None) -> None:
        """
        Update method called when observed subject changes.
        
        Args:
            subject (Subject): The subject that triggered the update
            data (Any): Optional data passed with the update
        """
        pass


class Subject(ABC):
    """
    Abstract base class for subjects in the Observer pattern.
    
    Subjects maintain a list of observers and notify them
    when their state changes.
    """
    
    def __init__(self):
        """Initialize the subject with an empty observer list."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to this subject.
        
        Args:
            observer (Observer): The observer to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from this subject.
        
        Args:
            observer (Observer): The observer to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, data: Any = None) -> None:
        """
        Notify all attached observers of a state change.
        
        Args:
            data (Any): Optional data to pass to observers
        """
        for observer in self._observers:
            observer.update(self, data)


class QuizCompletionObserver(Observer):
    """
    Observer for quiz completion events.
    
    Handles notifications when a quiz is completed.
    """
    
    def __init__(self, name: str):
        """
        Initialize the quiz completion observer.
        
        Args:
            name (str): Name identifier for this observer
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle quiz completion updates.
        
        Args:
            subject (Subject): The quiz manager subject
            data (Any): Quiz completion data
        """
        if data and isinstance(data, dict) and data.get('type') == 'quiz_complete':
            results = data.get('results', {})
            print(f"[{self.name}] Quiz completed!")
            print(f"[{self.name}] Final score: {results.get('final_score', 0)}")
            print(f"[{self.name}] Time taken: {results.get('elapsed_time', 0):.1f} seconds")


class TimeObserver(Observer):
    """
    Observer for time-related events.
    
    Handles notifications when quiz time expires or
    when time-related events occur.
    """
    
    def __init__(self, name: str):
        """
        Initialize the time observer.
        
        Args:
            name (str): Name identifier for this observer
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle time-related updates.
        
        Args:
            subject (Subject): The quiz manager subject
            data (Any): Time-related data
        """
        if data and isinstance(data, dict):
            if data.get('type') == 'quiz_started':
                duration = data.get('duration', 0)
                print(f"[{self.name}] Quiz started with {duration} seconds")
            
            elif data.get('type') == 'question_change':
                question_num = data.get('question_number', 0)
                total_questions = data.get('total_questions', 0)
                print(f"[{self.name}] Question {question_num}/{total_questions}")


class ScoreObserver(Observer):
    """
    Observer for score-related events.
    
    Handles notifications when scores change or
    when answer-related events occur.
    """
    
    def __init__(self, name: str):
        """
        Initialize the score observer.
        
        Args:
            name (str): Name identifier for this observer
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle score-related updates.
        
        Args:
            subject (Subject): The quiz manager subject
            data (Any): Score-related data
        """
        if data and isinstance(data, dict):
            if data.get('type') == 'answer_submitted':
                correct = data.get('correct', False)
                points = data.get('points', 0)
                current_score = data.get('current_score', 0)
                
                if correct:
                    print(f"[{self.name}] Correct answer! +{points} points")
                else:
                    print(f"[{self.name}] Incorrect answer. +0 points")
                
                print(f"[{self.name}] Current score: {current_score}")
            
            elif data.get('type') == 'questions_loaded':
                count = data.get('count', 0)
                print(f"[{self.name}] Loaded {count} questions") 