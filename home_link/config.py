import logging
import dataclasses
import os
import typing
import toml
import yaml


@dataclasses.dataclass
class ServerHttp:
    host: str
    port: int
    username: str = None
    password: str = None


@dataclasses.dataclass
class Entity:
    name: str
    value: typing.Any
    unit_of_measure: str


@dataclasses.dataclass
class Device:
    platform: str
    name: str
    host: str
    port: str
    data_type: str
    topic: str = None
    interval: int = None
    username: str = None
    password: str = None
    entities: dict[str, Entity] = None


class Config:
    CONFIG_FILENAME = "config.yaml"
    DEVICE_FILENAME = "device_{}.toml"

    _instance = None

    server_http: dict = None
    devices: dict[str, Device] = {}
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
        logging.info("load configuration")
        try:
            with open(self.CONFIG_FILENAME, "r") as file_config:
                config_obj: dict[str, typing.Any] = yaml.safe_load(file_config)
                self.log_level = config_obj.get("log_level").upper()
                self.server_http = ServerHttp(**config_obj.get("server_http"))
                if config_obj.get("devices") is None:
                    logging.info("no devices found!")
                    return
                self.devices = {str(device.get("name")): Device(**device) for device in config_obj.get("devices")}
        except FileNotFoundError:
            pass

    def update_device_entity(self, device_name: str, new_entity: Entity):
        logging.debug("update device %s, entity: %s", device_name, new_entity.name)
        device = self.devices.get(device_name)
        if device.entities is None:
            device.entities = {}
        device.entities.update({new_entity.name: new_entity})

        if not os.path.exists("data"):
            os.mkdir("data")
        with open(os.path.join("data", self.DEVICE_FILENAME.format(device_name)), "w") as file_device:
            entity_items = {e_name: e_data for e_name, e_data in device.entities.items()}
            entity_obj = {"entity": entity_items}
            toml.dump(entity_obj, file_device)
