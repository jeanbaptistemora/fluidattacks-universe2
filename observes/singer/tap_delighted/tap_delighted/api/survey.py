# Standard libraries
from typing import (
    Any,
    Callable,
    Dict,
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


JSON = Dict[str, Any]


class _SurveyResponse(NamedTuple):
    data: Iterator[JSON]


class SurveyResponsePage(_SurveyResponse):
    def __new__(cls, client: Client, page: PageId) -> 'SurveyResponsePage':
        data = handle_rate_limit(
            lambda: delighted.SurveyResponse.all(
                client=client,
                page=page.page,
                per_page=page.per_page
            ), 5
        )
        self = super(SurveyResponsePage, cls).__new__(cls, data)
        return self

    @classmethod
    def new(cls, client: Client, page: PageId) -> 'SurveyResponsePage':
        return cls(client, page)


def get_surveys(client: Client, page: PageId) -> SurveyResponsePage:
    return SurveyResponsePage.new(client, page)


class _SurveyApi(NamedTuple):
    get_surveys: Callable[[PageId], SurveyResponsePage]


class SurveyApi(_SurveyApi):
    def __new__(cls, client: Client) -> 'SurveyApi':
        self = super(SurveyApi, cls).__new__(
            cls,
            get_surveys=partial(get_surveys, client)
        )
        return self

    @classmethod
    def new(cls, client: Client) -> 'SurveyApi':
        return cls(client)
