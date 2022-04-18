# pylint: skip-file

from __future__ import (
    annotations,
)

from delighted import (
    Client,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_delighted.api.common import (
    handle_rate_limit,
    raw,
)
from typing import (
    Callable,
    NamedTuple,
)


class Metrics(NamedTuple):
    data: JsonObj

    @classmethod
    def new(cls, client: Client) -> IO[Metrics]:
        data = handle_rate_limit(lambda: raw.get_metrics(client), 5)
        return data.unwrap().map(cls)  # type: ignore


class MetricsApi(NamedTuple):
    get_metrics: Callable[[], IO[Metrics]]

    @classmethod
    def new(cls, client: Client) -> MetricsApi:
        return cls(get_metrics=partial(Metrics.new, client))
