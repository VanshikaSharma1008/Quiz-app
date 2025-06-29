"""
Pytest-style unit tests for the QuizManager service module.

This module contains comprehensive unit tests for the QuizManager class,
including quiz initialization, answer submission, timer integration, and observer patterns.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from services.quiz_manager import QuizManager
from models.question import Question
from models.user import User
from utils.timer import Timer
from patterns.observer import Observer


class TestQuizManager:
    """Test cases for QuizManager class using pytest."""
    
    @pytest.fixture
    def quiz_manager(self):
        """Create a quiz manager fixture for testing."""
        return QuizManager()
    
    @pytest.fixture
    def sample_questions(self):
        """Create sample questions for testing."""
        return [
            Question(
                text="What is 2+2?",
                question_type="mcq",
                options=["3", "4", "5", "6"],
                correct_answer="4",
                points=10,
                explanation="Basic arithmetic"
            ),
            Question(
                text="Is Python a programming language?",
                question_type="true_false",
                correct_answer=True,
                points=5,
                explanation="Python is indeed a programming language"
            )
        ]
    
    @pytest.fixture
    def mock_user(self):
        """Create a mock user for testing."""
        user = Mock(spec=User)
        user.name = "TestUser"
        user.current_score = 0
        user.add_points = Mock()
        user.start_new_quiz = Mock()
        user.complete_quiz = Mock()
        return user
    
    @pytest.fixture
    def mock_timer(self):
        """Create a mock timer for testing."""
        timer = Mock(spec=Timer)
        timer.get_remaining_time.return_value = 300
        timer.get_elapsed_time.return_value = 0
        timer.is_time_up.return_value = False
        timer.is_time_expired.return_value = False
        timer.start = Mock()
        timer.stop = Mock()
        timer.attach = Mock()
        return timer
    
    def test_quiz_manager_creation(self, quiz_manager):
        """Test that quiz manager is created with correct initial state."""
        assert len(quiz_manager.questions) == 0
        assert quiz_manager.current_question_index == 0
        assert quiz_manager.current_user is None
        assert quiz_manager.quiz_active is False
        assert quiz_manager.quiz_duration == 300
        assert quiz_manager.timer is None
    
    def test_load_questions(self, quiz_manager, sample_questions):
        """Test loading questions into the quiz manager."""
        quiz_manager.load_questions(sample_questions)
        
        assert len(quiz_manager.questions) == 2
        assert quiz_manager.current_question_index == 0
        assert quiz_manager.questions[0].text == "What is 2+2?"
        assert quiz_manager.questions[1].text == "Is Python a programming language?"
    
    def test_load_empty_questions_raises_error(self, quiz_manager):
        """Test that loading empty questions list raises ValueError."""
        with pytest.raises(ValueError, match="Questions list cannot be empty"):
            quiz_manager.load_questions([])
    
    @patch('services.quiz_manager.Timer')
    def test_start_quiz_initializes_timer_and_user(self, mock_timer_class, quiz_manager, sample_questions, mock_user):
        """Test that start_quiz properly initializes timer and sets user."""
        mock_timer_instance = Mock(spec=Timer)
        mock_timer_class.return_value = mock_timer_instance
        
        quiz_manager.load_questions(sample_questions)
        result = quiz_manager.start_quiz(mock_user, duration=60)
        
        # Check return value
        assert result is True
        
        # Check user initialization
        assert quiz_manager.current_user == mock_user
        assert quiz_manager.quiz_active is True
        assert quiz_manager.current_question_index == 0
        assert quiz_manager.quiz_duration == 60
        
        # Check timer initialization
        mock_timer_class.assert_called_once_with(60)
        mock_timer_instance.attach.assert_called_once_with(quiz_manager)
        mock_timer_instance.start.assert_called_once()
        
        # Check user methods called
        mock_user.start_new_quiz.assert_called_once()
    
    def test_start_quiz_no_questions_raises_error(self, quiz_manager, mock_user):
        """Test that starting quiz without questions raises ValueError."""
        with pytest.raises(ValueError, match="No questions loaded"):
            quiz_manager.start_quiz(mock_user)
    
    def test_start_quiz_no_user_raises_error(self, quiz_manager, sample_questions):
        """Test that starting quiz without user raises ValueError."""
        quiz_manager.load_questions(sample_questions)
        with pytest.raises(ValueError, match="User is required"):
            quiz_manager.start_quiz(None)
    
    def test_get_current_question(self, quiz_manager, sample_questions, mock_user):
        """Test getting the current question."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        current_question = quiz_manager.get_current_question()
        assert current_question is not None
        assert current_question.text == "What is 2+2?"
        assert current_question.question_type == "mcq"
    
    def test_get_current_question_no_questions(self, quiz_manager):
        """Test getting current question when no questions are loaded."""
        current_question = quiz_manager.get_current_question()
        assert current_question is None
    
    def test_get_current_question_index_out_of_bounds(self, quiz_manager, sample_questions, mock_user):
        """Test getting current question when index is out of bounds."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        quiz_manager.current_question_index = 10  # Out of bounds
        
        current_question = quiz_manager.get_current_question()
        assert current_question is None
    
    def test_submit_answer_correct(self, quiz_manager, sample_questions, mock_user):
        """Test submitting a correct answer."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        result = quiz_manager.submit_answer("4")
        
        # Check result
        assert result['correct'] is True
        assert result['points_earned'] == 10
        assert result['correct_answer'] == "4"
        assert result['explanation'] == "Basic arithmetic"
        assert result['current_score'] == 10
        
        # Check user score updated
        mock_user.add_points.assert_called_once_with(10)
        
        # Check question index moved
        assert quiz_manager.current_question_index == 1
    
    def test_submit_answer_incorrect(self, quiz_manager, sample_questions, mock_user):
        """Test submitting an incorrect answer."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        result = quiz_manager.submit_answer("3")
        
        # Check result
        assert result['correct'] is False
        assert result['points_earned'] == 0
        assert result['correct_answer'] == "4"
        assert result['current_score'] == 0
        
        # Check user score not updated
        mock_user.add_points.assert_not_called()
        
        # Check question index moved
        assert quiz_manager.current_question_index == 1
    
    def test_submit_answer_no_active_quiz_raises_error(self, quiz_manager):
        """Test that submitting answer without active quiz raises error."""
        with pytest.raises(ValueError, match="No active quiz"):
            quiz_manager.submit_answer("test")
    
    def test_submit_answer_no_current_question_raises_error(self, quiz_manager, mock_user):
        """Test that submitting answer without current question raises error."""
        quiz_manager.current_user = mock_user
        quiz_manager.quiz_active = True
        quiz_manager.questions = []
        
        with pytest.raises(ValueError, match="No current question"):
            quiz_manager.submit_answer("test")
    
    def test_submit_answer_time_expired(self, quiz_manager, sample_questions, mock_user):
        """Test that submitting answer when time is expired returns error."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Mock timer to be expired
        quiz_manager.timer.is_time_up.return_value = True
        
        result = quiz_manager.submit_answer("4")
        
        # Check error result
        assert result['correct'] is False
        assert result['points_earned'] == 0
        assert 'error' in result
        assert result['error'] == 'Time is up! Quiz ended.'
        
        # Check quiz is ended
        assert quiz_manager.quiz_active is False
    
    def test_next_question_moves_to_next(self, quiz_manager, sample_questions, mock_user):
        """Test that next_question moves to the next question."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        result = quiz_manager.next_question()
        
        assert result is True
        assert quiz_manager.current_question_index == 1
    
    def test_next_question_ends_quiz_on_last_question(self, quiz_manager, sample_questions, mock_user):
        """Test that next_question ends quiz when on last question."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        quiz_manager.current_question_index = 1  # Last question
        
        result = quiz_manager.next_question()
        
        assert result is False
        assert quiz_manager.quiz_active is False
    
    def test_end_quiz_returns_correct_summary(self, quiz_manager, sample_questions, mock_user):
        """Test that end_quiz returns correct summary."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        quiz_manager.submit_answer("4")  # Correct answer
        
        results = quiz_manager.end_quiz()
        
        # Check results
        assert results['total_questions'] == 2
        assert results['answered_questions'] == 1
        assert results['final_score'] == 10
        assert results['user_name'] == "TestUser"
        assert 'elapsed_time' in results
        
        # Check quiz state
        assert quiz_manager.quiz_active is False
        
        # Check user completion
        mock_user.complete_quiz.assert_called_once()
    
    def test_end_quiz_already_ended_returns_results(self, quiz_manager, sample_questions, mock_user):
        """Test that end_quiz returns results even when quiz already ended."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        quiz_manager.quiz_active = False  # Already ended
        
        results = quiz_manager.end_quiz()
        
        assert results['total_questions'] == 2
        assert results['answered_questions'] == 0
        assert results['final_score'] == 0
        assert results['user_name'] == "TestUser"
    
    def test_get_quiz_progress_active_quiz(self, quiz_manager, sample_questions, mock_user):
        """Test getting quiz progress for active quiz."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        progress = quiz_manager.get_quiz_progress()
        
        assert progress['active'] is True
        assert progress['current_question'] == 1
        assert progress['total_questions'] == 2
        assert 'remaining_time' in progress
        assert progress['current_score'] == 0
    
    def test_get_quiz_progress_inactive_quiz(self, quiz_manager):
        """Test getting quiz progress for inactive quiz."""
        progress = quiz_manager.get_quiz_progress()
        
        assert progress['active'] is False
    
    def test_get_quiz_progress_time_expired(self, quiz_manager, sample_questions, mock_user):
        """Test getting quiz progress when time is expired."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Mock timer to be expired
        quiz_manager.timer.is_time_expired.return_value = True
        
        progress = quiz_manager.get_quiz_progress()
        
        assert progress['active'] is False
        assert 'error' in progress
        assert progress['error'] == 'Time is up'
    
    def test_observer_notifications(self, quiz_manager, sample_questions, mock_user):
        """Test that observers are notified of quiz events."""
        mock_observer = Mock(spec=Observer)
        quiz_manager.attach(mock_observer)
        
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        quiz_manager.submit_answer("4")
        quiz_manager.end_quiz()
        
        # Should have received multiple notifications
        assert mock_observer.update.call_count > 0
        
        # Check specific notification types
        calls = mock_observer.update.call_args_list
        notification_types = [call[1].get('type') for call in calls if call[1] and isinstance(call[1], dict)]
        
        assert 'questions_loaded' in notification_types
        assert 'quiz_started' in notification_types
        assert 'answer_submitted' in notification_types
        assert 'quiz_complete' in notification_types
    
    def test_update_method_handles_time_expiration(self, quiz_manager, sample_questions, mock_user):
        """Test that update method handles time expiration notifications."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Simulate time expiration notification
        timer_data = {"time_expired": True}
        quiz_manager.update(quiz_manager.timer, timer_data)
        
        # Quiz should be automatically ended
        assert quiz_manager.quiz_active is False
    
    def test_update_method_ignores_non_expiration_data(self, quiz_manager, sample_questions, mock_user):
        """Test that update method ignores non-expiration data."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Simulate non-expiration notification
        timer_data = {"remaining_time": 100}
        quiz_manager.update(quiz_manager.timer, timer_data)
        
        # Quiz should still be active
        assert quiz_manager.quiz_active is True
    
    def test_error_handling_in_submit_answer(self, quiz_manager, sample_questions, mock_user):
        """Test error handling in submit_answer method."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Mock question to raise exception
        quiz_manager.questions[0].check_answer = Mock(side_effect=Exception("Test error"))
        
        result = quiz_manager.submit_answer("4")
        
        # Should return error result
        assert result['correct'] is False
        assert result['points_earned'] == 0
        assert 'error' in result
        assert 'Test error' in result['error']
    
    def test_error_handling_in_end_quiz(self, quiz_manager, sample_questions, mock_user):
        """Test error handling in end_quiz method."""
        quiz_manager.load_questions(sample_questions)
        quiz_manager.start_quiz(mock_user)
        
        # Mock timer to raise exception
        quiz_manager.timer.get_elapsed_time = Mock(side_effect=Exception("Timer error"))
        
        results = quiz_manager.end_quiz()
        
        # Should return empty results on error
        assert results == {} 