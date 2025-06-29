"""
Main entry point for the Quiz Application.

This module serves as the entry point for the quiz application,
orchestrating the initialization and execution of the quiz system.
"""

import sys
from services.quiz_manager import QuizManager
from quiz.ui import QuizUI
from quiz.observer import ScoreObserver, TimeObserver, QuizCompletionObserver
from patterns.factory import QuestionFactory
from models.user import User


def create_sample_questions():
    """
    Create sample questions for the quiz.
    
    Returns:
        List[Question]: List of sample questions
    """
    factory = QuestionFactory()
    
    questions = [
        # Multiple Choice Questions
        factory.create_question(
            question_type="mcq",
            text="Which data structure uses LIFO (Last In First Out)?",
            correct_answer="Stack",
            points=10,
            options=["Queue", "Array", "Stack", "Linked List"]
        ),
        factory.create_question(
            question_type="mcq",
            text="What is the output of: len(['AI', 'ML', 'DS'])?",
            correct_answer="3",
            points=10,
            options=["0", "1", "2", "3"]
        ),
        
        # True/False Questions
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


def main():
    """
    Main function to initialize and run the quiz application.
    
    This function sets up the quiz system, initializes the UI,
    and starts the quiz flow.
    """
    try:
        # Initialize quiz manager
        quiz_manager = QuizManager()
        
        # Load sample questions
        sample_questions = create_sample_questions()
        quiz_manager.load_questions(sample_questions)
        
        # Create and attach individual observers
        score_observer = ScoreObserver("ScoreObserver")
        time_observer = TimeObserver("TimeObserver")
        completion_observer = QuizCompletionObserver("CompletionObserver")

        quiz_manager.attach(score_observer)
        quiz_manager.attach(time_observer)
        quiz_manager.attach(completion_observer)
        
        # Initialize UI
        ui = QuizUI(quiz_manager)
        
        print("🎯 Quiz Application Ready!")
        print("📝 Questions loaded successfully")
        print("⏱️  Timer will start when quiz begins")
        print("🚀 Starting quiz...\n")
        
        # Start the quiz application
        ui.run()
        
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)
    except EOFError:
        print("\n\nInput stream closed. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again later.")
        sys.exit(1)


if __name__ == "__main__":
    main()
