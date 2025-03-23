# server.py
from mcp.server.fastmcp import FastMCP
from utils.application.env import EnvConfig
from utils.application.logger import logger
import importlib
import os

# Initialize FastMCP
mcp = FastMCP(
    EnvConfig.SERVER_NAME,
    **{
        "host": EnvConfig.HOST,
        "port": EnvConfig.PORT,
        "debug": EnvConfig.DEBUG_MCP,
        "log_level": EnvConfig.LOG_LEVEL,
    },
)

logger.info("🔧 MCP Server settings: %s", mcp.settings)


# Dynamically discover and register tools
def register_tools():
    tools_directory = os.path.join(os.path.dirname(__file__), "tools")
    for filename in os.listdir(tools_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"mcp_server.tools.{filename[:-3]}"  # Remove '.py' extension
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        callable(attr)
                        and hasattr(attr, "__name__")
                        and "tool" in attr.__name__.lower()
                    ):
                        mcp.tool()(attr)  # Register the tool dynamically
                        logger.info(f"🛠️  Registered tool: {attr.__name__}")
            except Exception as e:
                logger.error(f"❌ Failed to register tool from {filename}: {e}")


# Call the function to register all tools
register_tools()


def run_fastmcp():
    logger.info("Starting FastMCP Server")
    mcp.run(transport="sse")
