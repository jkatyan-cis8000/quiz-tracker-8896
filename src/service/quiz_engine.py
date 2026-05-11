from typing import List
from src.types.question import Question, Answer
from src.types.quiz import Quiz, QuizResult


class QuizEngine:
    def __init__(self, config):
        self.config = config
        self.current_quiz: Quiz = None
        self.current_question_index: int = 0
        self.user_answers: List[str] = []
        self.score: int = 0
        self.correct_count: int = 0
        self.wrong_count: int = 0

    def start_quiz(self, quiz: Quiz) -> None:
        self.current_quiz = quiz
        self.current_question_index = 0
        self.user_answers = []
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0

    def present_question(self) -> Question:
        return self.current_quiz.questions[self.current_question_index]

    def submit_answer(self, answer_text: str) -> bool:
        current_question = self.current_quiz.questions[self.current_question_index]
        self.user_answers.append(answer_text)

        correct_answer = next(
            (a for a in current_question.answers if a.is_correct), None
        )

        if correct_answer and correct_answer.text == answer_text:
            self.score += 1
            self.correct_count += 1
            return True
        else:
            self.wrong_count += 1
            return False

    def next_question(self) -> bool:
        self.current_question_index += 1
        return self.current_question_index < len(self.current_quiz.questions)

    def is_complete(self) -> bool:
        return self.current_question_index >= len(self.current_quiz.questions)

    def get_result(self) -> QuizResult:
        return QuizResult(
            score=self.score,
            total=len(self.current_quiz.questions),
            correct_count=self.correct_count,
            wrong_count=self.wrong_count,
            answers=self.user_answers,
        )

    def get_question_at(self, index: int) -> Question:
        return self.current_quiz.questions[index]

    def get_total_questions(self) -> int:
        return len(self.current_quiz.questions)
