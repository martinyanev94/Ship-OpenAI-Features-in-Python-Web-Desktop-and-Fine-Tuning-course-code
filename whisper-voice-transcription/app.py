import os
import threading
import tkinter as tk
from pathlib import Path
from tempfile import TemporaryDirectory
from tkinter import filedialog, messagebox, ttk

from openai import OpenAI
from pydub import AudioSegment

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
CHUNK_MS = 5 * 60 * 1000
MODEL = "whisper-1"


class WhisperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Voice transcription and translation")
        self.root.geometry("1000x650")
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.audio_path: Path | None = None

        toolbar = ttk.Frame(root, padding=10)
        toolbar.pack(fill="x")
        self.file_label = ttk.Label(toolbar, text="No audio file selected")
        self.file_label.pack(side="left", padx=(0, 12))
        ttk.Button(toolbar, text="Choose audio", command=self.choose_audio).pack(side="left")
        self.run_button = ttk.Button(toolbar, text="Process audio", command=self.start_processing)
        self.run_button.pack(side="left", padx=8)

        panes = ttk.Frame(root, padding=(10, 0, 10, 10))
        panes.pack(fill="both", expand=True)
        panes.columnconfigure(0, weight=1)
        panes.columnconfigure(1, weight=1)
        panes.rowconfigure(1, weight=1)

        ttk.Label(panes, text="Transcript").grid(row=0, column=0, sticky="w")
        ttk.Label(panes, text="English translation").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.transcript_box = tk.Text(panes, wrap="word", state="disabled")
        self.translation_box = tk.Text(panes, wrap="word", state="disabled")
        self.transcript_box.grid(row=1, column=0, sticky="nsew")
        self.translation_box.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        self.status = ttk.Label(root, text="Choose an audio file to begin", padding=10)
        self.status.pack(fill="x")

    def choose_audio(self) -> None:
        selected = filedialog.askopenfilename(
            title="Choose an audio file",
            filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.mp4 *.mpeg *.webm"), ("All files", "*.*")],
        )
        if selected:
            self.audio_path = Path(selected)
            self.file_label.config(text=self.audio_path.name)
            self.status.config(text="Audio selected. Ready to process.")

    def start_processing(self) -> None:
        if self.audio_path is None:
            messagebox.showwarning("Missing audio", "Choose an audio file first.")
            return
        if not os.environ.get("OPENAI_API_KEY"):
            messagebox.showerror("Missing API key", "Set OPENAI_API_KEY before starting the app.")
            return
        self.run_button.config(state="disabled")
        self.status.config(text="Processing audio...")
        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self) -> None:
        try:
            transcript, translation = process_file(self.client, self.audio_path)
        except Exception as exc:
            self.root.after(0, lambda: self.show_error(str(exc)))
            return
        self.root.after(0, lambda: self.show_results(transcript, translation))

    def show_results(self, transcript: str, translation: str) -> None:
        replace_text(self.transcript_box, transcript)
        replace_text(self.translation_box, translation)
        self.status.config(text="Processing complete. Review both outputs.")
        self.run_button.config(state="normal")

    def show_error(self, message: str) -> None:
        self.status.config(text="Processing failed.")
        self.run_button.config(state="normal")
        messagebox.showerror("Audio processing error", message)


def request_text(client: OpenAI, audio_path: Path, operation: str) -> str:
    with audio_path.open("rb") as audio_file:
        if operation == "transcription":
            response = client.audio.transcriptions.create(model=MODEL, file=audio_file)
        else:
            response = client.audio.translations.create(model=MODEL, file=audio_file)
    return response.text.strip()


def process_file(client: OpenAI, audio_path: Path | None) -> tuple[str, str]:
    if audio_path is None or not audio_path.exists():
        raise ValueError("The selected audio file is unavailable.")
    if audio_path.stat().st_size == 0:
        raise ValueError("The selected audio file is empty.")
    if audio_path.stat().st_size <= MAX_UPLOAD_BYTES:
        return request_text(client, audio_path, "transcription"), request_text(client, audio_path, "translation")

    audio = AudioSegment.from_file(audio_path)
    if len(audio) == 0:
        raise ValueError("The audio contains no duration.")
    transcript_parts: list[str] = []
    translation_parts: list[str] = []
    with TemporaryDirectory(prefix="whisper_chunks_") as directory:
        temporary_dir = Path(directory)
        for start in range(0, len(audio), CHUNK_MS):
            chunk = audio[start:start + CHUNK_MS]
            chunk_path = temporary_dir / f"chunk_{start:012d}.wav"
            chunk.export(chunk_path, format="wav")
            if chunk_path.stat().st_size == 0:
                raise ValueError(f"Chunk at {start} ms exported with no data.")
            transcript_parts.append(request_text(client, chunk_path, "transcription"))
            translation_parts.append(request_text(client, chunk_path, "translation"))
    return " ".join(part for part in transcript_parts if part), " ".join(part for part in translation_parts if part)


def replace_text(widget: tk.Text, value: str) -> None:
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert("1.0", value)
    widget.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    WhisperApp(root)
    root.mainloop()
