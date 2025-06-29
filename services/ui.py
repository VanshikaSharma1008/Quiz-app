        # Display final results
        if self.quiz_manager.quiz_active:
            final_results = self.quiz_manager.end_quiz()
        else:
            final_results = {
                'user_name': self.quiz_manager.current_user.name if self.quiz_manager.current_user else "Unknown",
                'final_score': self.quiz_manager.current_user.current_score if self.quiz_manager.current_user else 0,
                'answered_questions': self.quiz_manager.current_question_index,
                'total_questions': len(self.quiz_manager.questions),
                'elapsed_time': self.quiz_manager.timer.get_elapsed_time() if self.quiz_manager.timer else 0
            }
        self.display_final_results(final_results) 