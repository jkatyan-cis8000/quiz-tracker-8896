from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AnswerChoice:
    id: str
    text: str


@dataclass
class Question:
    id: str
    text: str
    choices: List[AnswerChoice]
    correct_choice_id: str


@dataclass
class Answer:
    question_id: str
    selected_choice_id: str


@dataclass
class Quiz:
    id: str
    title: str
    description: str
    questions: List[Question]
