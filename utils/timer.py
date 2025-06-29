"""
Timer utility for quiz application.

This module provides a Timer class for managing quiz timing,
including countdown functionality and time expiration detection.
"""

import time
import threading
from typing import Optional, Callable
from patterns.observer import Subject


class Timer(Subject):
    """
    Timer utility for quiz timing functionality.
    
    Provides countdown timer with observer notifications
    for time updates and expiration events.
    """
    
    def __init__(self, duration: int):
        """
        Initialize the timer.
        
        Args:
            duration (int): Timer duration in seconds
        """
        super().__init__()
        self.duration = duration
        self.remaining_time = duration
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.is_running = False
        self.is_expired = False
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
    
    def start(self) -> None:
        """Start the timer countdown."""
        try:
            if self.is_running:
                print("Timer is already running")
                return
            
            self.start_time = time.time()
            self.end_time = self.start_time + self.duration
            self.is_running = True
            self.is_expired = False
            self._stop_event.clear()
            
            # Start timer thread
            self._timer_thread = threading.Thread(target=self._countdown)
            self._timer_thread.daemon = True
            self._timer_thread.start()
            
            print(f"Timer started for {self.duration} seconds")
        except Exception as e:
            print(f"Error starting timer: {e}")
    
    def stop(self) -> None:
        """Stop the timer."""
        try:
            if not self.is_running:
                return
            
            self.is_running = False
            self._stop_event.set()
            
            if self._timer_thread and self._timer_thread.is_alive():
                self._timer_thread.join(timeout=1.0)
            
            print("Timer stopped")
        except Exception as e:
            print(f"Error stopping timer: {e}")
    
    def pause(self) -> None:
        """Pause the timer."""
        try:
            if not self.is_running:
                return
            
            self.is_running = False
            print("Timer paused")
        except Exception as e:
            print(f"Error pausing timer: {e}")
    
    def resume(self) -> None:
        """Resume the timer."""
        try:
            if self.is_running or self.is_expired:
                return
            
            self.is_running = True
            print("Timer resumed")
        except Exception as e:
            print(f"Error resuming timer: {e}")
    
    def get_remaining_time(self) -> int:
        """
        Get the remaining time in seconds.
        
        Returns:
            int: Remaining time in seconds, 0 if expired
        """
        try:
            if not self.is_running or self.is_expired:
                return 0
            
            if self.end_time is None:
                return 0
            
            remaining = max(0, int(self.end_time - time.time()))
            self.remaining_time = remaining
            
            if remaining == 0:
                self.is_expired = True
                self.is_running = False
            
            return remaining
        except Exception as e:
            print(f"Error getting remaining time: {e}")
            return 0
    
    def get_elapsed_time(self) -> int:
        """
        Get the elapsed time in seconds.
        
        Returns:
            int: Elapsed time in seconds
        """
        try:
            if self.start_time is None:
                return 0
            
            return int(time.time() - self.start_time)
        except Exception as e:
            print(f"Error getting elapsed time: {e}")
            return 0
    
    def is_time_expired(self) -> bool:
        """
        Check if the timer has expired.
        
        Returns:
            bool: True if timer has expired, False otherwise
        """
        try:
            if self.is_expired:
                return True
            
            if not self.is_running:
                return False
            
            remaining = self.get_remaining_time()
            if remaining == 0:
                self.is_expired = True
                self.is_running = False
                return True
            
            return False
        except Exception as e:
            print(f"Error checking if time expired: {e}")
            return False
    
    def is_time_up(self) -> bool:
        """
        Check if the timer has expired (alias for is_time_expired).
        
        Returns:
            bool: True if timer has expired, False otherwise
        """
        return self.is_time_expired()
    
    def _countdown(self) -> None:
        """Internal countdown method running in separate thread."""
        try:
            while self.is_running and not self._stop_event.is_set():
                remaining = self.get_remaining_time()
                
                # Notify observers of time update
                self.notify({
                    'remaining_time': remaining,
                    'time_expired': remaining == 0
                })
                
                if remaining == 0:
                    self.is_expired = True
                    self.is_running = False
                    
                    # Notify observers of time expiration
                    self.notify({
                        'time_expired': True,
                        'remaining_time': 0
                    })
                    break
                
                time.sleep(1)  # Update every second
        except Exception as e:
            print(f"Error in timer countdown: {e}")
    
    def reset(self, new_duration: Optional[int] = None) -> None:
        """
        Reset the timer with optional new duration.
        
        Args:
            new_duration (Optional[int]): New duration in seconds
        """
        try:
            self.stop()
            
            if new_duration is not None:
                self.duration = new_duration
            
            self.remaining_time = self.duration
            self.start_time = None
            self.end_time = None
            self.is_running = False
            self.is_expired = False
            
            print(f"Timer reset with duration: {self.duration} seconds")
        except Exception as e:
            print(f"Error resetting timer: {e}")
    
    def __str__(self) -> str:
        """Return string representation of the timer."""
        status = "running" if self.is_running else "stopped"
        remaining = self.get_remaining_time()
        return f"Timer(duration={self.duration}s, remaining={remaining}s, status={status})" 