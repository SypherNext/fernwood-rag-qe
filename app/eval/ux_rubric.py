"""Module 11: evaluate user experience as a separate axis from correctness
-- four independent true/false checks plus reasoning, not one blended
score.
"""
import json
import ollama

UX_MODEL = "llama3.2:3b"

UX_PROMPT = """You are reviewing a support assistant answer for USER EXPERIENCE
quality only — not whether it is factually correct.

For each of the following, answer true or false:
- clear: Is the answer easy to understand on first read?
- concise: Does it avoid unnecessary padding or repetition?
- appropriate_tone: Is the tone professional and friendly, not curt or robotic?
- actionable: If it cannot fully answer, does it still help the user (e.g. suggest what to do next), rather than just a dead end?

Respond with ONLY a JSON object:
{{"clear": true/false, "concise": true/false, "appropriate_tone": true/false, "actionable": true/false, "reasoning": "one sentence"}}

QUESTION: {question}
ANSWER: {answer}
"""


def evaluate_ux(question: str, answer: str) -> dict:
    prompt = UX_PROMPT.format(question=question, answer=answer)
    response = ollama.chat(model=UX_MODEL, messages=[{"role": "user", "content": prompt}], format="json")
    return json.loads(response["message"]["content"])
