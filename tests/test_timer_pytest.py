"""
Pytest-style unit tests for the Timer utility module.

This module contains comprehensive unit tests for the Timer class,
including timer functionality, observer notifications, and edge cases.
"""

import pytest
import time
from unittest.mock import Mock, patch
from utils.timer import Timer
from patterns.observer import Observer


class TestTimer:
    """Test cases for Timer class using pytest."""
    
    @pytest.fixture
    def timer(self):
        """Create a timer fixture for testing."""
        return Timer(duration=5)
    
    @pytest.fixture
    def mock_observer(self):
        """Create a mock observer for testing notifications."""
        return Mock(spec=Observer)
    
    def test_timer_creation(self, timer):
        """Test that timer is created with correct initial state."""
        assert timer.duration == 5
        assert timer.remaining_time == 5
        assert timer.is_running is False
        assert timer.is_expired is False
        assert timer.start_time is None
        assert timer.end_time is None
    
    def test_timer_start(self, timer):
        """Test that timer starts correctly."""
        timer.start()
        
        assert timer.is_running is True
        assert timer.is_expired is False
        assert timer.start_time is not None
        assert timer.end_time is not None
        assert timer.end_time > timer.start_time
    
    def test_timer_start_already_running(self, timer):
        """Test that starting an already running timer doesn't cause issues."""
        timer.start()
        initial_start_time = timer.start_time
        
        timer.start()  # Try to start again
        
        assert timer.is_running is True
        assert timer.start_time == initial_start_time  # Should not change
    
    def test_timer_stop(self, timer):
        """Test that timer stops correctly."""
        timer.start()
        timer.stop()
        
        assert timer.is_running is False
        assert timer._stop_event.is_set()
    
    def test_timer_stop_not_running(self, timer):
        """Test that stopping a non-running timer doesn't cause issues."""
        timer.stop()  # Should not raise any exceptions
        assert timer.is_running is False
    
    def test_timer_pause_resume(self, timer):
        """Test pause and resume functionality."""
        timer.start()
        assert timer.is_running is True
        
        timer.pause()
        assert timer.is_running is False
        
        timer.resume()
        assert timer.is_running is True
    
    def test_timer_resume_when_expired(self, timer):
        """Test that resuming an expired timer doesn't work."""
        timer.start()
        timer.is_expired = True
        timer.is_running = False
        
        timer.resume()
        assert timer.is_running is False  # Should not resume when expired
    
    def test_get_remaining_time_running(self, timer):
        """Test getting remaining time for running timer."""
        timer.start()
        remaining = timer.get_remaining_time()
        
        assert isinstance(remaining, int)
        assert 0 <= remaining <= 5
        assert remaining == timer.remaining_time
    
    def test_get_remaining_time_stopped(self, timer):
        """Test getting remaining time for stopped timer."""
        remaining = timer.get_remaining_time()
        assert remaining == 0
    
    def test_get_remaining_time_expired(self, timer):
        """Test getting remaining time for expired timer."""
        timer.start()
        timer.is_expired = True
        timer.is_running = False
        
        remaining = timer.get_remaining_time()
        assert remaining == 0
    
    def test_get_elapsed_time(self, timer):
        """Test getting elapsed time."""
        timer.start()
        time.sleep(0.1)  # Small delay
        
        elapsed = timer.get_elapsed_time()
        assert isinstance(elapsed, int)
        assert elapsed >= 0
    
    def test_get_elapsed_time_not_started(self, timer):
        """Test getting elapsed time for timer that hasn't started."""
        elapsed = timer.get_elapsed_time()
        assert elapsed == 0
    
    def test_is_time_expired_running(self, timer):
        """Test time expiration check for running timer."""
        timer.start()
        assert timer.is_time_expired() is False
    
    def test_is_time_expired_stopped(self, timer):
        """Test time expiration check for stopped timer."""
        assert timer.is_time_expired() is False
    
    def test_is_time_expired_expired(self, timer):
        """Test time expiration check for expired timer."""
        timer.is_expired = True
        assert timer.is_time_expired() is True
    
    def test_is_time_up_alias(self, timer):
        """Test that is_time_up() is an alias for is_time_expired()."""
        timer.start()
        assert timer.is_time_up() == timer.is_time_expired()
        
        timer.is_expired = True
        assert timer.is_time_up() == timer.is_time_expired()
    
    def test_timer_expiration_after_duration(self):
        """Test that timer expires after the specified duration."""
        short_timer = Timer(duration=1)
        short_timer.start()
        
        # Wait for timer to expire
        time.sleep(1.1)
        
        assert short_timer.is_time_expired() is True
        assert short_timer.get_remaining_time() == 0
        assert short_timer.is_running is False
    
    def test_timer_reset(self, timer):
        """Test timer reset functionality."""
        timer.start()
        time.sleep(0.1)
        
        timer.reset(new_duration=10)
        
        assert timer.duration == 10
        assert timer.remaining_time == 10
        assert timer.is_running is False
        assert timer.is_expired is False
        assert timer.start_time is None
        assert timer.end_time is None
    
    def test_timer_reset_without_new_duration(self, timer):
        """Test timer reset without specifying new duration."""
        original_duration = timer.duration
        timer.start()
        timer.reset()
        
        assert timer.duration == original_duration
        assert timer.is_running is False
        assert timer.is_expired is False
    
    def test_observer_attachment(self, timer, mock_observer):
        """Test that observers can be attached to timer."""
        timer.attach(mock_observer)
        assert mock_observer in timer._observers
    
    def test_observer_detachment(self, timer, mock_observer):
        """Test that observers can be detached from timer."""
        timer.attach(mock_observer)
        timer.detach(mock_observer)
        assert mock_observer not in timer._observers
    
    def test_observer_notification_on_start(self, timer, mock_observer):
        """Test that observers are notified when timer starts."""
        timer.attach(mock_observer)
        timer.start()
        
        # Observer should be notified during countdown
        time.sleep(0.1)
        assert mock_observer.update.called
    
    def test_observer_notification_on_expiration(self, timer, mock_observer):
        """Test that observers are notified when timer expires."""
        timer.attach(mock_observer)
        timer.start()
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Check that observer was notified of expiration
        calls = mock_observer.update.call_args_list
        expiration_notifications = [
            call for call in calls 
            if call[1] and isinstance(call[1], dict) and call[1].get('time_expired')
        ]
        assert len(expiration_notifications) > 0
    
    def test_multiple_observers(self, timer):
        """Test that multiple observers can be attached and notified."""
        observer1 = Mock(spec=Observer)
        observer2 = Mock(spec=Observer)
        
        timer.attach(observer1)
        timer.attach(observer2)
        timer.start()
        
        time.sleep(0.1)
        
        assert observer1.update.called
        assert observer2.update.called
    
    def test_timer_string_representation(self, timer):
        """Test timer string representation."""
        timer_str = str(timer)
        assert "Timer" in timer_str
        assert "duration=5" in timer_str
        assert "status=stopped" in timer_str
    
    def test_timer_string_representation_running(self, timer):
        """Test timer string representation when running."""
        timer.start()
        timer_str = str(timer)
        assert "status=running" in timer_str
    
    @patch('time.time')
    def test_timer_with_mocked_time(self, mock_time, timer):
        """Test timer behavior with mocked time."""
        mock_time.return_value = 100.0
        timer.start()
        
        mock_time.return_value = 105.0  # 5 seconds later
        remaining = timer.get_remaining_time()
        assert remaining == 0
        assert timer.is_time_expired() is True
    
    def test_timer_thread_safety(self):
        """Test that timer operations are thread-safe."""
        timer = Timer(duration=2)
        timer.start()
        
        # Simulate concurrent access
        import threading
        
        def check_remaining():
            return timer.get_remaining_time()
        
        threads = [threading.Thread(target=check_remaining) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should not raise any exceptions
        assert timer.is_running is True
    
    def test_timer_edge_cases(self, timer):
        """Test timer edge cases."""
        # Test with zero duration
        zero_timer = Timer(duration=0)
        zero_timer.start()
        assert zero_timer.is_time_expired() is True
        
        # Test with negative duration (should handle gracefully)
        negative_timer = Timer(duration=-1)
        negative_timer.start()
        assert negative_timer.get_remaining_time() == 0 