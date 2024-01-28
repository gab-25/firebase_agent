from enum import Enum
import logging
import pydantic
import toml


class Platform(Enum):
    SHELLY = "shelly"


class Device(pydantic.BaseModel):
    platform: Platform
    name: str
    host: str
    username: str = None
    password: str = None


class ConfigObj(pydantic.BaseModel):
    devices: list[Device] = []


class Config:
    FILENAME = "config.toml"

    def __init__(self) -> None:
        self.__read_yaml()

    def __read_yaml(self):
        logging.info("load config from file %s", self.FILENAME)
        with open(self.FILENAME, "r") as file:
            config_obj = ConfigObj(**toml.load(file))
            self.devices = config_obj.devices
