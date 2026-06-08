"""Chart widgets — warm editorial palette."""

from __future__ import annotations

import numpy as np
from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget

from ..utils.theme import (
    BORDER,
    CREAM,
    DIVIDER,
    FONT_SERIF,
    INK,
    INK_3,
    RADIUS_LG,
    RUST,
    SAND,
    SAND_2,
    TEXT_FAINT,
    VEHICLE_COLORS,
)


PALETTE = {
    "car": QColor(VEHICLE_COLORS["car"]),
    "bus": QColor(VEHICLE_COLORS["bus"]),
    "truck": QColor(VEHICLE_COLORS["truck"]),
    "van": QColor(VEHICLE_COLORS["van"]),
}


class ChartCard(CardWidget):
    """Card wrapper for charts — sand bg + hairline border, no heavy shadow."""

    def __init__(self, title: str, content: QWidget) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(320)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 20)
        layout.setSpacing(12)

        title_label = BodyLabel(title)
        title_label.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 16px;
            font-weight: 700;
            color: {INK};
            letter-spacing: -0.2px;
            """
        )
        layout.addWidget(title_label)
        layout.addWidget(content, 1)


class PieChartWidget(QWidget):
    """Donut chart with serif center total + readable legend."""

    def __init__(self) -> None:
        super().__init__()
        self.values = {key: 0 for key in PALETTE}
        self.setMinimumSize(420, 260)

    def set_values(self, values: dict[str, int]) -> None:
        self.values = {key: values.get(key, 0) for key in PALETTE}
        self.update()

    def paintEvent(self, event):  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        legend_width = 170
        side = min(self.height() - 30, self.width() - legend_width - 40)
        side = max(140, side)
        rect = QRectF(16, (self.height() - side) / 2, side, side)
        total = sum(self.values.values())

        if total <= 0:
            painter.setPen(QPen(QColor(TEXT_FAINT)))
            font = QFont(); font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No detection data")
            return

        start_angle = 90 * 16
        for key, value in self.values.items():
            span = -int(360 * 16 * value / total)
            painter.setBrush(PALETTE[key])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(rect, start_angle, span)
            start_angle += span

        # Donut cutout — cream-tinted inner circle
        inner_inset = side * 0.32
        inner = rect.adjusted(inner_inset, inner_inset, -inner_inset, -inner_inset)
        painter.setBrush(QColor(SAND))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(inner)

        # Serif total
        painter.setPen(QColor(INK))
        font = QFont("Cambria"); font.setPointSize(22); font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(total))

        font = QFont(); font.setPointSize(8); font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(TEXT_FAINT))
        sub_rect = QRectF(rect.left(), rect.center().y() + 14, rect.width(), 20)
        painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, "TOTAL")

        # Legend
        legend_x = int(rect.right()) + 28
        legend_y = int(rect.top()) + 6
        title_font = QFont(); title_font.setPointSize(10); title_font.setBold(True)
        value_font = QFont("Cambria"); value_font.setPointSize(11); value_font.setBold(True)
        for index, (key, value) in enumerate(self.values.items()):
            y = legend_y + index * 32
            painter.setBrush(PALETTE[key])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(legend_x, y, 10, 10, 2, 2)

            painter.setPen(QColor(INK_3))
            painter.setFont(title_font)
            painter.drawText(legend_x + 20, y + 10, key.title())

            painter.setPen(QColor(INK))
            painter.setFont(value_font)
            painter.drawText(legend_x + 20, y + 28, str(value))


class VehicleBarChartWidget(QWidget):
    """Vertical bar chart with subtle gridlines."""

    def __init__(self) -> None:
        super().__init__()
        self.values = {key: 0 for key in PALETTE}
        self.setMinimumHeight(260)

    def set_values(self, values: dict[str, int]) -> None:
        self.values = {key: values.get(key, 0) for key in PALETTE}
        self.update()

    def paintEvent(self, event):  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = self.rect().adjusted(48, 24, -20, -42)
        max_value = max(max(self.values.values()), 1)

        grid_pen = QPen(QColor(DIVIDER), 1)
        grid_pen.setStyle(Qt.PenStyle.DashLine)
        label_font = QFont(); label_font.setPointSize(9)
        painter.setFont(label_font)
        for index in range(5):
            y = rect.bottom() - int(rect.height() * index / 4)
            painter.setPen(grid_pen)
            painter.drawLine(rect.left(), y, rect.right(), y)
            painter.setPen(QColor(TEXT_FAINT))
            label = str(round(max_value * index / 4))
            painter.drawText(6, y - 8, 36, 16, Qt.AlignmentFlag.AlignRight, label)

        painter.setPen(QPen(QColor(BORDER), 1))
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

        count = len(PALETTE)
        slot_width = rect.width() / count
        bar_width = min(72, slot_width * 0.46)
        bold_font = QFont(); bold_font.setPointSize(10); bold_font.setBold(True)
        serif_font = QFont("Cambria"); serif_font.setPointSize(12); serif_font.setBold(True)

        for index, (key, color) in enumerate(PALETTE.items()):
            value = self.values.get(key, 0)
            height = int(rect.height() * value / max_value) if max_value else 0
            center_x = rect.left() + slot_width * index + slot_width / 2
            bar_rect = QRectF(center_x - bar_width / 2, rect.bottom() - height, bar_width, max(height, 2))

            # Subtle gradient bar (darker top, slightly lighter bottom)
            gradient = QLinearGradient(QPointF(bar_rect.left(), bar_rect.top()),
                                       QPointF(bar_rect.left(), bar_rect.bottom()))
            top = QColor(color)
            bot = QColor(color); bot.setAlphaF(0.85)
            gradient.setColorAt(0, top)
            gradient.setColorAt(1, bot)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.drawRoundedRect(bar_rect, 5, 5)

            # Category label below
            painter.setPen(QColor(INK_3))
            painter.setFont(bold_font)
            painter.drawText(
                int(center_x - slot_width / 2),
                rect.bottom() + 10,
                int(slot_width),
                20,
                Qt.AlignmentFlag.AlignCenter,
                key.title(),
            )
            # Value above bar — serif
            painter.setPen(QColor(INK))
            painter.setFont(serif_font)
            painter.drawText(
                int(center_x - slot_width / 2),
                max(rect.top(), int(bar_rect.top()) - 24),
                int(slot_width),
                20,
                Qt.AlignmentFlag.AlignCenter,
                str(value),
            )


class HistogramWidget(QWidget):
    """Grayscale histogram, soft-frame, rust-tinted bars."""

    def __init__(self, color: str = "#C4512A") -> None:
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

    def paintEvent(self, event):  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = self.rect().adjusted(34, 18, -12, -28)

        painter.setPen(QPen(QColor(BORDER), 1))
        painter.setBrush(QColor(CREAM))
        painter.drawRoundedRect(rect, 8, 8)

        grid_pen = QPen(QColor(DIVIDER), 1)
        grid_pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(grid_pen)
        for index in range(1, 4):
            y = rect.top() + int(rect.height() * index / 4)
            painter.drawLine(rect.left() + 6, y, rect.right() - 6, y)

        max_value = float(np.max(self.histogram)) if self.histogram.size else 0.0
        if max_value <= 0:
            painter.setPen(QColor(TEXT_FAINT))
            font = QFont(); font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No histogram data")
            return

        inner = rect.adjusted(6, 6, -6, -6)
        gradient = QLinearGradient(QPointF(inner.left(), inner.top()),
                                   QPointF(inner.left(), inner.bottom()))
        top = QColor(self.color); top.setAlphaF(0.85)
        bot = QColor(self.color); bot.setAlphaF(0.30)
        gradient.setColorAt(0, top)
        gradient.setColorAt(1, bot)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)

        step = inner.width() / 256
        for index, value in enumerate(self.histogram):
            x = inner.left() + index * step
            height = int(inner.height() * value / max_value)
            painter.drawRect(int(x), int(inner.bottom() - height), max(1, int(step)), height)

        painter.setPen(QColor(TEXT_FAINT))
        font = QFont(); font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(rect.left() - 22, rect.bottom() + 18, "0")
        painter.drawText(rect.right() - 24, rect.bottom() + 18, "255")
