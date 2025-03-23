import json
import os
from utils.application.logger import logger

# Load API keys from JSON file
API_KEYS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "config", "api_keys.json"
)


def load_api_keys():
    """Load valid API keys from a JSON file."""
    try:
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Failed to load API keys: %s", e)
        return []
