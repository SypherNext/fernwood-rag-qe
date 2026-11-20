"""Module 8: score the prompt-caused fabrication from
diagnose_prompt_failure.py with RAGAS's faithfulness metric. Paste your own
retrieved context and fabricated answer below before running."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragas import evaluate, EvaluationDataset
from ragas.metrics import Faithfulness
from ragas.llms import LangchainLLMWrapper
from ragas.run_config import RunConfig
from langchain_ollama import ChatOllama

row = [{
    "user_input": "What is the rate limit on Fernwood's public API?",
    "retrieved_contexts": ["<paste your retrieved context text here>"],
    "response": "<paste the fabricated answer you got above>",
    "reference": "Not documented. No public API is mentioned anywhere in the docs.",
}]

evaluator_llm = LangchainLLMWrapper(ChatOllama(model="qwen2.5:3b", temperature=0))
scored = evaluate(
    dataset=EvaluationDataset.from_list(row),
    metrics=[Faithfulness()],
    llm=evaluator_llm,
    run_config=RunConfig(timeout=300, max_workers=2),
)
print(scored.to_pandas()[["user_input", "faithfulness"]])
