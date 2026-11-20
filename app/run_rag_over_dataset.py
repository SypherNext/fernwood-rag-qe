import json
import os

from rag_pipeline import RagPipeline

DATASET_PATH = os.path.join(os.path.dirname(__file__), "golden_dataset.json")

with open(DATASET_PATH) as f:
    dataset = json.load(f)

pipeline = RagPipeline()

for case in dataset["cases"]:
    result = pipeline.ask(case["question"])
    print(f"[{case['id']}] {case['question']}")
    print(f"  retrieved: {result['retrieved_docs']}")
    print(f"  answer:    {result['answer']}")
    print(f"  reference: {case['reference_answer']}")
    print()
