# pylint: skip-file

from __future__ import (
    annotations,
)

from paginator import (
    PageId,
    PageOrAll,
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
from tap_checkly.api.common import (
    extractor,
    raw,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from typing import (
    Callable,
    Iterator,
    List,
    NamedTuple,
)


class EnvVarsPage(NamedTuple):
    data: List[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[EnvVarsPage]:
        data = raw.list_env_vars(client, page)
        return data.map(cls)


def _is_empty(iopage: IO[EnvVarsPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


class EnvVarsApi(NamedTuple):
    list_env_vars: Callable[[PageOrAll], Iterator[IO[EnvVarsPage]]]

    @classmethod
    def new(cls, client: Client) -> EnvVarsApi:
        return cls(
            list_env_vars=partial(
                extractor.extract_page,
                IO[EnvVarsPage],
                partial(EnvVarsPage.new, client),
                _is_empty,
            )
        )
