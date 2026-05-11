from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    max_quiz_duration_minutes: int = 30
    default_question_limit: int = 10
    randomize_questions: bool = True
    show_score_after_quiz: bool = True
    question_file_path: str = "data/sample_questions.json"


DEFAULT_CONFIG = Config()
