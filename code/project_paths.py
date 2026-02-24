from pathlib import Path

# Determine the root directory relative to this file
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define project data directories
RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw'
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
FINAL_DATA_DIR = ROOT_DIR / 'data' / 'final'

def ensure_dirs_exist():
    """Create data directories if they don't exist."""
    for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
