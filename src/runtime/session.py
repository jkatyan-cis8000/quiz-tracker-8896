from typing import List

from src.types.question import Answer, Quiz, Question


class QuizSession:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        self.answers: List[Answer] = []
        self.current_question_index = 0
        self.is_complete = False

    def answer_question(self, question_id: str, selected_choice_id: str) -> bool:
        if self.is_complete:
            return False
        if not self._is_valid_question(question_id):
            return False
        self.answers.append(Answer(question_id=question_id, selected_choice_id=selected_choice_id))
        self.current_question_index += 1
        if self.current_question_index >= len(self.quiz.questions):
            self.is_complete = True
        return True

    def get_current_question(self) -> Question:
        if self.is_complete:
            raise RuntimeError("Quiz is complete")
        return self.quiz.questions[self.current_question_index]

    def get_score(self) -> int:
        score = 0
        for answer in self.answers:
            question = next((q for q in self.quiz.questions if q.id == answer.question_id), None)
            if question and answer.selected_choice_id == question.correct_choice_id:
                score += 1
        return score

    def get_total_questions(self) -> int:
        return len(self.quiz.questions)

    def _is_valid_question(self, question_id: str) -> bool:
        return any(q.id == question_id for q in self.quiz.questions)
