"""Flask chat clone with server-side multi-turn conversation memory."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant in a browser chat clone.",
}

# Module-level conversation state: roles/messages list sent to Chat Completions.
chat_history = [SYSTEM_MESSAGE.copy()]
MAX_HISTORY_MESSAGES = 20


def _trim_history() -> None:
    """Keep the system message plus the newest turns under the cap."""
    system = chat_history[:1]
    rest = chat_history[1:]
    limit = MAX_HISTORY_MESSAGES - 1
    if len(rest) > limit:
        rest = rest[-limit:]
    chat_history[:] = system + rest


@app.route("/")
def index():
    """Serve the browser chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Accept JSON {"message": "..."}, append to history, return {"reply": "..."}."""
    if client is None:
        return jsonify({"error": "OPENAI_API_KEY is not set on the server."}), 500

    data = request.get_json(silent=True) or {}
    user_text = (data.get("message") or "").strip()
    if not user_text:
        return jsonify({"error": "message is required"}), 400

    chat_history.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    _trim_history()
    return jsonify({"reply": reply})


@app.route("/reset", methods=["POST"])
def reset():
    """Clear conversation memory back to the system message only."""
    chat_history[:] = [SYSTEM_MESSAGE.copy()]
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
