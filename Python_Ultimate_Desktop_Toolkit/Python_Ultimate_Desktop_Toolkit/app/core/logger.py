from datetime import datetime
from pathlib import Path


class ActivityLogger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        with self.path.open("a", encoding="utf-8") as file:
            file.write(line)
