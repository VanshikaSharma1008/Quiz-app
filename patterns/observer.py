"""
Observer pattern implementation for quiz application.

This module provides the Observer pattern for handling time-over
and UI update notifications throughout the quiz system.
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
        try:
            if observer not in self._observers:
                self._observers.append(observer)
        except Exception as e:
            print(f"Error attaching observer: {e}")
    
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from this subject.
        
        Args:
            observer (Observer): The observer to detach
        """
        try:
            if observer in self._observers:
                self._observers.remove(observer)
        except Exception as e:
            print(f"Error detaching observer: {e}")
    
    def notify(self, data: Any = None) -> None:
        """
        Notify all attached observers of a state change.
        
        Args:
            data (Any): Optional data to pass to observers
        """
        try:
            for observer in self._observers:
                observer.update(self, data)
        except Exception as e:
            print(f"Error notifying observers: {e}")


class QuizTimerObserver(Observer):
    """
    Observer for quiz timer events.
    
    Handles notifications when quiz time expires or
    when time-related events occur.
    """
    
    def __init__(self, name: str):
        """
        Initialize the quiz timer observer.
        
        Args:
            name (str): Name identifier for this observer
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle timer-related updates.
        
        Args:
            subject (Subject): The timer subject
            data (Any): Timer data (remaining time, time expired, etc.)
        """
        try:
            if data is None:
                return
            
            if isinstance(data, dict):
                if data.get('time_expired', False):
                    print(f"[{self.name}] Quiz time has expired!")
                elif 'remaining_time' in data:
                    print(f"[{self.name}] Time remaining: {data['remaining_time']} seconds")
        except Exception as e:
            print(f"Error in timer observer update: {e}")


class UIUpdateObserver(Observer):
    """
    Observer for UI update notifications.
    
    Handles notifications when quiz state changes
    that require UI updates.
    """
    
    def __init__(self, name: str):
        """
        Initialize the UI update observer.
        
        Args:
            name (str): Name identifier for this observer
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Handle UI update notifications.
        
        Args:
            subject (Subject): The subject triggering UI update
            data (Any): UI update data (question change, score update, etc.)
        """
        try:
            if data is None:
                return
            
            if isinstance(data, dict):
                update_type = data.get('type', 'unknown')
                if update_type == 'question_change':
                    print(f"[{self.name}] New question loaded")
                elif update_type == 'score_update':
                    print(f"[{self.name}] Score updated: {data.get('score', 0)}")
                elif update_type == 'quiz_complete':
                    print(f"[{self.name}] Quiz completed!")
        except Exception as e:
            print(f"Error in UI observer update: {e}") 