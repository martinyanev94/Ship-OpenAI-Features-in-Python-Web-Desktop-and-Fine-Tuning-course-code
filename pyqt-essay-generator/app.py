import os
import sys
from pathlib import Path

from openai import OpenAI
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class EssayGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set OPENAI_API_KEY before starting the application.")
        self.client = OpenAI(api_key=api_key)
        self.model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Essay Generator")
        self.resize(900, 650)
        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)
        layout.addWidget(QLabel("Enter the topic:"))
        self.topic_input = QLineEdit(self)
        self.topic_input.setPlaceholderText("Example: Ancient Egypt")
        layout.addWidget(self.topic_input)
        controls = QVBoxLayout()
        controls.addWidget(QLabel("Select maximum completion tokens:"))
        self.length_dropdown = QComboBox(self)
        self.length_dropdown.addItems(["500", "1000", "2000", "3000", "4000"])
        controls.addWidget(self.length_dropdown)
        generate_button = QPushButton("Generate Essay", self)
        generate_button.clicked.connect(self.generate_essay)
        controls.addWidget(generate_button)
        save_button = QPushButton("Save Essay", self)
        save_button.clicked.connect(self.save_essay)
        controls.addWidget(save_button)
        layout.addLayout(controls)
        self.essay_output = QTextEdit(self)
        self.essay_output.setReadOnly(True)
        layout.addWidget(self.essay_output)

    @staticmethod
    def parse_token_limit(value):
        try:
            limit = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError("Token limit must be a whole number.") from error
        if not 1 <= limit <= 4000:
            raise ValueError("Token limit must be between 1 and 4000.")
        return limit

    def generate_essay(self):
        topic = self.topic_input.text().strip()
        if not topic:
            self.essay_output.setPlainText("Enter a topic first.")
            return
        try:
            token_limit = self.parse_token_limit(self.length_dropdown.currentText())
        except ValueError as error:
            self.essay_output.setPlainText(f"Invalid token limit: {error}")
            return
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": f"Write a clear, self-contained essay about {topic}."}],
                max_tokens=token_limit,
            )
            essay = response.choices[0].message.content or ""
            self.essay_output.setPlainText(essay)
        except Exception as error:
            self.essay_output.setPlainText(f"Generation failed: {error}")

    def save_essay(self):
        text = self.essay_output.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "Nothing to save", "Generate an essay first.")
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save essay", "essay.txt", "Text files (*.txt)")
        if filename:
            Path(filename).write_text(text + "\n", encoding="utf-8")


def main():
    app = QApplication(sys.argv)
    try:
        window = EssayGenerator()
    except RuntimeError as error:
        QMessageBox.critical(None, "Configuration error", str(error))
        return 1
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
