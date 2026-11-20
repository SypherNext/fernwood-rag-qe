"""Module 6: build a RAGAS evaluation dataset from golden_dataset.json's
user_input/reference fields and RagPipeline.ask()'s real, current
retrieved_contexts/response output. Every row here is a fresh run of the
actual system, not a fixture.
"""
import json
import os

from rag_pipeline import RagPipeline

DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "golden_dataset.json")


def build_eval_rows(golden_path: str = DATASET_PATH) -> list[dict]:
    with open(golden_path) as f:
        dataset = json.load(f)

    pipeline = RagPipeline()
    rows = []
    for case in dataset["cases"]:
        result = pipeline.ask(case["question"])
        rows.append({
            "user_input": case["question"],
            "retrieved_contexts": result["retrieved_contexts"],
            "response": result["answer"],
            "reference": case["reference_answer"],
        })
    return rows
