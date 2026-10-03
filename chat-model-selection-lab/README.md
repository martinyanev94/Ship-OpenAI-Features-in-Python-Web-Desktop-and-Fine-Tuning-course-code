# Chat Model Selection Lab

This lab compares completion settings for a constrained bug-fixer while keeping the model and messages fixed.

## Run

Create a virtual environment, install the requirements, set OPENAI_API_KEY, and run:

```bash
python models.py
```

The harness compares temperature at a fixed max_tokens value, then compares max_tokens at a fixed temperature. It prints the response, finish reason, token usage, and elapsed time, and writes comparison.csv. Record observed completeness and usage in DECISION_NOTE_TEMPLATE.md. A single run is an observation, not a universal benchmark.
