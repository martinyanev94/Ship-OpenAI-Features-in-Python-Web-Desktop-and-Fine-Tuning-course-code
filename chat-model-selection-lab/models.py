import csv
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OUTPUT_CSV = Path(os.getenv("COMPARISON_CSV", "comparison.csv"))

PROFILES = {
    "temperature_low": {"temperature": 0.2, "max_tokens": 180},
    "temperature_high": {"temperature": 0.8, "max_tokens": 180},
    "ceiling_short": {"temperature": 0.2, "max_tokens": 180},
    "ceiling_roomy": {"temperature": 0.2, "max_tokens": 320},
}

MESSAGES = [
    {"role": "system", "content": "Explain the issue clearly and keep the proposed fix usable."},
    {"role": "user", "content": "Explain this constrained bug-fixer case: a factorial function receives a string instead of an integer and raises a TypeError. Give a concise explanation followed by corrected Python code. Do not invent runtime output."},
]

@dataclass
class RunResult:
    profile: str
    model: str
    temperature: float
    max_tokens: int
    elapsed_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    finish_reason: str
    text: str
    error: str = ""


def run_case(client: OpenAI, model: str, profile_name: str) -> RunResult:
    settings = PROFILES[profile_name]
    started = time.perf_counter()
    try:
        response = client.chat.completions.create(model=model, messages=MESSAGES, temperature=settings["temperature"], max_tokens=settings["max_tokens"])
        elapsed = time.perf_counter() - started
        choice = response.choices[0]
        usage = response.usage
        return RunResult(profile_name, model, settings["temperature"], settings["max_tokens"], elapsed, getattr(usage, "prompt_tokens", None), getattr(usage, "completion_tokens", None), getattr(usage, "total_tokens", None), choice.finish_reason or "", choice.message.content or "")
    except Exception as exc:
        return RunResult(profile_name, model, settings["temperature"], settings["max_tokens"], time.perf_counter() - started, None, None, None, "error", "", f"{type(exc).__name__}: {exc}")


def write_csv(results: list[RunResult], path: Path) -> None:
    fields = ["profile", "model", "temperature", "max_tokens", "elapsed_seconds", "prompt_tokens", "completion_tokens", "total_tokens", "finish_reason", "text", "error"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY before running the lab.", file=sys.stderr)
        return 1
    client = OpenAI()
    results = [run_case(client, MODEL, name) for name in PROFILES]
    write_csv(results, OUTPUT_CSV)
    for result in results:
        print(f"\n[{result.profile}] model={result.model}")
        if result.error:
            print(f"error={result.error}")
            continue
        print(result.text)
        print(f"finish_reason={result.finish_reason} prompt_tokens={result.prompt_tokens} completion_tokens={result.completion_tokens} total_tokens={result.total_tokens} elapsed_seconds={result.elapsed_seconds:.3f}")
    print(f"\nWrote comparison results to {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
