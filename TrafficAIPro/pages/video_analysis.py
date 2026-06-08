"""Professional video vehicle detection, tracking and counting page."""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, FluentIcon, InfoBar, InfoBarPosition, PrimaryPushButton, PushButton

from ..models.detection import DetectionSummary, VEHICLE_CLASSES
from ..services.detection_service import VehicleDetectionService
from ..services.image_service import ImageEnhancementService
from ..services.settings_service import SettingsService
from ..utils.theme import (
    BORDER,
    CARD_BORDER,
    DIVIDER,
    FONT_SERIF,
    GOLD,
    INK,
    INK_3,
    PRIMARY,
    PRIMARY_HOVER,
    PRIMARY_PRESSED,
    RUST,
    SAGE,
    SAND,
    SAND_2,
    SECONDARY_TEXT,
    SLATE,
    SUCCESS,
    TEXT,
    TEXT_FAINT,
)
from ..widgets.image_viewer import ImageViewer
from .base import Page


TRACKER_FILES = {
    "ByteTrack": "bytetrack.yaml",
    "BoT-SORT": "botsort.yaml",
}
DEFAULT_VIDEO_CONFIDENCE = 0.25
INFERENCE_FRAME_INTERVAL = 2


class VideoAnalysisPage(Page):
    """Run YOLO26 on RGB frames, track vehicles, and count line crossings."""

    def __init__(
        self,
        image_service: ImageEnhancementService,
        detection_service: VehicleDetectionService,
        settings: SettingsService,
    ) -> None:
        super().__init__("Video Analysis", "VideoAnalysisPage")
        # Tighter page rhythm so the toolbar + stats + 2 videos fit
        # a single 940 px viewport without scrolling.
        self.layout.setContentsMargins(28, 18, 28, 22)
        self.layout.setSpacing(12)
        self.image_service = image_service
        self.detection_service = detection_service
        self.settings = settings
        self.capture: cv2.VideoCapture | None = None
        self.video_path = ""
        self.frame_index = 0
        self.total_frames = 0
        self.last_summary = DetectionSummary()
        self.last_tick = time.perf_counter()

        self.tracked_ids = {name: set() for name in VEHICLE_CLASSES}
        self.previous_centers: dict[int, tuple[int, int]] = {}
        self.track_labels: dict[int, str] = {}
        self.line_initialized = False
        self.last_annotated_frame: np.ndarray | None = None
        self.last_tracks: list[dict[str, object]] = []
        self.last_processing_time = 0.0
        self.last_average_confidence = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_frame)

        self._build_controls()
        self._build_main_panels()
        self._build_timeline()
        self.layout.addStretch(1)

    def _build_controls(self) -> None:
        """Single compact toolbar — all controls fit in one row,
        grouped by hairline vertical dividers. Designed to keep the
        page short enough that the videos + stats fit in one viewport.
        """
        toolbar = CardWidget()
        toolbar.setBorderRadius(10)
        toolbar.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )
        toolbar_layout = QVBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(14, 8, 14, 8)
        toolbar_layout.setSpacing(8)

        # ----- Row 1: playback buttons + display toggles -----------------
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        # Buttons — full style with background, border AND padding-left for
        # icon (qfluentwidgets draws its icon outside Qt's text rect).
        primary_css = (
            f"PrimaryPushButton {{"
            f" background: {PRIMARY};"
            f" color: white;"
            f" border: none;"
            f" border-radius: 8px;"
            f" padding: 0 14px 0 30px;"
            f" font-size: 12.5px;"
            f" font-weight: 700;"
            f"}}"
            f"PrimaryPushButton:hover {{ background: {PRIMARY_HOVER}; }}"
            f"PrimaryPushButton:pressed {{ background: {PRIMARY_PRESSED}; }}"
        )
        ghost_css = (
            f"PushButton {{"
            f" background: {SAND};"
            f" color: {INK};"
            f" border: 1px solid {BORDER};"
            f" border-radius: 8px;"
            f" padding: 0 14px 0 28px;"
            f" font-size: 12.5px;"
            f" font-weight: 600;"
            f"}}"
            f"PushButton:hover {{ background: {SAND_2}; border: 1px solid #C4AA96; }}"
            f"PushButton:pressed {{ background: #E0D9CB; }}"
        )

        self.open_button = PrimaryPushButton(FluentIcon.VIDEO, "Open Video")
        self.open_button.setStyleSheet(primary_css)
        self.open_button.clicked.connect(self.open_video)

        self.start_button = PushButton(FluentIcon.PLAY, "Start")
        self.start_button.setStyleSheet(ghost_css)
        self.start_button.clicked.connect(self.start_video)

        self.reset_button = PushButton(FluentIcon.SYNC, "Reset")
        self.reset_button.setStyleSheet(ghost_css)
        self.reset_button.clicked.connect(self.reset_video)

        for btn in (self.open_button, self.start_button, self.reset_button):
            btn.setFixedHeight(32)
            btn.setMinimumWidth(90)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            row1.addWidget(btn)

        row1.addWidget(self._vdiv())

        # Toggles — keep original names: Track, Track ID, Line, Enhance
        self.tracking_check = CheckBox("Track")
        self.tracking_check.setChecked(True)
        self.tracking_check.stateChanged.connect(self._reset_tracking_state)
        self.track_id_check = CheckBox("Track ID")
        self.track_id_check.setChecked(True)
        self.line_check = CheckBox("Line")
        self.line_check.setChecked(True)
        self.enhance_check = CheckBox("Enhance")
        check_css = (
            f"CheckBox {{ color: {INK}; font-size: 12px; font-weight: 500; "
            f"spacing: 6px; padding: 0 2px; }}"
        )
        for cb in (self.tracking_check, self.track_id_check, self.line_check, self.enhance_check):
            cb.setStyleSheet(check_css)
            row1.addWidget(cb)

        row1.addStretch(1)
        toolbar_layout.addLayout(row1)

        # ----- Row 2: detection params + counting-line params -----------
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        self.tracker_combo = QComboBox()
        self.tracker_combo.addItems(TRACKER_FILES.keys())
        self.tracker_combo.setFixedWidth(100)
        self.tracker_combo.currentTextChanged.connect(lambda _: self._reset_tracking_state())
        row2.addWidget(self._lbl("Tracker"))
        row2.addWidget(self.tracker_combo)

        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.05, 0.95)
        self.confidence_spin.setSingleStep(0.05)
        self.confidence_spin.setValue(DEFAULT_VIDEO_CONFIDENCE)
        self.confidence_spin.setFixedWidth(76)
        row2.addWidget(self._lbl("Conf"))
        row2.addWidget(self.confidence_spin)

        self.iou_spin = QDoubleSpinBox()
        self.iou_spin.setRange(0.10, 0.95)
        self.iou_spin.setSingleStep(0.05)
        self.iou_spin.setValue(0.50)
        self.iou_spin.setFixedWidth(76)
        row2.addWidget(self._lbl("IOU"))
        row2.addWidget(self.iou_spin)

        row2.addWidget(self._vdiv())

        self.line_orientation = QComboBox()
        self.line_orientation.addItems(["Horizontal", "Vertical"])
        self.line_orientation.setFixedWidth(100)
        self.line_orientation.currentTextChanged.connect(self._line_orientation_changed)
        row2.addWidget(self._lbl("Counting Line"))
        row2.addWidget(self.line_orientation)

        self.line_position = QSpinBox()
        self.line_position.setRange(0, 9999)
        self.line_position.setValue(0)
        self.line_position.setSuffix(" px")
        self.line_position.setFixedWidth(88)
        row2.addWidget(self._lbl("Position"))
        row2.addWidget(self.line_position)

        row2.addStretch(1)
        toolbar_layout.addLayout(row2)

        self.layout.addWidget(toolbar)
        self._style_control_inputs()

    def _vdiv(self) -> QWidget:
        sep = QWidget()
        sep.setFixedWidth(1)
        sep.setMinimumHeight(28)
        sep.setStyleSheet(f"background: {DIVIDER};")
        return sep

    def _lbl(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"font-size: 11.5px; font-weight: 600; color: {INK_3}; "
            f"padding: 0 2px;"
        )
        return lbl

    def _style_control_inputs(self) -> None:
        input_style = f"""
            QComboBox, QSpinBox, QDoubleSpinBox {{
                color: {INK};
                background: #FFFFFF;
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 4px 14px 4px 8px;
                font-size: 12px;
                selection-background-color: #F5E0D5;
                selection-color: {INK};
                min-height: 22px;
            }}
            QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
                border-color: {RUST};
            }}
            QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {{
                color: {INK_3};
                background: {SAND};
            }}
            QComboBox QAbstractItemView {{
                color: {INK};
                background: #FFFFFF;
                border: 1px solid {BORDER};
                selection-background-color: #F5E0D5;
                selection-color: {INK};
            }}
        """
        for widget in (
            self.tracker_combo,
            self.confidence_spin,
            self.iou_spin,
            self.line_orientation,
            self.line_position,
        ):
            widget.setStyleSheet(input_style)

    def _build_main_panels(self) -> None:
        # 1) Compact Live Statistics strip
        self.analytics_panel = self._create_analytics_panel()
        self.layout.addWidget(self.analytics_panel)
        self.layout.addSpacing(10)

        # 2) Two video panels, equal width, sized to fit viewport
        grid = QGridLayout()
        grid.setSpacing(14)

        self.original_view = ImageViewer("Original Video")
        self.detection_view = ImageViewer("Detection + Tracking Result")

        # Right-sized canvas — large enough to read each bbox + class label
        # but compact enough that the whole page fits one viewport.
        self.original_view.image_label.setMinimumHeight(360)
        self.detection_view.image_label.setMinimumHeight(360)

        grid.addWidget(self.original_view, 0, 0)
        grid.addWidget(self.detection_view, 0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.layout.addLayout(grid)

    def _create_analytics_panel(self) -> QWidget:
        """Compact horizontal Live Statistics strip — title + status + 9 tiles
        on a single card. Designed to take < 90 px of vertical space.
        """
        panel = CardWidget()
        panel.setBorderRadius(10)
        panel.setStyleSheet(
            f"""
            CardWidget {{
                background: {SAND};
                border: 1px solid {BORDER};
            }}
            """
        )

        root = QHBoxLayout(panel)
        root.setContentsMargins(18, 10, 18, 10)
        root.setSpacing(14)

        # Left column — title + status (vertical, compact)
        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(2)

        title = QLabel("LIVE")
        title.setStyleSheet(
            f"font-size: 10px; font-weight: 700; "
            f"color: {INK}; letter-spacing: 1.6px;"
        )
        left.addWidget(title)

        self.status_label = BodyLabel("No video loaded")
        self.status_label.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {SAGE};"
        )
        self.status_label.setWordWrap(False)
        self.status_label.setMaximumWidth(150)
        left.addWidget(self.status_label)
        root.addLayout(left)

        # Vertical divider between status block and stat tiles
        root.addWidget(self._vdiv())

        # 9 stat tiles — equal stretch
        stat_config: list[tuple[str, str, str]] = [
            ("total",      "TOTAL",   RUST),
            ("car",        "CARS",    SLATE),
            ("bus",        "BUSES",   RUST),
            ("truck",      "TRUCKS",  GOLD),
            ("van",        "VANS",    SAGE),
            ("frame",      "FRAME",   INK_3),
            ("fps",        "FPS",     INK_3),
            ("time",       "TIME",    INK_3),
            ("confidence", "CONF",    INK),
        ]

        self.stat_labels: dict[str, QLabel] = {}
        for index, (key, label, color) in enumerate(stat_config):
            if index > 0:
                inner_sep = QWidget()
                inner_sep.setFixedWidth(1)
                inner_sep.setMinimumHeight(36)
                inner_sep.setStyleSheet(f"background: {DIVIDER};")
                root.addWidget(inner_sep, 0, Qt.AlignmentFlag.AlignVCenter)

            tile = QWidget()
            tile_layout = QVBoxLayout(tile)
            tile_layout.setContentsMargins(6, 2, 6, 2)
            tile_layout.setSpacing(1)

            caption = QLabel(label)
            caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
            caption.setStyleSheet(
                f"font-size: 9px; font-weight: 700; "
                f"color: {TEXT_FAINT}; letter-spacing: 1px;"
            )
            tile_layout.addWidget(caption)

            value = QLabel("0")
            value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value.setStyleSheet(
                f"font-family: {FONT_SERIF}; "
                f"font-size: 19px; font-weight: 700; "
                f"color: {color}; letter-spacing: -0.4px;"
            )
            tile_layout.addWidget(value)

            root.addWidget(tile, 1)
            self.stat_labels[key] = value

        return panel

    def _build_timeline(self) -> None:
        timeline = QHBoxLayout()
        timeline.setSpacing(10)
        timeline.addWidget(BodyLabel("Timeline"))
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        timeline.addWidget(self.progress, 1)
        self.layout.addLayout(timeline)

    def open_video(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Traffic Video",
            "",
            "Videos (*.mp4 *.avi *.mov *.mkv *.wmv)",
        )
        if not path:
            return
        self.stop_video()
        self.video_path = path
        self.capture = cv2.VideoCapture(path)
        if not self.capture.isOpened():
            InfoBar.error("Video error", f"Unable to open {Path(path).name}", parent=self, position=InfoBarPosition.TOP_RIGHT)
            self.capture = None
            return

        self.frame_index = 0
        self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        self.progress.setRange(0, max(1, self.total_frames))
        self.line_initialized = False
        self.last_annotated_frame = None
        self.last_tracks = []
        self._reset_tracking_state()
        self.status_label.setText(f"Loaded: {Path(path).name}")
        self.process_next_frame()

    def start_video(self) -> None:
        if self.capture is None:
            self.open_video()
            if self.capture is None:
                return
        if not self.detection_service.is_loaded:
            try:
                self.detection_service.load_model(self.settings.model_path)
            except Exception as exc:
                InfoBar.error("Model error", str(exc), parent=self, position=InfoBarPosition.TOP_RIGHT)
                return
        self.last_tick = time.perf_counter()
        self.timer.start(1)

    def stop_video(self) -> None:
        self.timer.stop()

    def reset_video(self) -> None:
        self.stop_video()
        self.frame_index = 0
        self.progress.setValue(0)
        self.last_annotated_frame = None
        self.last_tracks = []
        self.last_processing_time = 0.0
        self.last_average_confidence = 0.0
        self._reset_tracking_state()
        self.last_tick = time.perf_counter()
        if self.capture is None:
            self.status_label.setText("No video loaded")
            return
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.status_label.setText(f"Reset: {Path(self.video_path).name}")
        self.process_next_frame()

    def process_next_frame(self) -> None:
        if self.capture is None:
            return
        ok, frame = self.capture.read()
        if not ok:
            self.stop_video()
            self.status_label.setText("Video finished")
            return

        self.frame_index += 1
        now = time.perf_counter()
        fps = 1.0 / max(0.001, now - self.last_tick)
        self.last_tick = now

        self._configure_line_for_frame(frame)
        self.original_view.set_image(frame)

        yolo_input = self.image_service.enhance(frame) if self.enhance_check.isChecked() else frame
        annotated = yolo_input.copy()
        tracks: list[dict[str, object]] = []
        processing_time = self.last_processing_time
        average_confidence = self.last_average_confidence
        should_run_inference = self.last_annotated_frame is None or self.frame_index % INFERENCE_FRAME_INTERVAL == 1

        if self.detection_service.is_loaded and should_run_inference:
            try:
                if self.tracking_check.isChecked():
                    annotated, tracks, processing_time = self.detection_service.track(
                        yolo_input,
                        tracker=TRACKER_FILES[self.tracker_combo.currentText()],
                        confidence_threshold=self.confidence_spin.value(),
                        iou_threshold=self.iou_spin.value(),
                        show_track_id=self.track_id_check.isChecked(),
                    )
                    self._update_tracking_counts(tracks)
                else:
                    annotated, summary = self.detection_service.detect(
                        yolo_input,
                        Path(self.video_path).name,
                        self.confidence_spin.value(),
                    )
                    self.last_summary = summary
                    processing_time = summary.processing_time
                    tracks = [
                        {"label": detection.label, "confidence": detection.confidence, "track_id": None}
                        for detection in summary.detections
                    ]
                confidences = [float(track["confidence"]) for track in tracks]
                average_confidence = float(np.mean(confidences)) if confidences else 0.0
                self.last_annotated_frame = annotated.copy()
                self.last_tracks = tracks
                self.last_processing_time = processing_time
                self.last_average_confidence = average_confidence
            except Exception as exc:
                self.stop_video()
                InfoBar.warning("Video detection skipped", str(exc), parent=self, position=InfoBarPosition.TOP_RIGHT)
        elif self.last_tracks:
            annotated = self.detection_service.draw_tracks(
                yolo_input,
                self.last_tracks,
                self.track_id_check.isChecked(),
            )

        if self.line_check.isChecked():
            self._draw_counting_line(annotated)
        self.detection_view.set_image(annotated)
        self._update_analytics(fps, processing_time, average_confidence)
        self.progress.setValue(self.frame_index)

    def _reset_tracking_state(self, *_args: object) -> None:
        self.tracked_ids = {name: set() for name in VEHICLE_CLASSES}
        self.previous_centers.clear()
        self.track_labels.clear()
        self.last_annotated_frame = None
        self.last_tracks = []
        self.last_processing_time = 0.0
        self.last_average_confidence = 0.0
        self.detection_service.reset_tracking()
        self._update_analytics(0.0, 0.0, 0.0)

    def _line_orientation_changed(self, *_args: object) -> None:
        self.line_initialized = False
        self._reset_tracking_state()

    def _configure_line_for_frame(self, frame: np.ndarray) -> None:
        height, width = frame.shape[:2]
        is_horizontal = self.line_orientation.currentText() == "Horizontal"
        maximum = height - 1 if is_horizontal else width - 1
        self.line_position.setMaximum(maximum)
        if not self.line_initialized:
            self.line_position.setValue(int(height * 0.58) if is_horizontal else int(width * 0.50))
            self.line_initialized = True

    def _update_tracking_counts(self, tracks: list[dict[str, object]]) -> None:
        for track in tracks:
            track_id = track.get("track_id")
            label = str(track.get("label", ""))
            center = track.get("center")
            if track_id is None or label not in VEHICLE_CLASSES or not isinstance(center, tuple):
                continue

            normalized_id = int(track_id)
            self.tracked_ids[label].add(normalized_id)
            self.track_labels[normalized_id] = label
            self.previous_centers[normalized_id] = center

    def _draw_counting_line(self, image: np.ndarray) -> None:
        height, width = image.shape[:2]
        position = self.line_position.value()
        color = (0, 180, 255)
        if self.line_orientation.currentText() == "Horizontal":
            cv2.line(image, (0, position), (width, position), color, 3, cv2.LINE_AA)
            cv2.putText(image, "Counting Line", (16, max(26, position - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)
        else:
            cv2.line(image, (position, 0), (position, height), color, 3, cv2.LINE_AA)
            cv2.putText(image, "Counting Line", (min(width - 210, position + 10), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)

    def _update_analytics(self, fps: float, processing_time: float, average_confidence: float) -> None:
        total_unique = sum(len(ids) for ids in self.tracked_ids.values())
        self.stat_labels["total"].setText(str(total_unique))
        for label in VEHICLE_CLASSES:
            self.stat_labels[label].setText(str(len(self.tracked_ids[label])))
        self.stat_labels["frame"].setText(f"{self.frame_index}/{self.total_frames or '-'}")
        self.stat_labels["fps"].setText(f"{fps:.1f}")
        self.stat_labels["time"].setText(f"{processing_time * 1000:.0f} ms")
        self.stat_labels["confidence"].setText(f"{average_confidence:.1%}")
        mode = "tracking" if self.tracking_check.isChecked() else "detection only"
        self.status_label.setText(
            f"YOLO26 runs on {'enhanced' if self.enhance_check.isChecked() else 'original'} RGB frames. "
            f"Mode: {mode}. GPU: {self.detection_service.device}. ImgSz: {self.detection_service.imgsz}. "
            f"Inference: every {INFERENCE_FRAME_INTERVAL} frames."
        )
