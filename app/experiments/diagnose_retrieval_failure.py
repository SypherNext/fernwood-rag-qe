"""Module 8, Failure 1: score Module 5's real retrieval miss with RAGAS's
context recall metric instead of just eyeballing it."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragas import evaluate, EvaluationDataset
from ragas.metrics import ContextRecall
from ragas.llms import LangchainLLMWrapper
from ragas.run_config import RunConfig
from langchain_ollama import ChatOllama
from rag_pipeline import RagPipeline

pipeline = RagPipeline()
result = pipeline.ask("How do I mark something as finished?", top_k=1)

row = [{
    "user_input": "How do I mark something as finished?",
    "retrieved_contexts": result["retrieved_contexts"],
    "response": result["answer"],
    "reference": "Set the task's status to Done.",
}]

evaluator_llm = LangchainLLMWrapper(ChatOllama(model="qwen2.5:3b", temperature=0))
scored = evaluate(
    dataset=EvaluationDataset.from_list(row),
    metrics=[ContextRecall()],
    llm=evaluator_llm,
    run_config=RunConfig(timeout=300, max_workers=2),
)
print(scored.to_pandas()[["user_input", "context_recall"]])
