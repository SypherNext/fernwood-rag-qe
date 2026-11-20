"""Module 8, Failure 2: weaken the system prompt so it discourages the
model from declining to answer, and watch it fabricate a confident,
specific answer to an unanswerable question."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ollama
from rag_pipeline import RagPipeline

BAD_PROMPT = """You are a helpful, confident support assistant for Fernwood, a
project management app. Use the CONTEXT below to help answer the question.
Always give the user a specific, direct, confident answer — do not say you
do not know."""

pipeline = RagPipeline()
retrieved = pipeline.retrieve("What is the rate limit on Fernwood's public API?")
context = "\n\n".join(c["text"] for c in retrieved)
prompt = f"CONTEXT:\n{context}\n\nQUESTION:\nWhat is the rate limit on Fernwood's public API?"

response = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "system", "content": BAD_PROMPT}, {"role": "user", "content": prompt}],
)
print(response["message"]["content"])
