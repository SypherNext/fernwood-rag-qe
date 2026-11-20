"""Module 1: run the exact same prompt five times and watch real
non-deterministic output happen."""
import ollama

MODEL = "llama3.2:3b"
PROMPT = "In one sentence, what does test coverage mean?"

for i in range(5):
    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": PROMPT}])
    print(f"--- run {i + 1} ---")
    print(response["message"]["content"])
