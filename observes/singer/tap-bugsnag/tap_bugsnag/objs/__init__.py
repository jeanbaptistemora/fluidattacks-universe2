from dataclasses import (
    dataclass,
)
from singer_io.singer2.json import (
    JsonObj,
)


@dataclass(frozen=True)
class StabilityTrend:
    data: JsonObj
