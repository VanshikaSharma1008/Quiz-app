"""
Main entry point for the Quiz Application.

This module serves as the entry point for the quiz application,
orchestrating the initialization and execution of the quiz system.
"""

import sys
from quiz.quiz_manager import QuizManager
from quiz.ui import QuizUI
from quiz.observer import ScoreObserver, TimeObserver, QuizCompletionObserver


def main():
    """
    Main function to initialize and run the quiz application.
    
    This function sets up the quiz system, initializes the UI,
    and starts the quiz flow.
    """
    try:
        # Initialize quiz manager
        quiz_manager = QuizManager()
        
        # Create and attach individual observers
        score_observer = ScoreObserver("ScoreObserver")
        time_observer = TimeObserver("TimeObserver")
        completion_observer = QuizCompletionObserver("CompletionObserver")

        quiz_manager.attach(score_observer)
        quiz_manager.attach(time_observer)
        quiz_manager.attach(completion_observer)
        
        # Initialize UI
        ui = QuizUI(quiz_manager)
        
        # Start the quiz application
        ui.run()
        
    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
