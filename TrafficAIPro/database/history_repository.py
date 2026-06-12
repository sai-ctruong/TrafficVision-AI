"""SQLite repository for detection history."""

from __future__ import annotations

import csv
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np

from ..models.detection import DetectionSummary
from ..utils.paths import DB_PATH, HISTORY_IMAGE_DIR


class HistoryRepository:
    """Persist and query detection history."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_name TEXT NOT NULL,
                    detection_date TEXT NOT NULL,
                    car_count INTEGER NOT NULL,
                    bus_count INTEGER NOT NULL,
                    truck_count INTEGER NOT NULL,
                    van_count INTEGER NOT NULL,
                    total_vehicles INTEGER NOT NULL,
                    average_confidence REAL NOT NULL,
                    processing_time REAL NOT NULL,
                    result_image_path TEXT
                )
                """
            )
            self._ensure_column(connection, "result_image_path", "TEXT")
            self._ensure_column(connection, "detection_mode", "TEXT NOT NULL DEFAULT 'YOLO'")
            self._ensure_column(connection, "inference_time", "REAL NOT NULL DEFAULT 0")

    def _ensure_column(self, connection: sqlite3.Connection, name: str, definition: str) -> None:
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(detections)")}
        if name not in columns:
            connection.execute(f"ALTER TABLE detections ADD COLUMN {name} {definition}")

    def add(self, summary: DetectionSummary, result_image: np.ndarray | None = None) -> None:
        result_image_path = self._save_result_image(summary, result_image) if result_image is not None else ""
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO detections (
                    image_name, detection_date, car_count, bus_count, truck_count,
                    van_count, total_vehicles, average_confidence, processing_time,
                    result_image_path, detection_mode, inference_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    summary.image_name or "Untitled image",
                    summary.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    summary.counts.get("car", 0),
                    summary.counts.get("bus", 0),
                    summary.counts.get("truck", 0),
                    summary.counts.get("van", 0),
                    summary.total,
                    summary.average_confidence,
                    summary.processing_time,
                    result_image_path,
                    summary.detection_mode.value,
                    summary.processing_time,
                ),
            )

    def list(self, search: str = "", order_by: str = "detection_date DESC") -> list[sqlite3.Row]:
        safe_orders = {
            "Newest": "detection_date DESC",
            "Oldest": "detection_date ASC",
            "Most Vehicles": "total_vehicles DESC",
            "Highest Confidence": "average_confidence DESC",
        }
        order = safe_orders.get(order_by, order_by if order_by in safe_orders.values() else "detection_date DESC")
        query = "SELECT * FROM detections"
        values: tuple[str, ...] = ()
        if search:
            query += " WHERE image_name LIKE ?"
            values = (f"%{search}%",)
        query += f" ORDER BY {order}"
        with self._connect() as connection:
            return list(connection.execute(query, values))

    def delete(self, row_ids: Iterable[int]) -> None:
        ids = list(row_ids)
        if not ids:
            return
        placeholders = ",".join("?" for _ in ids)
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT result_image_path FROM detections WHERE id IN ({placeholders})",
                ids,
            ).fetchall()
            connection.execute(f"DELETE FROM detections WHERE id IN ({placeholders})", ids)
        for row in rows:
            path = Path(row["result_image_path"] or "")
            if path.exists() and path.is_file():
                path.unlink(missing_ok=True)

    def export_csv(self, path: str) -> None:
        rows = self.list()
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Image Name",
                    "Detection Date",
                    "Cars",
                    "Buses",
                    "Trucks",
                    "Vans",
                    "Total Vehicles",
                    "Average Confidence",
                    "Processing Time",
                    "Detection Mode",
                    "Inference Time",
                    "Result Image Path",
                ]
            )
            for row in rows:
                writer.writerow(
                    [
                        row["image_name"],
                        row["detection_date"],
                        row["car_count"],
                        row["bus_count"],
                        row["truck_count"],
                        row["van_count"],
                        row["total_vehicles"],
                        f"{row['average_confidence']:.4f}",
                        f"{row['processing_time']:.4f}",
                        row["detection_mode"] if "detection_mode" in row.keys() else "YOLO",
                        f"{row['inference_time']:.4f}" if "inference_time" in row.keys() else f"{row['processing_time']:.4f}",
                        row["result_image_path"] if "result_image_path" in row.keys() else "",
                    ]
                )

    def _save_result_image(self, summary: DetectionSummary, image: np.ndarray) -> str:
        HISTORY_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        stem = Path(summary.image_name or "untitled").stem
        safe_stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("._") or "untitled"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = HISTORY_IMAGE_DIR / f"{timestamp}_{safe_stem}.jpg"
        if not cv2.imwrite(str(path), image):
            return ""
        return str(path)
