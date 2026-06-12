"""Detection history page."""

from __future__ import annotations

from pathlib import Path

import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QAbstractItemView, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import ComboBox, FluentIcon, InfoBar, InfoBarPosition, PushButton, SearchLineEdit, TableWidget

from ..database.history_repository import HistoryRepository
from .base import Page
from ..utils.paths import EXPORT_DIR
from ..widgets.image_viewer import ImageViewer


class HistoryPage(Page):
    """Searchable SQLite detection history."""

    def __init__(self, history: HistoryRepository) -> None:
        super().__init__("History", "HistoryPage")
        self.history = history
        self._row_image_paths: dict[int, str] = {}

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
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Image Name",
                "Date",
                "Mode",
                "Cars",
                "Buses",
                "Trucks",
                "Vans",
                "Total",
                "Avg Confidence",
                "Inference",
            ]
        )
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.currentCellChanged.connect(self.show_selected_preview)

        self.preview = ImageViewer("Detected Image")
        self.preview.clear("Select a history row", "No history selected")

        content = QHBoxLayout()
        content.setSpacing(20)
        content.addWidget(self.table, 1)
        content.addWidget(self.preview, 0, Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(content, 1)
        self.refresh()

    def refresh(self) -> None:
        rows = self.history.list(self.search.text(), self.sort.currentText())
        self._row_image_paths.clear()
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            result_image_path = row["result_image_path"] if "result_image_path" in row.keys() else ""
            self._row_image_paths[row_index] = result_image_path or ""
            values = [
                row["id"],
                row["image_name"],
                row["detection_date"],
                row["detection_mode"] if "detection_mode" in row.keys() else "YOLO",
                row["car_count"],
                row["bus_count"],
                row["truck_count"],
                row["van_count"],
                row["total_vehicles"],
                f"{row['average_confidence']:.0%}",
                f"{row['inference_time']:.2f}s" if "inference_time" in row.keys() else f"{row['processing_time']:.2f}s",
            ]
            for col, value in enumerate(values):
                self.table.setItem(row_index, col, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
        if rows:
            self.table.selectRow(0)
            self.show_selected_preview(0, 0, -1, -1)
        else:
            self.preview.clear("No history records", "Run detection to create history")

    def show_selected_preview(self, current_row: int, *_args: object) -> None:
        if current_row < 0:
            self.preview.clear("Select a history row", "No history selected")
            return

        image_path = self._row_image_paths.get(current_row, "")
        if not image_path:
            self.preview.clear("No saved image", "This older record has no detected image")
            return

        path = Path(image_path)
        if not path.exists():
            self.preview.clear("Image file missing", path.name)
            return

        image = cv2.imread(str(path))
        if image is None:
            self.preview.clear("Unable to load image", path.name)
            return

        self.preview.set_image(image, path.name)

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
