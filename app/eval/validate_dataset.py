"""Module 3: mechanical structural validation of golden_dataset.json. This
cannot check that a reference answer is actually correct -- that's still on
the human reviewer, and is exactly why the manual review step isn't
skippable.
"""
import json
import os

REQUIRED_CATEGORIES = {"positive", "negative", "edge", "ambiguous", "unanswerable", "hallucination_trap"}


def validate(path: str) -> list[str]:
    with open(path) as f:
        data = json.load(f)

    errors = []
    seen_ids = set()
    seen_categories = set()

    for case in data["cases"]:
        if case["id"] in seen_ids:
            errors.append(f"duplicate id: {case['id']}")
        seen_ids.add(case["id"])
        seen_categories.add(case["category"])

        if not case["question"].strip():
            errors.append(f"{case['id']}: empty question")
        if not case["reference_answer"].strip():
            errors.append(f"{case['id']}: empty reference_answer")

    missing = REQUIRED_CATEGORIES - seen_categories
    if missing:
        errors.append(f"missing categories: {missing}")

    return errors


if __name__ == "__main__":
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "golden_dataset.json")
    errors = validate(dataset_path)
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for e in errors:
            print(f" - {e}")
    else:
        print("golden_dataset.json is structurally valid.")
