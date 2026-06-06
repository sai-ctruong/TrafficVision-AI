"""Premium glassmorphism metric cards."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QColor
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget, StrongBodyLabel

from ..utils.theme import PRIMARY, SECONDARY_TEXT


class MetricCard(CardWidget):
    """Premium glassmorphism card with icon, value and caption."""

    def __init__(self, title: str, value: str = "0", icon: FluentIcon | None = None) -> None:
        super().__init__()
        self.setBorderRadius(14)
        self.setMinimumHeight(130)
        
        # Glassmorphism style
        self.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            """
        )
        
        # Add soft shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(12)

        # Top row: icon and title
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self.icon = IconWidget(icon or FluentIcon.CAR)
        self.icon.setFixedSize(36, 36)
        top_row.addWidget(self.icon)

        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet(
            f"""
            font-size: 14px;
            font-weight: 600;
            color: {SECONDARY_TEXT};
            """
        )
        top_row.addWidget(self.title_label, 1)

        root.addLayout(top_row)
        root.addSpacing(4)

        # Large number value
        self.value_label = StrongBodyLabel(value)
        self.value_label.setObjectName("MetricValue")
        self.value_label.setStyleSheet(
            f"""
            font-size: 42px;
            font-weight: 700;
            color: {PRIMARY};
            letter-spacing: -1px;
            """
        )
        root.addWidget(self.value_label)
        root.addStretch(1)

    def set_value(self, value: int | float | str) -> None:
        self.value_label.setText(str(value))

