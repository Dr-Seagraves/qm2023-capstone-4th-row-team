import os
from pathlib import Path

def create_env_file():
    root_dir = Path(__file__).resolve().parent
    env_path = root_dir / '.env'
    env_content = (
        'FRED_API_KEY=ab3da5c0db78eb178a7f989483bc00de\n'
        'EIA_API_KEY=w7MRkxkPPuOvHfidYE3MMGCVw1NVW2G8fOzshThb\n'
        'NOAA_API_TOKEN=LxGdmHznUNXIuDpoRlfbDBDvGZTsdFaO\n'
    )
    env_path.write_text(env_content)
    print(f".env file created at {env_path}")

if __name__ == '__main__':
    create_env_file()
