"""Module 9: a hand-built LLM-as-a-judge evaluator. Pass/fail, deliberately
binary -- easier to validate and aggregate, harder for the model to fudge
than a numeric score.
"""
import json
import ollama

JUDGE_MODEL = "llama3.2:3b"

JUDGE_PROMPT = """You are a QA judge for a support assistant. Compare the ANSWER
to the REFERENCE for the given QUESTION. Decide PASS if the ANSWER conveys the
same meaning as the REFERENCE, even if worded differently. Decide FAIL if the
ANSWER contradicts the REFERENCE, is missing the key fact from the REFERENCE,
or fabricates something not in the REFERENCE.

Respond with ONLY a JSON object in this exact shape, no other text:
{{"verdict": "PASS" or "FAIL", "reasoning": "one sentence explaining why"}}

QUESTION: {question}
REFERENCE: {reference}
ANSWER: {answer}
"""


def judge_answer(question: str, answer: str, reference: str) -> dict:
    prompt = JUDGE_PROMPT.format(question=question, reference=reference, answer=answer)
    response = ollama.chat(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    return json.loads(response["message"]["content"])
