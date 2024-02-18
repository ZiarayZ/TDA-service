from typing import TypedDict, Literal
from uuid import uuid4


class Server(TypedDict):
    host: str
    port: int


class ConfigSchema(TypedDict):
    server: Server
    secret_key: int  # v4 guid as int


def fetch_default(
    prop_name: Literal["secret_key", "host", "port", "server", "configschema"],
):
    if prop_name == "secret_key":
        return uuid4().int
    elif prop_name == "host":
        return "0.0.0.0"
    elif prop_name == "port":
        return 5000
    elif prop_name == "server":
        return Server({"host": fetch_default("host"), "port": fetch_default("port")})
    elif prop_name == "configschema":
        return ConfigSchema(
            {
                "server": fetch_default("server"),
                "secret_key": fetch_default("secret_key"),
            }
        )
    else:  # shouldn't happen, but just incase
        raise IndexError(f"Missing key: {prop_name}")
