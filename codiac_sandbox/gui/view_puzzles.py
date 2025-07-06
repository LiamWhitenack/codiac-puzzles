# puzzle_ui.py

from PySide6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QTextEdit,
    QListWidgetItem,
    QSplitter,
    QWidget,
)
from PySide6.QtCore import Qt
import json

from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES, from_json


class PuzzleUI:
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.layout = QVBoxLayout()

        self.load_quotes()
        self.build_lists()
        self.build_splitter()

    def load_quotes(self):
        with open("resources/master-puzzle-list.json") as f:
            self.quotes_by_category: dict[str, list[dict]] = {}
            for q in json.load(f):
                self.quotes_by_category[q["type"]] = self.quotes_by_category.get(
                    q["type"], []
                ) + [q]
        self.quotes_by_category = {
            k: v for k, v in sorted(self.quotes_by_category.items())
        }

    def build_lists(self):
        self.category_list = QListWidget()
        self.category_list.addItems(list(self.quotes_by_category))
        self.category_list.currentItemChanged.connect(self.display_quotes)
        self.category_list.setMaximumWidth(200)

        self.quote_list = QListWidget()
        self.quote_list.itemClicked.connect(self.display_quote_details)

        self.detail_view = QTextEdit()

    def build_splitter(self):
        splitter = QSplitter()
        splitter.addWidget(self.category_list)
        splitter.addWidget(self.quote_list)
        splitter.addWidget(self.detail_view)
        splitter.setStretchFactor(0, 0)

        self.layout.addWidget(splitter)

    def display_quotes(self, current: QListWidgetItem, _):
        self.quote_list.clear()
        if current:
            category = current.text()
            for quote in self.quotes_by_category[category]:
                text = quote["string_to_encrypt"]
                item = QListWidgetItem(text)
                item.setData(Qt.UserRole, quote)
                self.quote_list.addItem(item)

    def display_quote_details(self, item: QListWidgetItem):
        puzzle_data: dict = item.data(Qt.UserRole)
        puzzle = from_json(PUZZLE_CLASSES[puzzle_data.pop("type")], puzzle_data)
        details = ""
        for key, value in puzzle.to_json().items():
            if key == "type":
                continue
            details += f"<b>{key.replace('_', ' ').title()}:</b> {value}<br>"
        self.detail_view.setHtml(details)
