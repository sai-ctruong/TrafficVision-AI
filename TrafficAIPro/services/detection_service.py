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
        self.device: int | str = "cpu"
        self.imgsz = 640

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

        self.device = self._preferred_device()
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
        results = self.model(
            image,
            conf=confidence_threshold,
            imgsz=self.imgsz,
            device=self.device,
            verbose=False,
        )
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

    def track(
        self,
        image: np.ndarray,
        tracker: str = "bytetrack.yaml",
        confidence_threshold: float = 0.25,
        iou_threshold: float = 0.5,
        show_track_id: bool = True,
    ) -> tuple[np.ndarray, list[dict[str, object]], float]:
        """Run YOLO tracking on a normal BGR/RGB-style frame and draw tracked vehicles."""
        if self.model is None:
            raise RuntimeError("Model is not loaded")

        started = time.perf_counter()
        results = self.model.track(
            source=image,
            tracker=tracker,
            persist=True,
            conf=confidence_threshold,
            iou=iou_threshold,
            imgsz=self.imgsz,
            device=self.device,
            verbose=False,
        )
        elapsed = time.perf_counter() - started
        result = results[0]

        annotated = image.copy()
        tracks: list[dict[str, object]] = []
        if result.boxes is None:
            return annotated, tracks, elapsed

        boxes = result.boxes
        xyxy_values = boxes.xyxy.cpu().numpy().astype(int)
        class_values = boxes.cls.cpu().numpy().astype(int)
        confidence_values = boxes.conf.cpu().numpy()
        id_values = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else [None] * len(xyxy_values)

        for bbox_array, class_id, confidence, track_id in zip(
            xyxy_values,
            class_values,
            confidence_values,
            id_values,
        ):
            raw_label = result.names.get(int(class_id), str(class_id)).lower()
            label = self._normalize_label(raw_label)
            if label is None:
                continue

            x1, y1, x2, y2 = bbox_array.tolist()
            normalized_track_id = int(track_id) if track_id is not None else None
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            tracks.append(
                {
                    "label": label,
                    "confidence": float(confidence),
                    "bbox": (x1, y1, x2, y2),
                    "track_id": normalized_track_id,
                    "center": center,
                }
            )
            display_id = normalized_track_id if show_track_id else None
            self._draw_box(annotated, label, float(confidence), (x1, y1, x2, y2), display_id)

        return annotated, tracks, elapsed

    def draw_tracks(
        self,
        image: np.ndarray,
        tracks: list[dict[str, object]],
        show_track_id: bool = True,
    ) -> np.ndarray:
        """Draw previously computed track boxes on a fresh frame."""
        annotated = image.copy()
        for track in tracks:
            label = str(track.get("label", ""))
            bbox = track.get("bbox")
            confidence = track.get("confidence")
            if label not in VEHICLE_CLASSES or not isinstance(bbox, tuple) or confidence is None:
                continue
            track_id = track.get("track_id")
            display_id = int(track_id) if show_track_id and track_id is not None else None
            self._draw_box(annotated, label, float(confidence), bbox, display_id)
        return annotated

    def reset_tracking(self) -> None:
        """Clear Ultralytics tracker state between videos or tracker changes."""
        if self.model is not None and getattr(self.model, "predictor", None) is not None:
            self.model.predictor = None

    def _preferred_device(self) -> int | str:
        """Use CUDA GPU when available, otherwise keep CPU compatibility."""
        try:
            import torch
        except ImportError:
            return "cpu"
        return 0 if torch.cuda.is_available() else "cpu"

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
        track_id: int | None = None,
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
        caption = f"{label.title()} #{track_id} {confidence:.2f}" if track_id is not None else f"{label.title()} {confidence:.0%}"
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
