import re
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QFileDialog, QMessageBox
from app.widgets.section import make_title


class AIAssistantPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("AI Assistant", "Offline assistant tools. API-based AI can be added later."))

        self.mode = QComboBox()
        self.mode.addItems(["Chat Assistant", "Grammar Checker", "Text Summarizer", "Translator Mock", "OCR Image to Text", "Text to Speech"])
        layout.addWidget(self.mode)

        self.input = QTextEdit()
        self.input.setPlaceholderText("Type or paste text here...")
        layout.addWidget(self.input, 2)

        row = QHBoxLayout()
        run = QPushButton("Run")
        run.clicked.connect(self.run_tool)
        clear = QPushButton("Clear")
        clear.clicked.connect(lambda: (self.input.clear(), self.output.clear()))
        row.addWidget(run)
        row.addWidget(clear)
        row.addStretch()
        layout.addLayout(row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output, 2)

    def run_tool(self):
        mode = self.mode.currentText()
        text = self.input.toPlainText().strip()
        if mode == "Chat Assistant":
            self.output.setPlainText(self.chat(text))
        elif mode == "Grammar Checker":
            self.output.setPlainText(self.grammar(text))
        elif mode == "Text Summarizer":
            self.output.setPlainText(self.summarize(text))
        elif mode == "Translator Mock":
            self.output.setPlainText("Translator placeholder: connect Google Translate/DeepL API later.\n\nInput:\n" + text)
        elif mode == "OCR Image to Text":
            self.ocr()
        elif mode == "Text to Speech":
            self.tts(text)

    def chat(self, text):
        lower = text.lower()
        if not text:
            return "Ask me something."
        if "hello" in lower or "hi" in lower:
            return "Hello! I am your offline toolkit assistant."
        if "project" in lower:
            return "This project is modular. Add new tools inside app/modules or plugins/."
        return "Offline assistant reply: I understood your message. For real AI, connect an API key later."

    def grammar(self, text):
        fixed = text
        fixed = re.sub(r"\bi\b", "I", fixed)
        fixed = re.sub(r"\s+", " ", fixed).strip()
        if fixed and fixed[-1] not in ".!?":
            fixed += "."
        return fixed or "No text provided."

    def summarize(self, text):
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) <= 2:
            return text or "No text provided."
        return " ".join(sentences[:2]) + "\n\nSummary generated using a simple offline rule."

    def ocr(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        try:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(path))
            self.output.setPlainText(text)
        except Exception as exc:
            self.output.setPlainText(f"OCR needs pytesseract plus Tesseract installed on your system.\nError: {exc}")

    def tts(self, text):
        if not text:
            return
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            self.output.setPlainText("Spoken successfully.")
        except Exception as exc:
            self.output.setPlainText(f"Text-to-speech unavailable: {exc}")
