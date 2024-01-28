from enum import Enum
import logging
from typing import Any
import pydantic
import toml


class Platform(str, Enum):
    SHELLY = "shelly"


class Device(pydantic.BaseModel):
    platform: Platform
    name: str
    host: str
    username: str = None
    password: str = None
    info: dict = None

    class Config:
        use_enum_values = True


class ConfigObj(pydantic.BaseModel):
    devices: list[Device] = []


class Config:
    FILENAME = "config.toml"

    __instance = None

    def __init__(self) -> None:
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__read_toml(cls.__instance)
        return cls.__instance

    def __read_toml(self):
        logging.info("load config from file %s", self.FILENAME)
        with open(self.FILENAME, "r") as file:
            config_obj = ConfigObj(**toml.load(file))
            self.devices = {device.name: device for device in config_obj.devices}

    def set_device_info(self, device_name: str, info: dict):
        device = self.devices.get(device_name)
        device.info = info
        with open(self.FILENAME, "w") as file:
            devices = list(self.devices.values())
            config_obj = ConfigObj(devices=devices)
            toml.dump(config_obj.model_dump(), file)
