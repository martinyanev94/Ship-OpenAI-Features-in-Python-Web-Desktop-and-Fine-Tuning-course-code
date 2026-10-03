from openai import OpenAI
import json
import os

client = OpenAI()
BASE_MODEL = os.getenv("BASE_MODEL", "gpt-3.5-turbo")
CUSTOM_MODEL_ID = os.environ["CUSTOM_MODEL_ID"]
HELD_OUT_TEXT = ("A small team replaced manual document review with an automated first pass. "
                 "Editors still approve the final result, but routine checks now happen earlier.")


def summarize(model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": HELD_OUT_TEXT}],
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    base_summary = summarize(BASE_MODEL)
    custom_summary = summarize(CUSTOM_MODEL_ID)
    report = {
        "held_out_text": HELD_OUT_TEXT,
        "base_model": BASE_MODEL,
        "custom_model": CUSTOM_MODEL_ID,
        "base_summary": base_summary,
        "custom_summary": custom_summary,
        "evaluation_notes": "Review meaning, concision, and completeness.",
    }
    with open("verification_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)
    print("Saved verification_report.json")


if __name__ == "__main__":
    main()
