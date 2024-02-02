import abc

from home_link.config import Device


class AbstractComponent(abc.ABC):
    def __init__(self, device: Device):
        self.host = device.host
        self.port = device.port
        self.name = device.name
        self.interval = device.interval

    @abc.abstractmethod
    async def connect(self):
        pass
