import sys
import json
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

from codiac_sandbox.hint_types import HintBase
from codiac_sandbox.puzzle_types import CryptographBase  # or wherever it's defined


def get_all_subclasses(cls: type[CryptographBase]) -> set[type[CryptographBase]]:
    subclasses = set()
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


PUZZLE_CLASSES: dict[str, type[CryptographBase]] = {
    subclass.__name__: subclass for subclass in get_all_subclasses(CryptographBase)
}


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
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.update_form(self.type_selector.currentText())

    def update_form(self, puzzle_type: str):
        cls = PUZZLE_CLASSES[puzzle_type]
        sig = inspect.signature(cls.__init__)
        ignored_params = {
            "self",
            "string_to_encrypt",
            "puzzle_type",
            "hints",
            "encryptionMap",
        }

        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if widget := item.widget():
                widget.setParent(None)

        self.fields.clear()
        for name, param in sig.parameters.items():
            if name in ignored_params:
                continue
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

        sig = inspect.signature(cls.__init__)
        ignored_params = {"self", "string_to_encrypt", "puzzle_type", "hints"}

        for name, param in sig.parameters.items():
            if name in ignored_params:
                continue
            text = self.fields[name].text()
            if not text and param.default != inspect.Parameter.empty:
                continue  # use default
            try:
                if "int" in str(param.annotation) and text:
                    kwargs[name] = int(text)
                elif "list" in str(param.annotation) or "List" in str(param.annotation):
                    kwargs[name] = [s.strip() for s in text.split(",")]
                else:
                    kwargs[name] = text
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid input for {name}: {e}")
                return

        try:
            obj = cls(**kwargs)
            self.generated_json = json.dumps(obj.to_json(), indent=2)
            QMessageBox.information(self, "Success", "Puzzle created.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not create puzzle:\n{e}")

    def copy_to_clipboard(self):
        if not self.generated_json:
            QMessageBox.warning(self, "Nothing to copy", "Submit a puzzle first.")
            return
        QApplication.clipboard().setText(self.generated_json)
        QMessageBox.information(self, "Copied", "JSON copied to clipboard.")
