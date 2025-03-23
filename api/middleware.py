import importlib
import json
import os
from utils.application.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "middlewares.json"
)


def load_middleware_from_config(app, type="api"):
    middlewares = []

    if not os.path.exists(CONFIG_PATH):
        return middlewares

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            middleware_configs = config.get(type, [])

        # Sort middlewares by priority (lower value = higher priority)
        middleware_configs.sort(key=lambda x: x.get("priority", 0), reverse=True)

        for middleware_config in middleware_configs:
            middleware_path = middleware_config.get("middleware")
            args = middleware_config.get("args", {})  # ✅ Extract optional arguments

            try:
                logger.debug(f"Attempting to load middleware: {middleware_path}")
                module_name, class_name = middleware_path.rsplit(".", 1)

                # ✅ Import module dynamically
                module = importlib.import_module(middleware_path)
                middleware_class = getattr(module, class_name)

                # ✅ Ensure it’s a subclass of BaseHTTPMiddleware
                if not issubclass(middleware_class, BaseHTTPMiddleware):
                    raise TypeError(
                        f"{class_name} is not a subclass of BaseHTTPMiddleware."
                    )

                # ✅ Instantiate middleware (ALWAYS pass `app`, optionally pass `args`)
                middleware_instance = app.add_middleware(middleware_class, **args)
                middlewares.append(middleware_instance)
                logger.info(
                    f"✔ Successfully loaded middleware: {middleware_class.__name__}"
                )

            except ModuleNotFoundError as e:
                logger.error(f"❌ Module not found: {module_name}. Error: {e}")
            except AttributeError as e:
                logger.error(
                    f"❌ Class '{class_name}' not found in module '{module_name}'. Error: {e}"
                )
            except Exception as e:
                logger.error(f"❌ Error loading middleware '{middleware_path}': {e}")

    except json.JSONDecodeError as e:
        logger.error(f"❌ Error parsing JSON config: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error reading config file: {e}")

    return middlewares
