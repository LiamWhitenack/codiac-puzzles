from codiac_sandbox.gui.new_puzzle_modal import AddPuzzleDialog


from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PySide6 Example")

        # Layout and widgets
        self._layout = QVBoxLayout()
        self.label = QLabel("Hello, world!")
        self.button = QPushButton("Click me")
        self.add_puzzle_button = QPushButton("Add Puzzle")  # New button

        self._layout.addWidget(self.label)
        self._layout.addWidget(self.button)
        self._layout.addWidget(self.add_puzzle_button)
        self.setLayout(self._layout)

        self.button.clicked.connect(self.handle_button_click)
        self.add_puzzle_button.clicked.connect(self.open_add_puzzle_dialog)

    def handle_button_click(self) -> None:
        self.label.setText("Button clicked!")

    def open_add_puzzle_dialog(self) -> None:
        dialog = AddPuzzleDialog()
        dialog.exec()
