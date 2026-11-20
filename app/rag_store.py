"""Builds an in-memory store of Fernwood's doc chunks, each with its embedding.

Fernwood's five doc files are each short enough to treat as one chunk per
file -- build_store() embeds all five once, in memory, no vector database
needed at this scale.
"""
import os
import ollama

EMBED_MODEL = "nomic-embed-text"
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")


def load_chunks() -> list[dict]:
    chunks = []
    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".md"):
            continue
        with open(os.path.join(DOCS_DIR, filename), encoding="utf-8") as f:
            text = f.read()
        chunks.append({"source_doc": filename, "text": text})
    return chunks


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def build_store() -> list[dict]:
    chunks = load_chunks()
    for chunk in chunks:
        chunk["embedding"] = embed(chunk["text"])
    return chunks


if __name__ == "__main__":
    store = build_store()
    for chunk in store:
        print(f"{chunk['source_doc']}: {len(chunk['embedding'])}-dim embedding")
