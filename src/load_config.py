import json
from pathlib import Path

CONFIG_PATH = Path("data/config.json")

DEFAULT_CONFIG = {
    "keyword_threshold": 0.75,
    "max_keywords": 20,
}


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return DEFAULT_CONFIG.copy()
