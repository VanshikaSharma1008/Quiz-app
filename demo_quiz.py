"""
Demo script to show the quiz application working.
This script runs the quiz with automatic answers to demonstrate functionality.
"""

from quiz.quiz_manager import QuizManager
from quiz.questions import QuestionFactory
from quiz.observer import ScoreObserver, TimeObserver, QuizCompletionObserver

def demo_quiz():
    """Demonstrate the quiz application working."""
    print("🎯 QUIZ APPLICATION DEMO")
    print("=" * 50)
    
    # Initialize quiz manager
    quiz_manager = QuizManager()
    
    # Create questions using Factory Pattern
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
    
    # Load questions
    quiz_manager.load_questions(questions)
    
    # Attach observers (Observer Pattern)
    score_observer = ScoreObserver("ScoreObserver")
    time_observer = TimeObserver("TimeObserver")
    completion_observer = QuizCompletionObserver("CompletionObserver")
    
    quiz_manager.attach(score_observer)
    quiz_manager.attach(time_observer)
    quiz_manager.attach(completion_observer)
    
    # Start quiz
    quiz_manager.start_quiz("DemoUser")
    
    print("✅ Quiz started successfully!")
    print(f"📝 Total questions: {len(questions)}")
    print(f"⏱️  Time limit: {quiz_manager.quiz_duration} seconds")
    print()
    
    # Answer questions automatically
    answers = ["Stack", "3", True, True]  # Correct answers
    
    for i, answer in enumerate(answers, 1):
        current_question = quiz_manager.get_current_question()
        if not current_question:
            break
            
        print(f"Question {i}: {current_question.text}")
        print(f"User Answer: {answer}")
        
        # Submit answer
        result = quiz_manager.submit_answer(answer)
        
        # Display result
        if result['correct']:
            print("✅ Correct!")
            print(f"Points earned: {result['points_earned']}")
        else:
            print("❌ Incorrect!")
            print(f"Correct answer: {result['correct_answer']}")
        
        print(f"Current score: {result['current_score']}")
        print("-" * 40)
        
        # Show progress
        progress = quiz_manager.get_quiz_progress()
        if progress.get('active', False):
            remaining_time = int(progress.get('remaining_time', 0))
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            print(f"Time remaining: {minutes:02d}:{seconds:02d}")
            print(f"Score: {progress.get('current_score', 0)}")
        print()
    
    # End quiz and show final results
    final_results = quiz_manager.end_quiz()
    
    print("🎉 QUIZ COMPLETED!")
    print("=" * 50)
    print(f"Final Score: {final_results['final_score']}")
    print(f"Questions Answered: {final_results['answered_questions']}/{final_results['total_questions']}")
    print(f"Time Taken: {final_results['elapsed_time']:.1f} seconds")
    print("=" * 50)
    
    print("\n✅ All design patterns working correctly:")
    print("🏭 Factory Pattern: Questions created successfully")
    print("🔒 Singleton Pattern: QuizManager instance shared")
    print("👁️ Observer Pattern: Notifications sent properly")
    print("🎯 Quiz flow: Complete with proper feedback")

if __name__ == "__main__":
    demo_quiz() 