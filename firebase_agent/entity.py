import dataclasses
import enum
import abc


class EntityType(enum.Enum):
    HTTP = "http"


class EntityAggregateType(enum.Enum):
    DAILY = "daily"
    HOURLY = "hourly"
    MINUTE = "minute"


class Entity(abc.ABC):
    pass


@dataclasses.dataclass
class HttpEntity(Entity):
    name: str
    url: str
    username: str = None
    password: str = None
    token: str = None
    value_prop: str = None
    create_aggregate: EntityAggregateType = None
