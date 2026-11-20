"""Module 4: compute and compare two real embeddings by hand, before
Module 5 folds this into the real pipeline."""
import ollama


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


question = "How many projects can I have on the Free plan?"
related_chunk = "The Free plan supports up to 3 active projects."
unrelated_chunk = "Invite a teammate to a project from Project Settings."

emb_question = embed(question)
emb_related = embed(related_chunk)
emb_unrelated = embed(unrelated_chunk)

print("question vs. related:  ", cosine_similarity(emb_question, emb_related))
print("question vs. unrelated:", cosine_similarity(emb_question, emb_unrelated))
