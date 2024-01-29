from enum import Enum
import logging
import pydantic
import toml


class Platform(str, Enum):
    SHELLY = "shelly"
    MQTT = "mqtt"
    HTTP = "http"


class Device(pydantic.BaseModel):
    platform: Platform
    name: str
    host: str
    username: str = None
    password: str = None
    info: dict = None
    state: dict = None

    class Config:
        use_enum_values = True


class ConfigObj(pydantic.BaseModel):
    log_level: str
    devices: list[Device] = []


class Config:
    FILENAME = "config.toml"

    _instance = None

    devices = {}
    log_level = "INFO"

    def __init__(self) -> None:
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._read_toml(cls._instance)
        return cls._instance

    def _read_toml(self):
        logging.info("load config from file %s", self.FILENAME)
        with open(self.FILENAME, "r") as file:
            config_obj = ConfigObj(**toml.load(file))
            self.devices = {device.name: device for device in config_obj.devices}
            self.log_level = config_obj.log_level.upper()

    def update_device(self, device_name: str, info: dict = None, state: dict = None):
        logging.debug("update device %s, info: %s, state: %s", device_name, info, state)
        device = self.devices.get(device_name)
        if info is not None:
            device.info = info
        if state is not None:
            device.state = state

        with open(self.FILENAME, "w") as file:
            devices = list(self.devices.values())
            config_obj = ConfigObj(log_level=self.log_level, devices=devices)
            toml.dump(config_obj.model_dump(), file)
