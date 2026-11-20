"""Module 5: confirm the retrieval miss end-to-end at two different top_k
values -- the wrong document wins at top_k=1, the right one joins it at
top_k=2, and only top_k changes between the two calls.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_pipeline import RagPipeline

pipeline = RagPipeline()

for k in (1, 2):
    result = pipeline.ask("How do I mark something as finished?", top_k=k)
    print(f"top_k={k}  retrieved={result['retrieved_docs']}")
    print(f"  answer: {result['answer']}")
