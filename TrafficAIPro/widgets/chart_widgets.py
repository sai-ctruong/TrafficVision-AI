"""Analytics chart widgets."""

from __future__ import annotations

import numpy as np
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
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
        self.setBorderRadius(14)
        self.setMinimumHeight(330)
        self.setStyleSheet(
            """
            CardWidget {
                background: #FFFFFF;
                border: 1px solid #E5EAF2;
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(10)
        title_label = BodyLabel(title)
        title_label.setStyleSheet(
            """
            font-size: 15px;
            font-weight: 700;
            color: #111827;
            """
        )
        layout.addWidget(title_label)
        layout.addWidget(content, 1)


class PieChartWidget(QWidget):
    """Small native painted pie chart for vehicle distribution."""

    def __init__(self) -> None:
        super().__init__()
        self.values = {key: 0 for key in PALETTE}
        self.setMinimumSize(420, 260)

    def set_values(self, values: dict[str, int]) -> None:
        self.values = {key: values.get(key, 0) for key in PALETTE}
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        legend_width = 150
        side = min(self.height() - 46, self.width() - legend_width - 56)
        side = max(120, side)
        rect = QRectF(20, 24, side, side)
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

        legend_x = int(rect.right()) + 30
        legend_y = int(rect.top()) + 8
        painter.setPen(QColor("#5f5f5f"))
        for index, (key, value) in enumerate(self.values.items()):
            y = legend_y + index * 30
            painter.setBrush(PALETTE[key])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(legend_x, y, 14, 14, 3, 3)
            painter.setPen(QColor("#5f5f5f"))
            painter.drawText(legend_x + 24, y + 13, f"{key.title()}  {value}")


class VehicleBarChartWidget(QWidget):
    """Lightweight native bar chart for vehicle totals."""

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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        rect = self.rect().adjusted(48, 24, -20, -42)
        max_value = max(max(self.values.values()), 1)

        painter.setPen(QPen(QColor("#D7DEE8"), 1))
        for index in range(5):
            y = rect.bottom() - int(rect.height() * index / 4)
            painter.drawLine(rect.left(), y, rect.right(), y)
            painter.setPen(QColor("#8A94A6"))
            label = str(round(max_value * index / 4))
            painter.drawText(6, y - 8, 36, 16, Qt.AlignmentFlag.AlignRight, label)
            painter.setPen(QPen(QColor("#D7DEE8"), 1))

        painter.setPen(QPen(QColor("#AAB4C2"), 1))
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

        count = len(PALETTE)
        slot_width = rect.width() / count
        bar_width = min(64, slot_width * 0.52)
        label_font = QFont()
        label_font.setPointSize(9)
        label_font.setBold(True)
        painter.setFont(label_font)

        for index, (key, color) in enumerate(PALETTE.items()):
            value = self.values.get(key, 0)
            height = int(rect.height() * value / max_value) if max_value else 0
            center_x = rect.left() + slot_width * index + slot_width / 2
            bar_rect = QRectF(center_x - bar_width / 2, rect.bottom() - height, bar_width, height)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(bar_rect, 5, 5)

            painter.setPen(QColor("#111827"))
            painter.drawText(
                int(center_x - slot_width / 2),
                rect.bottom() + 10,
                int(slot_width),
                20,
                Qt.AlignmentFlag.AlignCenter,
                key.title(),
            )
            painter.setPen(QColor("#6B7280"))
            painter.drawText(
                int(center_x - slot_width / 2),
                max(rect.top(), int(bar_rect.top()) - 22),
                int(slot_width),
                18,
                Qt.AlignmentFlag.AlignCenter,
                str(value),
            )


class HistogramWidget(QWidget):
    """Lightweight grayscale histogram chart."""

    def __init__(self, color: str = "#0F6CBD") -> None:
        super().__init__()
        self.histogram = np.zeros(256, dtype=float)
        self.color = QColor(color)
        self.setMinimumHeight(180)

    def set_histogram(self, histogram: np.ndarray | None) -> None:
        if histogram is None:
            self.histogram = np.zeros(256, dtype=float)
        else:
            self.histogram = histogram.astype(float)
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        rect = self.rect().adjusted(34, 18, -12, -28)

        painter.setPen(QPen(QColor("#D7DEE8"), 1))
        painter.drawRect(rect)
        for index in range(1, 4):
            y = rect.top() + int(rect.height() * index / 4)
            painter.drawLine(rect.left(), y, rect.right(), y)

        max_value = float(np.max(self.histogram)) if self.histogram.size else 0.0
        if max_value <= 0:
            painter.setPen(QColor("#8A94A6"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No histogram data")
            return

        painter.setPen(QPen(self.color, 1))
        step = rect.width() / 256
        for index, value in enumerate(self.histogram):
            x = rect.left() + index * step
            height = int(rect.height() * value / max_value)
            painter.drawLine(int(x), rect.bottom(), int(x), rect.bottom() - height)

        painter.setPen(QColor("#6B7280"))
        painter.drawText(rect.left() - 22, rect.bottom() + 18, "0")
        painter.drawText(rect.right() - 24, rect.bottom() + 18, "255")

