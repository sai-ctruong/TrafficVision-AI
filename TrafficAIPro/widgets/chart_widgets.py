"""Analytics chart widgets."""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget


PALETTE = {
    "car": QColor("#0078d4"),
    "bus": QColor("#107c10"),
    "truck": QColor("#e81123"),
    "van": QColor("#881798"),
}


class ChartCard(CardWidget):
    """Card wrapper for dashboard charts."""

    def __init__(self, title: str, content: QWidget) -> None:
        super().__init__()
        self.setBorderRadius(8)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(BodyLabel(title))
        layout.addWidget(content, 1)


class PieChartWidget(QWidget):
    """Small native painted pie chart for vehicle distribution."""

    def __init__(self) -> None:
        super().__init__()
        self.values = {key: 0 for key in PALETTE}
        self.setMinimumHeight(260)

    def set_values(self, values: dict[str, int]) -> None:
        self.values = {key: values.get(key, 0) for key in PALETTE}
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height()) - 52
        rect = QRectF(18, 18, side, side)
        total = sum(self.values.values())
        if total <= 0:
            painter.setPen(QPen(QColor("#8a8a8a")))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No detection data")
            return

        start_angle = 0
        for key, value in self.values.items():
            span = int(360 * 16 * value / total)
            painter.setBrush(PALETTE[key])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle, span)
            start_angle += span

        legend_x = int(rect.right()) + 28
        legend_y = 42
        painter.setPen(QColor("#5f5f5f"))
        for index, (key, value) in enumerate(self.values.items()):
            y = legend_y + index * 30
            painter.setBrush(PALETTE[key])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(legend_x, y, 14, 14, 3, 3)
            painter.setPen(QColor("#5f5f5f"))
            painter.drawText(legend_x + 24, y + 13, f"{key.title()}  {value}")

