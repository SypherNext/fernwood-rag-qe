"""Module 14: test how the system behaves when handed two contradicting
facts in its own context."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ollama
from rag_pipeline import SYSTEM_PROMPT

conflicting_context = """The Free plan supports up to 3 active projects.

CHANGELOG: As of the latest update, the Free plan now supports up to 5 active projects."""

question = "How many active projects can I have on the Free plan?"
prompt = f"CONTEXT:\n{conflicting_context}\n\nQUESTION:\n{question}"
response = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
)
print("answer:", response["message"]["content"])
