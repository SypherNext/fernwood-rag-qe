"""Module 6: the first real RAGAS evaluation against this project's own RAG
pipeline. Note the evaluator model is qwen2.5:3b, not llama3.2:3b -- a
small local model that reliably produces the structured output RAGAS's
metrics need internally; llama3.2:3b tends to fail metric calls with a
parsing error on this kind of structured judgment prompt.
"""
from ragas import evaluate, EvaluationDataset
from ragas.metrics import Faithfulness, ResponseRelevancy
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
    metrics=[Faithfulness(), ResponseRelevancy()],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
    run_config=RunConfig(timeout=300, max_workers=2),
)

print(result)
df = result.to_pandas()
print(df[["user_input", "faithfulness", "answer_relevancy"]])
