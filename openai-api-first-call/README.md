# First Chat Completions Call in Python

Dead-simple verification project: authenticate with an OpenAI API key from the environment and print a Chat Completions assistant message, then inspect request/response fields before any UI.

## Prerequisites

- Python 3.7 or later
- VS Code or another editor
- An OpenAI account and API key from https://platform.openai.com/account/api-keys

## Setup

```bash
cd openai-api-first-call
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Store the API key (do not commit secrets)

macOS / Linux:

```bash
export OPENAI_API_KEY="value-from-api-keys-page"
```

Windows Command Prompt:

```bat
set OPENAI_API_KEY=value-from-api-keys-page
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "value-from-api-keys-page"
```

Optional: copy `.env.example` to `.env` for your own notes. Scripts in this project read the OS environment; do not commit `.env`.

## Verify the environment

```bash
python verify_env.py
```

Expected: `OPENAI_API_KEY is set (N characters). Ready for Chat Completions.` The script never prints the secret itself.

## Run the minimal Chat Completions script

```bash
python first_completion.py
```

Expected: a short non-empty assistant sentence about primary colors (exact wording varies). The script prints `response.choices[0].message.content`, not the full ChatCompletion object.

## Inspect request and response shape

```bash
python inspect_response.py
```

Expected labeled lines: `model`, `role` (assistant), `content` (non-empty reply), `prompt_tokens`, `completion_tokens`, and `total_tokens` (positive integers; total equals prompt plus completion).

Optional auth check (then restore your real key):

```bash
export OPENAI_API_KEY="invalid-placeholder"
python inspect_response.py   # expect AuthenticationError
export OPENAI_API_KEY="value-from-api-keys-page"
python inspect_response.py   # labeled lines again
```

Fill `RESPONSE_CHECKLIST.md` from a successful live run plus a one-line note about the broken-key symptom.

## Project layout

- `verify_env.py` — confirm the API key is present without printing it
- `first_completion.py` — one-turn Chat Completions call that prints assistant text
- `inspect_response.py` — print model, role, content, and usage token fields
- `RESPONSE_CHECKLIST.md` — documented verification milestone
- `requirements.txt` — `openai>=1.0.0`
- `.env.example` / `.gitignore` — secret-safe local setup

## Next

The following lesson builds a Flask backend that calls Chat Completions and returns assistant content from a route.
