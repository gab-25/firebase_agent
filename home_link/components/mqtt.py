from home_link.components.base_component import BaseComponent
from home_link.config import Device


class MQTT(BaseComponent):
    def __init__(self, device: Device):
        super().__init__(device)
        self.interval = None

    async def connect_device(self):
        pass
