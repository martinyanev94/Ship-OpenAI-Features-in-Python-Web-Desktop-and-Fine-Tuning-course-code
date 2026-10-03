# Deploy Code Bug Fixer to Azure App Service

## Packaging checklist

- Entry file must be named `app.py` (Azure Python default).
- `requirements.txt` lists `flask`, `openai`, and `gunicorn`.
- Secrets stay out of git; use `.env.example` locally and Azure Application settings in the cloud.

## CLI (teaching example values)

Replace `bugfixer-demo` / `bugfixer-rg-8801` with the unique app name you choose and the
**Resource group** line printed by `az webapp up`.

```bash
# macOS example — install CLI, then verify
brew update && brew install azure-cli
az --version

az login
cd flask-code-bug-fixer
# PYTHON:3.11 = remote interpreter; B1 = Basic plan for this demo
az webapp up --runtime PYTHON:3.11 --sku B1 --name bugfixer-demo
# Sample up output:
#   Name: bugfixer-demo
#   Resource group: bugfixer-rg-8801
#   URL: https://bugfixer-demo.azurewebsites.net

# Same shell must still have OPENAI_API_KEY exported so "$OPENAI_API_KEY" expands
az webapp config appsettings set \
  --name bugfixer-demo \
  --resource-group bugfixer-rg-8801 \
  --settings OPENAI_API_KEY="$OPENAI_API_KEY"

# gunicorn serves module:object (app.py -> Flask `app`) on the platform $PORT
az webapp config set \
  --name bugfixer-demo \
  --resource-group bugfixer-rg-8801 \
  --startup-file "gunicorn --bind=0.0.0.0:$PORT app:app"
```

## Smoke test

1. Open `https://bugfixer-demo.azurewebsites.net/`
2. `GET /health` should include `"ok": true`
3. Submit `samples/factorial_type_error.py` + `samples/factorial_type_error.txt`
4. Confirm dual outputs match local fidelity checks in `FIXTURE_CHECK.md`

If `/fix` reports a missing key, the deploy worked but Application settings did not.
