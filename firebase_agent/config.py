import enum
import dataclasses
import configparser


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


_config = configparser.ConfigParser()
_config.read("./config")


def _get_config_entities() -> list[ConfigEntity]:
    _config_entities: list[ConfigEntity] = []
    for section in filter(lambda s: s not in ["GENERAL"], _config.sections()):
        config_entity = ConfigEntity(
            type=ConfigEntityType(_config[section].get("type")),
            name=section,
            url=_config[section].get("url"),
            username=_config[section].get("username"),
            password=_config[section].get("password"),
            token=_config[section].get("token"),
            value_prop=_config[section].get("value_prop"),
            create_aggregate=_config[section].getboolean("create_aggregate"),
        )
        _config_entities.append(config_entity)
    return _config_entities


config_general: dict = dict(_config["GENERAL"])
config_entities: list[ConfigEntity] = _get_config_entities()
