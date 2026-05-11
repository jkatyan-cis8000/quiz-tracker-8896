# Architecture

## Overview

This is a trivia quiz program that presents multiple-choice or short-answer questions on various topics. Users enter answers, and the game tracks their score. After answering all questions, the quiz displays the total correct answers.

## Layers

### `src/types/`
Pure type definitions for the quiz domain. No logic.
- `question.py`: Question, AnswerChoice, Quiz definitions
- `score.py`: Score, Result definitions
- `config.py`: Config definitions

### `src/config/`
Constants, settings, environment.
- `defaults.py`: Default configuration values (question count, display settings)
- `paths.py`: File paths for question banks

### `src/repo/`
Data access for question banks.
- `question_bank.py`: Load/save question banks from JSON files

### `src/providers/`
Cross-cutting concerns.
- `formatter.py`: Output formatting helpers

### `src/service/`
Business logic.
- `quiz_engine.py`: Quiz orchestration, scoring, answer validation

### `src/runtime/`
App lifecycle, orchestration, wiring.
- `session.py`: Quiz session management
- `main.py`: Entry point

### `src/ui/`
User-facing surfaces (CLI).
- `cli.py`: CLI interface for questions, answers, results

### `src/utils/`
Pure helpers; no domain logic, no internal imports.
