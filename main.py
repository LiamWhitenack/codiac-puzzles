import sys
from codiac_sandbox.gui import MainWindow
from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.showMaximized()
sys.exit(app.exec())
