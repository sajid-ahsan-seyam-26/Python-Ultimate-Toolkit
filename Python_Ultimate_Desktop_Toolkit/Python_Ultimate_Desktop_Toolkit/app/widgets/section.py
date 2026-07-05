from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


def make_title(text, subtitle=None):
    wrapper = QWidget()
    layout = QVBoxLayout(wrapper)
    layout.setContentsMargins(0, 0, 0, 10)
    title = QLabel(text)
    title.setObjectName("title")
    layout.addWidget(title)
    if subtitle:
        sub = QLabel(subtitle)
        sub.setObjectName("subtitle")
        sub.setWordWrap(True)
        layout.addWidget(sub)
    return wrapper


def centered_label(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setWordWrap(True)
    return label
