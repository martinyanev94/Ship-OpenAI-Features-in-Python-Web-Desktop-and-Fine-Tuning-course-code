# Stripe bug-fixer billing

## Run locally

```text
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export STRIPE_SECRET_KEY=sk_test_your_key
export STRIPE_PRICE_ID=price_your_test_price
export STRIPE_WEBHOOK_SECRET=whsec_your_forwarding_secret
python app.py
```

Use Stripe test mode. Forward Stripe test events to `http://localhost:5000/stripe/webhook` with the Stripe CLI, then complete Checkout with a Stripe test card. The webhook, not the success URL, changes `users.is_premium`.

Run tests with `pytest`.
