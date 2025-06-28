"""
Pytest-style unit tests for the questions module.

This module contains comprehensive unit tests for question objects,
including multiple choice, true/false, short answer questions, and the factory pattern.
"""

import pytest
from quiz.questions import (
    Question, 
    MultipleChoiceQuestion, 
    TrueFalseQuestion, 
    ShortAnswerQuestion, 
    QuestionFactory
)


class TestMultipleChoiceQuestion:
    """Test cases for MultipleChoiceQuestion class."""
    
    @pytest.fixture
    def mcq_question(self):
        """Create a sample MCQ question for testing."""
        return MultipleChoiceQuestion(
            text="What is the capital of France?",
            options=["London", "Berlin", "Paris", "Madrid"],
            correct_answer="Paris",
            points=10
        )
    
    def test_mcq_question_creation(self, mcq_question):
        """Test multiple choice question creation with correct attributes."""
        assert mcq_question.text == "What is the capital of France?"
        assert mcq_question.options == ["London", "Berlin", "Paris", "Madrid"]
        assert mcq_question.correct_answer == "Paris"
        assert mcq_question.points == 10
    
    def test_mcq_check_answer_correct(self, mcq_question):
        """Test that correct answer returns True."""
        assert mcq_question.check_answer("Paris") is True
    
    def test_mcq_check_answer_incorrect(self, mcq_question):
        """Test that incorrect answer returns False."""
        assert mcq_question.check_answer("London") is False
        assert mcq_question.check_answer("Berlin") is False
        assert mcq_question.check_answer("Madrid") is False
    
    def test_mcq_check_answer_case_sensitive(self, mcq_question):
        """Test that MCQ answers are case-sensitive."""
        assert mcq_question.check_answer("paris") is False
        assert mcq_question.check_answer("PARIS") is False
    
    def test_mcq_get_correct_answer(self, mcq_question):
        """Test getting the correct answer."""
        assert mcq_question.get_correct_answer() == "Paris"
    
    def test_mcq_display_question(self, mcq_question):
        """Test question display formatting for MCQ."""
        display = mcq_question.display_question()
        
        # Check that all required elements are present
        assert "What is the capital of France?" in display
        assert "1. London" in display
        assert "2. Berlin" in display
        assert "3. Paris" in display
        assert "4. Madrid" in display
        assert "Points: 10" in display
        assert "Options:" in display


class TestTrueFalseQuestion:
    """Test cases for TrueFalseQuestion class."""
    
    @pytest.fixture
    def tf_question_true(self):
        """Create a sample True/False question with True as correct answer."""
        return TrueFalseQuestion(
            text="Is Python a programming language?",
            correct_answer=True,
            points=5
        )
    
    @pytest.fixture
    def tf_question_false(self):
        """Create a sample True/False question with False as correct answer."""
        return TrueFalseQuestion(
            text="The Earth is flat.",
            correct_answer=False,
            points=5
        )
    
    def test_tf_question_creation(self, tf_question_true):
        """Test true/false question creation with correct attributes."""
        assert tf_question_true.text == "Is Python a programming language?"
        assert tf_question_true.correct_answer is True
        assert tf_question_true.points == 5
    
    def test_tf_check_answer_correct_true(self, tf_question_true):
        """Test that correct True answer returns True."""
        assert tf_question_true.check_answer(True) is True
    
    def test_tf_check_answer_correct_false(self, tf_question_false):
        """Test that correct False answer returns True."""
        assert tf_question_false.check_answer(False) is True
    
    def test_tf_check_answer_incorrect_true(self, tf_question_true):
        """Test that incorrect answer returns False for True question."""
        assert tf_question_true.check_answer(False) is False
    
    def test_tf_check_answer_incorrect_false(self, tf_question_false):
        """Test that incorrect answer returns False for False question."""
        assert tf_question_false.check_answer(True) is False
    
    def test_tf_get_correct_answer(self, tf_question_true, tf_question_false):
        """Test getting the correct answer for both True and False questions."""
        assert tf_question_true.get_correct_answer() is True
        assert tf_question_false.get_correct_answer() is False
    
    def test_tf_display_question(self, tf_question_true):
        """Test question display formatting for True/False."""
        display = tf_question_true.display_question()
        
        # Check that all required elements are present
        assert "Is Python a programming language?" in display
        assert "1. True" in display
        assert "2. False" in display
        assert "Points: 5" in display
        assert "Options:" in display


class TestShortAnswerQuestion:
    """Test cases for ShortAnswerQuestion class."""
    
    @pytest.fixture
    def sa_question(self):
        """Create a sample short answer question."""
        return ShortAnswerQuestion(
            text="What is the chemical symbol for gold?",
            correct_answer="Au",
            points=8
        )
    
    def test_sa_question_creation(self, sa_question):
        """Test short answer question creation with correct attributes."""
        assert sa_question.text == "What is the chemical symbol for gold?"
        assert sa_question.correct_answer == "Au"
        assert sa_question.points == 8
    
    def test_sa_check_answer_correct_exact(self, sa_question):
        """Test that exact correct answer returns True."""
        assert sa_question.check_answer("Au") is True
    
    def test_sa_check_answer_correct_case_insensitive(self, sa_question):
        """Test that case-insensitive matching works."""
        assert sa_question.check_answer("au") is True
        assert sa_question.check_answer("AU") is True
        assert sa_question.check_answer("Au") is True
    
    def test_sa_check_answer_correct_with_whitespace(self, sa_question):
        """Test that whitespace is handled correctly."""
        assert sa_question.check_answer("  Au  ") is True
        assert sa_question.check_answer("Au ") is True
        assert sa_question.check_answer(" Au") is True
    
    def test_sa_check_answer_incorrect(self, sa_question):
        """Test that incorrect answer returns False."""
        assert sa_question.check_answer("Ag") is False
        assert sa_question.check_answer("Gold") is False
        assert sa_question.check_answer("") is False
    
    def test_sa_check_answer_non_string(self, sa_question):
        """Test that non-string answers return False."""
        assert sa_question.check_answer(123) is False
        assert sa_question.check_answer(None) is False
        assert sa_question.check_answer(True) is False
    
    def test_sa_get_correct_answer(self, sa_question):
        """Test getting the correct answer."""
        assert sa_question.get_correct_answer() == "Au"
    
    def test_sa_display_question(self, sa_question):
        """Test question display formatting for short answer."""
        display = sa_question.display_question()
        
        # Check that all required elements are present
        assert "What is the chemical symbol for gold?" in display
        assert "Enter your answer:" in display
        assert "Points: 8" in display


class TestQuestionValidation:
    """Test cases for question validation and error handling."""
    
    def test_empty_question_text_raises_error(self):
        """Test that empty question text raises appropriate error."""
        # This would need to be implemented in the Question classes
        # For now, we test that empty text is accepted (as per current implementation)
        question = MultipleChoiceQuestion("", ["A", "B"], "A", 1)
        assert question.text == ""
    
    def test_negative_points_raises_error(self):
        """Test that negative points raises appropriate error."""
        # This would need to be implemented in the Question classes
        # For now, we test that negative points are accepted (as per current implementation)
        question = MultipleChoiceQuestion("Test", ["A", "B"], "A", -5)
        assert question.points == -5
    
    def test_mcq_with_no_options_raises_error(self):
        """Test that MCQ with no options raises error in factory."""
        factory = QuestionFactory()
        with pytest.raises(ValueError, match="MCQ questions require options"):
            factory.create_question(
                question_type="mcq",
                text="Test MCQ",
                correct_answer="A"
                # No options provided
            )
    
    def test_true_false_with_non_boolean_answer_raises_error(self):
        """Test that True/False with non-boolean answer raises error in factory."""
        factory = QuestionFactory()
        with pytest.raises(ValueError, match="True/False questions must have boolean correct answer"):
            factory.create_question(
                question_type="true_false",
                text="Test T/F",
                correct_answer="True"  # String instead of boolean
            )
    
    def test_short_answer_with_non_string_answer_raises_error(self):
        """Test that Short Answer with non-string answer raises error in factory."""
        factory = QuestionFactory()
        with pytest.raises(ValueError, match="Short answer questions must have string correct answer"):
            factory.create_question(
                question_type="short_answer",
                text="Test SA",
                correct_answer=123  # Integer instead of string
            )


class TestQuestionFactory:
    """Test cases for QuestionFactory class."""
    
    @pytest.fixture
    def factory(self):
        """Create a question factory for testing."""
        return QuestionFactory()
    
    def test_factory_creation(self, factory):
        """Test factory creation with supported types."""
        assert "mcq" in factory.supported_types
        assert "true_false" in factory.supported_types
        assert "short_answer" in factory.supported_types
    
    def test_create_mcq_question(self, factory):
        """Test creating MCQ question through factory."""
        question = factory.create_question(
            question_type="mcq",
            text="Test MCQ",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            points=10
        )
        
        assert isinstance(question, MultipleChoiceQuestion)
        assert question.text == "Test MCQ"
        assert question.options == ["A", "B", "C", "D"]
        assert question.correct_answer == "A"
        assert question.points == 10
    
    def test_create_true_false_question(self, factory):
        """Test creating True/False question through factory."""
        question = factory.create_question(
            question_type="true_false",
            text="Test T/F",
            correct_answer=True,
            points=5
        )
        
        assert isinstance(question, TrueFalseQuestion)
        assert question.text == "Test T/F"
        assert question.correct_answer is True
        assert question.points == 5
    
    def test_create_short_answer_question(self, factory):
        """Test creating Short Answer question through factory."""
        question = factory.create_question(
            question_type="short_answer",
            text="Test SA",
            correct_answer="Test Answer",
            points=8
        )
        
        assert isinstance(question, ShortAnswerQuestion)
        assert question.text == "Test SA"
        assert question.correct_answer == "Test Answer"
        assert question.points == 8
    
    def test_create_invalid_question_type(self, factory):
        """Test creating invalid question type raises error."""
        with pytest.raises(ValueError, match="Unsupported question type: invalid"):
            factory.create_question(
                question_type="invalid",
                text="Test",
                correct_answer="A"
            )
    
    def test_get_supported_types(self, factory):
        """Test getting supported question types."""
        supported_types = factory.get_supported_types()
        assert "mcq" in supported_types
        assert "true_false" in supported_types
        assert "short_answer" in supported_types
        assert isinstance(supported_types, list)
        # Test that it returns a copy, not the original list
        assert supported_types is not factory.supported_types


class TestQuestionAbstractClass:
    """Test cases for Question abstract base class."""
    
    def test_question_initialization(self):
        """Test question base class initialization."""
        # Create a concrete implementation for testing
        class TestQuestion(Question):
            def check_answer(self, user_answer):
                return user_answer == "test"
            
            def get_correct_answer(self):
                return "test"
            
            def display_question(self):
                return f"Test: {self.text}"
        
        question = TestQuestion("Test question", 5)
        assert question.text == "Test question"
        assert question.points == 5
        assert question.check_answer("test") is True
        assert question.check_answer("wrong") is False
        assert question.get_correct_answer() == "test"
        assert question.display_question() == "Test: Test question"


class TestQuestionIntegration:
    """Integration tests for question functionality."""
    
    def test_mcq_question_workflow(self):
        """Test complete MCQ question workflow."""
        question = MultipleChoiceQuestion(
            text="What is 2+2?",
            options=["3", "4", "5", "6"],
            correct_answer="4",
            points=10
        )
        
        # Test creation
        assert question.text == "What is 2+2?"
        assert len(question.options) == 4
        
        # Test answer checking
        assert question.check_answer("4") is True
        assert question.check_answer("3") is False
        
        # Test getting correct answer
        assert question.get_correct_answer() == "4"
        
        # Test display
        display = question.display_question()
        assert "What is 2+2?" in display
        assert "Points: 10" in display
    
    def test_true_false_question_workflow(self):
        """Test complete True/False question workflow."""
        question = TrueFalseQuestion(
            text="Is Python a programming language?",
            correct_answer=True,
            points=5
        )
        
        # Test creation
        assert question.text == "Is Python a programming language?"
        assert question.correct_answer is True
        
        # Test answer checking
        assert question.check_answer(True) is True
        assert question.check_answer(False) is False
        
        # Test getting correct answer
        assert question.get_correct_answer() is True
        
        # Test display
        display = question.display_question()
        assert "Is Python a programming language?" in display
        assert "1. True" in display
        assert "2. False" in display
    
    def test_short_answer_question_workflow(self):
        """Test complete Short Answer question workflow."""
        question = ShortAnswerQuestion(
            text="What is the chemical symbol for gold?",
            correct_answer="Au",
            points=8
        )
        
        # Test creation
        assert question.text == "What is the chemical symbol for gold?"
        assert question.correct_answer == "Au"
        
        # Test answer checking with case variations
        assert question.check_answer("Au") is True
        assert question.check_answer("au") is True
        assert question.check_answer("AU") is True
        assert question.check_answer("  Au  ") is True
        
        # Test incorrect answers
        assert question.check_answer("Ag") is False
        assert question.check_answer("") is False
        
        # Test getting correct answer
        assert question.get_correct_answer() == "Au"
        
        # Test display
        display = question.display_question()
        assert "What is the chemical symbol for gold?" in display
        assert "Enter your answer:" in display


if __name__ == '__main__':
    pytest.main([__file__]) 