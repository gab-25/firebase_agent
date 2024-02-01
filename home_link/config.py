import logging
from typing import Any
import pydantic
import toml
import yaml


class Device(pydantic.BaseModel):
    platform: str
    name: str
    host: str
    username: str = None
    password: str = None
    info: dict = None
    state: dict = None


class Config:
    CONFIG_FILENAME = "config.yaml"
    DEVICE_FILENAME = "device.toml"

    _instance = None

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
                config_obj: dict[str, Any] = yaml.safe_load(file_config)
                self.devices = {str(device.get("name")): Device(**device) for device in config_obj.get("devices")}
                self.log_level = config_obj.get("log_level").upper()

            with open(self.DEVICE_FILENAME, "r") as file_device:
                device_obj = toml.load(file_device)
                if device_obj.get("device") is None:
                    return
                for device_name, device_data in device_obj.get("device").items():
                    if device_name in self.devices:
                        self.devices.get(device_name).info = device_data.get("info")
                        self.devices.get(device_name).state = device_data.get("state")
        except FileNotFoundError:
            pass

    def update_device(self, device_name: str, info: dict = None, state: dict = None):
        logging.debug("update device %s, info: %s, state: %s", device_name, info, state)
        device = self.devices.get(device_name)
        if info is not None:
            device.info = info
        if state is not None:
            device.state = state

        with open(self.DEVICE_FILENAME, "w") as file_device:
            device_items = {
                d_name: {"info": d_data.info, "state": d_data.state} for d_name, d_data in self.devices.items()
            }
            device_obj = {"device": device_items}
            toml.dump(device_obj, file_device)
