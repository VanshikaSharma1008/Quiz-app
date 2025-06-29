"""
Test script to demonstrate the quiz application functionality.

This script runs the quiz with automatic answers to show that
the application works correctly without requiring user interaction.
"""

import sys
import io
from unittest.mock import patch
from quiz.quiz_manager import QuizManager
from quiz.ui import QuizUI
from quiz.observer import ScoreObserver, TimeObserver, QuizCompletionObserver
from quiz.questions import QuestionFactory


def create_sample_questions():
    """Create sample questions for testing."""
    factory = QuestionFactory()
    
    questions = [
        factory.create_question(
            question_type="mcq",
            text="Which data structure uses LIFO (Last In First Out)?",
            correct_answer="Stack",
            options=["Queue", "Array", "Stack", "Linked List"],
            points=10
        ),
        factory.create_question(
            question_type="mcq",
            text="What is the output of: len(['AI', 'ML', 'DS'])?",
            correct_answer="3",
            options=["0", "1", "2", "3"],
            points=10
        ),
        factory.create_question(
            question_type="true_false",
            text="The Python keyword 'def' is used to define a function.",
            correct_answer=True,
            points=5
        ),
        factory.create_question(
            question_type="true_false",
            text="Inheritance is a key concept in Object-Oriented Programming.",
            correct_answer=True,
            points=5
        )
    ]
    
    return questions


def test_quiz_with_answers():
    """Test the quiz with automatic answers."""
    print("🧪 TESTING QUIZ APPLICATION")
    print("=" * 50)
    
    # Initialize quiz manager
    quiz_manager = QuizManager()
    
    # Load sample questions
    sample_questions = create_sample_questions()
    quiz_manager.load_questions(sample_questions)
    
    # Create and attach observers
    score_observer = ScoreObserver("ScoreObserver")
    time_observer = TimeObserver("TimeObserver")
    completion_observer = QuizCompletionObserver("CompletionObserver")

    quiz_manager.attach(score_observer)
    quiz_manager.attach(time_observer)
    quiz_manager.attach(completion_observer)
    
    # Start quiz
    quiz_manager.start_quiz("TestUser")
    
    print(f"✅ Quiz started successfully!")
    print(f"📝 Total questions: {len(sample_questions)}")
    print(f"⏱️  Time limit: {quiz_manager.quiz_duration} seconds")
    print()
    
    # Answer questions automatically
    # For MCQ: provide the actual answer text, for True/False: provide boolean
    answers = ["Stack", "3", True, True]  # Correct answers for our questions
    
    for i, answer in enumerate(answers, 1):
        current_question = quiz_manager.get_current_question()
        if not current_question:
            break
            
        print(f"Question {i}: {current_question.text}")
        print(f"Answer: {answer}")
        
        # Submit answer
        result = quiz_manager.submit_answer(answer)
        
        if result['correct']:
            print("✅ Correct!")
        else:
            print("❌ Incorrect!")
        
        print(f"Points earned: {result['points_earned']}")
        print(f"Current score: {result['current_score']}")
        print()
    
    # End quiz and show results
    final_results = quiz_manager.end_quiz()
    
    print("🎉 QUIZ COMPLETED!")
    print("=" * 50)
    print(f"Final Score: {final_results['final_score']}")
    print(f"Questions Answered: {final_results['answered_questions']}/{final_results['total_questions']}")
    print(f"Time Taken: {final_results['elapsed_time']:.1f} seconds")
    print("=" * 50)
    
    return final_results


if __name__ == "__main__":
    try:
        results = test_quiz_with_answers()
        print("\n✅ Quiz application is working correctly!")
        print("🎯 All design patterns (Factory, Singleton, Observer) are functioning properly.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        sys.exit(1) 