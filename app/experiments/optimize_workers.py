"""Module 12: time the same small evaluation at different max_workers
settings to find out, on your own hardware, which concurrency setting
actually helps instead of just adding queuing overhead."""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragas import evaluate, EvaluationDataset
from ragas.metrics import Faithfulness
from ragas.llms import LangchainLLMWrapper
from ragas.run_config import RunConfig
from langchain_ollama import ChatOllama

from eval.build_eval_dataset import build_eval_rows

rows = build_eval_rows()[:4]  # a small, fixed slice -- same rows for every run
eval_dataset = EvaluationDataset.from_list(rows)
evaluator_llm = LangchainLLMWrapper(ChatOllama(model="qwen2.5:3b", temperature=0))

for workers in (1, 2, 4):
    start = time.time()
    evaluate(
        dataset=eval_dataset,
        metrics=[Faithfulness()],
        llm=evaluator_llm,
        run_config=RunConfig(timeout=300, max_workers=workers),
    )
    elapsed = time.time() - start
    print(f"max_workers={workers}: {elapsed:.1f}s")
