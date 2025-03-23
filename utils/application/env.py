import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class EnvConfig:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    SERVER_NAME = os.getenv("SERVER_NAME", "MCP Server")
    DEBUG_MCP = os.getenv("DEBUG", True)
