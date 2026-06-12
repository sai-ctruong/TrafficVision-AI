"""SAHI sliced inference adapter for TrafficVision AI."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..models.detection import (
    DetectionBox,
    DetectionMode,
    DetectionSummary,
    SahiSettings,
    VEHICLE_CLASSES,
)


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


class SahiVehicleDetector:
    """Run SAHI sliced prediction and return the existing app summary format."""

    def __init__(self, model_path: str, device: int | str = "cpu") -> None:
        self.model_path = model_path
        self.device = device
        self.model_name = Path(model_path).name
        self._model = None
        self._loaded_confidence: float | None = None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def load_model(self, confidence_threshold: float = 0.25) -> None:
        """Load the Ultralytics model through SAHI."""
        try:
            from sahi import AutoDetectionModel
        except ImportError as exc:
            raise RuntimeError("SAHI is not installed. Run pip install -r requirements.txt") from exc

        device = f"cuda:{self.device}" if isinstance(self.device, int) else str(self.device)
        self._model = AutoDetectionModel.from_pretrained(
            model_type="ultralytics",
            model_path=self.model_path,
            confidence_threshold=confidence_threshold,
            device=device,
        )
        self._loaded_confidence = confidence_threshold
        self.model_name = Path(self.model_path).name

    def detect(
        self,
        image: np.ndarray,
        image_name: str = "",
        confidence_threshold: float = 0.25,
        settings: SahiSettings | None = None,
    ) -> DetectionSummary:
        """Run sliced inference and normalize predictions for the app."""
        if self._model is None or self._loaded_confidence != confidence_threshold:
            self.load_model(confidence_threshold)

        try:
            from sahi.predict import get_sliced_prediction
        except ImportError as exc:
            raise RuntimeError("SAHI prediction utilities are not available.") from exc

        sahi_settings = settings or SahiSettings()
        started = time.perf_counter()
        result = get_sliced_prediction(
            image,
            self._model,
            slice_height=sahi_settings.slice_height,
            slice_width=sahi_settings.slice_width,
            overlap_height_ratio=sahi_settings.overlap_height_ratio,
            overlap_width_ratio=sahi_settings.overlap_width_ratio,
            verbose=0,
        )
        elapsed = time.perf_counter() - started

        counts = {name: 0 for name in VEHICLE_CLASSES}
        detections: list[DetectionBox] = []
        confidences: list[float] = []

        for prediction in result.object_prediction_list:
            label = self._normalize_label(str(prediction.category.name).lower())
            if label is None:
                continue

            confidence = float(prediction.score.value)
            x1, y1, x2, y2 = prediction.bbox.to_xyxy()
            bbox = (int(x1), int(y1), int(x2), int(y2))
            counts[label] += 1
            confidences.append(confidence)
            detections.append(DetectionBox(label, confidence, bbox))

        return DetectionSummary(
            image_name=image_name,
            counts=counts,
            average_confidence=float(np.mean(confidences)) if confidences else 0.0,
            processing_time=elapsed,
            detections=detections,
            detection_mode=DetectionMode.SAHI,
        )

    def _normalize_label(self, label: str) -> str | None:
        for token, normalized in CLASS_ALIASES.items():
            if token in label:
                return normalized
        return None
