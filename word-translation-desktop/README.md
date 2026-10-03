# Word Document Translator

A Tkinter desktop app that extracts paragraph text from a `.docx` file and sends it to Chat Completions for translation.

## Requirements

- Python 3.7 or later
- An OpenAI API key
- A `.docx` Word document
- Tkinter available in the Python installation

## Setup

From this directory, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set the API key without placing it in source code:

```bash
export OPENAI_API_KEY="your-key"
```

Optionally choose a model supported by your account:

```bash
export OPENAI_MODEL="gpt-3.5-turbo"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "gpt-3.5-turbo"
```

Run the application:

```bash
python app.py
```

## Verify the workflow

1. Select **Load Word document** and choose a `.docx` file containing paragraph text.
2. Confirm the extracted paragraphs appear in the **Source text** pane.
3. Choose a target language.
4. Select **Translate**.
5. Confirm the translated assistant content appears in the read-only **Translated text** pane.

If the source pane is empty, the document may contain no nonempty paragraphs. If translation fails, confirm the environment variable and the configured model before changing the document logic.
