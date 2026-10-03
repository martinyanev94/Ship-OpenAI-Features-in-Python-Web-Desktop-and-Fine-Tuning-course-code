# Outlook Email Reply Generator

This Windows-oriented Tkinter app reads the selected Outlook email through `win32com`, sends its subject and body to Chat Completions, and displays an editable draft. It also supports a deterministic fixture mode for testing the prompt and review workflow without Outlook.

## Setup

```text
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
set OPENAI_API_KEY=your-key
```

On macOS or Linux, use the platform-specific virtual-environment activation command. Fixture mode does not require Outlook, but it still requires an API key for generation.

## Run the activity

```text
python app.py --fixture
```

Review the generated draft against `sample_email.txt`. It should mention the personalized dashboard and account activity, address the request for an estimate, use a professional tone, and avoid claiming that development has started or promising a deadline.

## Run with Outlook on Windows

Open Outlook, select an email, then run:

```text
python app.py
```

The app displays the selected subject and body and never sends a message automatically. Review and edit the draft before using it elsewhere.
