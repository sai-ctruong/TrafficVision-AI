"""Modern left navigation sidebar with branding."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, FluentIcon, IconWidget, StrongBodyLabel

from ..utils.theme import APP_BACKGROUND, CARD_BORDER, PRIMARY, SECONDARY_TEXT, TEXT


class NavItem(QFrame):
    """Single sidebar navigation item with accent bar."""

    clicked = pyqtSignal(str)

    def __init__(self, key: str, text: str, icon: FluentIcon) -> None:
        super().__init__()
        self.key = key
        self._selected = False
        self.setObjectName("NavItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 16, 0)
        layout.setSpacing(14)

        # Left accent bar
        self.accent_bar = QWidget()
        self.accent_bar.setFixedSize(4, 48)
        layout.addWidget(self.accent_bar)

        self.icon = IconWidget(icon)
        self.icon.setFixedSize(20, 20)
        layout.addWidget(self.icon)

        self.label = BodyLabel(text)
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
            background = "#E3F2FD"
            accent_color = PRIMARY
            text_color = PRIMARY
            font_weight = 700
        else:
            background = "transparent"
            accent_color = "transparent"
            text_color = SECONDARY_TEXT
            font_weight = 500

        self.setStyleSheet(
            f"""
            #NavItem {{
                background: {background};
                border-radius: 0px 8px 8px 0px;
            }}
            #NavItem:hover {{
                background: #F5F9FC;
            }}
            """
        )
        self.accent_bar.setStyleSheet(
            f"""
            background: {accent_color};
            border-radius: 0px 2px 2px 0px;
            """
        )
        self.label.setStyleSheet(
            f"""
            font-size: 14px;
            font-weight: {font_weight};
            color: {text_color};
            """
        )


class Sidebar(QFrame):
    """260px Windows 11 Fluent Design sidebar with branding."""

    page_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)
        self.setStyleSheet(
            f"""
            #Sidebar {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FAFBFC, stop:1 #F8FAFB);
                border-right: 1px solid {CARD_BORDER};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 20)
        layout.setSpacing(4)

        # Branding section
        branding = QWidget()
        branding_layout = QVBoxLayout(branding)
        branding_layout.setContentsMargins(24, 0, 24, 0)
        branding_layout.setSpacing(4)

        brand_title = StrongBodyLabel("TrafficAI Pro")
        brand_title.setStyleSheet(
            f"""
            font-size: 18px;
            font-weight: 700;
            color: {PRIMARY};
            letter-spacing: -0.3px;
            """
        )
        branding_layout.addWidget(brand_title)

        brand_subtitle = BodyLabel("Computer Vision Suite")
        brand_subtitle.setStyleSheet(
            f"""
            font-size: 12px;
            color: {SECONDARY_TEXT};
            font-weight: 500;
            """
        )
        branding_layout.addWidget(brand_subtitle)

        layout.addWidget(branding)
        layout.addSpacing(32)

        # Navigation items
        self.items: dict[str, NavItem] = {}
        entries = [
            ("dashboard", "Dashboard", FluentIcon.HOME),
            ("processing", "Image Processing", FluentIcon.PHOTO),
            ("detection", "Vehicle Detection", FluentIcon.ROBOT),
            ("video", "Video Analysis", FluentIcon.VIDEO),
            ("analytics", "Analytics", FluentIcon.PIE_SINGLE),
            ("history", "History", FluentIcon.HISTORY),
        ]

        for key, text, icon in entries:
            item = NavItem(key, text, icon)
            item.clicked.connect(self.page_requested)
            self.items[key] = item
            layout.addWidget(item)

        layout.addStretch(1)

        # Settings at bottom
        settings = NavItem("settings", "Settings", FluentIcon.SETTING)
        settings.clicked.connect(self.page_requested)
        self.items["settings"] = settings
        layout.addWidget(settings)

        self.set_current("dashboard")

    def set_current(self, key: str) -> None:
        for item_key, item in self.items.items():
            item.set_selected(item_key == key)
