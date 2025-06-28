"""
Singleton pattern implementation for quiz application.

This module provides singleton classes for managing global state
such as scores and timers across the quiz application.
"""

from typing import Dict, List, Tuple, Optional
import threading


class ScoreManager:
    """
    Singleton class for managing global score tracking.
    
    Provides centralized score management across all quiz sessions
    with thread-safe operations.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure only one instance of ScoreManager exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ScoreManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the score manager (only once)."""
        if not hasattr(self, '_initialized'):
            self._scores: Dict[str, int] = {}
            self._quiz_history: Dict[str, List[Dict]] = {}
            self._lock = threading.Lock()
            self._initialized = True
    
    def add_score(self, user_name: str, score: int) -> None:
        """
        Add or update a user's score.
        
        Args:
            user_name (str): Name of the user
            score (int): Score to add/update
        """
        with self._lock:
            if user_name in self._scores:
                self._scores[user_name] += score
            else:
                self._scores[user_name] = score
    
    def get_user_score(self, user_name: str) -> int:
        """
        Get a user's current score.
        
        Args:
            user_name (str): Name of the user
            
        Returns:
            int: User's current score, 0 if not found
        """
        with self._lock:
            return self._scores.get(user_name, 0)
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top scores sorted by highest first, then by name for ties.
        
        Args:
            limit (int): Maximum number of scores to return
            
        Returns:
            List[Tuple[str, int]]: List of (user_name, score) tuples
        """
        with self._lock:
            sorted_scores = sorted(self._scores.items(), key=lambda x: (-x[1], x[0]))
            return sorted_scores[:limit]
    
    def add_quiz_result(self, user_name: str, quiz_data: Dict) -> None:
        """
        Add a quiz result to user's history.
        
        Args:
            user_name (str): Name of the user
            quiz_data (Dict): Quiz result data
        """
        with self._lock:
            if user_name not in self._quiz_history:
                self._quiz_history[user_name] = []
            self._quiz_history[user_name].append(quiz_data)
    
    def get_user_history(self, user_name: str) -> List[Dict]:
        """
        Get a user's quiz history.
        
        Args:
            user_name (str): Name of the user
            
        Returns:
            List[Dict]: List of quiz results
        """
        with self._lock:
            return self._quiz_history.get(user_name, [])
    
    def reset_scores(self) -> None:
        """Reset all scores and history."""
        with self._lock:
            self._scores.clear()
            self._quiz_history.clear()
    
    def get_total_users(self) -> int:
        """
        Get the total number of users with scores.
        
        Returns:
            int: Number of users
        """
        with self._lock:
            return len(self._scores)
    
    def get_average_score(self) -> float:
        """
        Get the average score across all users.
        
        Returns:
            float: Average score, 0.0 if no users
        """
        with self._lock:
            if not self._scores:
                return 0.0
            return sum(self._scores.values()) / len(self._scores)


class TimerManager:
    """
    Singleton class for managing global timer instances.
    
    Provides centralized timer management for coordinating
    multiple timers across the application.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure only one instance of TimerManager exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(TimerManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the timer manager (only once)."""
        if not hasattr(self, '_initialized'):
            self._timers: Dict[str, 'Timer'] = {}
            self._lock = threading.Lock()
            self._initialized = True
    
    def create_timer(self, timer_id: str, duration: int) -> 'Timer':
        """
        Create a new timer with the given ID and duration.
        
        Args:
            timer_id (str): Unique identifier for the timer
            duration (int): Timer duration in seconds
            
        Returns:
            Timer: Created timer instance
        """
        try:
            from utils.timer import Timer
            
            with self._lock:
                if timer_id in self._timers:
                    print(f"Timer {timer_id} already exists, returning existing timer")
                    return self._timers[timer_id]
                
                timer = Timer(duration)
                self._timers[timer_id] = timer
                print(f"Created timer {timer_id} with duration {duration}s")
                return timer
        except Exception as e:
            print(f"Error creating timer: {e}")
            raise
    
    def get_timer(self, timer_id: str) -> Optional['Timer']:
        """
        Get a timer by ID.
        
        Args:
            timer_id (str): Timer identifier
            
        Returns:
            Optional[Timer]: Timer instance or None if not found
        """
        try:
            with self._lock:
                return self._timers.get(timer_id)
        except Exception as e:
            print(f"Error getting timer: {e}")
            return None
    
    def stop_timer(self, timer_id: str) -> bool:
        """
        Stop a timer by ID.
        
        Args:
            timer_id (str): Timer identifier
            
        Returns:
            bool: True if timer was stopped, False if not found
        """
        try:
            with self._lock:
                timer = self._timers.get(timer_id)
                if timer:
                    timer.stop()
                    print(f"Stopped timer {timer_id}")
                    return True
                else:
                    print(f"Timer {timer_id} not found")
                    return False
        except Exception as e:
            print(f"Error stopping timer: {e}")
            return False
    
    def stop_all_timers(self) -> None:
        """Stop all active timers."""
        try:
            with self._lock:
                for timer_id, timer in self._timers.items():
                    timer.stop()
                print("Stopped all timers")
        except Exception as e:
            print(f"Error stopping all timers: {e}")
    
    def remove_timer(self, timer_id: str) -> bool:
        """
        Remove a timer from the manager.
        
        Args:
            timer_id (str): Timer identifier
            
        Returns:
            bool: True if timer was removed, False if not found
        """
        try:
            with self._lock:
                if timer_id in self._timers:
                    timer = self._timers[timer_id]
                    timer.stop()
                    del self._timers[timer_id]
                    print(f"Removed timer {timer_id}")
                    return True
                else:
                    print(f"Timer {timer_id} not found")
                    return False
        except Exception as e:
            print(f"Error removing timer: {e}")
            return False
    
    def get_active_timers(self) -> List[str]:
        """
        Get list of active timer IDs.
        
        Returns:
            List[str]: List of active timer IDs
        """
        try:
            with self._lock:
                active_timers = []
                for timer_id, timer in self._timers.items():
                    if timer.is_running:
                        active_timers.append(timer_id)
                return active_timers
        except Exception as e:
            print(f"Error getting active timers: {e}")
            return []
    
    def get_timer_count(self) -> int:
        """
        Get the total number of timers.
        
        Returns:
            int: Number of timers
        """
        try:
            with self._lock:
                return len(self._timers)
        except Exception as e:
            print(f"Error getting timer count: {e}")
            return 0
    
    def clear_all_timers(self) -> None:
        """Clear all timers from the manager."""
        try:
            with self._lock:
                for timer in self._timers.values():
                    timer.stop()
                self._timers.clear()
                print("Cleared all timers")
        except Exception as e:
            print(f"Error clearing timers: {e}")
