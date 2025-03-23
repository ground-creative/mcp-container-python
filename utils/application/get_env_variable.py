import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def get_env_variable(key: str, default=None) -> str:
    """
    Retrieves the value of an environment variable.

    Args:
        key (str): The environment variable key.
        default (str, optional): Default value if key is not found. Defaults to None.

    Returns:
        str: The environment variable value or default if not found.
    """
    return os.getenv(key, default)
