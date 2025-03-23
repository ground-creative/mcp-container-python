from fastapi import FastAPI
from mcp_server.server import mcp
from api.middleware import load_middleware_from_config
from utils.application.env import EnvConfig
from utils.application.logger import logger
import uvicorn

app = FastAPI()

load_middleware_from_config(app, "api")

# Mount the MCP SSE server inside FastAPI
app.mount("/", mcp.sse_app())


def run_fastapi():
    # logger.info("Starting FastAPI Server")
    uvicorn.run(app, host=EnvConfig.HOST, port=EnvConfig.PORT)
