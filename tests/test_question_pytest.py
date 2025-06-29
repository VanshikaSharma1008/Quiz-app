"""
Pytest-style unit tests for the Question model module.

This module contains comprehensive unit tests for the Question class,
including MCQ and True/False question functionality, answer checking, and validation.
"""

import pytest
from models.question import Question


class TestQuestion:
    """Test cases for Question class using pytest."""
    
    @pytest.fixture
    def mcq_question(self):
        """Create an MCQ question fixture for testing."""
        return Question(
            text="What is the capital of France?",
            question_type="mcq",
            options=["London", "Berlin", "Paris", "Madrid"],
            correct_answer="Paris",
            points=10,
            explanation="Paris is the capital and largest city of France."
        )
    
    @pytest.fixture
    def true_false_question(self):
        """Create a True/False question fixture for testing."""
        return Question(
            text="The Earth is flat.",
            question_type="true_false",
            correct_answer=False,
            points=5,
            explanation="The Earth is approximately spherical, not flat."
        )
    
    @pytest.fixture
    def short_answer_question(self):
        """Create a short answer question fixture for testing."""
        return Question(
            text="What is the chemical symbol for gold?",
            question_type="short_answer",
            correct_answer="Au",
            points=8,
            explanation="Au comes from the Latin word 'aurum' meaning gold."
        )
    
    def test_mcq_question_creation(self, mcq_question):
        """Test MCQ question creation with all attributes."""
        assert mcq_question.text == "What is the capital of France?"
        assert mcq_question.question_type == "mcq"
        assert mcq_question.options == ["London", "Berlin", "Paris", "Madrid"]
        assert mcq_question.correct_answer == "Paris"
        assert mcq_question.points == 10
        assert mcq_question.explanation == "Paris is the capital and largest city of France."
    
    def test_true_false_question_creation(self, true_false_question):
        """Test True/False question creation with all attributes."""
        assert true_false_question.text == "The Earth is flat."
        assert true_false_question.question_type == "true_false"
        assert true_false_question.correct_answer is False
        assert true_false_question.points == 5
        assert true_false_question.explanation == "The Earth is approximately spherical, not flat."
    
    def test_short_answer_question_creation(self, short_answer_question):
        """Test short answer question creation with all attributes."""
        assert short_answer_question.text == "What is the chemical symbol for gold?"
        assert short_answer_question.question_type == "short_answer"
        assert short_answer_question.correct_answer == "Au"
        assert short_answer_question.points == 8
        assert short_answer_question.explanation == "Au comes from the Latin word 'aurum' meaning gold."
    
    def test_mcq_check_answer_correct(self, mcq_question):
        """Test MCQ question with correct answer."""
        assert mcq_question.check_answer("Paris") is True
    
    def test_mcq_check_answer_incorrect(self, mcq_question):
        """Test MCQ question with incorrect answer."""
        assert mcq_question.check_answer("London") is False
        assert mcq_question.check_answer("Berlin") is False
        assert mcq_question.check_answer("Madrid") is False
    
    def test_mcq_check_answer_case_insensitive(self, mcq_question):
        """Test MCQ question with case-insensitive answer."""
        assert mcq_question.check_answer("paris") is True
        assert mcq_question.check_answer("PARIS") is True
        assert mcq_question.check_answer("Paris") is True
    
    def test_mcq_check_answer_whitespace_insensitive(self, mcq_question):
        """Test MCQ question with whitespace-insensitive answer."""
        assert mcq_question.check_answer("  Paris  ") is True
        assert mcq_question.check_answer("Paris ") is True
        assert mcq_question.check_answer(" Paris") is True
    
    def test_true_false_check_answer_correct(self, true_false_question):
        """Test True/False question with correct answer."""
        assert true_false_question.check_answer(False) is True
        assert true_false_question.check_answer("False") is True
        assert true_false_question.check_answer("false") is True
    
    def test_true_false_check_answer_incorrect(self, true_false_question):
        """Test True/False question with incorrect answer."""
        assert true_false_question.check_answer(True) is False
        assert true_false_question.check_answer("True") is False
        assert true_false_question.check_answer("true") is False
    
    def test_short_answer_check_answer_correct(self, short_answer_question):
        """Test short answer question with correct answer."""
        assert short_answer_question.check_answer("Au") is True
        assert short_answer_question.check_answer("au") is True
        assert short_answer_question.check_answer("AU") is True
    
    def test_short_answer_check_answer_incorrect(self, short_answer_question):
        """Test short answer question with incorrect answer."""
        assert short_answer_question.check_answer("Ag") is False
        assert short_answer_question.check_answer("Gold") is False
        assert short_answer_question.check_answer("") is False
    
    def test_get_correct_answer_mcq(self, mcq_question):
        """Test getting correct answer for MCQ question."""
        correct_answer = mcq_question.get_correct_answer()
        assert correct_answer == "Paris"
    
    def test_get_correct_answer_true_false(self, true_false_question):
        """Test getting correct answer for True/False question."""
        correct_answer = true_false_question.get_correct_answer()
        assert correct_answer is False
    
    def test_get_correct_answer_short_answer(self, short_answer_question):
        """Test getting correct answer for short answer question."""
        correct_answer = short_answer_question.get_correct_answer()
        assert correct_answer == "Au"
    
    def test_display_question_mcq(self, mcq_question):
        """Test displaying MCQ question."""
        display = mcq_question.display_question()
        
        assert "What is the capital of France?" in display
        assert "1. London" in display
        assert "2. Berlin" in display
        assert "3. Paris" in display
        assert "4. Madrid" in display
        assert "Points: 10" in display
    
    def test_display_question_true_false(self, true_false_question):
        """Test displaying True/False question."""
        display = true_false_question.display_question()
        
        assert "The Earth is flat." in display
        assert "1. True" in display
        assert "2. False" in display
        assert "Points: 5" in display
    
    def test_display_question_short_answer(self, short_answer_question):
        """Test displaying short answer question."""
        display = short_answer_question.display_question()
        
        assert "What is the chemical symbol for gold?" in display
        assert "Points: 8" in display
        assert "Options:" not in display  # Short answer shouldn't have options
    
    def test_question_validation_mcq_missing_options(self):
        """Test that MCQ question requires options."""
        with pytest.raises(ValueError, match="MCQ questions must have options"):
            Question(
                text="Test question",
                question_type="mcq",
                correct_answer="Answer",
                points=10
            )
    
    def test_question_validation_mcq_empty_options(self):
        """Test that MCQ question cannot have empty options."""
        with pytest.raises(ValueError, match="Options cannot be empty"):
            Question(
                text="Test question",
                question_type="mcq",
                options=[],
                correct_answer="Answer",
                points=10
            )
    
    def test_question_validation_mcq_correct_answer_not_in_options(self):
        """Test that MCQ correct answer must be in options."""
        with pytest.raises(ValueError, match="Correct answer must be one of the options"):
            Question(
                text="Test question",
                question_type="mcq",
                options=["A", "B", "C"],
                correct_answer="D",
                points=10
            )
    
    def test_question_validation_true_false_with_options(self):
        """Test that True/False question cannot have options."""
        with pytest.raises(ValueError, match="True/False questions should not have options"):
            Question(
                text="Test question",
                question_type="true_false",
                options=["True", "False"],
                correct_answer=True,
                points=10
            )
    
    def test_question_validation_true_false_invalid_answer(self):
        """Test that True/False question must have boolean answer."""
        with pytest.raises(ValueError, match="True/False questions must have boolean correct answer"):
            Question(
                text="Test question",
                question_type="true_false",
                correct_answer="Yes",
                points=10
            )
    
    def test_question_validation_negative_points(self):
        """Test that questions cannot have negative points."""
        with pytest.raises(ValueError, match="Points must be positive"):
            Question(
                text="Test question",
                question_type="mcq",
                options=["A", "B"],
                correct_answer="A",
                points=-5
            )
    
    def test_question_validation_zero_points(self):
        """Test that questions cannot have zero points."""
        with pytest.raises(ValueError, match="Points must be positive"):
            Question(
                text="Test question",
                question_type="mcq",
                options=["A", "B"],
                correct_answer="A",
                points=0
            )
    
    def test_question_validation_empty_text(self):
        """Test that questions cannot have empty text."""
        with pytest.raises(ValueError, match="Question text cannot be empty"):
            Question(
                text="",
                question_type="mcq",
                options=["A", "B"],
                correct_answer="A",
                points=10
            )
    
    def test_question_validation_unsupported_type(self):
        """Test that unsupported question types raise error."""
        with pytest.raises(ValueError, match="Unsupported question type"):
            Question(
                text="Test question",
                question_type="essay",
                correct_answer="Answer",
                points=10
            )
    
    def test_question_equality(self, mcq_question):
        """Test question equality comparison."""
        same_question = Question(
            text="What is the capital of France?",
            question_type="mcq",
            options=["London", "Berlin", "Paris", "Madrid"],
            correct_answer="Paris",
            points=10,
            explanation="Paris is the capital and largest city of France."
        )
        
        different_question = Question(
            text="What is the capital of Germany?",
            question_type="mcq",
            options=["London", "Berlin", "Paris", "Madrid"],
            correct_answer="Berlin",
            points=10
        )
        
        assert mcq_question == same_question
        assert mcq_question != different_question
    
    def test_question_hash(self, mcq_question):
        """Test that questions can be used in sets and as dictionary keys."""
        question_set = {mcq_question}
        question_dict = {mcq_question: "test"}
        
        assert mcq_question in question_set
        assert mcq_question in question_dict
    
    def test_question_string_representation(self, mcq_question):
        """Test question string representation."""
        question_str = str(mcq_question)
        assert "What is the capital of France?" in question_str
        assert "mcq" in question_str
        assert "10" in question_str
    
    def test_question_repr(self, mcq_question):
        """Test question repr representation."""
        question_repr = repr(mcq_question)
        assert "Question" in question_repr
        assert "What is the capital of France?" in question_repr
        assert "mcq" in question_repr
    
    def test_question_copy(self, mcq_question):
        """Test that questions can be copied."""
        import copy
        
        copied_question = copy.copy(mcq_question)
        assert copied_question == mcq_question
        assert copied_question is not mcq_question
    
    def test_question_deep_copy(self, mcq_question):
        """Test that questions can be deep copied."""
        import copy
        
        deep_copied_question = copy.deepcopy(mcq_question)
        assert deep_copied_question == mcq_question
        assert deep_copied_question is not mcq_question
        assert deep_copied_question.options is not mcq_question.options
    
    def test_question_serialization(self, mcq_question):
        """Test that questions can be serialized to dictionary."""
        question_dict = mcq_question.to_dict()
        
        assert question_dict['text'] == "What is the capital of France?"
        assert question_dict['question_type'] == "mcq"
        assert question_dict['options'] == ["London", "Berlin", "Paris", "Madrid"]
        assert question_dict['correct_answer'] == "Paris"
        assert question_dict['points'] == 10
        assert question_dict['explanation'] == "Paris is the capital and largest city of France."
    
    def test_question_deserialization(self):
        """Test that questions can be created from dictionary."""
        question_dict = {
            'text': 'Test question',
            'question_type': 'mcq',
            'options': ['A', 'B'],
            'correct_answer': 'A',
            'points': 5,
            'explanation': 'Test explanation'
        }
        
        question = Question.from_dict(question_dict)
        
        assert question.text == 'Test question'
        assert question.question_type == 'mcq'
        assert question.options == ['A', 'B']
        assert question.correct_answer == 'A'
        assert question.points == 5
        assert question.explanation == 'Test explanation' 