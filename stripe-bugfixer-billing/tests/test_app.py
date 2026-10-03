import json
import sqlite3

import app


def test_invalid_webhook_does_not_change_database(tmp_path, monkeypatch):
    database = tmp_path / "users.db"
    monkeypatch.setattr(app, "DATABASE_PATH", str(database))
    with app.db() as connection:
        connection.execute("INSERT INTO users(user_id, visits, is_premium) VALUES ('visitor-abc', 1, 0)")
        connection.commit()
    client = app.app.test_client()
    response = client.post("/stripe/webhook", data=b"forged", headers={"Stripe-Signature": "bad"})
    assert response.status_code == 400
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT is_premium FROM users WHERE user_id = 'visitor-abc'").fetchone()[0] == 0


def test_paid_completed_event_sets_premium_once(tmp_path, monkeypatch):
    database = tmp_path / "users.db"
    monkeypatch.setattr(app, "DATABASE_PATH", str(database))
    with app.db() as connection:
        connection.execute("INSERT INTO users(user_id, visits, is_premium) VALUES ('visitor-abc', 1, 0)")
        connection.commit()
    event = {"type": "checkout.session.completed", "data": {"object": {"payment_status": "paid", "metadata": {"visitor_id": "visitor-abc"}}}}
    monkeypatch.setattr(app.stripe.Webhook, "construct_event", lambda payload, signature, secret: event)
    client = app.app.test_client()
    assert client.post("/stripe/webhook", data=json.dumps(event), headers={"Stripe-Signature": "test"}).status_code == 200
    assert client.post("/stripe/webhook", data=json.dumps(event), headers={"Stripe-Signature": "test"}).status_code == 200
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT is_premium FROM users WHERE user_id = 'visitor-abc'").fetchone()[0] == 1
