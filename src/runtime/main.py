import sys

from src.config.defaults import DEFAULT_CONFIG
from src.types.question import Quiz
from src.runtime.session import QuizSession


def load_quiz() -> Quiz:
    from src.repo.question_bank import QuestionBankRepository
    repo = QuestionBankRepository(DEFAULT_CONFIG.question_file_path)
    return repo.load_quiz()


def run_quiz():
    quiz = load_quiz()
    session = QuizSession(quiz)
    
    print(f"Starting quiz: {quiz.title}")
    print(f"Description: {quiz.description}")
    print(f"Total questions: {len(quiz.questions)}")
    print()
    
    while not session.is_complete:
        question = session.get_current_question()
        print(f"Question {session.current_question_index + 1}: {question.text}")
        for choice in question.choices:
            print(f"  {choice.id}: {choice.text}")
        
        user_choice = input("Enter your choice: ").strip()
        if not session.answer_question(question.id, user_choice):
            print("Invalid choice. Try again.")
    
    score = session.get_score()
    total = session.get_total_questions()
    percentage = (score / total) * 100
    
    print()
    print(f"Quiz complete!")
    print(f"Score: {score}/{total} ({percentage:.1f}%)")
    
    if DEFAULT_CONFIG.show_score_after_quiz:
        if percentage >= 80:
            print("Excellent work!")
        elif percentage >= 50:
            print("Good job!")
        else:
            print("Keep practicing!")


def main():
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\nQuiz terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
