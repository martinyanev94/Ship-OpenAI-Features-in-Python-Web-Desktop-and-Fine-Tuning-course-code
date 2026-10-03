"""Inspect a live Chat Completions response: model, role, content, usage."""

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

    message = response.choices[0].message
    print("model:", response.model)
    print("role:", message.role)
    print("content:", message.content)
    print("prompt_tokens:", response.usage.prompt_tokens)
    print("completion_tokens:", response.usage.completion_tokens)
    print("total_tokens:", response.usage.total_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
