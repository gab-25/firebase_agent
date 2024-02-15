import dataclasses

@dataclasses.dataclass
class Entity:
    name: str
    url: str
    token: str = None
    value_prop: str = None
