import sys
from typing import List

from src.types.question import Question, Answer
from src.types.quiz import Quiz
from src.types.quiz import QuizResult
from src.service.quiz_engine import QuizEngine
from src.config.defaults import QuizConfig, CLIConfig


class CLI:
    def __init__(self, config: CLIConfig):
        self.config = config
        self.engine = QuizEngine(config.config)

    def run(self, quiz: Quiz) -> None:
        self.engine.start_quiz(quiz)

        while not self.engine.is_complete():
            self._display_question(self.engine.present_question())
            answer = self._get_user_answer()
            self.engine.submit_answer(answer)
            if not self.engine.next_question():
                break

        self._display_results(self.engine.get_result())

    def _display_question(self, question: Question) -> None:
        print(f"\n{question.text}")
        for i, answer in enumerate(question.answers):
            print(f"  {i + 1}. {answer.text}")

    def _get_user_answer(self) -> str:
        while True:
            try:
                user_input = input("\nEnter your answer (number): ").strip()
                answer_num = int(user_input)
                if 1 <= answer_num <= len(self.engine.current_quiz.questions[self.engine.current_question_index].answers):
                    return self.engine.current_quiz.questions[self.engine.current_question_index].answers[answer_num - 1].text
                print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nQuiz cancelled.")
                sys.exit(0)

    def _display_results(self, result: QuizResult) -> None:
        print("\n" + "=" * 40)
        print("QUIZ RESULTS")
        print("=" * 40)
        print(f"Score: {result.score}/{result.total}")
        print(f"Correct: {result.correct_count}")
        print(f"Wrong: {result.wrong_count}")

        if self.config.config.show_correct_answers:
            print("\nCorrect Answers:")
            for i, answer in enumerate(result.answers):
                question = self.engine.current_quiz.questions[i]
                correct = next(
                    (a.text for a in question.answers if a.is_correct), ""
                )
                status = "✓" if answer == correct else "✗"
                print(f"  {status} Q{i + 1}: {answer} (Correct: {correct})")


def parse_cli_args(args: List[str]) -> CLIConfig:
    config = QuizConfig()
    question_file = None

    i = 0
    while i < len(args):
        if args[i] == "--show-answers":
            config.show_correct_answers = True
        elif args[i] == "--shuffle-questions":
            config.shuffle_questions = True
        elif args[i] == "--shuffle-answers":
            config.shuffle_answers = True
        elif args[i] == "--file" and i + 1 < len(args):
            question_file = args[i + 1]
            i += 1
        i += 1

    return CLIConfig(config=config, question_file=question_file)
