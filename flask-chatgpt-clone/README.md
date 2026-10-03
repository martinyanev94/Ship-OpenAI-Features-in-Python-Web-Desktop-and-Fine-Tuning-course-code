# Flask Chat Clone with Conversation Memory

Browser chat backed by Flask and OpenAI Chat Completions, with server-side multi-turn history.

## This milestone

Runnable chat clone: AJAX UI posts to `POST /chat`, Flask keeps a `chat_history` roles/messages list, and follow-ups that depend on earlier user facts stay coherent. `POST /reset` clears memory.

## Prerequisites

- Python 3.7 or later
- An OpenAI API key via `OPENAI_API_KEY`
- Virtual environment with packages from `requirements.txt`

## Setup

```bash
cd flask-chatgpt-clone
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="value-from-api-keys-page"
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in a browser.

### Multi-turn check

1. Send: `My name is Mira and I am learning Flask.`
2. Wait for the bot reply (do not reload the page).
3. Send: `What is my name?`
4. Expected: the second reply refers to Mira (exact wording varies).
5. Optional: click **Reset**, ask `What is my name?` again — the name should no longer be known from history.

## API contract

- `POST /chat` with JSON `{"message": "..."}`
- Success: `{"reply": "..."}`
- Empty message: HTTP 400 `{"error": "message is required"}`
- `POST /reset` clears `chat_history` back to the system message: `{"ok": true}`

## Project layout

- `app.py` — `chat_history`, `POST /chat`, `POST /reset`, serves the UI
- `templates/index.html` — chat log, Send, Reset, AJAX `fetch`
- `requirements.txt` — `flask` and `openai`

## Notes

- History lives in process memory (fine for local learning; not multi-user isolation).
- `MAX_HISTORY_MESSAGES` trims oldest non-system turns so the context list does not grow without bound.

## Next

A bug-fixer that issues multiple Chat Completions calls—one for explanation, one for a fix.
