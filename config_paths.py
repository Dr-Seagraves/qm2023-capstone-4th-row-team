"""
config_paths.py
---------------
Central path configuration for the QM2023 Capstone Project.
Import this module from any script or notebook to get consistent,
absolute directory and file paths regardless of working directory.

Usage:
    from config_paths import FINAL_PANEL, FIGURES_DIR
"""

from pathlib import Path

# ── Project root (directory containing this file) ─────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent

# ── Data directories ──────────────────────────────────────────────────────────
DATA_DIR       = PROJECT_ROOT / "data"
RAW_DIR        = DATA_DIR / "raw"
PROCESSED_DIR  = DATA_DIR / "processed"
FINAL_DIR      = DATA_DIR / "final"

# ── Results directories ───────────────────────────────────────────────────────
RESULTS_DIR    = PROJECT_ROOT / "results"
FIGURES_DIR    = RESULTS_DIR / "figures"
TABLES_DIR     = RESULTS_DIR / "tables"
REPORTS_DIR    = RESULTS_DIR / "reports"

# ── Code directory ────────────────────────────────────────────────────────────
CODE_DIR       = PROJECT_ROOT / "code"

# ── Key data files ────────────────────────────────────────────────────────────
FINAL_PANEL          = FINAL_DIR / "final.csv"
ENRICHED_PANEL       = FINAL_DIR / "final_enriched.csv"
FRED_CLEAN     = PROCESSED_DIR / "fred_clean.csv"
NOAA_CLEAN     = PROCESSED_DIR / "noaa_clean.csv"

# ── Ensure all output directories exist on import ────────────────────────────
for _dir in [RAW_DIR, PROCESSED_DIR, FINAL_DIR, FIGURES_DIR, TABLES_DIR, REPORTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
