import dataclasses
import datetime
import typing


@dataclasses.dataclass
class Entity:
    name: str
    type: str
    value: typing.Any
    unit_of_measure: str
    ts: datetime.datetime


@dataclasses.dataclass
class Device:
    platform: str
    name: str
    host: str
    port: str
    data_type: str
    topic: str = None
    path: str = None
    interval: int = 10
    username: str = None
    password: str = None
    entities: dict[str, Entity] = None
