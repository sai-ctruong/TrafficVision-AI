"""YOLO vehicle detection service."""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np
from ..models.detection import DetectionBox, DetectionSummary, VEHICLE_CLASSES


CLASS_ALIASES = {
    "car": "car",
    "auto": "car",
    "automobile": "car",
    "bus": "bus",
    "truck": "truck",
    "lorry": "truck",
    "van": "van",
    "minivan": "van",
}


class VehicleDetectionService:
    """Load an Ultralytics model and run vehicle detection."""

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
        self.model = None
        self.model_name = Path(model_path).name

    @property
    def is_loaded(self) -> bool:
        return self.model is not None

    def load_model(self, model_path: str | None = None) -> None:
        """Load YOLO weights."""
        if model_path:
            self.model_path = model_path
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("Ultralytics is not installed. Run pip install -r requirements.txt") from exc

        self.model = YOLO(self.model_path)
        self.model_name = Path(self.model_path).name

    def detect(
        self,
        image: np.ndarray,
        image_name: str = "",
        confidence_threshold: float = 0.5,
    ) -> tuple[np.ndarray, DetectionSummary]:
        """Run inference and draw premium-styled bounding boxes."""
        if self.model is None:
            raise RuntimeError("Model is not loaded")

        started = time.perf_counter()
        results = self.model(image, conf=confidence_threshold, verbose=False)
        elapsed = time.perf_counter() - started
        result = results[0]

        annotated = image.copy()
        detections: list[DetectionBox] = []
        counts = {name: 0 for name in VEHICLE_CLASSES}
        confidences: list[float] = []

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                raw_label = result.names.get(class_id, str(class_id)).lower()
                label = self._normalize_label(raw_label)
                if label is None:
                    continue

                confidence = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int).tolist()
                counts[label] += 1
                confidences.append(confidence)
                detections.append(DetectionBox(label, confidence, (x1, y1, x2, y2)))
                self._draw_box(annotated, label, confidence, (x1, y1, x2, y2))

        summary = DetectionSummary(
            image_name=image_name,
            counts=counts,
            average_confidence=float(np.mean(confidences)) if confidences else 0.0,
            processing_time=elapsed,
            detections=detections,
        )
        return annotated, summary

    def _normalize_label(self, label: str) -> str | None:
        for token, normalized in CLASS_ALIASES.items():
            if token in label:
                return normalized
        return None

    def _draw_box(
        self,
        image: np.ndarray,
        label: str,
        confidence: float,
        bbox: tuple[int, int, int, int],
    ) -> None:
        palette = {
            "car": (0, 120, 212),
            "bus": (16, 124, 16),
            "truck": (232, 17, 35),
            "van": (136, 23, 152),
        }
        x1, y1, x2, y2 = bbox
        color = palette.get(label, (0, 120, 212))
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 3, cv2.LINE_AA)
        caption = f"{label.title()} {confidence:.0%}"
        (width, height), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
        top = max(0, y1 - height - 12)
        cv2.rectangle(image, (x1, top), (x1 + width + 16, y1), color, -1)
        cv2.putText(
            image,
            caption,
            (x1 + 8, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
