from home_link.components.abstract_component import AbstractComponent
from home_link.config import Device


class Mqtt(AbstractComponent):
    def __init__(self, device: Device):
        super().__init__(device)
        self.interval = None

    async def connect(self):
        pass
