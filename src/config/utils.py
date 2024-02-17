from typing import TypedDict


class Server(TypedDict):
    host: str
    port: int


defaultServer = Server(host="0.0.0.0", port=5000)


class ConfigSchema(TypedDict):
    server: Server


defaultConfig = ConfigSchema(server=defaultServer)
