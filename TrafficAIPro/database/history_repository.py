"""SQLite repository for detection history."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Iterable

from ..models.detection import DetectionSummary
from ..utils.paths import DB_PATH


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
                    processing_time REAL NOT NULL
                )
                """
            )

    def add(self, summary: DetectionSummary) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO detections (
                    image_name, detection_date, car_count, bus_count, truck_count,
                    van_count, total_vehicles, average_confidence, processing_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            connection.execute(f"DELETE FROM detections WHERE id IN ({placeholders})", ids)

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
                    ]
                )
