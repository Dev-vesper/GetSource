from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from src.internals.scanner import matches_extension, parse_extensions, scan_folder


class PickerDialog(QDialog):
    """Dialog for selecting files inside a folder with checkbox support."""

    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.folder = Path(folder)
        self.setWindowTitle(f"Pick files - {self.folder.name or self.folder}")
        self.resize(600, 540)
        self._build_ui()
        self._load_files()

    def _build_ui(self):
        """Build the dialog layout."""
        layout = QVBoxLayout(self)

        self.info = QLabel(f"Folder: {self.folder}")
        layout.addWidget(self.info)

        ext_row = QHBoxLayout()
        ext_row.addWidget(QLabel("Extensions:"))
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("e.g. py, ml")
        self.ext_input.returnPressed.connect(self.apply_extensions)
        ext_row.addWidget(self.ext_input)
        apply_btn = QPushButton("Select matching")
        apply_btn.clicked.connect(self.apply_extensions)
        ext_row.addWidget(apply_btn)
        layout.addLayout(ext_row)

        self.list = QListWidget()
        layout.addWidget(self.list)

        sel_row = QHBoxLayout()
        select_all = QPushButton("Select all")
        select_all.clicked.connect(self._select_all)
        clear_sel = QPushButton("Clear selection")
        clear_sel.clicked.connect(self._clear_selection)
        sel_row.addWidget(select_all)
        sel_row.addWidget(clear_sel)
        sel_row.addStretch()
        layout.addLayout(sel_row)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_files(self):
        """Populate the list with all scannable files of the folder."""
        files = scan_folder(self.folder)
        self.list.clear()
        for path in files:
            try:
                rel = path.relative_to(self.folder)
            except ValueError:
                rel = Path(path.name)
            item = QListWidgetItem(str(rel))
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list.addItem(item)
        self.info.setText(f"Folder: {self.folder}   ({self.list.count()} files)")

    def apply_extensions(self):
        """Check every file whose extension matches the entered list."""
        extensions = parse_extensions(self.ext_input.text())
        if not extensions:
            return
        for i in range(self.list.count()):
            item = self.list.item(i)
            path = item.data(Qt.ItemDataRole.UserRole)
            if matches_extension(path, extensions):
                item.setCheckState(Qt.CheckState.Checked)

    def _select_all(self):
        for i in range(self.list.count()):
            self.list.item(i).setCheckState(Qt.CheckState.Checked)

    def _clear_selection(self):
        for i in range(self.list.count()):
            self.list.item(i).setCheckState(Qt.CheckState.Unchecked)

    def selected_files(self):
        """Return the absolute paths of all checked files."""
        result = []
        for i in range(self.list.count()):
            item = self.list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                result.append(item.data(Qt.ItemDataRole.UserRole))
        return result

    def accept(self):
        """Validate selection before closing the dialog."""
        if not self.selected_files():
            QMessageBox.information(self, "No files", "Select at least one file.")
            return
        super().accept()
