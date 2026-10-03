# Django quiz generator

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
export OPENAI_API_KEY="your-key"
python manage.py runserver
```

Open `http://127.0.0.1:8000/`, generate a quiz, reload the history page, and use its Download link. The downloaded text is built from the persisted `Quiz` and related `Question` rows.
