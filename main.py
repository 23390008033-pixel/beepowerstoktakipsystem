"""
BeePower Stok Takip Sistemi
Giriş noktası / Entry point
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

import database as db
from styles import STYLESHEET
from ui_main import MainWindow


def main():
    # Initialize database
    db.initialize_db()

    app = QApplication(sys.argv)
    app.setApplicationName("BeePower Stok Takip")
    app.setOrganizationName("BeePower")

    # Apply global stylesheet
    app.setStyleSheet(STYLESHEET)

    # Default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
