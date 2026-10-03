# PyQt Essay Generator with Token Controls

A PyQt6 desktop app that sends a topic to Chat Completions and exposes the maximum completion-token limit in the UI.

## Setup

Use Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python app.py
```

Set OPENAI_MODEL optionally to choose an available chat model. Never commit an API key.

## Verify length control

1. Enter Ancient Egypt.
2. Generate with 500 selected and record the observed word or character count.
3. Select 2000, generate again, and compare the new draft and its ending.
4. Confirm that the second draft replaces the first rather than appending to it.
5. Call EssayGenerator.parse_token_limit("invalid") in a temporary validation check and confirm it raises ValueError before an API request.
6. Treat the token value as a maximum completion limit, not an exact word-count promise.
