import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Example")

        # Create layout and widgets
        self.layout = QVBoxLayout()
        self.label = QLabel("Hello, world!")
        self.button = QPushButton("Click me")

        # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        # Set layout on main window
        self.setLayout(self.layout)

        # Connect button click to method
        self.button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        self.label.setText("Button clicked!")
