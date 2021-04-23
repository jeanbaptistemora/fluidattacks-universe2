# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    NamedTuple,
)

# Third party libraries
from delighted import (
    Client,
)
from returns.curry import partial
from returns.io import IO

# Local libraries
from tap_delighted.api.common import (
    raw,
    handle_rate_limit,
)
from tap_delighted.common import (
    JSON,
)


class Metrics(NamedTuple):
    data: JSON

    @classmethod
    def new(cls, client: Client) -> IO[Metrics]:
        data = handle_rate_limit(
            lambda: raw.get_metrics(client), 5
        )
        return data.unwrap().map(cls)


class MetricsApi(NamedTuple):
    get_metrics: Callable[[], IO[Metrics]]

    @classmethod
    def new(cls, client: Client) -> MetricsApi:
        return cls(
            get_metrics=partial(Metrics.new, client)
        )
