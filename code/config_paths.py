
import pathlib
import os

# Define the project's root directory
# This assumes the script is in 'code/', so we go up one level.
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()

# Define data directories relative to the project root
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"

def ensure_dirs_exist():
    """
    Creates the data directories if they do not already exist.
    """
    print("Ensuring data directories exist...")
    for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR]:
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
    print("Directories are ready.")

if __name__ == '__main__':
    # When run as a script, this will check and create the directories.
    ensure_dirs_exist()
    print("\nDefined paths:")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Raw Data Directory: {RAW_DATA_DIR}")
    print(f"Processed Data Directory: {PROCESSED_DATA_DIR}")
    print(f"Final Data Directory: {FINAL_DATA_DIR}")
