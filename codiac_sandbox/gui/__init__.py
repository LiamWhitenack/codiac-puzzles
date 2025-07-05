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


# --- Quote Viewer Widget ---
class QuoteViewer(QWidget):
    def __init__(self, quotes_by_category):
        super().__init__()
        self.setWindowTitle("Quotes by Category")
        self.resize(900, 600)

        self.quotes_by_category = quotes_by_category

        layout = QHBoxLayout(self)

        # Category list
        self.category_list = QListWidget()
        self.category_list.addItems(sorted(quotes_by_category.keys()))
        self.category_list.currentItemChanged.connect(self.display_quotes)

        # Quote list
        self.quote_list = QListWidget()
        self.quote_list.itemClicked.connect(self.display_quote_details)

        # Details view
        self.detail_view = QTextEdit()
        self.detail_view.setReadOnly(True)

        # Assemble splitter layout
        splitter = QSplitter()
        splitter.addWidget(self.category_list)
        splitter.addWidget(self.quote_list)
        splitter.addWidget(self.detail_view)
        splitter.setStretchFactor(2, 2)

        layout.addWidget(splitter)

    def display_quotes(self, current: QListWidgetItem, _):
        self.quote_list.clear()
        if current:
            category = current.text()
            for quote in self.quotes_by_category[category]:
                text = quote["string_to_encrypt"][:60] + "..."
                item = QListWidgetItem(text)
                item.setData(Qt.UserRole, quote)
                self.quote_list.addItem(item)

    def display_quote_details(self, item: QListWidgetItem):
        quote = item.data(Qt.UserRole)
        details = f"<b>Quote:</b> {quote['string_to_encrypt']}<br><br>"
        for key, value in quote.items():
            if key != "string_to_encrypt":
                details += f"<b>{key.replace('_', ' ').title()}:</b> {value}<br>"
        self.detail_view.setHtml(details)


# --- Main Window ---
class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PySide6 Example")

        # Layout and widgets
        self._layout = QVBoxLayout()
        self.label = QLabel("Hello, world!")
        self.button = QPushButton("Click me")
        self.add_puzzle_button = QPushButton("Add Puzzle")
        self.view_quotes_button = QPushButton("View Quotes")  # New button

        self._layout.addWidget(self.label)
        self._layout.addWidget(self.button)
        self._layout.addWidget(self.add_puzzle_button)
        self._layout.addWidget(self.view_quotes_button)
        self.setLayout(self._layout)

        self.button.clicked.connect(self.handle_button_click)
        self.add_puzzle_button.clicked.connect(self.open_add_puzzle_dialog)
        self.view_quotes_button.clicked.connect(self.show_quote_viewer)

        # Load and group quotes once
        with open(
            "resources/master-puzzle-list.json"
        ) as f:  # or use your embedded JSON directly
            quotes = json.load(f)
        self.quotes_by_category = defaultdict(list)
        for q in quotes:
            self.quotes_by_category[q.get("puzzle_type", "Uncategorized")].append(q)

    def handle_button_click(self) -> None:
        self.label.setText("Button clicked!")

    def open_add_puzzle_dialog(self) -> None:
        dialog = AddPuzzleDialog()
        dialog.exec()

    def show_quote_viewer(self) -> None:
        self.viewer = QuoteViewer(self.quotes_by_category)
        self.viewer.show()
