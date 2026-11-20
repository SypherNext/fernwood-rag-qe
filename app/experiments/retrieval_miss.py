"""Module 5: print every chunk's similarity score for a question that means
the same thing as something in the docs, but doesn't share the docs'
vocabulary -- this is how the real retrieval miss at top_k=1 was found.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_pipeline import RagPipeline, cosine_similarity
from rag_store import embed

pipeline = RagPipeline()
question = "How do I mark something as finished?"

q_embedding = embed(question)
scores = [
    (cosine_similarity(q_embedding, chunk["embedding"]), chunk["source_doc"])
    for chunk in pipeline.store
]
scores.sort(key=lambda pair: pair[0], reverse=True)

for score, source_doc in scores:
    print(f"{score:.4f}  {source_doc}")
