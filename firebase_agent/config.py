import enum
import dataclasses


class ConfigEntityType(enum.Enum):
    HTTP = "http"


@dataclasses.dataclass
class ConfigEntity:
    type: ConfigEntityType
    name: str
    url: str
    username: str = None
    password: str = None
    token: str = None
    value_prop: str = None
    create_aggregate: bool = False
