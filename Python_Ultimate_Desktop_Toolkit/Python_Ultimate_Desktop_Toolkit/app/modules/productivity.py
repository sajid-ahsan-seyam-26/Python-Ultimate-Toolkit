import ast
import operator as op
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QTimer, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QListWidget, QTabWidget, QCalendarWidget, QSpinBox, QMessageBox
)
from app.widgets.section import make_title


OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg, ast.Mod: op.mod}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](eval_node(node.operand))
        raise ValueError("Unsupported expression")
    return eval_node(ast.parse(expr, mode="eval").body)


class CalculatorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.expr = QLineEdit()
        self.expr.setPlaceholderText("Example: (20 + 5) * 3")
        self.result = QLabel("Result:")
        btn = QPushButton("Calculate")
        btn.clicked.connect(self.calculate)
        layout.addWidget(self.expr); layout.addWidget(btn); layout.addWidget(self.result); layout.addStretch()

    def calculate(self):
        try:
            self.result.setText(f"Result: {safe_eval(self.expr.text())}")
        except Exception as exc:
            self.result.setText(f"Error: {exc}")


class NotesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.path = Path("user_data/notes.txt")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        layout = QVBoxLayout(self)
        self.notes = QTextEdit()
        if self.path.exists():
            self.notes.setPlainText(self.path.read_text(encoding="utf-8"))
        save = QPushButton("Save Notes")
        save.clicked.connect(self.save)
        layout.addWidget(self.notes); layout.addWidget(save)

    def save(self):
        self.path.write_text(self.notes.toPlainText(), encoding="utf-8")
        QMessageBox.information(self, "Saved", "Notes saved.")


class TodoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText("New task")
        add = QPushButton("Add"); add.clicked.connect(self.add_task)
        done = QPushButton("Remove Selected"); done.clicked.connect(self.remove_task)
        row.addWidget(self.input); row.addWidget(add); row.addWidget(done)
        self.list = QListWidget()
        layout.addLayout(row); layout.addWidget(self.list)

    def add_task(self):
        text = self.input.text().strip()
        if text:
            self.list.addItem(text)
            self.input.clear()

    def remove_task(self):
        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))


class TimerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.remaining = 0
        self.elapsed = 0
        layout = QVBoxLayout(self)
        self.stopwatch = QLabel("Stopwatch: 00:00")
        self.timer_label = QLabel("Timer: 00:00")
        self.minutes = QSpinBox(); self.minutes.setRange(1, 240); self.minutes.setValue(5); self.minutes.setSuffix(" minutes")
        row = QHBoxLayout()
        start_sw = QPushButton("Start Stopwatch"); start_sw.clicked.connect(self.start_stopwatch)
        reset_sw = QPushButton("Reset Stopwatch"); reset_sw.clicked.connect(self.reset_stopwatch)
        start_timer = QPushButton("Start Timer"); start_timer.clicked.connect(self.start_timer)
        row.addWidget(start_sw); row.addWidget(reset_sw); row.addWidget(self.minutes); row.addWidget(start_timer)
        layout.addWidget(self.stopwatch); layout.addWidget(self.timer_label); layout.addLayout(row); layout.addStretch()
        self.sw_timer = QTimer(); self.sw_timer.timeout.connect(self.tick_stopwatch)
        self.count_timer = QTimer(); self.count_timer.timeout.connect(self.tick_timer)

    def start_stopwatch(self):
        self.sw_timer.start(1000)

    def reset_stopwatch(self):
        self.elapsed = 0; self.sw_timer.stop(); self.stopwatch.setText("Stopwatch: 00:00")

    def tick_stopwatch(self):
        self.elapsed += 1
        self.stopwatch.setText(f"Stopwatch: {self.elapsed//60:02d}:{self.elapsed%60:02d}")

    def start_timer(self):
        self.remaining = self.minutes.value() * 60
        self.count_timer.start(1000)

    def tick_timer(self):
        self.remaining -= 1
        self.timer_label.setText(f"Timer: {self.remaining//60:02d}:{self.remaining%60:02d}")
        if self.remaining <= 0:
            self.count_timer.stop(); QMessageBox.information(self, "Timer", "Time is up!")


class ProductivityPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Productivity Suite", "Calculator, notes, calendar, todo, stopwatch and timer."))
        tabs = QTabWidget()
        tabs.addTab(CalculatorTab(), "Calculator")
        tabs.addTab(NotesTab(), "Notes")
        tabs.addTab(QCalendarWidget(), "Calendar")
        tabs.addTab(TodoTab(), "To-Do")
        tabs.addTab(TimerTab(), "Timer")
        layout.addWidget(tabs)
