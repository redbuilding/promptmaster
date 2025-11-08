# Promptmaster — Prompt Framework Enhancer

Promptmaster is a small CLI that takes a raw user prompt, selects up to three relevant prompt‑engineering frameworks, rewrites the prompt for each selected framework, optionally composes a single unified “ready‑to‑run” prompt, and saves the results to a timestamped Markdown file.

## Features
- Dynamic framework selection capped at 3, based on the user’s prompt.
- Per‑framework prompt rewriting for clear, labeled sections.
- Optional unified prompt synthesis from the multi‑framework output.
- Pluggable LLM providers (Ollama included by default).
- Outputs saved as Markdown into `enhanced_prompts/`.

## Quick Start
- Requirements: Python 3.9+, and an LLM backend (Ollama by default).
- Install deps:
  ```bash
  # (optional) create a virtualenv
  python -m venv .venv && source .venv/bin/activate
  # install dependencies
  pip install -r requirements.txt
  ```
- Configure environment (create a `.env` in the project root):
  ```env
  MODEL_PROVIDER=ollama
  OLLAMA_URL=http://localhost:11434/api/generate
  OLLAMA_MODEL=llama3:instruct   # or your local model name
  OUTPUT_DIR=enhanced_prompts
  ```
- Run the app:
  ```bash
  python main.py
  ```

## How It Works
1. You enter a prompt in the CLI.
2. `framework_selector.py` scans the prompt for keywords and selects up to three frameworks (order preserved, deduplicated). If nothing matches, it falls back to `CRISPE`.
3. `prompt_rewriter.py` generates a rewritten section for each framework (one model call per framework) via the configured provider.
4. `prompt_composer.py` tries to compose a unified prompt:
   - If a clearly marked “Rewritten Prompt” section exists, it uses that.
   - Otherwise it extracts first‑line fields (Role/Audience/Context/Ask/Task/Tone/Format/Action) and builds one concise prompt, cleaning markdown and punctuation.
   - If synthesis isn’t meaningful (e.g., only one framework with no extractable fields), it is omitted from the saved output.
5. `utils.save_prompt_to_markdown` saves the enhanced (and optionally unified) prompt to `enhanced_prompts/enhanced_prompt_YYYYMMDD_HHMMSS.md`.

## Frameworks
- Definitions live in `frameworks.json` (e.g., CRAFT, TACT, FEARS, CoT, DEEP, SCOR, ICED, Prompt Sandwich, RTCO, ReACT, CoT+SC, RAP, MAPP, SCQA, APE, PEEL, PAIR, RAISE, LEAP, GROW, DIET, TREE, CRISPE).
- Selection is handled by `framework_selector.py`. It uses simple keyword heuristics and returns at most 3 frameworks.
- You can tune selection by editing keyword triggers or the cap in `select_frameworks()`.

## Providers
- Base class: `base_provider.py`.
- Ollama provider: `providers/ollama_provider.py` (uses `requests` to call Ollama’s `/api/generate`).
- Configure in `.env` with `MODEL_PROVIDER=ollama`, `OLLAMA_URL`, and `OLLAMA_MODEL`.
- To add another provider, implement a class that inherits `BaseProvider` and return it in `get_provider()` in `prompt_rewriter.py`.

## Configuration
- `.env` variables (loaded by `config.py`):
  - `MODEL_PROVIDER` (default: `ollama`)
  - `OLLAMA_URL` (default: `http://localhost:11434/api/generate`)
  - `OLLAMA_MODEL` (default: `gpt-oss-20b` — change to your local model)
  - `OUTPUT_DIR` (default: `enhanced_prompts`)

## Usage Tips
- Use clear verbs in your prompt (e.g., “write”, “analyze”, “summarize”) to guide the framework selector.
- The app caps selection to 3 frameworks to keep results focused.
- For best unified prompts, include a final “Rewritten Prompt” section in the model output (the composer will prefer it when present).

## Troubleshooting
- Import error: If you see `ModuleNotFoundError: providers.base_provider`, ensure imports use `from base_provider import BaseProvider` (root‑level file), not a relative import from inside `providers/`.
- Ollama connection: If you see `Ollama connection error`, verify the model is pulled and the server is running at `OLLAMA_URL`.
- Unified prompt missing/awkward: With a single framework that doesn’t expose typical fields, the composer may omit the unified section. This is by design to avoid low‑quality synthesis.

## Project Structure
```
.
├── main.py                      # CLI entrypoint
├── config.py                    # Loads .env, constants
├── framework_selector.py        # Keyword heuristic → frameworks (max 3)
├── framework_loader.py          # Loads framework definitions
├── frameworks.json              # Framework catalog
├── prompt_rewriter.py           # Per-framework generation via provider
├── prompt_composer.py           # Optional unified prompt composition
├── utils.py                     # Save markdown outputs
├── base_provider.py             # Provider interface
└── providers/
    ├── __init__.py
    └── ollama_provider.py       # Ollama REST provider
```

## Extending
- Add frameworks: Update `frameworks.json` and (optionally) extend keyword triggers in `framework_selector.py`.
- Change selection behavior: Adjust triggers or scoring; change the max cap (currently 3) in `select_frameworks()`.
- Add providers: Implement a new class extending `BaseProvider` and return it from `get_provider()`.

---
Happy prompting! If you want, open an issue or PR to suggest better selection heuristics or new frameworks.
