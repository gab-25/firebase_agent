import abc
import typing

from home_link.config import Entity


class AbstractParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, name: str, value: typing.Any) -> Entity:
        pass
