# MCP ASGI PYTHON CONTAINER

This is a container that wraps fastmcp around a fastapi application. The wrapper adds the ability to use middleware and intercept requests, this way we can handle events such as authentication or validating request parameters.

## Installation

1. Clone the repository

```
git clone https://github.com/ground-creative/mcp-container-python.git
```

2. Change environment variables in env.sample file and rename it to .env

3. Create venv environment

```
python3 -m venv venv
source venv/bin/activate
```

4. Run requirements generator and install dependecies

```
python3 utils/application/generate_requirements.py
pip install -r requirements.txt
```

## Run the server

To run the server you can use one of the following commands:

```
# Run via fastapi wrapper
python3 run.py -s fastapi

# Run the mcp server directly
python3 run.py -s fastmcp
```

## Adding Tools

Create tools in folder mcp_server/tools. Use `{function_name}_tool` name convention like this example:

```
# mcp_server/tools/add.py
from utils.application.logger import logger # Use to add logging capabilities
from mcp.server.fastmcp import Context # Use `ctx: Context` as function param to get mcp context
from utils.application.global_state import global_state # Use to add and read global vars

@mcp.tool()
def add_numbers_tool(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

## Adding Tools Dependecies

1. Create file `config/libs.json` if not present with dependencies:

```
[
  {
    "package": "typing_extensions",
    "version": "4.12.2"
  }
]
```

2. Run requirements generator and install dependecies

```
python3 utils/application/generate_requirements.py
pip install -r requirements.txt
```

## Adding Middleware

1. Create middleware in `middlewares/api` folder as shown in the example:

```
# middlewares/MyMiddleware.py

from utils.application.logger import logger # Use to add logging capabilities
from mcp.server.fastmcp import Context # Use `ctx: Context` as function param to get mcp context
from utils.application.global_state import global_state # Use to add and read global vars
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, *args, **kwargs
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        """ Your code here """

        response = await call_next(request)
        return response

```

2. Create file `config/middlewares.json` if not present, and configure middlewares:

```
{
    "api": [
        {
            "middleware": "middlewares.api.MyMiddleware",
            "priority": 1,
        }
    ]
}
```

It's also possible to pass arguments to the middleware:

```
{
    "api": [
        {
            "middleware": "middlewares.api.MyMiddleware",
            "priority": 1,
            "args": {
                "some_arg": "some value"
            }
        }
    ]
}

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, some_arg, *args, **kwargs
    ):
        self._some_arg = some_arg
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        """ Your code here """

        response = await call_next(request)
        return response
```

### Using The Authentication middleware

1. Create a file `config/api_keys.json`:

```
[
    "YOUR KEY HERE",
    "ANOTHER KEY, THIS IS OPTIONAL"
]
```

The CheckAccessMiddleware can be used this way:

```
{
    "api": [
        {
            "middleware": "middlewares.api.CheckAccessMiddleware",
            "priority": 1,
            "args": {
                "get_keys_func": "utils.application.load_api_keys"
            }
        }
    ]
}
```

get_keys_func is optional, it's possible to create a custom function to match authentication keys against a different storage engine.

## Using global variables

To use global variables, simply import the GlobalState class:

```
from utils.application.global_state import global_state

def some_tool():
    all_globals = global_state.get_all()
    some_var = global_state.get("some-var")
    global_state.set("some_var", "somevalue", True) # The last parameter edits value if key already exists when set to true
```

## Using environment variables

To get environment variables added in the .env, use `get_env_variable` utility:

```
from utils.application.get_env_variable import get_env_variables

some_var = get_env_variable("VARIABLE_NAME")
```
