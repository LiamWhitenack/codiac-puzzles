from codiac_sandbox.gui.new_puzzle_modal import AddPuzzleDialog

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QTextEdit,
    QHBoxLayout,
    QListWidgetItem,
    QSplitter,
)
from PySide6.QtCore import Qt
from collections import defaultdict
import json

from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES, from_json


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Quotes by Category")

        # Main layout
        main_layout = QVBoxLayout()

        # Top controls
        self.add_puzzle_button = QPushButton("Add Puzzle")

        self.add_puzzle_button.clicked.connect(self.open_add_puzzle_dialog)

        top_controls_layout = QHBoxLayout()
        top_controls_layout.addWidget(self.add_puzzle_button)

        main_layout.addLayout(top_controls_layout)

        # Load quotes
        with open("resources/master-puzzle-list.json") as f:
            self.quotes_by_category: dict[str, list[dict]] = {}
            for q in json.load(f):
                self.quotes_by_category[q["type"]] = self.quotes_by_category.get(
                    q["type"], []
                ) + [q]
        self.quotes_by_category = {
            k: v for k, v in sorted(self.quotes_by_category.items())
        }

        # Category list
        self.category_list = QListWidget()
        self.category_list.addItems(list(self.quotes_by_category))
        self.category_list.currentItemChanged.connect(self.display_quotes)
        self.category_list.setMaximumWidth(200)

        # Quote list
        self.quote_list = QListWidget()
        self.quote_list.itemClicked.connect(self.display_quote_details)

        # Detail view
        self.detail_view = QTextEdit()

        # Splitter
        splitter = QSplitter()
        splitter.addWidget(self.category_list)
        splitter.addWidget(self.quote_list)
        splitter.addWidget(self.detail_view)
        splitter.setStretchFactor(0, 0)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def display_quotes(self, current: QListWidgetItem, _):
        self.quote_list.clear()
        if current:
            category = current.text()
            for quote in self.quotes_by_category[category]:
                text = quote["string_to_encrypt"][:120]
                item = QListWidgetItem(text)
                item.setData(Qt.UserRole, quote)  # type: ignore[attr-defined]
                self.quote_list.addItem(item)

    def display_quote_details(self, item: QListWidgetItem):

        puzzle_data: dict = item.data(256)
        puzzle = from_json(PUZZLE_CLASSES[puzzle_data.pop("type")], puzzle_data)
        details = ""
        for key, value in puzzle_data.items():
            if key in ["type"]:
                continue
            details += f"<b>{key.replace('_', ' ').title()}:</b> {value}<br>"
        self.detail_view.setHtml(details)

    def open_add_puzzle_dialog(self) -> None:
        AddPuzzleDialog().exec()
