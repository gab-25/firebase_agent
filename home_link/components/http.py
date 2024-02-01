from home_link.components.base_component import BaseComponent
from home_link.config import Device


class HTTP(BaseComponent):
    DEFAULT_INTERVAL = 10

    def __init__(self, device: Device):
        super().__init__(device)
        if self.interval is None:
            self.interval = self.DEFAULT_INTERVAL

    async def connect_device(self):
        pass
