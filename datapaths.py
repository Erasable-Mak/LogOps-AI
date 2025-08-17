from pathlib import Path
from app.settings import Settings

_settings = Settings()
DATA_DIR = Path(_settings.data_dir)
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "events.sqlite"
