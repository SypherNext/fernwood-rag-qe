"""Module 13: a fast, validated CI gate using Module 9's judge against a
curated smoke subset, compared to a stored baseline with a relative
threshold rather than a fixed absolute number.
"""
import argparse
import json
import sys

from rag_pipeline import RagPipeline
from eval.judge import judge_answer


def run_pass_rate(dataset_path: str) -> dict:
    with open(dataset_path) as f:
        dataset = json.load(f)

    pipeline = RagPipeline()
    results = []
    for case in dataset["cases"]:
        result = pipeline.ask(case["question"])
        verdict = judge_answer(case["question"], result["answer"], case["reference_answer"])
        results.append({"id": case["id"], "verdict": verdict["verdict"]})

    passed = sum(r["verdict"] == "PASS" for r in results)
    return {"pass_rate": passed / len(results), "total": len(results), "results": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--threshold", type=float, default=0.10)
    parser.add_argument("--report", default=None)
    args = parser.parse_args()

    current = run_pass_rate(args.dataset)

    with open(args.baseline) as f:
        baseline = json.load(f)

    regression = baseline["pass_rate"] - current["pass_rate"]
    print(f"baseline pass_rate: {baseline['pass_rate']:.2f}")
    print(f"current  pass_rate: {current['pass_rate']:.2f}")
    print(f"regression: {regression:.2f} (fail threshold: {args.threshold})")

    if args.report:
        with open(args.report, "w") as f:
            json.dump(current, f, indent=2)

    if regression > args.threshold:
        print(f"FAIL: pass rate dropped by more than {args.threshold}")
        sys.exit(1)

    print("PASS: no regression beyond threshold")


if __name__ == "__main__":
    main()
