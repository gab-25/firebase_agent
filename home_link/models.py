import pydantic


class Device(pydantic.BaseModel):
    id: str
    name: str
    producer: str
    model: str
    integration: str
    host: str
    firmware_version: str
    mac_address: str
    enable: bool


class Entity(pydantic.BaseModel):
    id: str
    name: str
    icon: str
    unit_of_measure: str
    device_id: str
    enable: bool


class Integration(pydantic.BaseModel):
    name: str
