# Whisper voice transcription and translation

This desktop app selects an audio file, sends it through separate transcription and English-translation requests, and displays both results. Files larger than 25 MB are decoded with PyDub, split into ordered five-minute chunks, processed one chunk at a time, and joined chronologically.

## Setup

Use Python 3.10 or later, create a virtual environment, and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set the API key in the shell that launches the app:

```bash
export OPENAI_API_KEY="your-key-here"
python app.py
```

On Windows PowerShell, use `$env:OPENAI_API_KEY = "your-key-here"` instead. Never commit the key.

PyDub may require FFmpeg for compressed formats such as MP3 or M4A. Install FFmpeg separately and make sure its executable is available on your PATH. WAV input avoids that decoding dependency.

## Verify the workflow

1. Choose an audio sample.
2. Select `Process audio`.
3. Confirm that the Transcript pane contains the spoken-language text.
4. Confirm that the English translation pane contains the English result.
5. Use an oversized file when available and verify that the beginning and ending content remain in chronological order.
6. Inspect boundary wording manually; a chunk boundary can split a word, so the joined text may need editorial review.

The application checks empty files, empty decoded audio, missing keys, missing selections, and zero-byte exported chunks before presenting results.
