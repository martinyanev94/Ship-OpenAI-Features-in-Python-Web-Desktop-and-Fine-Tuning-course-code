import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from docx import Document
from openai import OpenAI


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Document Translator")
        self.root.geometry("1000x650")

        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.language_var = tk.StringVar(value="Spanish")

        self._build_ui()

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        controls = ttk.Frame(self.root, padding=10)
        controls.grid(row=0, column=0, sticky="ew")
        controls.columnconfigure(3, weight=1)

        ttk.Button(controls, text="Load Word document", command=self.load_document).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Label(controls, text="Target language:").grid(row=0, column=1, padx=(0, 6))
        language_picker = ttk.Combobox(
            controls,
            textvariable=self.language_var,
            values=("Spanish", "French", "German", "Italian", "English"),
            state="readonly",
            width=16,
        )
        language_picker.grid(row=0, column=2, padx=(0, 8))
        ttk.Button(controls, text="Translate", command=self.translate_document).grid(
            row=0, column=3, sticky="w"
        )

        panes = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        panes.grid(row=1, column=0, sticky="nsew")
        panes.columnconfigure(0, weight=1)
        panes.columnconfigure(1, weight=1)
        panes.rowconfigure(1, weight=1)

        ttk.Label(panes, text="Source text").grid(row=0, column=0, sticky="w", padx=(0, 6))
        ttk.Label(panes, text="Translated text").grid(row=0, column=1, sticky="w", padx=(6, 0))

        self.source_text = tk.Text(panes, wrap="word")
        self.source_text.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        self.translated_text = tk.Text(panes, wrap="word", state="disabled")
        self.translated_text.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

    def load_document(self):
        path = filedialog.askopenfilename(
            filetypes=[("Word documents", "*.docx")]
        )
        if not path:
            return

        try:
            document = Document(path)
            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]
            source_text = "\n".join(paragraphs)
        except Exception as exc:
            messagebox.showerror("Document error", str(exc))
            return

        self.source_text.delete("1.0", "end")
        self.source_text.insert("1.0", source_text)

        if not source_text:
            messagebox.showwarning(
                "No paragraph text",
                "The document did not contain nonempty paragraphs.",
            )

    def translate_document(self):
        source_text = self.source_text.get("1.0", "end-1c").strip()
        target_language = self.language_var.get().strip()

        if not source_text:
            messagebox.showwarning("Missing text", "Load a Word document first.")
            return
        if not target_language:
            messagebox.showwarning("Missing language", "Choose a target language.")
            return
        if self.client is None:
            messagebox.showerror(
                "Missing API key",
                "Set OPENAI_API_KEY before starting the application.",
            )
            return

        messages = [
            {
                "role": "system",
                "content": (
                    "Translate the supplied document accurately. "
                    "Preserve paragraph breaks and return only the translation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Target language: {target_language}\n\n"
                    f"Document text:\n{source_text}"
                ),
            },
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            translated_text = response.choices[0].message.content.strip()
        except Exception as exc:
            messagebox.showerror("Translation failed", str(exc))
            return

        self.translated_text.config(state="normal")
        self.translated_text.delete("1.0", "end")
        self.translated_text.insert("1.0", translated_text)
        self.translated_text.config(state="disabled")


def main():
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
