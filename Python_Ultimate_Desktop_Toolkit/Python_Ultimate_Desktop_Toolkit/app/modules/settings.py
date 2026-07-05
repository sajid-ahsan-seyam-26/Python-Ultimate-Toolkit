from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox
from app.widgets.section import make_title


class SettingsPage(QWidget):
    def __init__(self, settings_store, theme_manager, apply_callback):
        super().__init__()
        self.settings = settings_store
        self.theme_manager = theme_manager
        self.apply_callback = apply_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Settings", "Theme, accent color, username and app preferences."))

        self.theme = QComboBox()
        self.theme.addItems(["dark", "light"])
        self.theme.setCurrentText(self.settings.get("theme", "dark"))

        self.accent = QLineEdit(self.settings.get("accent", "#2563eb"))
        self.username = QLineEdit(self.settings.get("username", "Guest"))

        layout.addWidget(QLabel("Theme")); layout.addWidget(self.theme)
        layout.addWidget(QLabel("Accent color HEX")); layout.addWidget(self.accent)
        layout.addWidget(QLabel("Username")); layout.addWidget(self.username)

        save = QPushButton("Save Settings")
        save.clicked.connect(self.save)
        layout.addWidget(save)
        layout.addStretch()

    def save(self):
        self.settings.set("theme", self.theme.currentText())
        self.settings.set("accent", self.accent.text().strip() or "#2563eb")
        self.settings.set("username", self.username.text().strip() or "Guest")
        self.apply_callback()
        QMessageBox.information(self, "Settings", "Settings saved.")
