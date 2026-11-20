"""The RAG system under test for the rest of this project: retrieve relevant
Fernwood doc chunks for a question, then generate a grounded answer from
them with a local Ollama model.

ask() takes an optional gen_model override so Module 10's model comparison
can swap only the generation model while holding retrieval, the prompt, and
everything else identical between runs.
"""
import ollama

from rag_store import build_store, embed

GEN_MODEL = "llama3.2:3b"
TOP_K = 2

SYSTEM_PROMPT = """You are a support assistant for Fernwood, a project management app.
Answer the user's question using ONLY the CONTEXT below. If the answer is not
contained in the CONTEXT, say exactly: "Not documented." Do not use any
outside knowledge."""


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


class RagPipeline:
    def __init__(self):
        self.store = build_store()

    def retrieve(self, question: str, top_k: int = TOP_K) -> list[dict]:
        q_embedding = embed(question)
        scored = [
            (cosine_similarity(q_embedding, chunk["embedding"]), chunk)
            for chunk in self.store
        ]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def ask(self, question: str, top_k: int = TOP_K, gen_model: str = GEN_MODEL) -> dict:
        retrieved = self.retrieve(question, top_k=top_k)
        context = "\n\n".join(chunk["text"] for chunk in retrieved)
        prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        response = ollama.chat(
            model=gen_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return {
            "question": question,
            "answer": response["message"]["content"],
            "retrieved_contexts": [c["text"] for c in retrieved],
            "retrieved_docs": [c["source_doc"] for c in retrieved],
        }
