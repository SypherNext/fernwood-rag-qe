# Fernwood RAG QE

A small, real, local RAG system that answers questions about **Fernwood**, a
fictional project-management app, paired with a full AI-quality-engineering
evaluation suite built around it: an engineered golden dataset, RAGAS
metrics, a hand-built LLM-as-a-judge, a user-experience rubric, a fair
model comparison, and a CI/CD quality gate.

It retrieves from five short Markdown docs about Fernwood (`app/docs/`),
answers with a local Ollama model, and is evaluated end to end with
[RAGAS](https://github.com/explodinggradients/ragas) — no hosted LLM API,
no per-call cost, nothing leaving your machine.

It is the companion code for the Sypher course "AI Quality Engineering with
RAGAS" (`ai-qe-ragas`). `app/` is the finished project; the course has you
build every file in it, module by module, by hand.

**GitHub repository:** link coming soon (fernwood-rag-qe)

## What it needs that a typical AI course doesn't

Nothing paid. This course and this repository are deliberately local-first:
every model call — generation, embedding, and the LLM-as-a-judge calls RAGAS
and this project's own judge make — runs against [Ollama](https://ollama.com)
on your own machine. There is no API key to create, no bill, and no network
dependency once the models are pulled.

## Set up your computer

You need Git, Python 3.11 (RAGAS's dependency chain has the most reliable
prebuilt wheels on 3.11 at the time of writing — a newer interpreter can
work but may need to build some dependencies from source), and Ollama.

| Tool | Windows | macOS | Ubuntu or Debian |
| --- | --- | --- | --- |
| Git | `winget install --id Git.Git -e` | `brew install git` | `sudo apt update && sudo apt install -y git` |
| Python 3.11 | `winget install Python.Python.3.11` | `brew install python@3.11` | `sudo apt install -y python3.11 python3.11-venv` |
| Ollama | Download the installer from [ollama.com](https://ollama.com) | `brew install --cask ollama` | `curl -fsSL https://ollama.ai/install.sh \| sh` |

Open a new terminal and check each tool:

```bash
git --version
python3.11 --version   # python --version on Windows, if 3.11 is your default
ollama --version
```

### Get the code

```bash
git clone <fernwood-rag-qe repository URL> fernwood-rag-qe
cd fernwood-rag-qe/app
```

Every command below runs from `app/`, the project root the scripts actually
import against.

### Pull the models

This project uses three local models: one for generation, one for
embeddings, and a second generation model used for model comparison and as
the RAGAS evaluator.

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull qwen2.5:3b
```

Confirm the server is up:

```bash
ollama serve   # if it isn't already running in the background
curl http://localhost:11434
# Ollama is running
```

## Run the app

1. **Create and activate a virtual environment**, then install dependencies:

   ```bash
   python3.11 -m venv venv        # Windows: python -m venv venv
   source venv/bin/activate       # Windows PowerShell: venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Confirm the RAGAS pin matters.** Install exactly what `requirements.txt`
   pins, not a bare `pip install ragas`. At the time this project was built,
   a bare `pip install ragas` resolves the newest `langchain-community`
   release available — but that release has dropped an internal module
   RAGAS's own code still imports directly, and the import fails with
   `ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'`
   the moment you try to use RAGAS, even though the install itself reported
   success. Pinning `langchain-community<0.4` (already in
   `requirements.txt`) keeps you on a version that still has it.

   ```python
   # check_ragas.py-style sanity check, run from a Python shell:
   import ragas
   from ragas import evaluate, EvaluationDataset
   from ragas.metrics import Faithfulness
   from ragas.llms import LangchainLLMWrapper
   print("ragas version:", ragas.__version__)
   print("imports OK")
   ```

3. **Build the RAG store and ask it something:**

   ```bash
   python run_rag_over_dataset.py
   ```

   This builds an in-memory, embedded store of all five Fernwood docs, runs
   every question in `golden_dataset.json` through the pipeline, and prints
   each answer next to its reference answer.

4. **Reproduce the real retrieval miss:**

   ```bash
   python experiments/retrieval_miss.py
   python experiments/confirm_miss.py
   ```

   `"How do I mark something as finished?"` doesn't share `projects-and-tasks.md`'s
   vocabulary. At `top_k=1` only the wrong document (`data-export-and-deletion.md`)
   gets retrieved and the pipeline correctly answers `"Not documented."` — the
   retrieval miss, not a generation bug. At `top_k=2` the right document also
   makes it into context and the answer becomes correct.

5. **Run a real RAGAS evaluation:**

   ```bash
   python -m eval.run_first_eval
   python -m eval.run_all_metrics
   ```

   Expect this to take real, noticeable time — every row runs one or more
   real LLM calls per metric, on CPU unless Ollama has GPU access on your
   machine (check with `curl -s http://localhost:11434/api/ps` and look at
   `size_vram`).

6. **Validate and run the hand-built judge:**

   ```bash
   python -m eval.validate_judge
   python -m eval.compare_models
   ```

7. **Run the CI smoke gate locally**, the same thing the GitHub Actions
   workflow runs on every pull request:

   ```bash
   python -m eval.ci_gate --dataset golden_dataset_smoke.json --baseline baseline.json --threshold 0.10
   ```

## Run the advanced test categories

```bash
python experiments/test_injection.py
python experiments/test_conflicting_info.py
python experiments/test_multihop.py
```

Each of these is a deliberate, disclosed, educational test against this
one local project — a prompt-injection resistance check, a
conflicting-sources check, and a multi-hop retrieval-depth check. None of
these prove the system is immune to the failure in general; they confirm
one specific, reproducible result on this specific system.

## Project layout

```text
fernwood-rag-qe/
  app/
    docs/                        Fernwood's five source-of-truth doc files
      getting-started.md
      projects-and-tasks.md
      sharing-and-permissions.md
      billing-and-plans.md
      data-export-and-deletion.md
    rag_store.py                  load_chunks/embed/build_store -- the in-memory embedded store
    rag_pipeline.py                RagPipeline: retrieve() + ask(), with a gen_model override for fair model comparison
    run_rag_over_dataset.py        runs every golden_dataset.json case through the pipeline
    golden_dataset.json            12 engineered, validated cases across 6 categories
    golden_dataset_smoke.json      3-case curated subset used by the fast PR gate
    baseline.json                  last accepted smoke-gate pass rate, versioned with the dataset
    eval/
      validate_dataset.py          structural validation (no duplicate ids, every category present)
      build_eval_dataset.py        golden_dataset.json + RagPipeline.ask() -> a RAGAS EvaluationDataset
      run_first_eval.py            Faithfulness + ResponseRelevancy, run for real
      run_all_metrics.py           all 6 RAGAS metrics this project uses, run for real
      judge.py                     hand-built pass/fail LLM-as-a-judge
      validate_judge.py            validates judge.py against known-good/known-bad cases
      ux_rubric.py                 a separate, non-correctness user-experience rubric
      full_row_eval.py             layers ux_rubric.py on top of judge.py without merging scores
      compare_models.py            fair llama3.2:3b vs qwen2.5:3b scorecard (quality, latency, consistency)
      ci_gate.py                   the PR/nightly quality gate: pass rate vs. baseline, relative threshold
    experiments/                   small, disposable scripts for one concept at a time
    requirements.txt
    .gitignore
  .github/workflows/eval.yml       PR smoke gate + scheduled full nightly evaluation
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai'`.**
  You installed a bare `pip install ragas` instead of the pinned
  `requirements.txt`. Reinstall with `langchain-community<0.4`.
- **A RAGAS metric call fails with a parsing error using `llama3.2:3b` as
  the evaluator.** This is expected and the reason this project's evaluator
  model is `qwen2.5:3b`, not `llama3.2:3b` — RAGAS's metrics need fairly
  involved structured output internally, and `llama3.2:3b` is less
  reliable at producing it. Use `qwen2.5:3b` as the `evaluator_llm`.
- **RAGAS calls time out or queue forever.** A single local Ollama server
  doesn't process RAGAS's default concurrency (`max_workers` up to 16) the
  way a large hosted API might. Every script in `eval/` already sets
  `RunConfig(max_workers=2, timeout=300)` — if you still see timeouts, lower
  `max_workers` further, or check `ollama ps`/`curl .../api/ps` for whether
  another model is also loaded and competing for the same CPU.
- **Scores move slightly between identical runs.** Expected. Generation and
  every LLM-as-a-judge call are non-deterministic. Never trust a single
  run's exact number; compare against a stored baseline with a relative
  threshold, which is exactly what `eval/ci_gate.py` does.
- **`pytest`-style import errors running anything under `eval/` or
  `experiments/`.** Run commands from `app/` (not the repo root, and not
  from inside `eval/` or `experiments/`), so the top-level `rag_pipeline`
  and `rag_store` modules are importable.

## License

Copyright (C) 2026 SypherNext

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). You may
use, study and change it. If you share a modified version, or run one as a website or service
that other people use, you must make your full modified source code available under the same
license. See [LICENSE](LICENSE) for the full terms.
