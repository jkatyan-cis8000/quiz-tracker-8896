from dataclasses import dataclass
from typing import List
from .question import Question


@dataclass
class Quiz:
    id: str
    title: str
    questions: List[Question]


@dataclass
class QuizResult:
    score: int
    total: int
    correct_count: int
    wrong_count: int
    answers: List[str]
