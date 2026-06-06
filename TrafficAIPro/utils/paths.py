"""Path helpers for TrafficAI Pro."""

from __future__ import annotations

from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = APP_ROOT.parent
DATA_DIR = APP_ROOT / "database"
EXPORT_DIR = APP_ROOT / "exports"
WEIGHTS_DIR = APP_ROOT / "models" / "weights"
DEFAULT_MODEL_PATH = WEIGHTS_DIR / "Car_YOLO26_Best.pt"
DB_PATH = DATA_DIR / "trafficai_history.sqlite3"


def ensure_app_dirs() -> None:
    """Create runtime directories used by the app."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

