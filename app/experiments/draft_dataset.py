"""Module 3: use Ollama to generate a first draft of golden-dataset
question/answer pairs, then review every claim against the real doc text
line by line -- this draft never goes into golden_dataset.json unchecked."""
import os

DOC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "billing-and-plans.md")

import ollama

with open(DOC_PATH) as f:
    doc_text = f.read()

prompt = f"""Based only on the following documentation, write 2 question/answer
pairs a user might ask. Answer only from the text given.

DOCUMENTATION:
{doc_text}
"""

response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
print(response["message"]["content"])
