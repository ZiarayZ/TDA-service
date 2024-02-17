from typing import TypedDict


class Server(TypedDict):
    host: str
    port: int


class ConfigSchema(TypedDict):
    server: Server
    secret_key: int  # v4 guid as int
