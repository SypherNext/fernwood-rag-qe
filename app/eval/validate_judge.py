"""Module 9: validate the hand-built judge against known-good and
known-bad cases before trusting its verdict on anything else.
"""
from eval.judge import judge_answer

cases = [
    {
        "question": "How many active projects can I have on the Free plan?",
        "reference": "Up to 3 active projects.",
        "answer": "You can have up to 3 active projects on the Free plan.",
        "expected": "PASS",   # known-good: correct, different wording
    },
    {
        "question": "How many active projects can I have on the Free plan?",
        "reference": "Up to 3 active projects.",
        "answer": "You can have up to 10 active projects on the Free plan.",
        "expected": "FAIL",   # known-bad: wrong number
    },
    {
        "question": "Does the Free plan include priority support?",
        "reference": "No. Priority support is only included on the Team plan.",
        "answer": "No, priority support is only available on the Team plan.",
        "expected": "PASS",   # known-good: correct, rephrased
    },
    {
        "question": "Does the Free plan include priority support?",
        "reference": "No. Priority support is only included on the Team plan.",
        "answer": "Yes, all plans include priority support.",
        "expected": "FAIL",   # known-bad: direct contradiction
    },
]

if __name__ == "__main__":
    correct = 0
    for case in cases:
        result = judge_answer(case["question"], case["answer"], case["reference"])
        match = result["verdict"] == case["expected"]
        correct += match
        print(f"expected={case['expected']:4s} got={result['verdict']:4s} match={match}  reasoning={result['reasoning']}")

    print(f"\n{correct}/{len(cases)} judge verdicts matched the known-correct answer.")
