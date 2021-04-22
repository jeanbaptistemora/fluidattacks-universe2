# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    List,
    NamedTuple,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO

# Local libraries
from paginator import (
    PageId,
    PageOrAll,
)
from tap_checkly.api.common import (
    raw,
    extractor,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


class EnvVarsPage(NamedTuple):
    data: IO[List[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> EnvVarsPage:
        data = raw.list_env_vars(client, page)
        return cls(data)


class EnvVarsApi(NamedTuple):
    list_env_vars: Callable[[PageOrAll], Iterator[EnvVarsPage]]

    @classmethod
    def new(cls, client: Client) -> EnvVarsApi:
        return cls(
            list_env_vars=partial(
                extractor.extract_page,
                EnvVarsPage,
                partial(EnvVarsPage.new, client),
                lambda page: page.data.map(bool) == IO(False),
            )
        )
