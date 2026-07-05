from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QApplication, QMessageBox
from app.widgets.section import make_title

try:
    import psutil
except Exception:
    psutil = None


class UtilitiesPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("System Utilities", "CPU, RAM, disk, battery, processes, screenshot."))

        self.stats = QLabel("Stats loading...")
        self.stats.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(self.stats)

        row = QHBoxLayout()
        process_btn = QPushButton("Show Processes")
        process_btn.clicked.connect(self.show_processes)
        screenshot_btn = QPushButton("Take Screenshot")
        screenshot_btn.clicked.connect(self.take_screenshot)
        recorder_btn = QPushButton("Screen Recorder Info")
        recorder_btn.clicked.connect(self.screen_recorder_info)
        row.addWidget(process_btn)
        row.addWidget(screenshot_btn)
        row.addWidget(recorder_btn)
        row.addStretch()
        layout.addLayout(row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1500)
        self.update_stats()

    def update_stats(self):
        if psutil is None:
            self.stats.setText("Install psutil to see system stats.")
            return
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        battery = psutil.sensors_battery()
        battery_text = f"{battery.percent}%" if battery else "N/A"
        self.stats.setText(f"CPU: {cpu}%   RAM: {ram}%   Disk: {disk}%   Battery: {battery_text}")

    def show_processes(self):
        if psutil is None:
            self.output.setPlainText("Install psutil to see process list.")
            return
        lines = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                lines.append(f"{info['pid']:>6}  {info['name']:<30} CPU {info['cpu_percent']}  RAM {info['memory_percent']:.2f}%")
            except Exception:
                pass
            if len(lines) >= 120:
                break
        self.output.setPlainText("\n".join(lines))

    def take_screenshot(self):
        screen = QApplication.primaryScreen()
        if not screen:
            return
        out_dir = Path("user_data/screenshots")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pixmap = screen.grabWindow(0)
        pixmap.save(str(path))
        QMessageBox.information(self, "Screenshot", f"Saved: {path}")

    def screen_recorder_info(self):
        self.output.setPlainText("Screen recording can be added with mss + opencv-python. This project includes the UI hook for it.")
