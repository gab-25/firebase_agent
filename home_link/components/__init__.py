from home_link.components.base_component import BaseComponent
from home_link.components.http import HTTP
from home_link.components.mqtt import MQTT
from home_link.components.shelly import Shelly


COMPONENTS: dict[str, BaseComponent] = {
    "shelly": Shelly,
    "mqtt": MQTT,
    "http": HTTP,
}
