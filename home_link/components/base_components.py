from abc import ABC
from enum import Enum


class TypeComponents(Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class BaseComponents(ABC):
    name: str = None
    icon: str = None
    type: TypeComponents = None
