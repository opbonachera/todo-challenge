
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
log_dir = BASE_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "app.log"

file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="a")

logger = logging.getLogger("app")

logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)