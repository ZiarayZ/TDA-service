from typing import TypedDict


class Server(TypedDict):
    host: str
    port: int


class ConfigSchema(TypedDict):
    server: Server


defaultServer = Server(host="0.0.0.0", port=5000)
defaultConfig = ConfigSchema(server=defaultServer)
