import json
from pathlib import Path


class SettingsStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = {
            "theme": "dark",
            "accent": "#2563eb",
            "username": "Guest",
            "app_lock_enabled": False
        }
        self.load()

    def load(self):
        if self.path.exists():
            try:
                self.data.update(json.loads(self.path.read_text(encoding="utf-8")))
            except Exception:
                pass

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
