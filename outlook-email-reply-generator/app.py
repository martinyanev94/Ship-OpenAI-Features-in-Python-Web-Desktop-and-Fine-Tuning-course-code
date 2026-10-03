import argparse
import os
import tkinter as tk
from tkinter import messagebox

from openai import OpenAI


FIXTURE_SUBJECT = "Personalized account activity dashboard"
FIXTURE_BODY = """Hi Martin,
I have an exciting new feature request for you. Our users have been asking for a personalized dashboard that provides an overview of their account activity and statistics.
I would appreciate it if you could start working on this feature and provide an estimate for the development effort required.
Regards,
Bill."""


def build_prompt(subject, body):
    return f"""Draft a professional reply to this email.

Subject: {subject}
Body:
{body}

Acknowledge the dashboard request and address the estimate.
Do not claim development has started or promise a deadline.
Keep the reply concise and ready for human review."""


def generate_reply(client, subject, body):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=[{"role": "user", "content": build_prompt(subject, body)}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def read_outlook_selection():
    try:
        import win32com.client

        outlook = win32com.client.Dispatch("Outlook.Application")
        selection = outlook.ActiveExplorer().Selection
        if selection.Count == 0:
            raise RuntimeError("Select an email in Outlook first.")
        item = selection.Item(1)
        if getattr(item, "MessageClass", "") != "IPM.Note":
            raise RuntimeError("The selected Outlook item is not an email.")
        return item.Subject or "(no subject)", item.Body or ""
    except ImportError as exc:
        raise RuntimeError("Outlook mode requires Windows and pywin32.") from exc
    except Exception as exc:
        raise RuntimeError(f"Could not read the Outlook selection: {exc}") from exc


def create_app(subject, body):
    client = OpenAI()
    root = tk.Tk()
    root.title("Outlook Reply Generator")
    root.geometry("760x560")

    tk.Label(root, text=f"Subject: {subject}", anchor="w").pack(fill="x", padx=12, pady=(12, 4))
    source = tk.Text(root, height=9, wrap="word")
    source.pack(fill="x", padx=12)
    source.insert("1.0", body)
    source.configure(state="disabled")

    tk.Label(root, text="Editable reply draft", anchor="w").pack(fill="x", padx=12, pady=(12, 4))
    output = tk.Text(root, height=12, wrap="word")
    output.pack(fill="both", expand=True, padx=12)

    def on_generate():
        try:
            draft = generate_reply(client, subject, body)
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.insert("1.0", draft)
        except Exception as exc:
            messagebox.showerror("Reply generation failed", str(exc))

    tk.Button(root, text="Generate draft", command=on_generate).pack(pady=12)
    return root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true", help="Use the sample email instead of Outlook")
    args = parser.parse_args()
    if args.fixture:
        subject, body = FIXTURE_SUBJECT, FIXTURE_BODY
    else:
        subject, body = read_outlook_selection()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before generating a reply.")
    create_app(subject, body).mainloop()


if __name__ == "__main__":
    main()
