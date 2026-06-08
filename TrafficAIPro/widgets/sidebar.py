"""Dark-brown editorial sidebar (Warm Editorial mockup)."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, FluentIcon, IconWidget

from ..utils.theme import (
    BROWN_2,
    CREAM,
    FONT_SERIF,
    RUST,
    SAGE,
    SIDEBAR_BG,
    SIDEBAR_BORDER,
    SIDEBAR_HOVER,
    SIDEBAR_TEXT,
    SIDEBAR_TEXT_FAINT,
    SIDEBAR_TEXT_MUTED,
)


class SectionLabel(QLabel):
    """Tiny uppercase caption — MAIN / DETECT / REPORTS."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setStyleSheet(
            f"""
            color: {SIDEBAR_TEXT_FAINT};
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.5px;
            padding: 10px 10px 4px 12px;
            margin-top: 4px;
            """
        )


class NavItem(QFrame):
    """A row in the dark sidebar."""

    clicked = pyqtSignal(str)

    def __init__(self, key: str, text: str, icon: FluentIcon) -> None:
        super().__init__()
        self.key = key
        self._selected = False
        self._hover = False
        self.setObjectName("NavItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)

        self.icon = IconWidget(icon)
        self.icon.setFixedSize(15, 15)
        layout.addWidget(self.icon)

        self.label = BodyLabel(text)
        layout.addWidget(self.label, 1)

        self.refresh()

    def mousePressEvent(self, event):  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.key)
        super().mousePressEvent(event)

    def enterEvent(self, event):  # type: ignore[override]
        self._hover = True
        self.refresh()
        super().enterEvent(event)

    def leaveEvent(self, event):  # type: ignore[override]
        self._hover = False
        self.refresh()
        super().leaveEvent(event)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.refresh()

    def refresh(self) -> None:
        if self._selected:
            background = RUST
            text_color = "#FFFFFF"
            font_weight = 600
        elif self._hover:
            background = SIDEBAR_HOVER
            text_color = "rgba(255, 255, 255, 0.85)"
            font_weight = 500
        else:
            background = "transparent"
            text_color = SIDEBAR_TEXT
            font_weight = 500

        self.setStyleSheet(
            f"""
            #NavItem {{
                background: {background};
                border-radius: 5px;
                margin: 1px 14px;
            }}
            """
        )
        self.label.setStyleSheet(
            f"""
            font-size: 13.5px;
            font-weight: {font_weight};
            color: {text_color};
            background: transparent;
            """
        )


class BrandHeader(QWidget):
    """Wordmark + tagline + live model pill (sidebar top)."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(4)

        title = QLabel("TrafficAI Pro")
        title.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 21px;
            font-weight: 700;
            color: {CREAM};
            letter-spacing: -0.5px;
            """
        )
        layout.addWidget(title)

        sub = QLabel("Vehicle Detection & Analytics")
        sub.setStyleSheet(
            "font-size: 11px; color: rgba(255,255,255,0.40); font-weight: 500; letter-spacing: 0.3px;"
        )
        layout.addWidget(sub)

        # Model pill
        pill = QFrame()
        pill.setObjectName("ModelPill")
        pill.setStyleSheet(
            """
            #ModelPill {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 999px;
            }
            """
        )
        pill_layout = QHBoxLayout(pill)
        pill_layout.setContentsMargins(12, 6, 14, 6)
        pill_layout.setSpacing(8)

        self.led = QLabel()
        self.led.setFixedSize(6, 6)
        self.led.setStyleSheet(f"background: {SAGE}; border-radius: 3px;")
        pill_layout.addWidget(self.led)

        self.pill_text = QLabel("Car_YOLO26_Best.pt")
        self.pill_text.setStyleSheet(
            "font-size: 11px; color: rgba(255,255,255,0.60); font-weight: 500;"
        )
        pill_layout.addWidget(self.pill_text, 1)

        layout.addSpacing(12)
        layout.addWidget(pill)


class SidebarFooter(QFrame):
    """Footer with a small quota track + avatar tile."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("SidebarFooter")
        self.setStyleSheet(
            f"""
            #SidebarFooter {{
                background: transparent;
                border-top: 1px solid {SIDEBAR_BORDER};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 18)
        layout.setSpacing(8)

        # Quota label row
        quota_row = QHBoxLayout()
        quota_row.setContentsMargins(0, 0, 0, 0)
        key = QLabel("Model")
        key.setStyleSheet(
            "font-size: 10px; color: rgba(255,255,255,0.35); letter-spacing: 0.3px;"
        )
        quota_row.addWidget(key)
        quota_row.addStretch(1)
        self.quota_val = QLabel("Ready")
        self.quota_val.setStyleSheet(
            "font-size: 10px; color: rgba(255,255,255,0.55); font-weight: 600;"
        )
        quota_row.addWidget(self.quota_val)
        layout.addLayout(quota_row)

        # Quota progress bar
        track = QFrame()
        track.setFixedHeight(2)
        track.setStyleSheet("background: rgba(255,255,255,0.10); border-radius: 1px;")
        track_layout = QHBoxLayout(track)
        track_layout.setContentsMargins(0, 0, 0, 0)
        track_layout.setSpacing(0)
        self.quota_fill = QFrame()
        self.quota_fill.setStyleSheet(f"background: {RUST}; border-radius: 1px;")
        track_layout.addWidget(self.quota_fill, 65)
        track_layout.addWidget(QFrame(), 35)
        layout.addWidget(track)

        # User row
        layout.addSpacing(6)
        user_row = QHBoxLayout()
        user_row.setContentsMargins(0, 0, 0, 0)
        user_row.setSpacing(10)

        avatar = QLabel("AI")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"""
            background: {BROWN_2};
            color: {CREAM};
            font-size: 11px;
            font-weight: 700;
            border-radius: 14px;
            """
        )
        user_row.addWidget(avatar)

        self.user_label = QLabel("Local workspace")
        self.user_label.setStyleSheet(
            "font-size: 12px; color: rgba(255,255,255,0.55); font-weight: 500;"
        )
        user_row.addWidget(self.user_label, 1)
        layout.addLayout(user_row)


class Sidebar(QFrame):
    """Dark-brown editorial sidebar (256 px)."""

    page_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(256)
        self.setStyleSheet(
            f"""
            #Sidebar {{
                background: {SIDEBAR_BG};
            }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.brand = BrandHeader()
        root.addWidget(self.brand)

        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: {SIDEBAR_BORDER};")
        root.addWidget(divider)
        root.addSpacing(8)

        self.items: dict[str, NavItem] = {}
        sections = [
            ("MAIN", [("dashboard", "Dashboard", FluentIcon.HOME)]),
            (
                "DETECT",
                [
                    ("processing", "Image Processing", FluentIcon.PHOTO),
                    ("detection", "Vehicle Detection", FluentIcon.ROBOT),
                    ("video", "Video Analysis", FluentIcon.VIDEO),
                ],
            ),
            (
                "REPORTS",
                [
                    ("analytics", "Analytics", FluentIcon.PIE_SINGLE),
                    ("history", "History", FluentIcon.HISTORY),
                ],
            ),
        ]

        for caption, entries in sections:
            root.addWidget(SectionLabel(caption))
            for key, text, icon in entries:
                item = NavItem(key, text, icon)
                item.clicked.connect(self.page_requested)
                self.items[key] = item
                root.addWidget(item)
            root.addSpacing(6)

        root.addStretch(1)

        self.footer = SidebarFooter()
        root.addWidget(self.footer)

        self.set_current("dashboard")

    def set_current(self, key: str) -> None:
        for item_key, item in self.items.items():
            item.set_selected(item_key == key)

    def set_status(self, text: str, color: str = SAGE) -> None:
        """Update the live model pill + footer."""
        self.brand.pill_text.setText(text)
        self.brand.led.setStyleSheet(f"background: {color}; border-radius: 3px;")
        self.footer.quota_val.setText(text if len(text) < 22 else "Updated")
