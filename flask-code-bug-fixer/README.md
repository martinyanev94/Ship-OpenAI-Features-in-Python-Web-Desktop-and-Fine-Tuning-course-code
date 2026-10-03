# Flask Code Bug-Fixer

Dual Chat Completions bug-fixer with a browser UI, deployed to Azure App Service
with `OPENAI_API_KEY` supplied as a cloud application setting.

## This milestone

Package `app.py` + `requirements.txt`, deploy with the Azure CLI, set the OpenAI
key as an App Service setting (not in source), and smoke-test the public HTTPS
URL against the same factorial dual-output check used locally.

## Prerequisites

- Python 3.7 or later
- OpenAI API key in `OPENAI_API_KEY`
- Azure account (free tier signup is enough to start)
- Azure CLI (`az --version` succeeds)

## Local setup

```bash
cd flask-code-bug-fixer
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="value-from-api-keys-page"
python app.py
```

Open `http://127.0.0.1:5000/`.

## Azure deploy

See `DEPLOY_AZURE.md` for the full CLI sequence. Summary:

1. Keep the entry file named `app.py`.
2. `az login` then `az webapp up --runtime PYTHON:3.11 --sku B1` from this folder.
3. Copy the printed **Resource group** into the next commands.
4. `az webapp config appsettings set ... OPENAI_API_KEY="$OPENAI_API_KEY"` (shell must still export the key).
5. Startup: `gunicorn --bind=0.0.0.0:$PORT app:app`
6. Smoke-test `https://YOUR_APP.azurewebsites.net/` with `/health` and the factorial fixture.

Local shell export and Azure Application settings use the **same** variable name
so `os.environ.get("OPENAI_API_KEY")` in `app.py` needs no code fork.

## Fixture (local or Azure)

Paste **Code** from `samples/factorial_type_error.py` and **Error** from
`samples/factorial_type_error.txt`, then click **Code Fix**. See `FIXTURE_CHECK.md`.

## API contract

- `GET /` serves `templates/index.html`
- `GET /health` → `{"ok": true, "openai_configured": ...}`
- `POST /fix` with JSON `code` and `error`
- Success: `{"explanation": "...", "fixed_code": "..."}`
- Missing fields: HTTP 400
- Missing API key: HTTP 500

## Next

Add a SQL user database for visits and access tracking before Stripe gating.
