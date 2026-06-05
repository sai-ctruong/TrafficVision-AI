"""Shared visual constants for the TrafficAI Pro interface."""

APP_BACKGROUND = "#F3F6FA"
CARD_BACKGROUND = "#FFFFFF"
CARD_BORDER = "#E5EAF2"
PRIMARY = "#0F6CBD"
PRIMARY_HOVER = "#0B5CAB"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
ERROR = "#DC2626"
TEXT = "#111827"
SECONDARY_TEXT = "#6B7280"
MUTED_TEXT = "#8A94A6"
SOFT_BLUE = "#EAF3FF"
SOFT_GREEN = "#ECFDF3"
SOFT_ORANGE = "#FFF7ED"
SOFT_RED = "#FEF2F2"


def app_style_sheet() -> str:
    """Return the app-level light Fluent dashboard style."""
    return f"""
    QWidget {{
        font-family: 'Segoe UI', 'Microsoft YaHei UI';
        color: {TEXT};
    }}
    QScrollArea {{
        border: none;
        background: {APP_BACKGROUND};
    }}
    #PageView {{
        background: {APP_BACKGROUND};
    }}
    #MetricValue {{
        color: {PRIMARY};
    }}
    QTableWidget {{
        background: {CARD_BACKGROUND};
        color: {TEXT};
        gridline-color: {CARD_BORDER};
        border: 1px solid {CARD_BORDER};
        border-radius: 8px;
        selection-background-color: {PRIMARY};
    }}
    QHeaderView::section {{
        background: #EEF3F8;
        color: {TEXT};
        border: none;
        padding: 8px;
        font-weight: 600;
    }}
    """

