class ThemeManager:
    def __init__(self, settings_store):
        self.settings = settings_store

    def current_stylesheet(self):
        theme = self.settings.get("theme", "dark")
        accent = self.settings.get("accent", "#2563eb")
        if theme == "light":
            return self.light(accent)
        return self.dark(accent)

    def dark(self, accent):
        return f"""
            QWidget {{
                background: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            QMainWindow {{ background: #0f172a; }}
            QLabel#title {{ font-size: 28px; font-weight: 800; color: white; }}
            QLabel#subtitle {{ color: #94a3b8; font-size: 15px; }}
            QListWidget#sidebar {{
                background: #020617;
                border: none;
                padding: 10px;
            }}
            QListWidget#sidebar::item {{
                padding: 12px 10px;
                border-radius: 8px;
                margin: 2px 0;
            }}
            QListWidget#sidebar::item:selected {{
                background: {accent};
                color: white;
            }}
            QPushButton {{
                background: {accent};
                border: none;
                color: white;
                padding: 9px 12px;
                border-radius: 8px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: #1d4ed8; }}
            QLineEdit, QTextEdit, QPlainTextEdit, QTreeView, QListWidget, QTableWidget, QSpinBox, QComboBox {{
                background: #111827;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
                color: #e5e7eb;
            }}
            QTabWidget::pane {{ border: 1px solid #334155; border-radius: 8px; }}
            QTabBar::tab {{ background: #111827; padding: 9px 14px; border-radius: 8px; margin: 2px; }}
            QTabBar::tab:selected {{ background: {accent}; }}
        """

    def light(self, accent):
        return f"""
            QWidget {{
                background: #f8fafc;
                color: #0f172a;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14px;
            }}
            QLabel#title {{ font-size: 28px; font-weight: 800; color: #0f172a; }}
            QLabel#subtitle {{ color: #475569; font-size: 15px; }}
            QListWidget#sidebar {{
                background: #e2e8f0;
                border: none;
                padding: 10px;
            }}
            QListWidget#sidebar::item {{
                padding: 12px 10px;
                border-radius: 8px;
                margin: 2px 0;
            }}
            QListWidget#sidebar::item:selected {{
                background: {accent};
                color: white;
            }}
            QPushButton {{
                background: {accent};
                border: none;
                color: white;
                padding: 9px 12px;
                border-radius: 8px;
                font-weight: 600;
            }}
            QLineEdit, QTextEdit, QPlainTextEdit, QTreeView, QListWidget, QTableWidget, QSpinBox, QComboBox {{
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 6px;
                color: #0f172a;
            }}
            QTabWidget::pane {{ border: 1px solid #cbd5e1; border-radius: 8px; }}
            QTabBar::tab {{ background: #e2e8f0; padding: 9px 14px; border-radius: 8px; margin: 2px; }}
            QTabBar::tab:selected {{ background: {accent}; color: white; }}
        """
