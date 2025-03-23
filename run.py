import argparse
import logging
from api.main import run_fastapi
from mcp_server.server import run_fastmcp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def start_fastapi():
    """Start the FastAPI server."""
    logger.info("Starting FastAPI server...")
    run_fastapi()


def start_fastmcp():
    """Start the FastMCP server."""
    logger.info("Starting FastMCP server...")
    run_fastmcp()


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Choose which server to start.")
    parser.add_argument(
        "-s",
        "--server",
        choices=["fastapi", "fastmcp"],
        required=True,
        help="Specify which server to start: 'fastapi' or 'fastmcp'",
    )
    args = parser.parse_args()

    # Start the server based on the provided argument
    if args.server == "fastapi":
        logger.info("Selected server: FastAPI")
        start_fastapi()
    elif args.server == "fastmcp":
        logger.info("Selected server: FastMCP")
        start_fastmcp()
