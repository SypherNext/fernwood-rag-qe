"""Module 2: run the same prompt through two different local models and
compare the results side by side -- a first impression, not yet the fair,
controlled comparison Module 10 builds."""
import ollama

PROMPT = "In one sentence, what does test coverage mean?"
MODELS = ["llama3.2:3b", "qwen2.5:3b"]

for model in MODELS:
    response = ollama.chat(model=model, messages=[{"role": "user", "content": PROMPT}])
    print(f"--- {model} ---")
    print(response["message"]["content"])
