import sys
import inspect

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QWidget,
    QMessageBox,
)

from codiac_sandbox.crud.create import save_puzzle
from codiac_sandbox.crud.create import get_puzzle_parameters
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES


class AddPuzzleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Puzzle")
        self.setMinimumWidth(450)

        self._layout = QVBoxLayout(self)

        self.type_selector = QComboBox()
        self.type_selector.addItems(PUZZLE_CLASSES.keys())
        self._layout.addWidget(QLabel("Select Puzzle Type"))
        self._layout.addWidget(self.type_selector)

        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self._layout.addWidget(self.form_widget)

        self.submit_button = QPushButton("Submit")
        self.copy_button = QPushButton("Copy to Clipboard")
        self._layout.addWidget(self.submit_button)
        self._layout.addWidget(self.copy_button)

        self.fields = {}
        self.generated_json = ""

        self.type_selector.currentTextChanged.connect(self.update_form)
        self.submit_button.clicked.connect(self.handle_submit)

        self.update_form(self.type_selector.currentText())

    def update_form(self, puzzle_type: str):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if widget := item.widget():
                widget.setParent(None)

        self.fields.clear()
        for name, param in get_puzzle_parameters(puzzle_type).items():
            field = QLineEdit()
            placeholder = (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else ""
            )
            if param.default != inspect.Parameter.empty:
                placeholder += f" (default: {param.default})"
            field.setPlaceholderText(placeholder.strip())
            self.fields[name] = field
            self.form_layout.addRow(QLabel(name), field)

    def handle_submit(self):
        puzzle_type = self.type_selector.currentText()
        cls = PUZZLE_CLASSES[puzzle_type]
        kwargs = {}

        for name, param in get_puzzle_parameters(puzzle_type).items():
            text = self.fields[name].text()
            if not text and param.default != inspect.Parameter.empty:
                return
            try:
                if "int" in str(param.annotation) and text:
                    kwargs[name] = int(text)
                elif "list" in str(param.annotation):
                    kwargs[name] = [s.strip() for s in text.split(",")]
                else:
                    kwargs[name] = text
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid input for {name}: {e}")
                return

        try:
            save_puzzle("resources/master-puzzle-list.json", cls, kwargs)
            QMessageBox.information(self, "Success", "Puzzle created.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not create puzzle:\n{e}")
