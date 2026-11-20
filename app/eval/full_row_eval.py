"""Module 11: layer the UX rubric onto Module 9's correctness judge --
keep both results separate instead of merging them into one score."""
from eval.judge import judge_answer
from eval.ux_rubric import evaluate_ux


def evaluate_row(question: str, answer: str, reference: str) -> dict:
    return {
        "correctness": judge_answer(question, answer, reference),
        "user_experience": evaluate_ux(question, answer),
    }
