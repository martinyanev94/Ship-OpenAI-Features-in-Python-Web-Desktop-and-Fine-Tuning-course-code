import hashlib
import os
import secrets
import sqlite3
from pathlib import Path

import stripe
from flask import Flask, jsonify, redirect, request, render_template, make_response

app = Flask(__name__)
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("users.db")))
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")


def db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, visits INTEGER NOT NULL DEFAULT 0, is_premium INTEGER NOT NULL DEFAULT 0)")
    return connection


def visitor_id_from_request():
    raw = request.cookies.get("visitor_id")
    if raw:
        return raw
    return secrets.token_urlsafe(18)


def ensure_visitor(visitor_id):
    with db() as connection:
        connection.execute("INSERT INTO users(user_id, visits) VALUES (?, 1) ON CONFLICT(user_id) DO UPDATE SET visits = visits + 1", (visitor_id,))
        connection.commit()


def set_premium(visitor_id):
    with db() as connection:
        connection.execute("UPDATE users SET is_premium = 1 WHERE user_id = ?", (visitor_id,))
        connection.commit()


def is_premium(visitor_id):
    with db() as connection:
        row = connection.execute("SELECT is_premium FROM users WHERE user_id = ?", (visitor_id,)).fetchone()
    return bool(row and row[0])


@app.get("/")
def index():
    visitor_id = visitor_id_from_request()
    ensure_visitor(visitor_id)
    response = make_response(render_template("index.html", premium=is_premium(visitor_id)))
    response.set_cookie("visitor_id", visitor_id, httponly=True, samesite="Lax")
    return response


@app.post("/checkout")
def checkout():
    visitor_id = visitor_id_from_request()
    ensure_visitor(visitor_id)
    if not stripe.api_key or not STRIPE_PRICE_ID:
        return jsonify(error="Stripe is not configured"), 500
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
        client_reference_id=visitor_id,
        metadata={"visitor_id": visitor_id},
        success_url=os.environ.get("SUCCESS_URL", "http://localhost:5000/?checkout=success"),
        cancel_url=os.environ.get("CANCEL_URL", "http://localhost:5000/?checkout=cancelled"),
    )
    return redirect(session.url, code=303)


@app.post("/stripe/webhook")
def stripe_webhook():
    payload = request.get_data()
    signature = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, signature, WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify(error="invalid webhook"), 400
    session = event["data"]["object"]
    if event["type"] == "checkout.session.completed" and session.get("payment_status") == "paid":
        visitor_id = session.get("metadata", {}).get("visitor_id") or session.get("client_reference_id")
        if visitor_id:
            set_premium(visitor_id)
    return jsonify(received=True)


@app.post("/fix")
def fix():
    visitor_id = visitor_id_from_request()
    ensure_visitor(visitor_id)
    if not is_premium(visitor_id):
        return jsonify(error="Premium access required", checkout_url="/checkout"), 402
    body = request.get_json(silent=True) or {}
    code = body.get("code", "").strip()
    error = body.get("error", "").strip()
    if not code or not error:
        return jsonify(error="code and error are required"), 400
    return jsonify(explanation="Premium access confirmed; connect the existing OpenAI fix flow here.", fixed_code=code)


@app.get("/health")
def health():
    return jsonify(ok=True, stripe_configured=bool(stripe.api_key and STRIPE_PRICE_ID))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
