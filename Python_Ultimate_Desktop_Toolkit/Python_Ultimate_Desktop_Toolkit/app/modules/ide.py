import os
import re
import sys
import tempfile
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QPlainTextEdit, QTextEdit, QLineEdit, QLabel, QMessageBox
)
from app.widgets.section import make_title


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#60a5fa"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else",
            "except", "False", "finally", "for", "from", "global", "if", "import", "in", "is",
            "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return", "True", "try",
            "while", "with", "yield"
        ]
        for word in keywords:
            self.rules.append((QRegularExpression(rf"\b{word}\b"), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#34d399"))
        self.rules.append((QRegularExpression(r"'.*?'"), string_format))
        self.rules.append((QRegularExpression(r'".*?"'), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#94a3b8"))
        self.rules.append((QRegularExpression(r"#[^\n]*"), comment_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#f59e0b"))
        self.rules.append((QRegularExpression(r"\b[0-9]+\b"), number_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class IDEPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.current_file = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Python IDE", "Write, open, save and run Python code."))

        toolbar = QHBoxLayout()
        for label, action in [
            ("New", self.new_file), ("Open", self.open_file), ("Save", self.save_file),
            ("Save As", self.save_as_file), ("Run ▶", self.run_code)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(action)
            toolbar.addWidget(btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        findbar = QHBoxLayout()
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace")
        find_btn = QPushButton("Find")
        find_btn.clicked.connect(self.find_text)
        replace_btn = QPushButton("Replace All")
        replace_btn.clicked.connect(self.replace_all)
        findbar.addWidget(self.find_input)
        findbar.addWidget(self.replace_input)
        findbar.addWidget(find_btn)
        findbar.addWidget(replace_btn)
        layout.addLayout(findbar)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText('print("Hello from Python Ultimate Desktop Toolkit!")')
        self.editor.setFont(QFont("Consolas", 12))
        self.highlighter = PythonHighlighter(self.editor.document())
        layout.addWidget(self.editor, 3)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Program output will appear here...")
        layout.addWidget(QLabel("Terminal Output"))
        layout.addWidget(self.output, 1)

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def new_file(self):
        self.current_file = None
        self.editor.clear()
        self.output.clear()
        self.log("IDE new file")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py);;All Files (*)")
        if path:
            self.current_file = Path(path)
            self.editor.setPlainText(self.current_file.read_text(encoding="utf-8"))
            self.log(f"Opened file: {path}")

    def save_file(self):
        if not self.current_file:
            return self.save_as_file()
        self.current_file.write_text(self.editor.toPlainText(), encoding="utf-8")
        self.log(f"Saved file: {self.current_file}")

    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Python File", "script.py", "Python Files (*.py);;All Files (*)")
        if path:
            self.current_file = Path(path)
            self.save_file()

    def run_code(self):
        code = self.editor.toPlainText()
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += "\n--- ERRORS ---\n" + result.stderr
            self.output.setPlainText(output or "Code executed successfully. No output.")
            self.log("Executed Python code")
        except subprocess.TimeoutExpired:
            self.output.setPlainText("Execution stopped: code took longer than 15 seconds.")
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def find_text(self):
        term = self.find_input.text()
        if not term:
            return
        found = self.editor.find(term)
        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(cursor.Start)
            self.editor.setTextCursor(cursor)
            self.editor.find(term)

    def replace_all(self):
        find = self.find_input.text()
        replace = self.replace_input.text()
        if not find:
            return
        text = self.editor.toPlainText().replace(find, replace)
        self.editor.setPlainText(text)
        self.log("IDE replace all")
