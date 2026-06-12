"""Dashboard page — glass cards on an atmospheric depth canvas."""

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
from qfluentwidgets import BodyLabel, CardWidget, FluentIcon, IconWidget

from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from ..utils.paths import APP_ROOT, WORKSPACE_ROOT
from ..utils.theme import (
    BORDER,
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
    SUCCESS,
    TEXT_FAINT,
    VEHICLE_COLORS,
    VEHICLE_COLORS_SOFT,
)
from ..widgets.metric_card import MetricCard
from .base import Page
from .project_information import (
    AcademicFactsStrip,
    ArchitectureStep,
    FooterCard,
    HeroBanner,
    MemberCard,
    SectionTitle as ProjectSectionTitle,
    _soft_shadow as _project_soft_shadow,
)


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _apply_glass(card: CardWidget, accent: str = RUST, blur: int = 28) -> None:
    """Make a CardWidget translucent so the depth blobs glow through."""
    card.setStyleSheet(
        f"""
        CardWidget {{
            background: rgba(255, 251, 244, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.65);
        }}
        CardWidget:hover {{
            background: rgba(255, 252, 246, 0.72);
            border: 1px solid rgba({_hex_to_rgb(accent)}, 0.35);
        }}
        """
    )
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(6)
    shadow.setColor(QColor(60, 30, 10, 38))
    card.setGraphicsEffect(shadow)


def _apply_glass_frame(frame: QFrame, blur: int = 24) -> None:
    """Translucent variant for plain QFrame (no CardWidget selector)."""
    frame.setStyleSheet(
        """
        QFrame {
            background: rgba(255, 251, 244, 0.55);
            border: 1.5px dashed rgba(154, 117, 96, 0.55);
            border-radius: 12px;
        }
        """
    )
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(5)
    shadow.setColor(QColor(60, 30, 10, 30))
    frame.setGraphicsEffect(shadow)


class InfoCard(CardWidget):
    """Compact card — sand surface, serif title, body text."""

    def __init__(self, title: str, body: str, icon: FluentIcon, accent: str) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setMinimumHeight(120)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 18)
        layout.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(10)

        chip = QFrame()
        chip.setFixedSize(26, 26)
        h = accent.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        chip.setStyleSheet(
            f"""
            QFrame {{
                background: rgba({r}, {g}, {b}, 0.14);
                border-radius: 6px;
            }}
            """
        )
        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(0, 0, 0, 0)
        icon_widget = IconWidget(icon)
        icon_widget.setFixedSize(14, 14)
        chip_layout.addWidget(icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        header.addWidget(chip)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"""
            font-family: {FONT_SERIF};
            font-size: 15px;
            font-weight: 600;
            color: {INK};
            """
        )
        header.addWidget(title_label, 1, Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(header)

        self.body_label = BodyLabel(body)
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet(
            f"font-size: 13px; color: {INK_3}; line-height: 1.55;"
        )
        layout.addWidget(self.body_label)
        layout.addStretch(1)


class ModelInfoCard(CardWidget):
    """Right-column model info card — 2-col grid of key/value pairs."""

    def __init__(self) -> None:
        super().__init__()
        self.setBorderRadius(RADIUS_LG)
        self.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header strip
        head = QFrame()
        head.setStyleSheet(
            f"background: {SAND_2}; border-bottom: 1px solid {BORDER};"
        )
        head_layout = QHBoxLayout(head)
        head_layout.setContentsMargins(18, 12, 18, 12)

        title = QLabel("Model Info")
        title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {INK};")
        head_layout.addWidget(title)
        head_layout.addStretch(1)

        live = QLabel("● Online")
        live.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {SAGE};")
        head_layout.addWidget(live)
        root.addWidget(head)

        # Body grid
        body = QFrame()
        body_layout = QGridLayout(body)
        body_layout.setContentsMargins(18, 14, 18, 16)
        body_layout.setHorizontalSpacing(16)
        body_layout.setVerticalSpacing(12)

        items = [
            ("ARCHITECTURE", "YOLO26n", INK),
            ("SIZE", "5.4 MB", INK),
            ("mAP@50", "0.981", SAGE),
            ("PRECISION", "0.955", SAGE),
            ("RECALL", "0.951", SAGE),
            ("DEVICE", "Tesla T4", INK),
        ]
        for i, (key, val, color) in enumerate(items):
            key_label = QLabel(key)
            key_label.setStyleSheet(
                f"font-size: 10px; color: {TEXT_FAINT}; letter-spacing: 0.5px; font-weight: 600;"
            )
            val_label = QLabel(val)
            val_label.setStyleSheet(
                f"font-size: 13px; font-weight: 600; color: {color};"
            )
            cell = QVBoxLayout()
            cell.setSpacing(2)
            cell.addWidget(key_label)
            cell.addWidget(val_label)
            body_layout.addLayout(cell, i // 2, i % 2)

        root.addWidget(body)


class UploadHintCard(QFrame):
    """Dashed-border upload hint with icon + label."""

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            f"""
            QFrame {{
                background: #FBF8F1;
                border: 1.5px dashed #C4AA96;
                border-radius: {RADIUS_LG}px;
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 22, 20, 22)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = IconWidget(FluentIcon.CLOUD)
        icon.setFixedSize(28, 28)
        layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Upload new image or video")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 13px; color: {INK_3}; font-weight: 600;")
        layout.addWidget(title)

        sub = QLabel("JPG, PNG, MP4  ·  Max 50 MB")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 11px; color: {TEXT_FAINT};")
        layout.addWidget(sub)


class DashboardPage(Page):
    """Project landing information followed by the operational dashboard."""

    def __init__(self) -> None:
        super().__init__("Project Information", "DashboardPage")

        # Traffic-video background + atmospheric color washes.
        # Drop a custom file at assets/backgrounds/dashboard.mp4 to override.
        backgrounds_dir = APP_ROOT / "assets" / "backgrounds"
        video_candidates = [
            backgrounds_dir / "dashboard.mp4",
            backgrounds_dir / "traffic.mp4",
            WORKSPACE_ROOT / "test_video.mp4",
        ]
        self.view.enable_video_background(video_candidates)
        self.view.depth_blobs = True
        self.view.update()
        self._mode_summaries: dict[str, DetectionSummary] = {}

        self._add_project_information()
        self.layout.addWidget(ProjectSectionTitle("Dashboard", "Detection Dashboard"))

        # ---- Stat strip ----------------------------------------------
        stat_grid = QGridLayout()
        stat_grid.setSpacing(14)

        card_accents = {
            "total": (RUST,  "TODAY",    RUST_LIGHT),
            "car":   (SLATE, "DOMINANT", SLATE_LIGHT),
            "bus":   (RUST,  "LOW",      RUST_LIGHT),
            "truck": (GOLD,  "NORMAL",   GOLD_LIGHT),
            "van":   (SAGE,  "NORMAL",   SAGE_LIGHT),
        }
        card_titles = {
            "total": "Total Vehicles", "car": "Cars", "bus": "Buses",
            "truck": "Trucks", "van": "Vans",
        }
        self.cards: dict[str, MetricCard] = {}
        for index, (key, (accent, badge, bg)) in enumerate(card_accents.items()):
            card = MetricCard(card_titles[key], "0", None, accent, badge=badge, badge_bg=bg)
            _apply_glass(card, accent=accent, blur=22)
            self.cards[key] = card
            stat_grid.addWidget(card, 0, index)
        self.layout.addLayout(stat_grid)
        self.layout.addSpacing(12)

        # ---- Two-column: details + right column ----------------------
        two_col = QHBoxLayout()
        two_col.setSpacing(20)

        # Left — DETAILS info cards (2x2)
        left = QVBoxLayout()
        left.setSpacing(14)

        details_grid = QGridLayout()
        details_grid.setSpacing(14)
        self.summary = InfoCard(
            "Recent Detection Summary", "No recent detection",
            FluentIcon.HISTORY, RUST,
        )
        self.stats = InfoCard(
            "Quick Statistics",
            "Cars 0  ·  Buses 0  ·  Trucks 0  ·  Vans 0",
            FluentIcon.PIE_SINGLE, SLATE,
        )
        self.performance = InfoCard(
            "Performance Metrics",
            "Processing time 0.00s  ·  Average confidence 0%",
            FluentIcon.SPEED_HIGH, SAGE,
        )
        self.model = InfoCard(
            "Model Information", "YOLO26 model pending",
            FluentIcon.ROBOT, GOLD,
        )
        for info_card, accent in (
            (self.summary, RUST),
            (self.stats, SLATE),
            (self.performance, SAGE),
            (self.model, GOLD),
        ):
            _apply_glass(info_card, accent=accent, blur=32)
        details_grid.addWidget(self.summary, 0, 0)
        details_grid.addWidget(self.stats, 0, 1)
        details_grid.addWidget(self.performance, 1, 0)
        details_grid.addWidget(self.model, 1, 1)
        details_grid.setColumnStretch(0, 1)
        details_grid.setColumnStretch(1, 1)
        left.addLayout(details_grid)
        left.addStretch(1)
        two_col.addLayout(left, 1)

        # Right — model info + upload hint
        right = QVBoxLayout()
        right.setSpacing(14)
        model_info = ModelInfoCard()
        _apply_glass(model_info, accent=GOLD, blur=32)
        right.addWidget(model_info)

        self.hardware = InfoCard(
            "Hardware Status",
            self._hardware_status_text("Mock", "Green", "None"),
            FluentIcon.ROBOT,
            SAGE,
        )
        _apply_glass(self.hardware, accent=SAGE, blur=28)
        right.addWidget(self.hardware)

        self.comparison = InfoCard(
            "Standard YOLO vs SAHI",
            "Run both modes on traffic media to compare detections.",
            FluentIcon.SPEED_HIGH,
            RUST,
        )
        _apply_glass(self.comparison, accent=RUST, blur=28)
        right.addWidget(self.comparison)

        upload_hint = UploadHintCard()
        _apply_glass_frame(upload_hint, blur=24)
        right.addWidget(upload_hint)
        right.addStretch(1)
        right_wrap = QFrame()
        right_wrap.setFixedWidth(300)
        right_wrap.setLayout(right)
        two_col.addWidget(right_wrap)

        self.layout.addLayout(two_col)
        self.layout.addWidget(FooterCard())
        self.layout.addStretch(1)

    def _add_project_information(self) -> None:
        self.layout.setSpacing(22)
        self.layout.addWidget(HeroBanner())
        self.layout.addWidget(AcademicFactsStrip())

        self.layout.addWidget(ProjectSectionTitle("Team", "Team Members"))
        team_grid = QGridLayout()
        team_grid.setSpacing(14)
        members = [
            ("Trịnh Nhật Anh", "23110074", "NA", RUST, RUST_LIGHT),
            ("Phạm Công Trường", "23110163", "CT", SLATE, SLATE_LIGHT),
            ("Trần Minh Huy", "23110106", "MH", SAGE, SAGE_LIGHT),
        ]
        for index, member in enumerate(members):
            team_grid.addWidget(MemberCard(*member), 0, index)
            team_grid.setColumnStretch(index, 1)
        self.layout.addLayout(team_grid)

        self.layout.addWidget(ProjectSectionTitle("Architecture", "System Architecture"))
        self.layout.addWidget(self._build_architecture_flow())

    def _build_architecture_flow(self) -> CardWidget:
        flow_card = CardWidget()
        flow_card.setBorderRadius(RADIUS_LG)
        flow_card.setStyleSheet(
            """
            CardWidget {
                background: rgba(255, 251, 244, 0.72);
                border: 1px solid rgba(255, 255, 255, 0.68);
            }
            """
        )
        _project_soft_shadow(flow_card, blur=24, y_offset=7)

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
                arrow = BodyLabel("→")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setStyleSheet(
                    f"font-size: 24px; font-weight: 800; color: {TEXT_FAINT};"
                )
                layout.addWidget(arrow)

        return flow_card

    def update_summary(self, summary: DetectionSummary, model_name: str) -> None:
        self._mode_summaries[summary.detection_mode.value] = summary
        self.cards["total"].set_value(summary.total)
        for key in VEHICLE_CLASSES:
            self.cards[key].set_value(summary.counts.get(key, 0))
        self.summary.body_label.setText(
            f"{summary.image_name}: {summary.total} vehicles detected"
        )
        self.stats.body_label.setText(
            "  ·  ".join(
                f"{key.title()} {summary.counts.get(key, 0)}" for key in VEHICLE_CLASSES
            )
        )
        self.performance.body_label.setText(
            f"Processing time {summary.processing_time:.2f}s  ·  "
            f"Average confidence {summary.average_confidence:.0%}"
        )
        self.performance.body_label.setText(
            f"Detection Mode: {summary.detection_mode.display_name}\n"
            f"Inference Time: {summary.processing_time:.2f}s  -  Avg FPS: {summary.fps:.1f}\n"
            f"Average confidence {summary.average_confidence:.0%}"
        )
        self.model.body_label.setText(
            f"Model Status: Loaded\n"
            f"Active model: {model_name}\n"
            f"Total Detections: {len(summary.detections)}  -  Vehicle Count: {summary.total}"
        )
        self._update_detection_comparison()

    def update_hardware_status(self, mode: str, traffic_light: str, last_sent_data: str) -> None:
        """Update optional Arduino integration status."""
        mode_text = "Connected" if mode == "Connected" else "Mock"
        traffic_text = {"G": "Green", "Y": "Yellow", "R": "Red"}.get(
            traffic_light,
            traffic_light if traffic_light in {"Green", "Yellow", "Red"} else "Green",
        )
        self.hardware.body_label.setText(
            self._hardware_status_text(mode_text, traffic_text, last_sent_data or "None")
        )

    def _hardware_status_text(self, mode: str, traffic_light: str, last_sent_data: str) -> str:
        return (
            f"Arduino Mode: {mode}\n"
            f"Traffic Light: {traffic_light}\n"
            f"Last Sent Data: {last_sent_data}"
        )

    def _update_detection_comparison(self) -> None:
        yolo = self._mode_summaries.get("YOLO")
        sahi = self._mode_summaries.get("SAHI")
        if yolo is None or sahi is None:
            latest = next(reversed(self._mode_summaries.values()), None)
            latest_mode = latest.detection_mode.display_name if latest else "YOLO"
            self.comparison.body_label.setText(
                f"Latest mode: {latest_mode}\n"
                "Run the other mode to populate comparison metrics."
            )
            return

        vehicle_delta = sahi.total - yolo.total
        detection_delta = len(sahi.detections) - len(yolo.detections)
        time_delta = sahi.processing_time - yolo.processing_time
        self.comparison.body_label.setText(
            f"Vehicle Count Difference: {vehicle_delta:+d}\n"
            f"Inference Time Difference: {time_delta:+.2f}s\n"
            f"Detection Difference: {detection_delta:+d}"
        )
