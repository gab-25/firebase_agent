import abc


class AbstractParser(abc.ABC):

    @abc.abstractmethod
    def parse(self):
        pass
