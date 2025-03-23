from utils.application.env import EnvConfig
import logging

valid_log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
if EnvConfig.LOG_LEVEL not in valid_log_levels:
    EnvConfig.LOG_LEVEL = "INFO"  # Default to INFO if the value is invalid

# Configure logging
logging.basicConfig(
    level=getattr(logging, EnvConfig.LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
