"""
User interface module for the quiz application.

This module handles the display of questions, collection of user input,
and presentation of quiz results and progress information.
"""

import sys
from typing import Any, Optional
from services.quiz_manager import QuizManager
from models.question import Question
from models.user import User


class QuizUI:
    """
    User interface class for the quiz application.
    
    This class handles all user interactions including displaying
    questions, collecting answers, and showing results.
    """
    
    def __init__(self, quiz_manager: QuizManager):
        """
        Initialize the quiz UI.
        
        Args:
            quiz_manager (QuizManager): The quiz manager instance
        """
        self.quiz_manager = quiz_manager
    
    def display_welcome(self) -> None:
        """
        Display welcome message and instructions.
        """
        print("=" * 50)
        print("🎯 WELCOME TO THE QUIZ APPLICATION! 🎯")
        print("=" * 50)
        print("This application demonstrates:")
        print("• Factory Pattern for creating different question types")
        print("• Singleton Pattern for quiz state management")
        print("• Observer Pattern for notifications")
        print("• Professional software engineering practices")
        print("=" * 50)
    
    def get_user_name(self) -> str:
        """
        Get user name from input.
        
        Returns:
            str: User's name
        """
        while True:
            name = input("Enter your name: ").strip()
            if name:
                return name
            print("Please enter a valid name.")
    
    def display_question(self, question: Question, question_number: int, total_questions: int) -> None:
        """
        Display a question to the user.
        
        Args:
            question (Question): Question to display
            question_number (int): Current question number
            total_questions (int): Total number of questions
        """
        print(f"\n--- Question {question_number}/{total_questions} ---")
        print(question.display_question())
    
    def get_user_answer(self, question: Question) -> Any:
        """
        Get user's answer for a question.
        
        Args:
            question (Question): Question being answered
            
        Returns:
            Any: User's answer
        """
        while True:
            try:
                answer = input("Your answer: ").strip()
                
                if question.question_type == "mcq":
                    choice = int(answer)
                    if 1 <= choice <= len(question.options):
                        return question.options[choice - 1]
                    else:
                        print(f"Please enter a number between 1 and {len(question.options)}")
                
                elif question.question_type == "true_false":
                    if answer == "1":
                        return True
                    elif answer == "2":
                        return False
                    else:
                        print("Please enter 1 for True or 2 for False")
                
                else:
                    if answer:
                        return answer
                    else:
                        print("Please enter an answer")
                        
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nQuiz interrupted. Goodbye!")
                sys.exit(0)
    
    def display_result(self, result: dict) -> None:
        """
        Display the result of an answer.
        
        Args:
            result (dict): Result dictionary from quiz manager
        """
        if result.get('correct', False):
            print("✅ Correct!")
            print(f"Points earned: {result.get('points_earned', 0)}")
        else:
            print("❌ Incorrect!")
            print(f"Correct answer: {result.get('correct_answer', 'Unknown')}")

        print(f"Current score: {result.get('current_score', 0)}")
        print("-" * 40)
    
    def display_progress(self, progress: dict) -> None:
        """
        Display quiz progress information.
        
        Args:
            progress (dict): Progress information from quiz manager
        """
        if progress.get('active', False):
            remaining_time = int(progress.get('remaining_time', 0))
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            print(f"\nTime remaining: {minutes:02d}:{seconds:02d}")
            print(f"Score: {progress.get('current_score', 0)}")
    
    def display_final_results(self, results: dict) -> None:
        """
        Display final quiz results.
        
        Args:
            results (dict): Final quiz results
        """
        print("\n" + "=" * 50)
        print("🎉 QUIZ COMPLETED! 🎉")
        print("=" * 50)
        print(f"Player: {results.get('user_name', 'Unknown')}")
        print(f"Final Score: {results.get('final_score', 0)}")
        print(f"Questions Answered: {results.get('answered_questions', 0)}/{results.get('total_questions', 0)}")
        print(f"Time Taken: {results.get('elapsed_time', 0):.1f} seconds")
        print("=" * 50)
    
    def run(self) -> None:
        """
        Run the main quiz application.
        
        This method orchestrates the entire quiz flow from start to finish.
        """
        try:
            # Display welcome
            self.display_welcome()
            
            # Get user name and create User object
            user_name = self.get_user_name()
            user = User(user_name)
            
            # Start quiz (questions should be loaded by now)
            if not self.quiz_manager.start_quiz(user):
                print("Error: Could not start quiz. Exiting.")
                return
            
            print(f"\nQuiz started for {user_name}!")
            print("Let's begin!\n")
            
            # Main quiz loop
            while self.quiz_manager.quiz_active:
                if self.quiz_manager.timer and self.quiz_manager.timer.is_time_expired():
                    print("\n⏰ Time is up! The quiz has ended.\n")
                    self.quiz_manager.quiz_active = False
                    break
                
                current_question = self.quiz_manager.get_current_question()
                if not current_question:
                    break
                
                # Get quiz progress
                progress = self.quiz_manager.get_quiz_progress()
                if not progress.get('active', False):
                    break
                
                # Display question
                self.display_question(
                    current_question,
                    progress.get('current_question', 1),
                    progress.get('total_questions', 1)
                )
                
                # Get user answer
                user_answer = self.get_user_answer(current_question)
                
                # Submit answer
                result = self.quiz_manager.submit_answer(user_answer)
                self.display_result(result)
                
                # Display updated progress after answer
                self.display_progress(self.quiz_manager.get_quiz_progress())
                
                # Check if quiz is complete (after answering the last question)
                if self.quiz_manager.current_question_index >= len(self.quiz_manager.questions):
                    self.quiz_manager.quiz_active = False
                    break
            
            # Display final results
            final_results = self.quiz_manager.end_quiz()
            self.display_final_results(final_results)
            
        except KeyboardInterrupt:
            print("\n\nQuiz interrupted. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again later.") 