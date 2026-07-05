from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


def create_plugin():
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.addWidget(QLabel("This is an example plugin. Add your own .py plugin files inside the plugins folder."))
    layout.addStretch()
    return {"title": "Example Plugin", "page": page}
