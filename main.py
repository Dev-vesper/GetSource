import sys

from PyQt6.QtWidgets import QApplication

from src.frontend.style import STYLESHEET
from src.frontend.window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
