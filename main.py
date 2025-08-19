import sys
import os
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget
from window.form import Ui_Form

def resource_path(rel_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # (Optional) set on this window explicitly too:
        self.setWindowIcon(QtGui.QIcon(resource_path("assets/icon.ico")))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set app icon (affects all windows/dialogs)
    app.setWindowIcon(QtGui.QIcon(resource_path("assets/icon.ico")))

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
