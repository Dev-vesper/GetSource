from pathlib import Path

from PyQt6.QtCore import QDir, QThread, Qt, pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from src.frontend.picker import PickerDialog
from src.internals.exporter import write_markdown


class ExportWorker(QThread):
    """Background worker that writes the markdown file off the UI thread."""

    done = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, entries, output_path):
        super().__init__()
        self.entries = entries
        self.output_path = output_path

    def run(self):
        try:
            write_markdown(self.entries, self.output_path)
        except Exception as exc:
            self.failed.emit(str(exc))
            return
        self.done.emit(self.output_path)


class MainWindow(QMainWindow):
    """Main window: file tree on the left, collected files on the right."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Source Collector")
        self.resize(1050, 680)
        self.selected_files = []
        self._worker = None
        self._build_ui()

    def _build_ui(self):
        """Assemble the entire window layout."""
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Filesystem"))
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.doubleClicked.connect(lambda _: self.add_folder())
        left_layout.addWidget(self.tree)
        splitter.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Selected files"))
        self.file_list = QListWidget()
        right_layout.addWidget(self.file_list)
        splitter.addWidget(right)

        splitter.setSizes([520, 530])
        root.addWidget(splitter)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Folder")
        add_btn.clicked.connect(self.add_folder)
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_all)
        self.export_btn = QPushButton("Export Markdown")
        self.export_btn.clicked.connect(self.export)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(remove_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.export_btn)
        root.addLayout(btn_row)

    def add_folder(self):
        """Open the picker dialog for the folder selected in the tree."""
        index = self.tree.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "No folder", "Select a folder first.")
            return
        path = Path(self.model.filePath(index))
        if not path.is_dir():
            path = path.parent

        dialog = PickerDialog(str(path), self)
        if not dialog.exec():
            return

        base = path.parent
        for file_path in dialog.selected_files():
            if any(p == file_path for p, _ in self.selected_files):
                continue
            try:
                display = str(Path(file_path).relative_to(base))
            except ValueError:
                display = str(file_path)
            self.selected_files.append((file_path, display))
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.file_list.addItem(item)

    def remove_selected(self):
        """Remove the currently highlighted rows from the collection."""
        for item in self.file_list.selectedItems():
            path = item.data(Qt.ItemDataRole.UserRole)
            self.selected_files = [(p, d) for p, d in self.selected_files if p != path]
            self.file_list.takeItem(self.file_list.row(item))

    def clear_all(self):
        """Drop every collected file."""
        self.selected_files.clear()
        self.file_list.clear()

    def export(self):
        """Start a background export of the collected files."""
        if self._worker is not None:
            return
        if not self.selected_files:
            QMessageBox.information(self, "Empty", "No files selected.")
            return
        out, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown", "output.md", "Markdown (*.md)"
        )
        if not out:
            return

        self.export_btn.setEnabled(False)
        self.export_btn.setText("Exporting...")

        self._worker = ExportWorker(list(self.selected_files), out)
        self._worker.done.connect(self._on_export_done)
        self._worker.failed.connect(self._on_export_failed)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def _on_export_done(self, path):
        """Notify the user that the file was written."""
        QMessageBox.information(self, "Done", f"Saved to:\n{path}")

    def _on_export_failed(self, message):
        """Show an error dialog if the export failed."""
        QMessageBox.critical(self, "Export failed", message)

    def _on_worker_finished(self):
        """Restore the export button once the worker is done."""
        self.export_btn.setEnabled(True)
        self.export_btn.setText("Export Markdown")
        self._worker = None
