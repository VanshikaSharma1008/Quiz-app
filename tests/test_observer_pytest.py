"""
Pytest-style unit tests for the Observer pattern module.

This module contains comprehensive unit tests for the Subject and Observer classes,
including attachment, detachment, notification, and specific observer implementations.
"""

import pytest
from unittest.mock import Mock, patch
from patterns.observer import Subject, Observer
from quiz.observer import ScoreObserver, TimeObserver, QuizCompletionObserver


class TestSubject:
    """Test cases for Subject class using pytest."""
    
    @pytest.fixture
    def subject(self):
        """Create a subject fixture for testing."""
        return Subject()
    
    @pytest.fixture
    def mock_observer(self):
        """Create a mock observer for testing."""
        return Mock(spec=Observer)
    
    def test_subject_creation(self, subject):
        """Test that subject is created with empty observers list."""
        assert hasattr(subject, '_observers')
        assert len(subject._observers) == 0
    
    def test_attach_observer(self, subject, mock_observer):
        """Test that observers can be attached to subject."""
        subject.attach(mock_observer)
        assert mock_observer in subject._observers
        assert len(subject._observers) == 1
    
    def test_attach_multiple_observers(self, subject):
        """Test that multiple observers can be attached."""
        observer1 = Mock(spec=Observer)
        observer2 = Mock(spec=Observer)
        observer3 = Mock(spec=Observer)
        
        subject.attach(observer1)
        subject.attach(observer2)
        subject.attach(observer3)
        
        assert len(subject._observers) == 3
        assert observer1 in subject._observers
        assert observer2 in subject._observers
        assert observer3 in subject._observers
    
    def test_attach_same_observer_twice(self, subject, mock_observer):
        """Test that attaching the same observer twice doesn't duplicate it."""
        subject.attach(mock_observer)
        subject.attach(mock_observer)
        
        assert len(subject._observers) == 1
        assert mock_observer in subject._observers
    
    def test_detach_observer(self, subject, mock_observer):
        """Test that observers can be detached from subject."""
        subject.attach(mock_observer)
        subject.detach(mock_observer)
        
        assert mock_observer not in subject._observers
        assert len(subject._observers) == 0
    
    def test_detach_nonexistent_observer(self, subject, mock_observer):
        """Test that detaching non-existent observer doesn't cause issues."""
        subject.detach(mock_observer)  # Should not raise any exceptions
        assert len(subject._observers) == 0
    
    def test_notify_observers(self, subject, mock_observer):
        """Test that all observers are notified with data."""
        subject.attach(mock_observer)
        test_data = {"message": "test", "value": 42}
        
        subject.notify(test_data)
        
        mock_observer.update.assert_called_once_with(subject, test_data)
    
    def test_notify_multiple_observers(self, subject):
        """Test that multiple observers are notified."""
        observer1 = Mock(spec=Observer)
        observer2 = Mock(spec=Observer)
        observer3 = Mock(spec=Observer)
        
        subject.attach(observer1)
        subject.attach(observer2)
        subject.attach(observer3)
        
        test_data = {"message": "test"}
        subject.notify(test_data)
        
        observer1.update.assert_called_once_with(subject, test_data)
        observer2.update.assert_called_once_with(subject, test_data)
        observer3.update.assert_called_once_with(subject, test_data)
    
    def test_notify_no_observers(self, subject):
        """Test that notify works when no observers are attached."""
        test_data = {"message": "test"}
        subject.notify(test_data)  # Should not raise any exceptions
    
    def test_notify_with_none_data(self, subject, mock_observer):
        """Test that notify works with None data."""
        subject.attach(mock_observer)
        subject.notify(None)
        
        mock_observer.update.assert_called_once_with(subject, None)
    
    def test_clear_observers(self, subject):
        """Test that all observers can be cleared."""
        observer1 = Mock(spec=Observer)
        observer2 = Mock(spec=Observer)
        
        subject.attach(observer1)
        subject.attach(observer2)
        assert len(subject._observers) == 2
        
        subject._observers.clear()
        assert len(subject._observers) == 0
    
    def test_observer_count(self, subject):
        """Test getting observer count."""
        assert len(subject._observers) == 0
        
        observer1 = Mock(spec=Observer)
        observer2 = Mock(spec=Observer)
        
        subject.attach(observer1)
        assert len(subject._observers) == 1
        
        subject.attach(observer2)
        assert len(subject._observers) == 2
        
        subject.detach(observer1)
        assert len(subject._observers) == 1


class TestObserver:
    """Test cases for Observer base class using pytest."""
    
    def test_observer_is_abstract(self):
        """Test that Observer is an abstract base class."""
        # Should not be able to instantiate Observer directly
        with pytest.raises(TypeError):
            Observer()
    
    def test_observer_has_update_method(self):
        """Test that Observer has update method signature."""
        # Create a concrete observer class for testing
        class ConcreteObserver(Observer):
            def update(self, subject, data=None):
                pass
        
        observer = ConcreteObserver()
        assert hasattr(observer, 'update')
        assert callable(observer.update)


class TestScoreObserver:
    """Test cases for ScoreObserver class using pytest."""
    
    @pytest.fixture
    def score_observer(self):
        """Create a score observer fixture for testing."""
        return ScoreObserver()
    
    @pytest.fixture
    def mock_subject(self):
        """Create a mock subject for testing."""
        return Mock()
    
    def test_score_observer_creation(self, score_observer):
        """Test that score observer is created correctly."""
        assert isinstance(score_observer, Observer)
        assert isinstance(score_observer, ScoreObserver)
    
    def test_score_observer_update_correct_answer(self, score_observer, mock_subject):
        """Test score observer response to correct answer."""
        data = {
            'type': 'answer_submitted',
            'correct': True,
            'points': 10,
            'current_score': 15
        }
        
        # Mock print to capture output
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, data)
            
            # Check that correct message was printed
            mock_print.assert_called_with("[ScoreObserver] Correct answer! +10 points")
    
    def test_score_observer_update_incorrect_answer(self, score_observer, mock_subject):
        """Test score observer response to incorrect answer."""
        data = {
            'type': 'answer_submitted',
            'correct': False,
            'points': 0,
            'current_score': 5
        }
        
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, data)
            
            mock_print.assert_called_with("[ScoreObserver] Incorrect answer. +0 points")
    
    def test_score_observer_update_score_display(self, score_observer, mock_subject):
        """Test score observer displays current score."""
        data = {
            'type': 'answer_submitted',
            'correct': True,
            'points': 10,
            'current_score': 25
        }
        
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, data)
            
            # Should print both correct answer and current score
            calls = mock_print.call_args_list
            score_call = [call for call in calls if "Current score: 25" in str(call)]
            assert len(score_call) > 0
    
    def test_score_observer_ignores_non_answer_events(self, score_observer, mock_subject):
        """Test score observer ignores non-answer events."""
        data = {
            'type': 'quiz_started',
            'user': 'TestUser'
        }
        
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, data)
            
            # Should not print anything for non-answer events
            mock_print.assert_not_called()
    
    def test_score_observer_handles_missing_data(self, score_observer, mock_subject):
        """Test score observer handles missing or invalid data."""
        # Test with None data
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, None)
            mock_print.assert_not_called()
        
        # Test with empty dict
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, {})
            mock_print.assert_not_called()
        
        # Test with missing type
        with patch('builtins.print') as mock_print:
            score_observer.update(mock_subject, {'correct': True})
            mock_print.assert_not_called()


class TestTimeObserver:
    """Test cases for TimeObserver class using pytest."""
    
    @pytest.fixture
    def time_observer(self):
        """Create a time observer fixture for testing."""
        return TimeObserver()
    
    @pytest.fixture
    def mock_subject(self):
        """Create a mock subject for testing."""
        return Mock()
    
    def test_time_observer_creation(self, time_observer):
        """Test that time observer is created correctly."""
        assert isinstance(time_observer, Observer)
        assert isinstance(time_observer, TimeObserver)
    
    def test_time_observer_update_quiz_started(self, time_observer, mock_subject):
        """Test time observer response to quiz start."""
        data = {
            'type': 'quiz_started',
            'duration': 300
        }
        
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, data)
            
            mock_print.assert_called_with("[TimeObserver] Quiz started with 300 seconds")
    
    def test_time_observer_update_question_change(self, time_observer, mock_subject):
        """Test time observer response to question change."""
        data = {
            'type': 'question_change',
            'question_number': 3,
            'total_questions': 5
        }
        
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, data)
            
            mock_print.assert_called_with("[TimeObserver] Question 3/5")
    
    def test_time_observer_update_time_expired(self, time_observer, mock_subject):
        """Test time observer response to time expiration."""
        data = {
            'type': 'time_expired',
            'remaining_time': 0
        }
        
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, data)
            
            mock_print.assert_called_with("[TimeObserver] Time expired!")
    
    def test_time_observer_ignores_other_events(self, time_observer, mock_subject):
        """Test time observer ignores non-time related events."""
        data = {
            'type': 'answer_submitted',
            'correct': True
        }
        
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, data)
            
            mock_print.assert_not_called()
    
    def test_time_observer_handles_missing_data(self, time_observer, mock_subject):
        """Test time observer handles missing or invalid data."""
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, None)
            mock_print.assert_not_called()
        
        with patch('builtins.print') as mock_print:
            time_observer.update(mock_subject, {})
            mock_print.assert_not_called()


class TestQuizCompletionObserver:
    """Test cases for QuizCompletionObserver class using pytest."""
    
    @pytest.fixture
    def completion_observer(self):
        """Create a completion observer fixture for testing."""
        return QuizCompletionObserver()
    
    @pytest.fixture
    def mock_subject(self):
        """Create a mock subject for testing."""
        return Mock()
    
    def test_completion_observer_creation(self, completion_observer):
        """Test that completion observer is created correctly."""
        assert isinstance(completion_observer, Observer)
        assert isinstance(completion_observer, QuizCompletionObserver)
    
    def test_completion_observer_update_quiz_complete(self, completion_observer, mock_subject):
        """Test completion observer response to quiz completion."""
        data = {
            'type': 'quiz_complete',
            'results': {
                'final_score': 85,
                'total_questions': 10,
                'answered_questions': 10,
                'elapsed_time': 120.5
            }
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            # Should print completion message
            calls = mock_print.call_args_list
            completion_calls = [call for call in calls if "Quiz completed!" in str(call)]
            assert len(completion_calls) > 0
    
    def test_completion_observer_display_final_score(self, completion_observer, mock_subject):
        """Test completion observer displays final score."""
        data = {
            'type': 'quiz_complete',
            'results': {
                'final_score': 75,
                'total_questions': 8,
                'answered_questions': 8,
                'elapsed_time': 95.2
            }
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            calls = mock_print.call_args_list
            score_calls = [call for call in calls if "Final score: 75" in str(call)]
            assert len(score_calls) > 0
    
    def test_completion_observer_display_time_taken(self, completion_observer, mock_subject):
        """Test completion observer displays time taken."""
        data = {
            'type': 'quiz_complete',
            'results': {
                'final_score': 60,
                'total_questions': 5,
                'answered_questions': 5,
                'elapsed_time': 180.0
            }
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            calls = mock_print.call_args_list
            time_calls = [call for call in calls if "Time taken: 180.0 seconds" in str(call)]
            assert len(time_calls) > 0
    
    def test_completion_observer_ignores_non_completion_events(self, completion_observer, mock_subject):
        """Test completion observer ignores non-completion events."""
        data = {
            'type': 'answer_submitted',
            'correct': True
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            mock_print.assert_not_called()
    
    def test_completion_observer_handles_missing_results(self, completion_observer, mock_subject):
        """Test completion observer handles missing results data."""
        data = {
            'type': 'quiz_complete'
            # Missing 'results' key
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            # Should handle gracefully without printing
            mock_print.assert_not_called()
    
    def test_completion_observer_handles_incomplete_results(self, completion_observer, mock_subject):
        """Test completion observer handles incomplete results data."""
        data = {
            'type': 'quiz_complete',
            'results': {
                'final_score': 50
                # Missing other fields
            }
        }
        
        with patch('builtins.print') as mock_print:
            completion_observer.update(mock_subject, data)
            
            # Should still print completion message
            calls = mock_print.call_args_list
            completion_calls = [call for call in calls if "Quiz completed!" in str(call)]
            assert len(completion_calls) > 0


class TestObserverIntegration:
    """Integration tests for observer pattern."""
    
    def test_multiple_observers_on_same_subject(self):
        """Test that multiple observers can be attached to the same subject."""
        subject = Subject()
        score_observer = ScoreObserver()
        time_observer = TimeObserver()
        completion_observer = QuizCompletionObserver()
        
        # Attach all observers
        subject.attach(score_observer)
        subject.attach(time_observer)
        subject.attach(completion_observer)
        
        assert len(subject._observers) == 3
        
        # Test notification
        data = {
            'type': 'answer_submitted',
            'correct': True,
            'points': 10,
            'current_score': 20
        }
        
        with patch('builtins.print') as mock_print:
            subject.notify(data)
            
            # Score observer should respond
            score_calls = [call for call in mock_print.call_args_list if "ScoreObserver" in str(call)]
            assert len(score_calls) > 0
    
    def test_observer_detachment_works(self):
        """Test that observers can be detached and stop receiving notifications."""
        subject = Subject()
        score_observer = ScoreObserver()
        
        subject.attach(score_observer)
        assert len(subject._observers) == 1
        
        subject.detach(score_observer)
        assert len(subject._observers) == 0
        
        # Should not receive notifications after detachment
        data = {'type': 'answer_submitted', 'correct': True}
        with patch('builtins.print') as mock_print:
            subject.notify(data)
            mock_print.assert_not_called()
    
    def test_observer_pattern_with_real_data(self):
        """Test observer pattern with realistic quiz data."""
        subject = Subject()
        score_observer = ScoreObserver()
        time_observer = TimeObserver()
        
        subject.attach(score_observer)
        subject.attach(time_observer)
        
        # Simulate quiz events
        events = [
            {'type': 'quiz_started', 'duration': 300},
            {'type': 'question_change', 'question_number': 2, 'total_questions': 5},
            {'type': 'answer_submitted', 'correct': True, 'points': 10, 'current_score': 15},
            {'type': 'answer_submitted', 'correct': False, 'points': 0, 'current_score': 15}
        ]
        
        with patch('builtins.print') as mock_print:
            for event in events:
                subject.notify(event)
            
            # Should have received multiple notifications
            assert mock_print.call_count > 0
            
            # Check specific observer responses
            score_calls = [call for call in mock_print.call_args_list if "ScoreObserver" in str(call)]
            time_calls = [call for call in mock_print.call_args_list if "TimeObserver" in str(call)]
            
            assert len(score_calls) > 0
            assert len(time_calls) > 0 