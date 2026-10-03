"""Flask code bug-fixer with dual Chat Completions and text-area UI."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1024
TEMPERATURE = 0.2


def _explain_error(code: str, error: str) -> str:
    """Ask Chat Completions for a plain-English explanation without a rewrite."""
    explain_prompt = (
        "Explain the error in this code without fixing it:"
        f"\n\n{code}\n\nError:\n\n{error}"
    )
    explain_completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": explain_prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return explain_completion.choices[0].message.content


def _fix_code(code: str, error: str) -> str:
    """Ask Chat Completions for corrected source only."""
    fix_prompt = (
        f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
        " \n Respond only with the fixed code."
    )
    fix_completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": fix_prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return fix_completion.choices[0].message.content


@app.route("/")
def index():
    """Serve the bug-fixer text-area UI."""
    return render_template("index.html")


@app.route("/fix", methods=["POST"])
def fix_code():
    """Accept JSON {code, error}; return {explanation, fixed_code} via two creates."""
    if client is None:
        return jsonify({"error": "OPENAI_API_KEY is not set on the server."}), 500

    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    error = (data.get("error") or "").strip()
    if not code or not error:
        return jsonify({"error": "code and error are required"}), 400

    explanation = _explain_error(code, error)
    fixed_code = _fix_code(code, error)
    return jsonify({"explanation": explanation, "fixed_code": fixed_code})


@app.route("/health")
def health():
    """Simple liveness check for local and Azure smoke tests."""
    return jsonify({"ok": True, "openai_configured": client is not None})


if __name__ == "__main__":
    # Local only. On Azure App Service, gunicorn loads `app:app`.
    app.run(debug=True)
