from home_link.components.abstract_component import AbstractComponent
from home_link.components.http import Http
from home_link.components.mqtt import Mqtt
from home_link.components.parsers.abstract_parser import AbstractParser
from home_link.components.parsers.json import Json
from home_link.components.parsers.shelly import Shelly

CLASS_PARSERS: list[AbstractParser] = [Json, Shelly]
CLASS_COMPONENTS: list[AbstractComponent] = [Http, Mqtt]


@property
def platforms() -> dict[str, AbstractComponent]:
    return {class_component.__class__.__name__.lower(): class_component for class_component in CLASS_COMPONENTS}


@property
def data_types() -> dict[str, AbstractParser]:
    return {class_parser.__class__.__name__.lower(): class_parser for class_parser in CLASS_PARSERS}
