from home_link.components.abstract_component import AbstractComponent
from home_link.config import Device


class HTTP(AbstractComponent):
    DEFAULT_INTERVAL = 10

    def __init__(self, device: Device):
        super().__init__(device)
        if self.interval is None:
            self.interval = self.DEFAULT_INTERVAL

    async def connect(self):
        pass
