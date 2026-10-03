"""Confirm OPENAI_API_KEY is available without printing the secret."""

from __future__ import annotations

import os
import sys


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. Export it in this shell before running scripts.",
            file=sys.stderr,
        )
        return 1
    print(
        f"OPENAI_API_KEY is set ({len(api_key)} characters). "
        "Ready for Chat Completions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
