import abc
import typing
from home_link.firebase import Firebase
from home_link.parsers import data_types

from home_link.config import Config, Device, Entity
from home_link.parsers.abstract_parser import AbstractParser


class AbstractComponent(abc.ABC):
    def __init__(self, device: Device):
        self.host = device.host
        self.port = device.port
        self.name = device.name
        self.interval = device.interval
        self.entities = device.entities

        self.parser: AbstractParser = data_types().get(device.data_type)()

    @abc.abstractmethod
    async def connect(self):
        pass

    def decode_entity(self, name: str, data: typing.Any) -> Entity:
        return self.parser.parse(name, data)

    def publish_entity(self, new_entity: Entity):
        firebase = Firebase.instance()
        if firebase.is_initialize:
            firebase.publish(self.name, new_entity)
