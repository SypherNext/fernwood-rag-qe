"""Module 2: ask the model something specific and checkable that it has no
real way to know, and watch it fabricate a confident-sounding answer."""
import ollama

MODEL = "llama3.2:3b"
PROMPT = "According to the latest industry survey, what percentage of QA teams have adopted AI-assisted testing tools?"

response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": PROMPT}])
print(response["message"]["content"])
