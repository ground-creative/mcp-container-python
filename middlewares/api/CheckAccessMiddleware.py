import os
import importlib
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.application.logger import logger
from utils.application.global_state import global_state


class CheckAccessMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, get_keys_func="utils.application.load_api_keys", *args, **kwargs
    ):
        super().__init__(app)

        # Dynamically import the function using importlib
        try:
            module_name, function_name = get_keys_func.rsplit(".", 1)
            module = importlib.import_module(get_keys_func)
            self.get_keys_func = getattr(module, function_name)
            self.valid_api_keys = (
                self.get_keys_func()
            )  # Call the function to load the keys
            logger.info(
                f"Successfully loaded the function {get_keys_func} for API key validation."
            )
        except (ImportError, AttributeError) as e:
            logger.error(
                f"Error importing or accessing function '{get_keys_func}': {e}"
            )
            self.valid_api_keys = (
                []
            )  # Default to an empty list if the function cannot be loaded

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("x-api-key")

        # Log headers for debugging
        logger.debug("Request Headers: %s", request.headers)

        # Check if API key is present and valid
        if not api_key:
            logger.error("API key missing in request headers.")
            return JSONResponse(status_code=400, content={"detail": "API key missing."})

        # Verify if the provided API key exists in the valid keys list
        if api_key not in self.valid_api_keys:
            logger.error("Invalid API key provided")
            return JSONResponse(status_code=401, content={"detail": "Invalid API key."})

        global_state.set("api_key", api_key, True)

        # Log the raw body in debug mode
        if os.getenv("LOG_LEVEL", "INFO") == "DEBUG":
            body = await request.body()
            logger.debug("Raw Request Body: %s", body.decode())

        # Proceed with the request
        response = await call_next(request)
        return response
