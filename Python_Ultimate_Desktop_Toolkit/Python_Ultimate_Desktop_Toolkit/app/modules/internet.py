import os
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QTextEdit, QMessageBox
from app.widgets.section import make_title

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_OK = True
except Exception:
    WEBENGINE_OK = False

try:
    import qrcode
except Exception:
    qrcode = None

try:
    import requests
except Exception:
    requests = None


class InternetPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Internet Toolkit", "Browser, QR generator, speed test helper and downloader."))

        row = QHBoxLayout()
        self.url = QLineEdit("https://www.python.org")
        go = QPushButton("Open")
        go.clicked.connect(self.open_url)
        row.addWidget(self.url)
        row.addWidget(go)
        layout.addLayout(row)

        if WEBENGINE_OK:
            self.browser = QWebEngineView()
            self.browser.setMinimumHeight(280)
            layout.addWidget(self.browser)
        else:
            self.browser = None
            layout.addWidget(QLabel("QtWebEngine not available. URLs will open in your default browser."))

        qr_row = QHBoxLayout()
        self.qr_text = QLineEdit()
        self.qr_text.setPlaceholderText("Text or URL for QR code")
        qr_btn = QPushButton("Generate QR")
        qr_btn.clicked.connect(self.generate_qr)
        qr_row.addWidget(self.qr_text)
        qr_row.addWidget(qr_btn)
        layout.addLayout(qr_row)
        self.qr_preview = QLabel("QR preview")
        self.qr_preview.setMinimumHeight(160)
        layout.addWidget(self.qr_preview)

        download_row = QHBoxLayout()
        self.download_url = QLineEdit()
        self.download_url.setPlaceholderText("File URL to download")
        dl_btn = QPushButton("Download")
        dl_btn.clicked.connect(self.download_file)
        speed_btn = QPushButton("Run Speed Test")
        speed_btn.clicked.connect(self.speed_test)
        download_row.addWidget(self.download_url)
        download_row.addWidget(dl_btn)
        download_row.addWidget(speed_btn)
        layout.addLayout(download_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def open_url(self):
        url = self.url.text().strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if self.browser:
            self.browser.setUrl(QUrl(url))
        else:
            webbrowser.open(url)
        self.log(f"Opened URL: {url}")

    def generate_qr(self):
        if qrcode is None:
            QMessageBox.warning(self, "Missing dependency", "Install qrcode and Pillow to generate QR codes.")
            return
        text = self.qr_text.text().strip()
        if not text:
            return
        out_dir = Path("user_data/qr")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "qr_code.png"
        img = qrcode.make(text)
        img.save(path)
        self.qr_preview.setPixmap(QPixmap(str(path)).scaledToHeight(150))
        self.output.append(f"QR saved: {path}")
        self.log("QR generated")

    def download_file(self):
        if requests is None:
            QMessageBox.warning(self, "Missing dependency", "Install requests to use downloader.")
            return
        url = self.download_url.text().strip()
        if not url:
            return
        filename = os.path.basename(urlparse(url).path) or "downloaded_file"
        save_path, _ = QFileDialog.getSaveFileName(self, "Save download", filename)
        if not save_path:
            return
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            Path(save_path).write_bytes(r.content)
            self.output.append(f"Downloaded: {save_path}")
        except Exception as exc:
            self.output.append(f"Download failed: {exc}")

    def speed_test(self):
        try:
            import speedtest
            st = speedtest.Speedtest()
            st.get_best_server()
            down = st.download() / 1_000_000
            up = st.upload() / 1_000_000
            self.output.append(f"Download: {down:.2f} Mbps\nUpload: {up:.2f} Mbps")
        except Exception as exc:
            self.output.append(f"Speed test unavailable: {exc}")
