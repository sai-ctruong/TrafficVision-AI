"""Path helpers for TrafficAI Pro."""

from __future__ import annotations

from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = APP_ROOT.parent
DATA_DIR = APP_ROOT / "database"
EXPORT_DIR = APP_ROOT / "exports"
DEFAULT_MODEL_PATH = WORKSPACE_ROOT / "best_oto.pt"
DB_PATH = DATA_DIR / "trafficai_history.sqlite3"


def ensure_app_dirs() -> None:
    """Create runtime directories used by the app."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

