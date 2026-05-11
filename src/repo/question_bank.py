import json
from typing import List

from src.types.question import AnswerChoice, Question, Quiz


class QuestionBankRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_quiz(self) -> Quiz:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        questions: List[Question] = []
        for q in data['questions']:
            choices = [
                AnswerChoice(id=c['id'], text=c['text'])
                for c in q['choices']
            ]
            questions.append(Question(
                id=q['id'],
                text=q['text'],
                choices=choices,
                correct_choice_id=q['correct_choice_id']
            ))
        
        return Quiz(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            questions=questions
        )

    def save_quiz(self, quiz: Quiz) -> None:
        data = {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'questions': [
                {
                    'id': q.id,
                    'text': q.text,
                    'choices': [
                        {'id': c.id, 'text': c.text}
                        for c in q.choices
                    ],
                    'correct_choice_id': q.correct_choice_id
                }
                for q in quiz.questions
            ]
        }
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
