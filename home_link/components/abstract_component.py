import abc

from home_link.config import Config, Device


class AbstractComponent(abc.ABC):
    def __init__(self, device: Device):
        self.host = device.host
        self.port = device.port
        self.name = device.name
        self.interval = device.interval
        self.state = device.state

    @abc.abstractmethod
    async def connect(self):
        pass

    def update_state(self, new_value: dict):
        if self.state is None:
            self.state = {}
        self.state.update(new_value)
        Config.instance().update_device_state(self.name, self.state)
