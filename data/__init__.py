from orjson import loads
import typing


class Twitter(typing.TypedDict):
    api_key: str
    api_secret: str

class ConfigType(typing.TypedDict):
    token: str
    mysql: typing.Dict[str, typing.Any]
    twitter: Twitter

with open("config.json", "r") as f:
    CONFIG: ConfigType = loads(f.read())