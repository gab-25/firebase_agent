from enum import Enum
import logging
import pydantic
import yaml


class Platform(Enum):
    SHELLY = "shelly"


class Device(pydantic.BaseModel):
    platform: Platform
    name: str
    host: str


class ConfigObj(pydantic.BaseModel):
    devices: list[Device] = []


class Config:
    FILENAME = "config.yml"

    def __init__(self) -> None:
        self.__read_yaml()

    def __read_yaml(self):
        logging.info("load config from file %s", self.FILENAME)
        with open(self.FILENAME, "r") as file:
            config_obj = ConfigObj(**yaml.safe_load(file))
            self.devices = config_obj.devices
