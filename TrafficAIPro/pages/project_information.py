"""Project information showcase page."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget, StrongBodyLabel

from .base import Page
from ..utils.theme import (
    BORDER,
    CREAM,
    FONT_SERIF,
    GOLD,
    GOLD_LIGHT,
    INK,
    INK_3,
    RADIUS_LG,
    RUST,
    RUST_LIGHT,
    SAGE,
    SAGE_LIGHT,
    SAND,
    SAND_2,
    SLATE,
    SLATE_LIGHT,
    TEXT_FAINT,
)


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _soft_shadow(widget: QWidget, blur: int = 26, y_offset: int = 8) -> None:
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(60, 30, 10, 32))
    widget.setGraphicsEffect(shadow)


def _badge(text: str, accent: str = RUST, background: str = RUST_LIGHT) -> QLabel:
    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet(
        f"""
        QLabel {{
            background: {background};
            color: {accent};
            border: 1px solid rgba({_hex_to_rgb(accent)}, 0.16);
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
        }}
        """
    )
    return label


class HeroBanner(CardWidget):
    """Premium project title banner."""

    def __init__(self) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(260)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A1208,
                    stop:0.52 #3D2B1F,
                    stop:1 #C4512A
                );
                border: 1px solid rgba(255, 255, 255, 0.16);
            }}
            """
        )
        _soft_shadow(self, blur=34, y_offset=10)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(16)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        icon_shell = QFrame()
        icon_shell.setFixedSize(54, 54)
        icon_shell.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 14px;
            }
            """
        )
        icon_layout = QHBoxLayout(icon_shell)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon = IconWidget(FluentIcon.ROBOT)
        icon.setFixedSize(28, 28)
        icon_layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(icon_shell)

        title_box = QVBoxLayout()
        title_box.setSpacing(4)
        title = QLabel("TrafficVision AI")
        title.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 38px;
            font-weight: 800;
            color: {CREAM};
            letter-spacing: 0;
            """
        )
        subtitle = QLabel("YOLOv26-powered Vehicle Detection and Traffic Analytics System")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            """
            font-size: 16px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.76);
            """
        )
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        top_row.addLayout(title_box, 1)
        layout.addLayout(top_row)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(10)
        for badge_text in ("YOLOv26", "Computer Vision", "Traffic Analytics", "Vehicle Detection"):
            badge = QLabel(badge_text)
            badge.setStyleSheet(
                """
                QLabel {
                    background: rgba(255, 255, 255, 0.12);
                    color: rgba(255, 255, 255, 0.88);
                    border: 1px solid rgba(255, 255, 255, 0.16);
                    border-radius: 999px;
                    padding: 7px 12px;
                    font-size: 12px;
                    font-weight: 700;
                }
                """
            )
            badge_row.addWidget(badge)
        badge_row.addStretch(1)
        layout.addLayout(badge_row)

        description = BodyLabel(
            "TrafficVision AI is an intelligent traffic monitoring system that uses "
            "YOLOv26 to detect, classify, and analyze road vehicles in real time."
        )
        description.setWordWrap(True)
        description.setStyleSheet(
            """
            font-size: 14px;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.78);
            max-width: 760px;
            """
        )
        layout.addWidget(description)
        layout.addStretch(1)


class SectionTitle(QWidget):
    """Small section header used throughout the showcase page."""

    def __init__(self, eyebrow: str, title: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(4)

        eyebrow_label = QLabel(eyebrow.upper())
        eyebrow_label.setStyleSheet(
            f"font-size: 10px; font-weight: 800; color: {TEXT_FAINT}; letter-spacing: 1.6px;"
        )
        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 26px;
            font-weight: 800;
            color: {INK};
            letter-spacing: 0;
            """
        )
        layout.addWidget(eyebrow_label)
        layout.addWidget(title_label)


class InfoCard(CardWidget):
    """Project metadata card."""

    def __init__(self, title: str, value: str, icon: FluentIcon, accent: str, soft: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(132)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            CardWidget:hover {{
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.34);
                background: #FBF8F1;
            }}
            """
        )
        _soft_shadow(self, blur=20, y_offset=6)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        chip = QFrame()
        chip.setFixedSize(34, 34)
        chip.setStyleSheet(f"background: {soft}; border-radius: 9px;")
        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(0, 0, 0, 0)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(18, 18)
        chip_layout.addWidget(icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(chip)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"font-size: 11px; font-weight: 800; color: {TEXT_FAINT}; letter-spacing: 0.8px;"
        )
        layout.addWidget(title_label)

        value_label = BodyLabel(value)
        value_label.setWordWrap(True)
        value_label.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {INK};")
        layout.addWidget(value_label)
        layout.addStretch(1)


class ListCard(CardWidget):
    """Compact card for a list of stack/class chips."""

    def __init__(self, title: str, values: list[str], icon: FluentIcon, accent: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(150)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )
        _soft_shadow(self, blur=20, y_offset=6)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.setSpacing(10)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(20, 20)
        header.addWidget(icon_widget)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: 800; color: {INK};")
        header.addWidget(title_label)
        header.addStretch(1)
        layout.addLayout(header)

        chip_grid = QGridLayout()
        chip_grid.setHorizontalSpacing(8)
        chip_grid.setVerticalSpacing(8)
        for index, value in enumerate(values):
            chip_grid.addWidget(_badge(value, accent=accent, background=CREAM), index // 3, index % 3)
        layout.addLayout(chip_grid)
        layout.addStretch(1)


class AcademicFactCard(CardWidget):
    """Small premium fact card placed directly below the hero."""

    def __init__(self, title: str, value: str, icon: FluentIcon, accent: str, soft: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(116)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            CardWidget:hover {{
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.34);
                background: #FBF8F1;
            }}
            """
        )
        _soft_shadow(self, blur=20, y_offset=6)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        icon_shell = QFrame()
        icon_shell.setFixedSize(42, 42)
        icon_shell.setStyleSheet(
            f"""
            QFrame {{
                background: {soft};
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.14);
                border-radius: 12px;
            }}
            """
        )
        icon_layout = QHBoxLayout(icon_shell)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(21, 21)
        icon_layout.addWidget(icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_shell)

        text_box = QVBoxLayout()
        text_box.setSpacing(5)
        title_label = QLabel(title.upper())
        title_label.setStyleSheet(
            f"font-size: 10px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1.2px;"
        )
        value_label = BodyLabel(value)
        value_label.setWordWrap(True)
        value_label.setStyleSheet(f"font-size: 14px; font-weight: 850; color: {INK};")
        text_box.addWidget(title_label)
        text_box.addWidget(value_label)
        text_box.addStretch(1)
        layout.addLayout(text_box, 1)


class AcademicFactsStrip(QWidget):
    """Course, university and dataset facts elevated below the hero banner."""

    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        facts = [
            (
                "Course",
                "Digital Image Processing",
                FluentIcon.INFO,
                RUST,
                RUST_LIGHT,
            ),
            (
                "University",
                "Ho Chi Minh City University of Technology and Engineering (HCMUTE)",
                FluentIcon.HOME,
                SLATE,
                SLATE_LIGHT,
            ),
            (
                "Dataset",
                "Vehicle Detection Dataset",
                FluentIcon.PHOTO,
                SAGE,
                SAGE_LIGHT,
            ),
        ]
        for index, fact in enumerate(facts):
            layout.addWidget(AcademicFactCard(*fact), 0, index)
            layout.setColumnStretch(index, 1)


class ProjectProfilePanel(CardWidget):
    """Single premium profile block replacing fragmented info cards."""

    def __init__(self) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(260)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )
        _soft_shadow(self, blur=30, y_offset=9)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(22)

        brief = QVBoxLayout()
        brief.setSpacing(12)

        eyebrow = QLabel("ACADEMIC DEFENSE PROFILE")
        eyebrow.setStyleSheet(
            f"font-size: 10px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1.5px;"
        )
        brief.addWidget(eyebrow)

        title = QLabel("Built for real-time traffic understanding")
        title.setWordWrap(True)
        title.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 28px;
            font-weight: 850;
            color: {INK};
            letter-spacing: 0;
            """
        )
        brief.addWidget(title)

        description = BodyLabel(
            "TrafficVision AI combines image enhancement, YOLOv26 detection, vehicle classification, "
            "analytics, and report-ready dashboards inside a professional desktop interface."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"font-size: 13.5px; line-height: 1.65; color: {INK_3};")
        brief.addWidget(description)

        fact_grid = QGridLayout()
        fact_grid.setHorizontalSpacing(10)
        fact_grid.setVerticalSpacing(10)
        facts = [
            ("Course", "Digital Image Processing", RUST, RUST_LIGHT),
            ("University", "HCMUTE", SLATE, SLATE_LIGHT),
            ("Dataset", "Vehicle Detection Dataset", SAGE, SAGE_LIGHT),
            ("Academic Year", "2025-2026", GOLD, GOLD_LIGHT),
        ]
        for index, (caption, value, accent, soft) in enumerate(facts):
            fact_grid.addWidget(self._fact_tile(caption, value, accent, soft), index // 2, index % 2)
        brief.addLayout(fact_grid)
        layout.addLayout(brief, 5)

        divider = QFrame()
        divider.setFixedWidth(1)
        divider.setStyleSheet(f"background: {BORDER};")
        layout.addWidget(divider)

        highlights = QVBoxLayout()
        highlights.setSpacing(10)
        highlights.addWidget(
            self._feature_row(
                FluentIcon.ROBOT,
                "YOLOv26 Detection Core",
                "Ultralytics-powered vehicle detection pipeline",
                ["YOLOv26", "Ultralytics"],
                RUST,
                RUST_LIGHT,
            )
        )
        highlights.addWidget(
            self._feature_row(
                FluentIcon.CAR,
                "Vehicle Intelligence",
                "Classification coverage for main road vehicle groups",
                ["Car", "Bus", "Truck", "Van"],
                SAGE,
                SAGE_LIGHT,
            )
        )
        highlights.addWidget(
            self._feature_row(
                FluentIcon.PIE_SINGLE,
                "Analytics Experience",
                "Dashboard, history, charts, and presentation-ready reports",
                ["Python", "PyQt6", "OpenCV"],
                SLATE,
                SLATE_LIGHT,
            )
        )
        layout.addLayout(highlights, 4)

    def _fact_tile(self, caption: str, value: str, accent: str, soft: str) -> QFrame:
        tile = QFrame()
        tile.setStyleSheet(
            f"""
            QFrame {{
                background: {soft};
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.14);
                border-radius: 10px;
            }}
            """
        )
        layout = QVBoxLayout(tile)
        layout.setContentsMargins(13, 10, 13, 10)
        layout.setSpacing(4)
        caption_label = QLabel(caption.upper())
        caption_label.setStyleSheet(
            f"font-size: 9px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1px;"
        )
        value_label = QLabel(value)
        value_label.setWordWrap(True)
        value_label.setStyleSheet(f"font-size: 13px; font-weight: 850; color: {accent};")
        layout.addWidget(caption_label)
        layout.addWidget(value_label)
        return tile

    def _feature_row(
        self,
        icon: FluentIcon,
        title: str,
        description: str,
        chips: list[str],
        accent: str,
        soft: str,
    ) -> QFrame:
        row = QFrame()
        row.setStyleSheet(
            f"""
            QFrame {{
                background: {CREAM};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
            """
        )
        layout = QHBoxLayout(row)
        layout.setContentsMargins(14, 13, 14, 13)
        layout.setSpacing(12)

        chip = QFrame()
        chip.setFixedSize(38, 38)
        chip.setStyleSheet(f"background: {soft}; border-radius: 10px;")
        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(0, 0, 0, 0)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(20, 20)
        chip_layout.addWidget(icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(chip)

        copy = QVBoxLayout()
        copy.setSpacing(5)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: 850; color: {INK};")
        desc_label = BodyLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"font-size: 12px; color: {INK_3}; font-weight: 600;")
        copy.addWidget(title_label)
        copy.addWidget(desc_label)

        chip_row = QHBoxLayout()
        chip_row.setSpacing(6)
        for chip_text in chips:
            chip_row.addWidget(_badge(chip_text, accent=accent, background=soft))
        chip_row.addStretch(1)
        copy.addLayout(chip_row)

        layout.addLayout(copy, 1)
        return row


class ProjectOverviewCard(CardWidget):
    """Large polished project overview block."""

    def __init__(self) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(210)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )
        _soft_shadow(self, blur=28, y_offset=8)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(22)

        left = QVBoxLayout()
        left.setSpacing(10)

        label = QLabel("PROJECT SHOWCASE")
        label.setStyleSheet(
            f"font-size: 10px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1.5px;"
        )
        left.addWidget(label)

        title = QLabel("TrafficVision AI")
        title.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 30px;
            font-weight: 850;
            color: {INK};
            letter-spacing: 0;
            """
        )
        left.addWidget(title)

        subtitle = BodyLabel("YOLOv26-Based Vehicle Detection and Traffic Analytics System")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"font-size: 15px; font-weight: 750; color: {RUST};")
        left.addWidget(subtitle)

        body = BodyLabel(
            "A computer vision desktop application for detecting vehicles, classifying traffic "
            "objects, analyzing detection results, and presenting visual reports in a clean PyQt6 interface."
        )
        body.setWordWrap(True)
        body.setStyleSheet(f"font-size: 13px; line-height: 1.6; color: {INK_3};")
        left.addWidget(body)

        chip_row = QHBoxLayout()
        chip_row.setSpacing(8)
        for text, accent, soft in (
            ("Digital Image Processing", RUST, RUST_LIGHT),
            ("HCMUTE", SLATE, SLATE_LIGHT),
            ("2025-2026", SAGE, SAGE_LIGHT),
        ):
            chip_row.addWidget(_badge(text, accent=accent, background=soft))
        chip_row.addStretch(1)
        left.addLayout(chip_row)
        layout.addLayout(left, 3)

        divider = QFrame()
        divider.setFixedWidth(1)
        divider.setStyleSheet(f"background: {BORDER};")
        layout.addWidget(divider)

        right = QGridLayout()
        right.setHorizontalSpacing(10)
        right.setVerticalSpacing(10)
        highlights = [
            ("MODEL", "YOLOv26", RUST, RUST_LIGHT),
            ("APP", "PyQt6", SLATE, SLATE_LIGHT),
            ("VISION", "OpenCV", SAGE, SAGE_LIGHT),
            ("OUTPUT", "Reports", GOLD, GOLD_LIGHT),
        ]
        for index, (caption, value, accent, soft) in enumerate(highlights):
            mini = QFrame()
            mini.setStyleSheet(
                f"""
                QFrame {{
                    background: {soft};
                    border: 1px solid rgba({_hex_to_rgb(accent)}, 0.14);
                    border-radius: 10px;
                }}
                """
            )
            mini_layout = QVBoxLayout(mini)
            mini_layout.setContentsMargins(14, 12, 14, 12)
            mini_layout.setSpacing(4)
            caption_label = QLabel(caption)
            caption_label.setStyleSheet(
                f"font-size: 9px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1px;"
            )
            value_label = QLabel(value)
            value_label.setStyleSheet(f"font-size: 15px; font-weight: 850; color: {accent};")
            mini_layout.addWidget(caption_label)
            mini_layout.addWidget(value_label)
            right.addWidget(mini, index // 2, index % 2)
        layout.addLayout(right, 2)


class MemberCard(CardWidget):
    """Modern team member profile card."""

    def __init__(self, name: str, student_id: str, initials: str, accent: str, soft: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(190)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            CardWidget:hover {{
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.35);
                background: #FBF8F1;
            }}
            """
        )
        _soft_shadow(self, blur=22, y_offset=7)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(12)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        avatar = QLabel(initials)
        avatar.setFixedSize(64, 64)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"""
            QLabel {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {soft},
                    stop:1 #FFFFFF
                );
                color: {accent};
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.18);
                border-radius: 32px;
                font-size: 18px;
                font-weight: 850;
            }}
            """
        )
        top_row.addWidget(avatar)

        identity = QVBoxLayout()
        identity.setSpacing(5)

        name_label = QLabel(name)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"font-size: 18px; font-weight: 850; color: {INK};")
        identity.addWidget(name_label)

        member_label = QLabel("TRAFFICVISION AI TEAM")
        member_label.setStyleSheet(
            f"font-size: 9px; font-weight: 850; color: {TEXT_FAINT}; letter-spacing: 1.1px;"
        )
        identity.addWidget(member_label)

        top_row.addLayout(identity, 1)
        layout.addLayout(top_row)

        id_panel = QFrame()
        id_panel.setStyleSheet(
            f"""
            QFrame {{
                background: {soft};
                border: 1px solid rgba({_hex_to_rgb(accent)}, 0.14);
                border-radius: 10px;
            }}
            """
        )
        id_layout = QHBoxLayout(id_panel)
        id_layout.setContentsMargins(12, 9, 12, 9)
        id_layout.setSpacing(8)
        id_caption = QLabel("Student ID")
        id_caption.setStyleSheet(f"font-size: 11px; font-weight: 750; color: {INK_3};")
        id_value = QLabel(student_id)
        id_value.setStyleSheet(f"font-size: 13px; font-weight: 850; color: {accent};")
        id_layout.addWidget(id_caption)
        id_layout.addStretch(1)
        id_layout.addWidget(id_value)
        layout.addWidget(id_panel)
        layout.addStretch(1)


class ArchitectureStep(CardWidget):
    """One step in the system architecture flow."""

    def __init__(self, title: str, icon: FluentIcon, accent: str, soft: str) -> None:
        super().__init__()
        self.setBorderRadius(10)
        self.setMinimumSize(142, 118)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )
        _soft_shadow(self, blur=16, y_offset=5)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 13, 12, 13)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chip = QFrame()
        chip.setFixedSize(34, 34)
        chip.setStyleSheet(f"background: {soft}; border-radius: 9px;")
        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(0, 0, 0, 0)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(18, 18)
        chip_layout.addWidget(icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(chip, 0, Qt.AlignmentFlag.AlignCenter)

        label = BodyLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet(f"font-size: 12.5px; font-weight: 800; color: {INK};")
        layout.addWidget(label)


class FooterCard(CardWidget):
    """Academic footer with a polished product-page feel."""

    def __init__(self) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND_2};
                border: 1px solid {BORDER};
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 16, 22, 16)
        layout.setSpacing(14)

        icon = IconWidget(FluentIcon.INFO)
        icon.setFixedSize(22, 22)
        layout.addWidget(icon)

        text = BodyLabel(
            "TrafficVision AI  |  Ho Chi Minh City University of Technology and Engineering  |  "
            "Academic Year 2025-2026"
        )
        text.setWordWrap(True)
        text.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {INK_3};")
        layout.addWidget(text, 1)


class ProjectInformationPage(Page):
    """Premium project information page for defense presentations."""

    def __init__(self) -> None:
        super().__init__("Project Information", "ProjectInformationPage")
        self.layout.setSpacing(22)

        self.layout.addWidget(HeroBanner())

        self._add_project_information()

        self.layout.addWidget(SectionTitle("Team", "Team Members"))
        self._add_team_members()

        self.layout.addWidget(SectionTitle("Architecture", "System Architecture"))
        self._add_architecture_flow()

        self.layout.addWidget(FooterCard())
        self.layout.addStretch(1)

    def _add_project_information(self) -> None:
        self.layout.addWidget(AcademicFactsStrip())

    def _add_team_members(self) -> None:
        grid = QGridLayout()
        grid.setSpacing(14)
        members = [
            (
                "Trịnh Nhật Anh",
                "23110074",
                "NA",
                RUST,
                RUST_LIGHT,
            ),
            (
                "Phạm Công Trường",
                "23110163",
                "CT",
                SLATE,
                SLATE_LIGHT,
            ),
            (
                "Trần Minh Huy",
                "23110106",
                "MH",
                SAGE,
                SAGE_LIGHT,
            ),
        ]
        for index, member in enumerate(members):
            grid.addWidget(MemberCard(*member), 0, index)
            grid.setColumnStretch(index, 1)
        self.layout.addLayout(grid)

    def _add_architecture_flow(self) -> None:
        flow_card = CardWidget()
        flow_card.setBorderRadius(RADIUS_LG)
        flow_card.setStyleSheet(
            f"""
            CardWidget {{
                background: {CREAM};
                border: 1px solid {BORDER};
            }}
            """
        )
        _soft_shadow(flow_card, blur=24, y_offset=7)

        layout = QHBoxLayout(flow_card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        steps = [
            ("Video/Image", FluentIcon.PHOTO, SLATE, SLATE_LIGHT),
            ("Image Processing", FluentIcon.PALETTE, RUST, RUST_LIGHT),
            ("YOLOv26 Detection", FluentIcon.ROBOT, SAGE, SAGE_LIGHT),
            ("Vehicle Classification", FluentIcon.CAR, GOLD, GOLD_LIGHT),
            ("Traffic Analytics", FluentIcon.PIE_SINGLE, RUST, RUST_LIGHT),
            ("Dashboard & Reports", FluentIcon.SPEED_HIGH, SLATE, SLATE_LIGHT),
        ]
        for index, (title, icon, accent, soft) in enumerate(steps):
            layout.addWidget(ArchitectureStep(title, icon, accent, soft), 1)
            if index < len(steps) - 1:
                arrow = StrongBodyLabel("→")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {TEXT_FAINT};")
                layout.addWidget(arrow)

        self.layout.addWidget(flow_card)
