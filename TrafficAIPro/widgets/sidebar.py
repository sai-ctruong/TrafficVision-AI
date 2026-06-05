"""Modern left navigation sidebar."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, FluentIcon, IconWidget

from ..utils.theme import APP_BACKGROUND, CARD_BORDER, PRIMARY, SECONDARY_TEXT, TEXT


class NavItem(QFrame):
    """Single sidebar navigation item."""

    clicked = pyqtSignal(str)

    def __init__(self, key: str, text: str, icon: FluentIcon) -> None:
        super().__init__()
        self.key = key
        self._selected = False
        self.setObjectName("NavItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(12)
        self.indicator = QWidget()
        self.indicator.setFixedSize(3, 20)
        self.indicator.setStyleSheet("background: transparent; border-radius: 2px;")
        self.icon = IconWidget(icon)
        self.icon.setFixedSize(22, 22)
        self.label = BodyLabel(text)
        self.label.setStyleSheet(f"font-size: 14px; color: {TEXT};")
        layout.addWidget(self.indicator)
        layout.addWidget(self.icon)
        layout.addWidget(self.label, 1)
        self.refresh()

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.key)
        super().mousePressEvent(event)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.refresh()

    def refresh(self) -> None:
        if self._selected:
            background = "#E8F1FC"
            indicator = PRIMARY
            text = TEXT
        else:
            background = "transparent"
            indicator = "transparent"
            text = SECONDARY_TEXT
        self.setStyleSheet(
            f"""
            #NavItem {{
                background: {background};
                border-radius: 10px;
            }}
            #NavItem:hover {{
                background: #EEF4FB;
            }}
            """
        )
        self.indicator.setStyleSheet(f"background: {indicator}; border-radius: 2px;")
        self.label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {text};")


class Sidebar(QFrame):
    """Windows 11-style navigation sidebar."""

    page_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        self.setStyleSheet(
            f"""
            #Sidebar {{
                background: {APP_BACKGROUND};
                border-right: 1px solid {CARD_BORDER};
            }}
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 18, 12, 18)
        layout.setSpacing(7)
        self.items: dict[str, NavItem] = {}
        entries = [
            ("dashboard", "Dashboard", FluentIcon.HOME),
            ("processing", "Image Processing", FluentIcon.PHOTO),
            ("detection", "Detection", FluentIcon.ROBOT),
            ("analytics", "Analytics", FluentIcon.PIE_SINGLE),
            ("history", "History", FluentIcon.HISTORY),
        ]
        for key, text, icon in entries:
            item = NavItem(key, text, icon)
            item.clicked.connect(self.page_requested)
            self.items[key] = item
            layout.addWidget(item)
        layout.addStretch(1)
        settings = NavItem("settings", "Settings", FluentIcon.SETTING)
        settings.clicked.connect(self.page_requested)
        self.items["settings"] = settings
        layout.addWidget(settings)
        self.set_current("dashboard")

    def set_current(self, key: str) -> None:
        for item_key, item in self.items.items():
            item.set_selected(item_key == key)

