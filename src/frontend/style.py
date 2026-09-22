"""Application stylesheet."""

STYLESHEET = """
QMainWindow, QDialog { background: #1e1f22; color: #e6e6e6; }
QWidget { font-family: 'Segoe UI', 'Inter', sans-serif; font-size: 12px; }
QLabel { color: #d8d8d8; }
QPushButton {
    background: #313438;
    color: #e6e6e6;
    border: 1px solid #40444a;
    padding: 6px 12px;
    border-radius: 4px;
}
QPushButton:hover { background: #3d4147; }
QPushButton:pressed { background: #2a2d31; }
QLineEdit, QListWidget, QTreeView {
    background: #26282c;
    color: #e6e6e6;
    border: 1px solid #3a3d42;
    border-radius: 3px;
    selection-background-color: #2d6cdf;
}
QListWidget::item { padding: 4px 6px; }
QListWidget::item:selected { background: #2d6cdf; color: #ffffff; }
QTreeView::item { padding: 2px 4px; }
QHeaderView::section { background: #2a2d31; color: #c8c8c8; border: none; padding: 4px; }
"""
