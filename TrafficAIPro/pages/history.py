"""Detection history page."""

from __future__ import annotations

from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import ComboBox, FluentIcon, InfoBar, InfoBarPosition, PushButton, SearchLineEdit, TableWidget

from ..database.history_repository import HistoryRepository
from .base import Page
from ..utils.paths import EXPORT_DIR


class HistoryPage(Page):
    """Searchable SQLite detection history."""

    def __init__(self, history: HistoryRepository) -> None:
        super().__init__("History", "HistoryPage")
        self.history = history

        toolbar = QHBoxLayout()
        self.search = SearchLineEdit()
        self.search.setPlaceholderText("Search image name")
        self.search.textChanged.connect(self.refresh)
        self.sort = ComboBox()
        self.sort.addItems(["Newest", "Oldest", "Most Vehicles", "Highest Confidence"])
        self.sort.currentTextChanged.connect(self.refresh)
        self.delete_button = PushButton(FluentIcon.DELETE, "Delete")
        self.delete_button.clicked.connect(self.delete_selected)
        self.export_button = PushButton(FluentIcon.SAVE, "Export")
        self.export_button.clicked.connect(self.export)
        toolbar.addWidget(self.search, 1)
        toolbar.addWidget(self.sort)
        toolbar.addWidget(self.delete_button)
        toolbar.addWidget(self.export_button)
        self.layout.addLayout(toolbar)

        self.table = TableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Image Name", "Date", "Cars", "Buses", "Trucks", "Vans", "Total", "Avg Confidence"]
        )
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)
        self.layout.addWidget(self.table, 1)
        self.refresh()

    def refresh(self) -> None:
        rows = self.history.list(self.search.text(), self.sort.currentText())
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            values = [
                row["id"],
                row["image_name"],
                row["detection_date"],
                row["car_count"],
                row["bus_count"],
                row["truck_count"],
                row["van_count"],
                row["total_vehicles"],
                f"{row['average_confidence']:.0%}",
            ]
            for col, value in enumerate(values):
                self.table.setItem(row_index, col, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()

    def delete_selected(self) -> None:
        rows = {item.row() for item in self.table.selectedItems()}
        ids = [int(self.table.item(row, 0).text()) for row in rows if self.table.item(row, 0)]
        self.history.delete(ids)
        self.refresh()
        InfoBar.success("History updated", f"Deleted {len(ids)} record(s)", parent=self, position=InfoBarPosition.TOP_RIGHT)

    def export(self) -> None:
        default_path = str(EXPORT_DIR / "trafficai_history.csv")
        path, _ = QFileDialog.getSaveFileName(self, "Export history", default_path, "CSV (*.csv)")
        if not path:
            return
        self.history.export_csv(path)
        InfoBar.success("Export complete", path, parent=self, position=InfoBarPosition.TOP_RIGHT)
