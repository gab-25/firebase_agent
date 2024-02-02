import re
from typing import Any
from home_link.config import Entity
from home_link.parsers.abstract_parser import AbstractParser


class Shelly(AbstractParser):

    def parse(self, name: str, value: Any) -> Entity:
        if re.match("/", name):
            paths = filter(lambda n: len(n) > 0, name.split("/"))
            return Entity(name=".".join(paths), value=str(value), unit_of_measure="m")

        return Entity(name=name, value=str(value), unit_of_measure="m")
