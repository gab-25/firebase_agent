from abc import ABC, abstractmethod

from home_link.config import Device


class BaseComponent(ABC):
    interval: int = None

    def __init__(self, device: Device):
        self.name = device.name

    @abstractmethod
    async def connect_device(self):
        pass
