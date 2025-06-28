"""
Console observer for the quiz application.

This module provides a console-based observer that prints notifications
to the console when quiz events occur.
"""

from typing import Any
from .observer import Observer, Subject


class ConsoleObserver(Observer):
    """
    Console observer that prints notifications to the console.
    
    This observer implements the Observer pattern to display
    real-time notifications during quiz execution.
    """
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """
        Update method called when observed subject changes.
        
        Args:
            subject (Subject): The subject that triggered the update
            data (Any): Optional data passed with the update
        """
        # Handle string notifications (direct messages)
        if isinstance(data, str):
            print(f"[📢 NOTIFICATION] {data}")
            return
        
        # Handle dictionary data (structured notifications)
        if data and isinstance(data, dict):
            if data.get('type') == 'answer_submitted':
                correct = data.get('correct', False)
                current_score = data.get('current_score', 0)
                
                if correct:
                    print(f"[📢 NOTIFICATION] Correct answer! Score is now {current_score}")
                else:
                    print(f"[📢 NOTIFICATION] Incorrect answer.")
            
            elif data.get('type') == 'quiz_complete':
                print(f"[📢 NOTIFICATION] Quiz has ended.")
            
            elif data.get('type') == 'time_expired':
                print(f"[📢 NOTIFICATION] ⏰ Time is up!") 