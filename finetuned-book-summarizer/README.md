# Fine-Tuned Concise Summarizer

This project compares a base chat model with a completed fine-tuned model on held-out text.

## Verify on held-out text

Set `CUSTOM_MODEL_ID` to the identifier printed after a fine-tune job reaches `succeeded`, then run:

```bash
export CUSTOM_MODEL_ID='the-printed-model-id'
python main.py
```

The script sends the same held-out paragraph to the base model and custom model, extracts each assistant message, and saves `verification_report.json`. Inspect the report for preserved meaning, concise style, and completeness.
