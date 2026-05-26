from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.styles import STYLE

import sys

app = QApplication(sys.argv)
app.setStyleSheet(STYLE)

window = MainWindow()
window.show()


sys.exit(app.exec())
