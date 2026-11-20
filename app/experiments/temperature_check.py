"""Module 2: temperature=0 and a fixed seed get you much closer to the
same answer every run than Module 1's defaults -- not a guarantee of a
byte-identical response every time."""
import ollama

MODEL = "llama3.2:3b"
PROMPT = "In one sentence, what does test coverage mean?"

for i in range(3):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        options={"temperature": 0, "seed": 42},
    )
    print(f"--- run {i + 1} ---")
    print(response["message"]["content"])
