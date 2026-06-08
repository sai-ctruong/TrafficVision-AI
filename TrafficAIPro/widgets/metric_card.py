"""Editorial metric card — sand surface, status badge, big serif number."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget, StrongBodyLabel

from ..utils.theme import (
    BORDER,
    FONT_SERIF,
    INK,
    INK_3,
    PRIMARY,
    RADIUS_LG,
    RUST_LIGHT,
    SAND,
    SECONDARY_TEXT,
)


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


class MetricCard(CardWidget):
    """A KPI tile in the warm-editorial style.

    Layout (matches the v4 mockup):
        ┌─────────────────────┐
        │  [BADGE]            │
        │                     │
        │  42                 │   ← Fraunces serif, huge
        │  Total Vehicles     │   ← small uppercase
        └─────────────────────┘
    """

    def __init__(
        self,
        title: str,
        value: str = "0",
        icon: FluentIcon | None = None,
        accent: str = PRIMARY,
        badge: str = "",
        badge_bg: str = RUST_LIGHT,
    ) -> None:
        super().__init__()
        self.accent = accent
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(120)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            CardWidget:hover {{
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.35);
            }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 14, 18, 16)
        root.setSpacing(8)

        # Top row: badge + (icon ghost)
        top = QHBoxLayout()
        top.setSpacing(8)

        self.badge_label = BodyLabel(badge or title.upper())
        self.badge_label.setStyleSheet(
            f"""
            background: {badge_bg};
            color: {accent};
            font-size: 10px;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 10px;
            letter-spacing: 0.4px;
            """
        )
        top.addWidget(self.badge_label, 0, Qt.AlignmentFlag.AlignLeft)
        top.addStretch(1)
        root.addLayout(top)

        # Serif value — big editorial number
        self.value_label = StrongBodyLabel(str(value))
        self.value_label.setObjectName("MetricValue")
        self.value_label.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 32px;
            font-weight: 700;
            color: {accent};
            letter-spacing: -1.2px;
            """
        )
        root.addWidget(self.value_label)

        # Caption
        self.title_label = BodyLabel(title)
        self.title_label.setStyleSheet(
            f"""
            font-size: 11.5px;
            font-weight: 500;
            color: {INK_3};
            """
        )
        root.addWidget(self.title_label)
        root.addStretch(1)

    def set_value(self, value: int | float | str) -> None:
        self.value_label.setText(str(value))
