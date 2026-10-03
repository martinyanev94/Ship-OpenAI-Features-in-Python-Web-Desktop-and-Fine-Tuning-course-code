# ChatGPT + DALL-E PowerPoint Generator

This project turns a topic into four slide records, generates one DALL-E image per slide, downloads numbered local assets, and assembles an openable PowerPoint deck.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
```

On Windows PowerShell, use `$env:OPENAI_API_KEY="your-key"` instead.

## Generate a deck

```bash
python slide_generator.py "Solar energy for small businesses"
```

The deck is written to `output/solar_deck.pptx`; images are written to `output/assets/`.

## Verify the artifact

```bash
python inspect_deck.py output/solar_deck.pptx
```

The verifier checks that every slide contains nonempty text and at least one image. Open the resulting `.pptx` in PowerPoint or another compatible viewer and spot-check that each image matches its slide text.

The script expects an OpenAI API key in the environment and never stores the key in source code. If generation stops partway through, inspect the reported boundary and rerun after correcting the configuration or network problem.
