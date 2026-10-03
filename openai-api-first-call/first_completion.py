"""Minimal Chat Completions call: one user message, print assistant text."""

from __future__ import annotations

import os
import sys

from openai import OpenAI


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. Export it in this shell before running scripts.",
            file=sys.stderr,
        )
        return 1

    client = OpenAI(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": "Name three primary colors in one short sentence.",
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    print(response.choices[0].message.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
