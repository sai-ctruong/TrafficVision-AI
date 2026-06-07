"""Professional video vehicle detection, tracking and counting page."""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np
from PyQt6.QtCore import QTimer
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
from ..utils.theme import CARD_BORDER, PRIMARY, SECONDARY_TEXT, SUCCESS, TEXT
from ..widgets.image_viewer import ImageViewer
from .base import Page


TRACKER_FILES = {
    "ByteTrack": "bytetrack.yaml",
    "BoT-SORT": "botsort.yaml",
}
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
        self.crossed_counts = {name: 0 for name in VEHICLE_CLASSES}
        self.counted_ids: set[int] = set()
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
        self._build_explanation()
        self._build_main_panels()
        self._build_timeline()
        self.layout.addStretch(1)

    def _build_controls(self) -> None:
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.open_button = PrimaryPushButton(FluentIcon.VIDEO, "Open Video")
        self.open_button.clicked.connect(self.open_video)
        actions.addWidget(self.open_button)

        self.start_button = PushButton(FluentIcon.PLAY, "Start")
        self.start_button.clicked.connect(self.start_video)
        actions.addWidget(self.start_button)

        self.reset_button = PushButton(FluentIcon.SYNC, "Reset")
        self.reset_button.clicked.connect(self.reset_video)
        actions.addWidget(self.reset_button)

        self.tracking_check = CheckBox("Enable Tracking")
        self.tracking_check.setChecked(True)
        self.tracking_check.stateChanged.connect(self._reset_tracking_state)
        actions.addWidget(self.tracking_check)

        actions.addWidget(BodyLabel("Tracker"))
        self.tracker_combo = QComboBox()
        self.tracker_combo.addItems(TRACKER_FILES.keys())
        self.tracker_combo.currentTextChanged.connect(lambda _: self._reset_tracking_state())
        actions.addWidget(self.tracker_combo)

        actions.addWidget(BodyLabel("Confidence"))
        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.05, 0.95)
        self.confidence_spin.setSingleStep(0.05)
        self.confidence_spin.setValue(max(0.05, min(0.95, self.settings.confidence)))
        actions.addWidget(self.confidence_spin)

        actions.addWidget(BodyLabel("IOU"))
        self.iou_spin = QDoubleSpinBox()
        self.iou_spin.setRange(0.10, 0.95)
        self.iou_spin.setSingleStep(0.05)
        self.iou_spin.setValue(0.50)
        actions.addWidget(self.iou_spin)

        self.track_id_check = CheckBox("Show Track ID")
        self.track_id_check.setChecked(True)
        actions.addWidget(self.track_id_check)

        self.line_check = CheckBox("Show Counting Line")
        self.line_check.setChecked(True)
        actions.addWidget(self.line_check)

        self.enhance_check = CheckBox("Enhance RGB")
        actions.addWidget(self.enhance_check)

        actions.addStretch(1)
        self.layout.addLayout(actions)

        line_controls = QHBoxLayout()
        line_controls.setSpacing(10)
        line_controls.addWidget(BodyLabel("Counting Line"))
        self.line_orientation = QComboBox()
        self.line_orientation.addItems(["Horizontal", "Vertical"])
        self.line_orientation.currentTextChanged.connect(self._line_orientation_changed)
        line_controls.addWidget(self.line_orientation)
        line_controls.addWidget(BodyLabel("Position"))
        self.line_position = QSpinBox()
        self.line_position.setRange(0, 9999)
        self.line_position.setValue(0)
        self.line_position.setSuffix(" px")
        line_controls.addWidget(self.line_position)
        line_controls.addStretch(1)
        self.layout.addLayout(line_controls)

    def _build_explanation(self) -> None:
        explanation = BodyLabel(
            "Tracking is used to assign a unique ID to each detected vehicle across frames. "
            "This prevents repeated counting of the same vehicle in multiple frames."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet(
            f"""
            font-size: 13px;
            color: {SECONDARY_TEXT};
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid {CARD_BORDER};
            border-radius: 8px;
            padding: 12px;
            """
        )
        self.layout.addWidget(explanation)

    def _build_main_panels(self) -> None:
        grid = QGridLayout()
        grid.setSpacing(14)

        self.original_view = ImageViewer("Original Video")
        self.detection_view = ImageViewer("Detection + Tracking Result")
        self.analytics_panel = self._create_analytics_panel()

        grid.addWidget(self.original_view, 0, 0)
        grid.addWidget(self.detection_view, 0, 1)
        grid.addWidget(self.analytics_panel, 0, 2)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        self.layout.addLayout(grid)

    def _create_analytics_panel(self) -> QWidget:
        panel = CardWidget()
        panel.setBorderRadius(8)
        panel.setMinimumWidth(300)
        panel.setStyleSheet(
            f"""
            CardWidget {{
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid {CARD_BORDER};
            }}
            """
        )
        root = QVBoxLayout(panel)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(12)

        title = BodyLabel("Live Statistics")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {TEXT};")
        root.addWidget(title)

        self.stat_labels: dict[str, QLabel] = {}
        for key, label in [
            ("total", "Total Vehicles"),
            ("car", "Cars"),
            ("bus", "Buses"),
            ("truck", "Trucks"),
            ("van", "Vans"),
            ("crossed", "Vehicles Crossed Line"),
            ("frame", "Current Frame"),
            ("fps", "FPS"),
            ("time", "Processing Time"),
            ("confidence", "Average Confidence"),
        ]:
            row = QHBoxLayout()
            caption = BodyLabel(label)
            caption.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 13px;")
            value = QLabel("0")
            value.setStyleSheet(f"color: {PRIMARY}; font-size: 20px; font-weight: 700;")
            row.addWidget(caption)
            row.addStretch(1)
            row.addWidget(value)
            root.addLayout(row)
            self.stat_labels[key] = value

        self.status_label = BodyLabel("No video loaded")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {SUCCESS};")
        root.addStretch(1)
        root.addWidget(self.status_label)
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
        self.crossed_counts = {name: 0 for name in VEHICLE_CLASSES}
        self.counted_ids.clear()
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

            previous = self.previous_centers.get(normalized_id)
            if previous is not None and normalized_id not in self.counted_ids:
                if self._crossed_line(previous, center):
                    self.counted_ids.add(normalized_id)
                    self.crossed_counts[label] += 1
            self.previous_centers[normalized_id] = center

    def _crossed_line(self, previous: tuple[int, int], current: tuple[int, int]) -> bool:
        position = self.line_position.value()
        if self.line_orientation.currentText() == "Horizontal":
            previous_side = previous[1] - position
            current_side = current[1] - position
        else:
            previous_side = previous[0] - position
            current_side = current[0] - position
        return previous_side == 0 or current_side == 0 or (previous_side < 0 < current_side) or (current_side < 0 < previous_side)

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
        crossed_total = sum(self.crossed_counts.values())
        total_unique = sum(len(ids) for ids in self.tracked_ids.values())
        self.stat_labels["total"].setText(str(total_unique))
        for label in VEHICLE_CLASSES:
            self.stat_labels[label].setText(str(self.crossed_counts[label]))
        self.stat_labels["crossed"].setText(str(crossed_total))
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
