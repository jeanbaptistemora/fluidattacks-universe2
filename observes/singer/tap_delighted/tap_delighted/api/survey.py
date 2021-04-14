# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
)

# Third party libraries
from delighted import (
    Client,
)
from returns.curry import (
    partial,
)
from returns.io import IO

# Local libraries
from paginator import (
    PageId,
)
from tap_delighted.api.common import (
    raw,
    handle_rate_limit,
)
from tap_delighted.common import (
    JSON,
)


class SurveyPage(NamedTuple):
    data: IO[Iterator[JSON]]

    @classmethod
    def new(cls, client: Client, page: PageId) -> SurveyPage:
        data = handle_rate_limit(
            lambda: raw.list_surveys(
                client=client,
                page=page,
            ), 5
        )
        return cls(data.unwrap())


class SurveyApi(NamedTuple):
    get_surveys: Callable[[PageId], SurveyPage]

    @classmethod
    def new(cls, client: Client) -> SurveyApi:
        return cls(
            get_surveys=partial(SurveyPage.new, client)
        )
