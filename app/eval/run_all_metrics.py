"""Module 7: run all six of this course's RAGAS metrics for real against
RagPipeline's own output -- faithfulness, response relevancy, context
precision, context recall, context entity recall, and noise sensitivity.
"""
from ragas import evaluate, EvaluationDataset
from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    ContextPrecision,
    ContextRecall,
    ContextEntityRecall,
    NoiseSensitivity,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from langchain_ollama import ChatOllama, OllamaEmbeddings

from eval.build_eval_dataset import build_eval_rows

rows = build_eval_rows()
eval_dataset = EvaluationDataset.from_list(rows)

evaluator_llm = LangchainLLMWrapper(ChatOllama(model="qwen2.5:3b", temperature=0))
evaluator_embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text"))

result = evaluate(
    dataset=eval_dataset,
    metrics=[
        Faithfulness(),
        ResponseRelevancy(),
        ContextPrecision(),
        ContextRecall(),
        ContextEntityRecall(),
        NoiseSensitivity(),
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
    run_config=RunConfig(timeout=300, max_workers=2),
)

df = result.to_pandas()
cols = ["user_input", "faithfulness", "answer_relevancy", "context_precision",
        "context_recall", "context_entity_recall", "noise_sensitivity(mode=relevant)"]
print(df[cols].to_string())
