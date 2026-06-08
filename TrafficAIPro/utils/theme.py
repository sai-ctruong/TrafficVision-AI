"""Design tokens for the TrafficAI Pro interface.

"Warm Editorial" theme — inspired by the v4 mockup:
    * cream / sand / brown earth-tone canvas (never plain white)
    * dark brown ("ink") sidebar with a small live model pill
    * rust orange as the primary accent
    * sage / gold / slate accents for status & per-class identity
    * Fraunces-style serif for headlines, sans for body
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Surfaces (warm canvas)
# ---------------------------------------------------------------------------
CREAM = "#FAF8F3"
SAND = "#F3EFE6"
SAND_2 = "#EAE4D9"
SAND_3 = "#DDD6C8"

APP_BACKGROUND = CREAM
SURFACE = SAND
SURFACE_MUTED = "#F7F3EA"
SURFACE_HOVER = SAND_2
CARD_BACKGROUND = SAND

# Sidebar (almost-black warm brown ink)
SIDEBAR_BG = "#1A1208"
SIDEBAR_BORDER = "rgba(255, 255, 255, 0.08)"
SIDEBAR_TEXT = "rgba(255, 255, 255, 0.75)"
SIDEBAR_TEXT_MUTED = "rgba(255, 255, 255, 0.45)"
SIDEBAR_TEXT_FAINT = "rgba(255, 255, 255, 0.25)"
SIDEBAR_HOVER = "rgba(255, 255, 255, 0.06)"

# Hairline borders
BORDER = SAND_3
BORDER_STRONG = "#C4AA96"
CARD_BORDER = BORDER
DIVIDER = SAND_2

# ---------------------------------------------------------------------------
# Typography ink
# ---------------------------------------------------------------------------
INK = "#1A1208"                # primary text — warm near-black
INK_2 = "#3D2B1F"              # rich brown
INK_3 = "#6B5543"              # readable body brown
BROWN = "#3D2B1F"
BROWN_2 = "#6B4E37"
BROWN_3 = "#9A7560"
BROWN_4 = "#C4AA96"

TEXT = INK
TEXT_MUTED = INK_3
SECONDARY_TEXT = INK_3
TEXT_FAINT = BROWN_3
MUTED_TEXT = BROWN_3

# ---------------------------------------------------------------------------
# Accent — rust orange
# ---------------------------------------------------------------------------
RUST = "#C4512A"
RUST_HOVER = "#B34A25"
RUST_PRESSED = "#9C3F1F"
RUST_LIGHT = "#FAF0EA"
RUST_DIM = "#F5E0D5"

ACCENT = RUST
PRIMARY = RUST
PRIMARY_HOVER = RUST_HOVER
PRIMARY_PRESSED = RUST_PRESSED
ACCENT_SOFT = RUST_LIGHT
ACCENT_TINT = RUST_DIM

# ---------------------------------------------------------------------------
# Semantic colors
# ---------------------------------------------------------------------------
SAGE = "#4A6741"
SAGE_LIGHT = "#EAF0E8"
SAGE_DIM = "#D5E4D2"
GOLD = "#C9882A"
GOLD_LIGHT = "#FDF5E6"
GOLD_DIM = "#F5DFA8"
SLATE = "#4A5568"
SLATE_LIGHT = "#EEF2F7"

SUCCESS = SAGE
SUCCESS_SOFT = SAGE_LIGHT
WARNING = GOLD
WARNING_SOFT = GOLD_LIGHT
ERROR = "#C4512A"              # share rust for danger — keeps palette tight
ERROR_SOFT = RUST_LIGHT
INFO = SLATE
INFO_SOFT = SLATE_LIGHT

SOFT_BLUE = SLATE_LIGHT
SOFT_GREEN = SAGE_LIGHT
SOFT_ORANGE = RUST_LIGHT
SOFT_RED = RUST_LIGHT

# ---------------------------------------------------------------------------
# Per-class vehicle palette (matches mockup)
# ---------------------------------------------------------------------------
VEHICLE_COLORS = {
    "total": RUST,        # rust — hero metric
    "car":   SLATE,       # slate — neutral
    "bus":   RUST,        # rust — eye-catching
    "truck": GOLD,        # gold
    "van":   SAGE,        # sage
}
VEHICLE_COLORS_SOFT = {
    "total": RUST_LIGHT,
    "car":   SLATE_LIGHT,
    "bus":   RUST_LIGHT,
    "truck": GOLD_LIGHT,
    "van":   SAGE_LIGHT,
}

# ---------------------------------------------------------------------------
# Typography stacks
# ---------------------------------------------------------------------------
# Serif (editorial headlines) — Fraunces if installed, else system serifs.
FONT_SERIF = (
    "'Fraunces', 'Source Serif Pro', 'Source Serif 4', "
    "'Cambria', 'Georgia', 'Times New Roman', serif"
)
# Sans (body & UI) — Instrument Sans if installed, else Inter/Segoe.
FONT_SANS = (
    "'Instrument Sans', 'Inter', 'SF Pro Display', "
    "'Segoe UI Variable', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
)
FONT_FAMILY = FONT_SANS

# ---------------------------------------------------------------------------
# Radii
# ---------------------------------------------------------------------------
RADIUS_SM = 5
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_PILL = 999


def app_style_sheet() -> str:
    """Global QSS applied at the QMainWindow level."""
    return f"""
    QWidget {{
        font-family: {FONT_SANS};
        color: {INK};
        font-size: 13px;
    }}

    QScrollArea {{
        border: none;
        background: transparent;
    }}
    #PageView {{
        background: {APP_BACKGROUND};
    }}

    /* Hairline scrollbars in warm palette */
    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 4px 2px 4px 0;
    }}
    QScrollBar::handle:vertical {{
        background: {SAND_3};
        border-radius: 4px;
        min-height: 32px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {BROWN_4}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none; border: none; height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent; height: 10px; margin: 0 4px 2px 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {SAND_3}; border-radius: 4px; min-width: 32px;
    }}
    QScrollBar::handle:horizontal:hover {{ background: {BROWN_4}; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none; border: none; width: 0;
    }}

    /* Tables */
    QTableWidget {{
        background: {CREAM};
        color: {INK};
        gridline-color: {DIVIDER};
        border: 1px solid {BORDER};
        border-radius: {RADIUS_LG}px;
        selection-background-color: {RUST_LIGHT};
        selection-color: {INK};
        alternate-background-color: {SURFACE_MUTED};
    }}
    QTableWidget::item {{
        padding: 12px 14px;
        border: none;
    }}
    QHeaderView::section {{
        background: {SAND};
        color: {INK_3};
        border: none;
        border-bottom: 1px solid {BORDER};
        padding: 12px 14px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    QHeaderView {{ background: transparent; }}

    QToolTip {{
        background: {INK};
        color: {CREAM};
        border: none;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 12px;
    }}

    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background: {SAND};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 6px 10px;
        selection-background-color: {RUST_LIGHT};
        selection-color: {INK};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 1px solid {RUST};
    }}

    QProgressBar {{
        background: {SAND_2};
        border: none;
        border-radius: 4px;
        text-align: center;
        height: 6px;
        color: transparent;
    }}
    QProgressBar::chunk {{
        background: {RUST};
        border-radius: 4px;
    }}

    #MetricValue {{ color: {INK}; }}
    """
