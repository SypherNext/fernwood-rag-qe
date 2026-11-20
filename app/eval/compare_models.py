"""Module 10: a fair, controlled scorecard comparing llama3.2:3b against
qwen2.5:3b -- the golden dataset, retrieval configuration, prompt, and
judge all held constant; only the generation model varies.
"""
import json
import os
import time

from rag_pipeline import RagPipeline
from eval.judge import judge_answer

MODELS = ["llama3.2:3b", "qwen2.5:3b"]
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "golden_dataset.json")


def run_scorecard(models: list[str], golden_path: str = DATASET_PATH) -> dict:
    with open(golden_path) as f:
        dataset = json.load(f)

    pipeline = RagPipeline()
    scorecard = {model: {"passed": 0, "total": 0, "latencies": []} for model in models}

    for case in dataset["cases"]:
        for model in models:
            start = time.time()
            result = pipeline.ask(case["question"], gen_model=model)
            elapsed = time.time() - start

            verdict = judge_answer(case["question"], result["answer"], case["reference_answer"])

            scorecard[model]["total"] += 1
            scorecard[model]["passed"] += verdict["verdict"] == "PASS"
            scorecard[model]["latencies"].append(elapsed)

    return scorecard


if __name__ == "__main__":
    scorecard = run_scorecard(MODELS)
    for model, stats in scorecard.items():
        avg_latency = sum(stats["latencies"]) / len(stats["latencies"])
        print(f"{model}")
        print(f"  pass rate: {stats['passed']}/{stats['total']}")
        print(f"  avg latency: {avg_latency:.2f}s")
