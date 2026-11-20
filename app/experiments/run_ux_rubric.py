"""Module 11: run the UX rubric on a terse-but-correct answer and a
longer, warmer answer to the same question, and compare the verdicts."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.ux_rubric import evaluate_ux

cases = [
    ("Can a Viewer edit tasks in a project?", "Not documented."),
    ("Can a Viewer edit tasks in a project?",
     "No, Viewers only have read-only access, so they cannot edit tasks. "
     "If you need edit access, ask a project Owner to change your role to Editor."),
]

for question, answer in cases:
    result = evaluate_ux(question, answer)
    print(f"answer: {answer}")
    print(f"  ux: {result}")
    print()
