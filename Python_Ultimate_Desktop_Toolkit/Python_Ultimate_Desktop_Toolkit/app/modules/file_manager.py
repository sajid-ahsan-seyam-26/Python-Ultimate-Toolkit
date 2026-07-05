import os
import zipfile
from pathlib import Path

from PySide6.QtCore import QDir
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTreeView,
    QFileSystemModel, QLineEdit, QTextEdit, QMessageBox, QInputDialog
)
from app.widgets.section import make_title


class FileManagerPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("File Manager", "Explore, search, rename, compress and extract files."))

        controls = QHBoxLayout()
        for label, method in [
            ("Choose Folder", self.choose_folder), ("Rename Selected", self.rename_selected),
            ("Compress ZIP", self.compress_selected), ("Extract ZIP", self.extract_zip)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            controls.addWidget(btn)
        layout.addLayout(controls)

        searchbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files in current folder")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_files)
        searchbar.addWidget(self.search_input)
        searchbar.addWidget(search_btn)
        layout.addLayout(searchbar)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        layout.addWidget(self.tree, 3)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output, 1)

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def current_path(self):
        index = self.tree.currentIndex()
        return Path(self.model.filePath(index)) if index.isValid() else None

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose folder", QDir.homePath())
        if folder:
            self.tree.setRootIndex(self.model.index(folder))
            self.log(f"File manager folder: {folder}")

    def rename_selected(self):
        path = self.current_path()
        if not path or not path.exists():
            return
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=path.name)
        if ok and new_name:
            new_path = path.with_name(new_name)
            try:
                path.rename(new_path)
                self.output.append(f"Renamed to: {new_path}")
            except Exception as exc:
                QMessageBox.warning(self, "Error", str(exc))

    def compress_selected(self):
        path = self.current_path()
        if not path or not path.exists():
            return
        zip_path, _ = QFileDialog.getSaveFileName(self, "Save ZIP", f"{path.stem}.zip", "ZIP Files (*.zip)")
        if not zip_path:
            return
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                if path.is_file():
                    zipf.write(path, path.name)
                else:
                    for file in path.rglob("*"):
                        if file.is_file():
                            zipf.write(file, file.relative_to(path.parent))
            self.output.append(f"Created ZIP: {zip_path}")
        except Exception as exc:
            QMessageBox.warning(self, "ZIP Error", str(exc))

    def extract_zip(self):
        zip_path, _ = QFileDialog.getOpenFileName(self, "Choose ZIP", "", "ZIP Files (*.zip)")
        if not zip_path:
            return
        out_dir = QFileDialog.getExistingDirectory(self, "Extract to", QDir.homePath())
        if not out_dir:
            return
        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(out_dir)
            self.output.append(f"Extracted to: {out_dir}")
        except Exception as exc:
            QMessageBox.warning(self, "Extract Error", str(exc))

    def search_files(self):
        root_index = self.tree.rootIndex()
        root_path = Path(self.model.filePath(root_index))
        term = self.search_input.text().lower().strip()
        self.output.clear()
        if not term:
            return
        count = 0
        for path in root_path.rglob("*"):
            if term in path.name.lower():
                self.output.append(str(path))
                count += 1
                if count >= 200:
                    self.output.append("Stopped at 200 results.")
                    break
        self.output.append(f"\nFound {count} result(s).")
