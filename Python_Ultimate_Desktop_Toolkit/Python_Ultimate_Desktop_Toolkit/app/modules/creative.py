from pathlib import Path
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QPixmap, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QFileDialog, QLabel, QTextEdit, QMessageBox
from app.widgets.section import make_title


class PaintCanvas(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 420)
        self.pixmap_obj = QPixmap(900, 520)
        self.pixmap_obj.fill(Qt.white)
        self.setPixmap(self.pixmap_obj)
        self.last_point = QPoint()
        self.pen_color = QColor("black")
        self.pen_width = 4

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.pixmap_obj)
            painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.setPixmap(self.pixmap_obj)

    def clear(self):
        self.pixmap_obj.fill(Qt.white)
        self.setPixmap(self.pixmap_obj)

    def save(self, path):
        self.pixmap_obj.save(path)


class CreativePage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Creative Tools", "Paint, image-to-PDF, PDF creator, color picker and AI hooks."))

        self.canvas = PaintCanvas()
        layout.addWidget(self.canvas)

        row = QHBoxLayout()
        for label, method in [
            ("Choose Color", self.choose_color), ("Clear Paint", self.canvas.clear),
            ("Save Paint", self.save_paint), ("Image to PDF", self.image_to_pdf),
            ("Text to PDF", self.text_to_pdf), ("Background Remover Info", self.bg_info)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            row.addWidget(btn)
        row.addStretch()
        layout.addLayout(row)

        self.text = QTextEdit()
        self.text.setPlaceholderText("Write text here for PDF Creator...")
        layout.addWidget(self.text)

    def choose_color(self):
        color = QColorDialog.getColor(self.canvas.pen_color, self, "Pick color")
        if color.isValid():
            self.canvas.pen_color = color

    def save_paint(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save painting", "painting.png", "PNG Image (*.png)")
        if path:
            self.canvas.save(path)
            QMessageBox.information(self, "Saved", path)

    def image_to_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose image", "", "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        save, _ = QFileDialog.getSaveFileName(self, "Save PDF", "image.pdf", "PDF Files (*.pdf)")
        if not save:
            return
        try:
            from PIL import Image
            img = Image.open(path).convert("RGB")
            img.save(save)
            QMessageBox.information(self, "PDF saved", save)
        except Exception as exc:
            QMessageBox.warning(self, "Error", f"Install Pillow. Error: {exc}")

    def text_to_pdf(self):
        save, _ = QFileDialog.getSaveFileName(self, "Save PDF", "document.pdf", "PDF Files (*.pdf)")
        if not save:
            return
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(save, pagesize=A4)
            width, height = A4
            y = height - 50
            for line in self.text.toPlainText().splitlines():
                c.drawString(50, y, line[:100])
                y -= 18
                if y < 50:
                    c.showPage(); y = height - 50
            c.save()
            QMessageBox.information(self, "PDF saved", save)
        except Exception as exc:
            QMessageBox.warning(self, "Error", f"Install reportlab. Error: {exc}")

    def bg_info(self):
        QMessageBox.information(self, "Background Remover", "For AI background removal, install rembg and add an image processing function here. The project already includes the tool hook.")
