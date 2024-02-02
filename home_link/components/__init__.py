from home_link.components.abstract_component import AbstractComponent
from home_link.components.http import HTTP
from home_link.components.mqtt import MQTT

CLASS_ENTITIES_TYPE: list = []
CLASS_COMPONENTS: list[AbstractComponent] = [HTTP, MQTT]


@property
def platforms() -> dict[str, AbstractComponent]:
    return {class_component.__class__.__name__.lower(): class_component for class_component in CLASS_COMPONENTS}
