"""
Quiz Application Core Package.

This package contains the core logic for the quiz application,
including question management, quiz state handling, UI components,
and observer pattern implementation.
"""

__version__ = "1.0.0"
__author__ = "Quiz App Team"

from .questions import Question, QuestionFactory
from .quiz_manager import QuizManager
from .ui import QuizUI
from .observer import Observer, Subject

__all__ = [
    "Question",
    "QuestionFactory", 
    "QuizManager",
    "QuizUI",
    "Observer",
    "Subject"
] 