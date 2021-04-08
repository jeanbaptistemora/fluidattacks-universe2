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
import delighted
from delighted import (
    Client,
)
from returns.curry import (
    partial,
)

# Local libraries
from paginator import (
    PageId,
)
from tap_delighted.api.common import (
    handle_rate_limit,
)
from tap_delighted.common import (
    JSON,
)


class SurveyResponsePage(NamedTuple):
    data: Iterator[JSON]

    @classmethod
    def new(cls, client: Client, page: PageId) -> SurveyResponsePage:
        data = handle_rate_limit(
            lambda: delighted.SurveyResponse.all(
                client=client,
                page=page.page,
                per_page=page.per_page
            ), 5
        )
        return cls(data)


class SurveyApi(NamedTuple):
    get_surveys: Callable[[PageId], SurveyResponsePage]

    @classmethod
    def new(cls, client: Client) -> SurveyApi:
        return cls(
            get_surveys=partial(SurveyResponsePage.new, client)
        )
