"""Premium metric card widgets."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget, StrongBodyLabel


class MetricCard(CardWidget):
    """Compact analytics card with icon, value and caption."""

    def __init__(self, title: str, value: str = "0", icon: FluentIcon | None = None) -> None:
        super().__init__()
        self.setBorderRadius(8)
        self.setMinimumHeight(112)

        root = QHBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(14)

        self.icon = IconWidget(icon or FluentIcon.CAR)
        self.icon.setFixedSize(34, 34)
        root.addWidget(self.icon, 0, Qt.AlignmentFlag.AlignTop)

        content = QVBoxLayout()
        content.setSpacing(6)
        self.title_label = BodyLabel(title)
        self.value_label = StrongBodyLabel(value)
        self.value_label.setObjectName("MetricValue")
        self.value_label.setStyleSheet("font-size: 30px; font-weight: 700;")
        content.addWidget(self.title_label)
        content.addWidget(self.value_label)
        content.addStretch(1)
        root.addLayout(content, 1)

    def set_value(self, value: int | float | str) -> None:
        self.value_label.setText(str(value))

