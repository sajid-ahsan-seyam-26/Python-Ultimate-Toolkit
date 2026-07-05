from pathlib import Path
from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from app.widgets.section import make_title

try:
    import cv2
except Exception:
    cv2 = None


class CameraPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        self.cap = None
        self.last_frame = None
        self.face_detection = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Camera Studio", "Webcam preview, take photo, optional face detection."))

        self.preview = QLabel("Camera preview will appear here. Install opencv-python and connect a webcam.")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(430)
        self.preview.setStyleSheet("border: 1px solid #334155; border-radius: 12px;")
        layout.addWidget(self.preview)

        buttons = QHBoxLayout()
        for text, method in [
            ("Start Camera", self.start_camera), ("Stop", self.stop_camera),
            ("Take Photo", self.take_photo), ("Toggle Face Detection", self.toggle_face_detection)
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(method)
            buttons.addWidget(btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def start_camera(self):
        if cv2 is None:
            QMessageBox.warning(self, "Missing dependency", "Install opencv-python to use the camera.")
            return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.warning(self, "Camera Error", "Could not open webcam.")
            return
        self.timer.start(30)
        self.log("Camera started")

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.preview.setText("Camera stopped.")
        self.log("Camera stopped")

    def toggle_face_detection(self):
        self.face_detection = not self.face_detection

    def update_frame(self):
        if not self.cap:
            return
        ok, frame = self.cap.read()
        if not ok:
            return
        self.last_frame = frame.copy()

        if self.face_detection and cv2 is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.preview.setPixmap(QPixmap.fromImage(image).scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def take_photo(self):
        if cv2 is None or self.last_frame is None:
            QMessageBox.information(self, "No frame", "Start the camera first.")
            return
        out_dir = Path("user_data/photos")
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = out_dir / f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(str(filename), self.last_frame)
        QMessageBox.information(self, "Saved", f"Photo saved: {filename}")
        self.log(f"Photo saved: {filename}")

    def closeEvent(self, event):
        self.stop_camera()
        super().closeEvent(event)
