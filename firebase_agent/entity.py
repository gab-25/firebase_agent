import datetime
import numpy


class Entity:
    id: str = None

    def __init__(
        self,
        ts: datetime.datetime = datetime.datetime.utcnow(),
        value: float = 0,
        data: dict = None,
    ) -> None:
        self.ts = ts
        self.value = float(value)
        self.data = data

    def to_dict(self) -> dict:
        return {
            "ts": self.ts,
            "value": self.value,
            "data": self.data,
        }


class EntityAggregate:
    id: str = None
    max: float = 0
    min: float = 0
    avg: float = 0
    sum: float = 0
    count: int = 0
    values: list[float]

    def __init__(self, start_ts: datetime.datetime, end_ts: datetime.datetime) -> None:
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.values = []

    def add_value(self, value: float) -> None:
        self.values.append(value)
        self.max = numpy.max(self.values)
        self.min = numpy.min(self.values)
        self.avg = numpy.average(self.values)
        self.sum = numpy.sum(self.values)
        self.count = len(self.values)

    def to_dict(self) -> dict:
        return {
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "max": self.max,
            "min": self.min,
            "avg": self.avg,
            "sum": self.sum,
            "count": self.count,
            "values": self.values,
        }
