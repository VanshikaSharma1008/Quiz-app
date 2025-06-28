"""
Unit tests for quiz application.

This module contains comprehensive unit tests for the quiz logic,
including tests for questions, users, quiz manager, and utilities.
"""

import unittest
from unittest.mock import Mock, patch
from models.question import Question
from models.user import User
from services.quiz_manager import QuizManager
from utils.timer import Timer
from patterns.factory import QuestionFactory
from patterns.singleton import ScoreManager


class TestQuestion(unittest.TestCase):
    """Test cases for the Question class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcq_question = Question(
            text="What is the capital of France?",
            question_type="mcq",
            options=["London", "Berlin", "Paris", "Madrid"],
            correct_answer="Paris",
            points=10,
            explanation="Paris is the capital and largest city of France."
        )
        
        self.tf_question = Question(
            text="The Earth is flat.",
            question_type="true_false",
            correct_answer=False,
            points=5,
            explanation="The Earth is approximately spherical, not flat."
        )
    
    def test_mcq_question_creation(self):
        """Test MCQ question creation."""
        self.assertEqual(self.mcq_question.text, "What is the capital of France?")
        self.assertEqual(self.mcq_question.question_type, "mcq")
        self.assertEqual(self.mcq_question.options, ["London", "Berlin", "Paris", "Madrid"])
        self.assertEqual(self.mcq_question.correct_answer, "Paris")
        self.assertEqual(self.mcq_question.points, 10)
    
    def test_true_false_question_creation(self):
        """Test True/False question creation."""
        self.assertEqual(self.tf_question.text, "The Earth is flat.")
        self.assertEqual(self.tf_question.question_type, "true_false")
        self.assertEqual(self.tf_question.correct_answer, False)
        self.assertEqual(self.tf_question.points, 5)
    
    def test_check_answer_correct(self):
        """Test correct answer checking."""
        self.assertTrue(self.mcq_question.check_answer("Paris"))
        self.assertTrue(self.tf_question.check_answer(False))
    
    def test_check_answer_incorrect(self):
        """Test incorrect answer checking."""
        self.assertFalse(self.mcq_question.check_answer("London"))
        self.assertFalse(self.tf_question.check_answer(True))
    
    def test_get_correct_answer(self):
        """Test getting correct answer."""
        self.assertEqual(self.mcq_question.get_correct_answer(), "Paris")
        self.assertEqual(self.tf_question.get_correct_answer(), False)


class TestUser(unittest.TestCase):
    """Test cases for the User class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User("TestUser")
    
    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user.name, "TestUser")
        self.assertEqual(self.user.current_score, 0)
        self.assertEqual(self.user.total_score, 0)
        self.assertEqual(self.user.quizzes_taken, 0)
    
    def test_start_new_quiz(self):
        """Test starting a new quiz."""
        self.user.current_score = 50
        self.user.start_new_quiz()
        self.assertEqual(self.user.current_score, 0)
    
    def test_add_points(self):
        """Test adding points."""
        self.user.add_points(10)
        self.assertEqual(self.user.current_score, 10)
        
        self.user.add_points(5)
        self.assertEqual(self.user.current_score, 15)
    
    def test_add_negative_points(self):
        """Test adding negative points raises error."""
        with self.assertRaises(ValueError):
            self.user.add_points(-5)
    
    def test_complete_quiz(self):
        """Test completing a quiz."""
        self.user.current_score = 25
        self.user.complete_quiz()
        self.assertEqual(self.user.total_score, 25)
        self.assertEqual(self.user.quizzes_taken, 1)
    
    def test_get_average_score(self):
        """Test calculating average score."""
        # No quizzes taken
        self.assertEqual(self.user.get_average_score(), 0.0)
        
        # One quiz taken
        self.user.current_score = 80
        self.user.complete_quiz()
        self.assertEqual(self.user.get_average_score(), 80.0)
        
        # Multiple quizzes
        self.user.current_score = 90
        self.user.complete_quiz()
        self.assertEqual(self.user.get_average_score(), 85.0)


class TestQuizManager(unittest.TestCase):
    """Test cases for the QuizManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.quiz_manager = QuizManager()
        self.user = User("TestUser")
        
        self.questions = [
            Question(
                text="What is 2+2?",
                question_type="mcq",
                options=["3", "4", "5", "6"],
                correct_answer="4",
                points=10
            ),
            Question(
                text="Is Python a programming language?",
                question_type="true_false",
                correct_answer=True,
                points=5
            )
        ]
    
    def test_quiz_manager_creation(self):
        """Test quiz manager creation."""
        self.assertEqual(len(self.quiz_manager.questions), 0)
        self.assertEqual(self.quiz_manager.current_question_index, 0)
        self.assertIsNone(self.quiz_manager.current_user)
        self.assertFalse(self.quiz_manager.quiz_active)
    
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
        result = self.quiz_manager.start_quiz(self.user)
        
        self.assertTrue(result)
        self.assertTrue(self.quiz_manager.quiz_active)
        self.assertEqual(self.quiz_manager.current_user, self.user)
        self.assertEqual(self.quiz_manager.current_question_index, 0)
    
    def test_start_quiz_no_questions(self):
        """Test starting quiz without questions raises error."""
        with self.assertRaises(ValueError):
            self.quiz_manager.start_quiz(self.user)
    
    def test_get_current_question(self):
        """Test getting current question."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz(self.user)
        
        current_question = self.quiz_manager.get_current_question()
        self.assertEqual(current_question.text, "What is 2+2?")
    
    def test_submit_correct_answer(self):
        """Test submitting correct answer."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz(self.user)
        
        result = self.quiz_manager.submit_answer("4")
        
        self.assertTrue(result['correct'])
        self.assertEqual(result['points_earned'], 10)
        self.assertEqual(self.user.current_score, 10)
    
    def test_submit_incorrect_answer(self):
        """Test submitting incorrect answer."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz(self.user)
        
        result = self.quiz_manager.submit_answer("3")
        
        self.assertFalse(result['correct'])
        self.assertEqual(result['points_earned'], 0)
        self.assertEqual(self.user.current_score, 0)
    
    def test_end_quiz(self):
        """Test ending a quiz."""
        self.quiz_manager.load_questions(self.questions)
        self.quiz_manager.start_quiz(self.user)
        self.quiz_manager.submit_answer("4")  # Correct answer
        
        results = self.quiz_manager.end_quiz()
        
        self.assertFalse(self.quiz_manager.quiz_active)
        self.assertEqual(results['final_score'], 10)
        self.assertEqual(results['total_questions'], 2)
        self.assertEqual(results['answered_questions'], 1)


class TestTimer(unittest.TestCase):
    """Test cases for the Timer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.timer = Timer(5)  # 5 second timer
    
    def test_timer_creation(self):
        """Test timer creation."""
        self.assertEqual(self.timer.duration, 5)
        self.assertEqual(self.timer.remaining_time, 5)
        self.assertFalse(self.timer.is_running)
        self.assertFalse(self.timer.is_expired)
    
    def test_timer_start_stop(self):
        """Test timer start and stop."""
        self.timer.start()
        self.assertTrue(self.timer.is_running)
        
        self.timer.stop()
        self.assertFalse(self.timer.is_running)
    
    def test_get_remaining_time(self):
        """Test getting remaining time."""
        self.timer.start()
        remaining = self.timer.get_remaining_time()
        self.assertGreaterEqual(remaining, 0)
        self.assertLessEqual(remaining, 5)
    
    def test_timer_expiration(self):
        """Test timer expiration."""
        # Use a very short timer for testing
        short_timer = Timer(1)
        short_timer.start()
        
        # Wait for timer to expire
        import time
        time.sleep(1.1)
        
        self.assertTrue(short_timer.is_time_expired())
        self.assertEqual(short_timer.get_remaining_time(), 0)


class TestQuestionFactory(unittest.TestCase):
    """Test cases for the QuestionFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = QuestionFactory()
    
    def test_create_mcq_question(self):
        """Test creating MCQ question."""
        question = self.factory.create_question(
            question_type="mcq",
            text="Test MCQ",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            points=10
        )
        
        self.assertEqual(question.question_type, "mcq")
        self.assertEqual(question.text, "Test MCQ")
        self.assertEqual(question.options, ["A", "B", "C", "D"])
    
    def test_create_true_false_question(self):
        """Test creating True/False question."""
        question = self.factory.create_question(
            question_type="true_false",
            text="Test T/F",
            correct_answer=True,
            points=5
        )
        
        self.assertEqual(question.question_type, "true_false")
        self.assertEqual(question.text, "Test T/F")
        self.assertEqual(question.correct_answer, True)
    
    def test_create_invalid_question_type(self):
        """Test creating invalid question type raises error."""
        with self.assertRaises(ValueError):
            self.factory.create_question(
                question_type="invalid",
                text="Test",
                correct_answer="A"
            )


class TestScoreManager(unittest.TestCase):
    """Test cases for the ScoreManager singleton."""
    
    def test_singleton_instance(self):
        """Test that ScoreManager is a singleton."""
        instance1 = ScoreManager()
        instance2 = ScoreManager()
        
        self.assertIs(instance1, instance2)
    
    def test_score_tracking(self):
        """Test score tracking functionality."""
        score_manager = ScoreManager()
        score_manager.reset_scores()
        
        score_manager.add_score("user1", 100)
        score_manager.add_score("user2", 150)
        score_manager.add_score("user1", 50)
        
        self.assertEqual(score_manager.get_user_score("user1"), 150)
        self.assertEqual(score_manager.get_user_score("user2"), 150)
        
        top_scores = score_manager.get_top_scores(2)
        self.assertEqual(len(top_scores), 2)
        self.assertCountEqual(top_scores, [("user1", 150), ("user2", 150)])


if __name__ == '__main__':
    unittest.main() 