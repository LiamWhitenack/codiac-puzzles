import sys
from codiac_sandbox import MainWindow
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
