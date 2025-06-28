"""
Unit tests for the quiz manager module.

This module contains comprehensive unit tests for the QuizManager class,
including singleton pattern, quiz state management, and observer notifications.
"""

import unittest
import time
from unittest.mock import Mock, patch
from quiz.quiz_manager import QuizManager
from quiz.questions import MultipleChoiceQuestion, TrueFalseQuestion
from quiz.observer import Observer


class TestQuizManager(unittest.TestCase):
    """Test cases for QuizManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset singleton instance for each test
        QuizManager._instance = None
        self.quiz_manager = QuizManager()
        
        self.questions = [
            MultipleChoiceQuestion(
                text="What is 2+2?",
                options=["3", "4", "5", "6"],
                correct_answer="4",
                points=10
            ),
            TrueFalseQuestion(
                text="Is Python a programming language?",
                correct_answer=True,
                points=5
            )
        ]
    
    def test_singleton_pattern(self):
        """Test that QuizManager is a singleton."""
        instance1 = QuizManager()
        instance2 = QuizManager()
        self.assertIs(instance1, instance2)
    
    def test_quiz_manager_creation(self):
        """Test quiz manager creation."""
        self.assertEqual(len(self.quiz_manager.questions), 0)
        self.assertEqual(self.quiz_manager.current_question_index, 0)
        self.assertIsNone(self.quiz_manager.current_user)
        self.assertFalse(self.quiz_manager.quiz_active)
        self.assertEqual(self.quiz_manager.current_score, 0)
    
    def test_load_questions(self):
        """Test loading questions."""
        self.quiz_manager.load_questions(self.questions)
        self.assertEqual(len(self.quiz_manager.questions), 2)
        self.assertEqual(self.quiz_manager.current_question_index, 0)
    
    def test_load_empty_questions(self):
        """Test loading empty questions list raises error."""
        with self.assertRaises(ValueError):
            self.quiz_manager.load_questions([])
    
    def test_start_quiz(self):
        """Test starting a quiz."""
        self.quiz_manager.load_questions(self.questions)
        result = self.quiz_manager.start_quiz("TestUser")
        
        self.assertTrue(result)
        self.assertTrue(self.quiz_manager.quiz_active)
        self.assertEqual(self.quiz_manager.current_user, "TestUser")
        self.assertEqual(self.quiz_manager.current_question_index, 0)
        self.assertEqual(self.quiz_manager.current_score, 0)
        self.assertIsNotNone(self.quiz_manager.start_time)
    
    def test_start_quiz_no_questions(self):
        """Test starting quiz without questions raises error."""
        with self.assertRaises(ValueError):
            self.quiz_manager.start_quiz("TestUser")
    
    def test_get_current_question(self):
        """Test getting current question."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        
        current_question = self.quiz_manager.get_current_question()
        self.assertEqual(current_question.text, "What is 2+2?")
    
    def test_submit_correct_answer(self):
        """Test submitting correct answer."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        
        result = self.quiz_manager.submit_answer("4")
        
        self.assertTrue(result['correct'])
        self.assertEqual(result['points_earned'], 10)
        self.assertEqual(result['current_score'], 10)
        self.assertEqual(self.quiz_manager.current_score, 10)
    
    def test_submit_incorrect_answer(self):
        """Test submitting incorrect answer."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        
        result = self.quiz_manager.submit_answer("3")
        
        self.assertFalse(result['correct'])
        self.assertEqual(result['points_earned'], 0)
        self.assertEqual(result['current_score'], 0)
        self.assertEqual(self.quiz_manager.current_score, 0)
    
    def test_next_question(self):
        """Test moving to next question."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        
        # Submit first answer
        self.quiz_manager.submit_answer("4")
        
        # Should be on second question now
        current_question = self.quiz_manager.get_current_question()
        self.assertEqual(current_question.text, "Is Python a programming language?")
    
    def test_end_quiz(self):
        """Test ending a quiz."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        self.quiz_manager.submit_answer("4")  # Correct answer
        
        results = self.quiz_manager.end_quiz()
        
        self.assertFalse(self.quiz_manager.quiz_active)
        self.assertEqual(results['user_name'], "TestUser")
        self.assertEqual(results['final_score'], 10)
        self.assertEqual(results['total_questions'], 2)
        self.assertEqual(results['answered_questions'], 1)
        self.assertIn('elapsed_time', results)
    
    def test_get_quiz_progress(self):
        """Test getting quiz progress."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        
        progress = self.quiz_manager.get_quiz_progress()
        
        self.assertTrue(progress['active'])
        self.assertEqual(progress['current_question'], 1)
        self.assertEqual(progress['total_questions'], 2)
        self.assertIn('remaining_time', progress)
        self.assertEqual(progress['current_score'], 0)
    
    def test_get_remaining_time(self):
        """Test getting remaining time."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser", duration=60)
        
        remaining_time = self.quiz_manager.get_remaining_time()
        self.assertGreater(remaining_time, 0)
        self.assertLessEqual(remaining_time, 60)
    
    def test_is_time_expired(self):
        """Test time expiration check."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser", duration=1)
        
        # Should not be expired immediately
        self.assertFalse(self.quiz_manager.is_time_expired())
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertTrue(self.quiz_manager.is_time_expired())
    
    def test_submit_answer_no_active_quiz(self):
        """Test submitting answer without active quiz raises error."""
        with self.assertRaises(ValueError):
            self.quiz_manager.submit_answer("test")
    
    def test_end_quiz_no_active_quiz(self):
        """Test ending quiz without active quiz raises error."""
        with self.assertRaises(ValueError):
            self.quiz_manager.end_quiz()
    
    def test_observer_notifications(self):
        """Test observer notifications."""
        mock_observer = Mock(spec=Observer)
        self.quiz_manager.attach(mock_observer)
        
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz("TestUser")
        self.quiz_manager.submit_answer("4")
        self.quiz_manager.end_quiz()
        
        # Should have received multiple notifications
        self.assertGreater(mock_observer.update.call_count, 0)


class TestQuizManagerThreading(unittest.TestCase):
    """Test cases for QuizManager threading behavior."""
    
    def setUp(self):
        """Set up test fixtures."""
        QuizManager._instance = None
        self.quiz_manager = QuizManager()
    
    def test_thread_safety(self):
        """Test that QuizManager is thread-safe."""
        import threading
        
        def load_questions():
            questions = [
                MultipleChoiceQuestion("Test", ["A", "B"], "A", 1)
            ]
            self.quiz_manager.load_questions(questions)
        
        def start_quiz():
            self.quiz_manager.start_quiz("TestUser")
        
        # Create threads
        thread1 = threading.Thread(target=load_questions)
        thread2 = threading.Thread(target=start_quiz)
        
        # Start threads
        thread1.start()
        thread1.join()
        thread2.start()
        thread2.join()
        
        # Should not raise any exceptions
        self.assertTrue(self.quiz_manager.quiz_active)


if __name__ == '__main__':
    unittest.main() 