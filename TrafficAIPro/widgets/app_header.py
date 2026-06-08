"""Cream top bar — eyebrow + search + sand actions + rust CTA."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    IndeterminateProgressRing,
    PrimaryPushButton,
    PushButton,
    SearchLineEdit,
)

from ..utils.theme import (
    BORDER,
    CREAM,
    ERROR,
    INK,
    INK_3,
    PRIMARY,
    PRIMARY_HOVER,
    PRIMARY_PRESSED,
    RUST_DIM,
    RUST_LIGHT,
    SAND,
    SAND_2,
    SECONDARY_TEXT,
    SUCCESS,
    SURFACE_HOVER,
    TEXT_FAINT,
    WARNING,
)


class ModelStatusPill(QWidget):
    """Subtle pill — dot + label, sand background, hairline border."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("StatusPill")
        self.setStyleSheet(
            f"""
            #StatusPill {{
                background: {SAND};
                border: 1px solid {BORDER};
                border-radius: 999px;
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 14, 6)
        layout.setSpacing(8)

        self.dot = QLabel()
        self.dot.setFixedSize(7, 7)
        self.dot.setStyleSheet(f"background: {ERROR}; border-radius: 3px;")
        layout.addWidget(self.dot)

        self.spinner = IndeterminateProgressRing(self)
        self.spinner.setFixedSize(13, 13)
        self.spinner.setStrokeWidth(2)
        self.spinner.hide()
        layout.addWidget(self.spinner)

        self.label = BodyLabel("Model not loaded")
        self.label.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {INK_3};"
        )
        layout.addWidget(self.label)

    def set_status(self, text: str, state: str) -> None:
        palette = {
            "loaded": SUCCESS,
            "loading": WARNING,
            "processing": WARNING,
            "error": ERROR,
            "not_loaded": ERROR,
        }
        color = palette.get(state, ERROR)
        self.dot.setStyleSheet(f"background: {color}; border-radius: 3px;")
        if state in ("loading", "processing"):
            self.dot.hide()
            self.spinner.show()
        else:
            self.spinner.hide()
            self.dot.show()
        self.label.setText(text)


# QFluentWidgets's PushButton draws its icon *outside* of Qt's QPushButton
# paint flow (it does NOT call super().setIcon, so Qt centers the text as if
# no icon were present). Solution: reserve room on the LEFT via padding so
# Qt's centered text starts after the icon area.
_ICON_LEFT_PAD = 30


def _ghost_button(icon: FluentIcon, text: str) -> PushButton:
    btn = PushButton(icon, text)
    btn.setFixedHeight(34)
    btn.setMinimumWidth(128)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        f"""
        PushButton {{
            background: {SAND};
            color: {INK_3};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 0 14px 0 {_ICON_LEFT_PAD}px;
            font-size: 13px;
            font-weight: 500;
            text-align: center;
        }}
        PushButton:hover {{
            background: {SAND_2};
            color: {INK};
        }}
        PushButton:pressed {{
            background: #E0D9CB;
        }}
        """
    )
    return btn


def _danger_button(icon: FluentIcon, text: str) -> PushButton:
    btn = PushButton(icon, text)
    btn.setFixedHeight(34)
    btn.setMinimumWidth(128)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        f"""
        PushButton {{
            background: {SAND};
            color: {PRIMARY};
            border: 1px solid {RUST_DIM};
            border-radius: 8px;
            padding: 0 14px 0 {_ICON_LEFT_PAD}px;
            font-size: 13px;
            font-weight: 500;
            text-align: center;
        }}
        PushButton:hover {{
            background: {RUST_LIGHT};
        }}
        """
    )
    return btn


def _primary_button(icon: FluentIcon, text: str) -> PrimaryPushButton:
    btn = PrimaryPushButton(icon, text)
    btn.setFixedHeight(34)
    btn.setMinimumWidth(156)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        f"""
        PrimaryPushButton {{
            background: {PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0 16px 0 {_ICON_LEFT_PAD + 2}px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.1px;
            text-align: center;
        }}
        PrimaryPushButton:hover {{ background: {PRIMARY_HOVER}; }}
        PrimaryPushButton:pressed {{ background: {PRIMARY_PRESSED}; }}
        """
    )
    return btn


class AppHeader(QFrame):
    """60 px cream top bar with eyebrow + search + actions + status pill."""

    load_model_requested = pyqtSignal()
    upload_image_requested = pyqtSignal()
    run_detection_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AppHeader")
        self.setFixedHeight(60)
        self.setStyleSheet(
            f"""
            #AppHeader {{
                background: {CREAM};
                border-bottom: 1px solid {BORDER};
            }}
            """
        )

        root = QHBoxLayout(self)
        root.setContentsMargins(28, 12, 28, 12)
        root.setSpacing(16)

        # Eyebrow — uppercase page context
        self.eyebrow = QLabel("WORKSPACE")
        self.eyebrow.setStyleSheet(
            f"""
            font-size: 11px;
            color: {TEXT_FAINT};
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            """
        )
        root.addWidget(self.eyebrow, 1)

        # Search bar
        self.search = SearchLineEdit()
        self.search.setPlaceholderText("Search detections, images…")
        self.search.setFixedHeight(34)
        self.search.setFixedWidth(240)
        self.search.setStyleSheet(
            f"""
            SearchLineEdit {{
                background: {SAND};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding-left: 4px;
                font-size: 13px;
                color: {INK};
            }}
            SearchLineEdit:focus {{
                border: 1px solid {PRIMARY};
                background: {CREAM};
            }}
            """
        )
        root.addWidget(self.search)

        # Actions
        actions = QHBoxLayout()
        actions.setSpacing(8)

        self.load_button = _ghost_button(FluentIcon.ROBOT, "Load Model")
        self.upload_button = _ghost_button(FluentIcon.PHOTO, "Upload")
        self.run_button = _primary_button(FluentIcon.PLAY, "Run Detection")

        self.load_button.clicked.connect(self.load_model_requested)
        self.upload_button.clicked.connect(self.upload_image_requested)
        self.run_button.clicked.connect(self.run_detection_requested)

        actions.addWidget(self.load_button)
        actions.addWidget(self.upload_button)
        actions.addWidget(self.run_button)

        separator = QWidget()
        separator.setFixedSize(1, 22)
        separator.setStyleSheet(f"background: {BORDER};")
        actions.addSpacing(4)
        actions.addWidget(separator)
        actions.addSpacing(4)

        self.status_pill = ModelStatusPill()
        actions.addWidget(self.status_pill)

        root.addLayout(actions)

    def set_status(self, text: str, state: str) -> None:
        self.status_pill.set_status(text, state)

    def set_eyebrow(self, text: str) -> None:
        self.eyebrow.setText(text.upper())
