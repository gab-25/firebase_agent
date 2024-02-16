import datetime
import numpy


class Entity:
    id: str = None

    def __init__(
        self,
        ts: datetime.datetime = datetime.datetime.utcnow(),
        value: float | str = 0,
        data: dict = None,
    ) -> None:
        self.ts = ts
        self.value = float(value) if isinstance(value, str) else value
        self.data = data


class EntityAggregate:
    id: str = None
    max: float = 0
    min: float = 0
    avg: float = 0
    sum: float = 0
    count: int = 0
    values = []

    def __init__(self, ts: datetime.datetime) -> None:
        self.ts = ts

    def add_value(self, value: float) -> None:
        self.values.append(value)
        self.max = numpy.max(self.values)
        self.min = numpy.min(self.values)
        self.avg = numpy.average(self.values)
        self.sum = numpy.sum(self.values)
        self.count = len(self.values)
