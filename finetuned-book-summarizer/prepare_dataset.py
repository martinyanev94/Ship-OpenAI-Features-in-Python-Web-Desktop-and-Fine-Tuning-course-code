from pathlib import Path
import json
import sys


def validate(path: Path) -> int:
    errors = []
    lines = path.read_text(encoding="utf-8").splitlines()
    nonempty = [line for line in lines if line.strip()]

    for line_number, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON ({exc.msg})")
            continue
        messages = row.get("messages")
        if not isinstance(messages, list) or len(messages) != 2:
            errors.append(f"line {line_number}: expected two messages")
            continue
        roles = [message.get("role") for message in messages]
        if roles != ["user", "assistant"]:
            errors.append(f"line {line_number}: roles must be user, assistant")
        for message in messages:
            content = message.get("content")
            if not isinstance(content, str) or not content.strip():
                errors.append(f"line {line_number}: content cannot be empty")
        assistant_content = messages[1].get("content", "")
        if "\n" in assistant_content:
            errors.append(f"line {line_number}: assistant content must be one line")

    if len(nonempty) < 4:
        errors.append("dataset must contain at least four examples")
    if errors:
        raise ValueError("\n".join(errors))
    return len(nonempty)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python prepare_dataset.py data/train.jsonl", file=sys.stderr)
        raise SystemExit(2)
    try:
        count = validate(Path(sys.argv[1]))
        print(f"validated {count} JSONL examples")
    except (OSError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
