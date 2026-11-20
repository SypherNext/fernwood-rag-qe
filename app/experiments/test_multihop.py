"""Module 14: test whether retrieval depth is enough to gather every
document a multi-part question actually needs."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_pipeline import RagPipeline

pipeline = RagPipeline()
question = "If I am on the Pro plan, how many teammates can I have, and can a Viewer edit tasks?"

for k in (2, 4):
    result = pipeline.ask(question, top_k=k)
    print(f"top_k={k}  docs={result['retrieved_docs']}")
    print(f"  answer: {result['answer']}")
