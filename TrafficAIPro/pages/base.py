"""Base page helpers."""

from __future__ import annotations

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import ScrollArea, TitleLabel


class Page(ScrollArea):
    """Scrollable page with a title and content body."""

    def __init__(self, title: str, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setWidgetResizable(True)
        self.view = QWidget()
        self.setWidget(self.view)
        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(18)
        self.layout.addWidget(TitleLabel(title))

