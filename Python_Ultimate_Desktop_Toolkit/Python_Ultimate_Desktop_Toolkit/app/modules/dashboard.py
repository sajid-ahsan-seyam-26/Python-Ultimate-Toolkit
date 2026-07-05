from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from PySide6.QtCore import Qt
from app.widgets.section import make_title


FEATURES = [
    ("📝 Python IDE", "Run code, open/save files, output panel, find/replace."),
    ("📷 Camera Studio", "Webcam preview, photo capture, optional face/QR detection."),
    ("🎵 Multimedia", "Audio/video player, playlist, volume, stream URL."),
    ("🎮 Games", "Tic Tac Toe, 2048, memory game and game hub."),
    ("🌐 Internet", "Mini browser, speed test, QR generator, downloader."),
    ("📁 File Manager", "Explore, search, rename, ZIP, extract files."),
    ("🤖 AI Assistant", "Offline chat, grammar helper, summary, OCR/TTS hooks."),
    ("🛠️ Utilities", "CPU/RAM/Disk, battery, processes, screenshots."),
    ("📊 Productivity", "Calculator, notes, calendar, todo, timer."),
    ("🎨 Creative", "Paint, image editor, color picker, PDF helpers."),
]


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Python Ultimate Desktop Toolkit", "A modular all-in-one desktop application for portfolio and learning."))
        grid = QGridLayout()
        for index, (title, desc) in enumerate(FEATURES):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet("QFrame { border: 1px solid #334155; border-radius: 14px; padding: 14px; }")
            c_layout = QVBoxLayout(card)
            heading = QLabel(title)
            heading.setStyleSheet("font-size: 18px; font-weight: 800;")
            body = QLabel(desc)
            body.setWordWrap(True)
            c_layout.addWidget(heading)
            c_layout.addWidget(body)
            grid.addWidget(card, index // 2, index % 2)
        layout.addLayout(grid)
        layout.addStretch()
