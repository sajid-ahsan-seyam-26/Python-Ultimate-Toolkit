import sys
from pathlib import Path

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QMessageBox
except Exception as exc:
    print("PySide6 is required. Install dependencies with: pip install -r requirements.txt")
    raise

from app.core.settings_store import SettingsStore
from app.core.logger import ActivityLogger
from app.core.theme_manager import ThemeManager
from app.core.plugin_manager import PluginManager

from app.modules.dashboard import DashboardPage
from app.modules.ide import IDEPage
from app.modules.camera import CameraPage
from app.modules.media_player import MultimediaPage
from app.modules.games import GamesPage
from app.modules.internet import InternetPage
from app.modules.file_manager import FileManagerPage
from app.modules.ai_assistant import AIAssistantPage
from app.modules.utilities import UtilitiesPage
from app.modules.productivity import ProductivityPage
from app.modules.creative import CreativePage
from app.modules.settings import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).resolve().parent
        self.settings_store = SettingsStore(self.base_dir / "user_data" / "settings.json")
        self.logger = ActivityLogger(self.base_dir / "logs" / "activity.log")
        self.theme_manager = ThemeManager(self.settings_store)

        self.setWindowTitle("Python Ultimate Desktop Toolkit")
        self.resize(1280, 780)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setObjectName("sidebar")

        self.pages = QStackedWidget()
        self.page_map = []

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(container)

        self.add_page("🏠 Dashboard", DashboardPage())
        self.add_page("📝 Python IDE", IDEPage(self.logger))
        self.add_page("📷 Camera Studio", CameraPage(self.logger))
        self.add_page("🎵 Multimedia Player", MultimediaPage(self.logger))
        self.add_page("🎮 Mini Game Center", GamesPage(self.logger))
        self.add_page("🌐 Internet Toolkit", InternetPage(self.logger))
        self.add_page("📁 File Manager", FileManagerPage(self.logger))
        self.add_page("🤖 AI Assistant", AIAssistantPage(self.logger))
        self.add_page("🛠️ System Utilities", UtilitiesPage(self.logger))
        self.add_page("📊 Productivity Suite", ProductivityPage(self.logger))
        self.add_page("🎨 Creative Tools", CreativePage(self.logger))

        self.load_plugins()
        self.add_page("⚙️ Settings", SettingsPage(self.settings_store, self.theme_manager, self.apply_theme))

        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)
        self.apply_theme()
        self.logger.log("Application started")

    def add_page(self, title, page):
        self.sidebar.addItem(title)
        self.pages.addWidget(page)
        self.page_map.append((title, page))

    def apply_theme(self):
        app = QApplication.instance()
        if app:
            app.setStyleSheet(self.theme_manager.current_stylesheet())

    def load_plugins(self):
        plugin_dir = self.base_dir / "plugins"
        manager = PluginManager(plugin_dir)
        for plugin in manager.load_plugins():
            try:
                title = plugin.get("title", "Plugin")
                page = plugin["page"]
                self.add_page(f"🔌 {title}", page)
                self.logger.log(f"Loaded plugin: {title}")
            except Exception as exc:
                self.logger.log(f"Plugin load failed: {exc}")

    def closeEvent(self, event):
        self.logger.log("Application closed")
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Python Ultimate Desktop Toolkit")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
