import json
from pathlib import Path

CONFIG_PATH = Path("data/config.json")


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {"keyword_threshold": 0.75, "max_keywords": 20}


config = load_config()
threshold = config["keyword_threshold"]
max_keywords = config["max_keywords"]
