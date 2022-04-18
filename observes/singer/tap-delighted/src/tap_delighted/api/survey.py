# pylint: skip-file

from __future__ import (
    annotations,
)

from delighted import (
    Client,
)
from paginator import (
    AllPages,
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
from tap_delighted.api.common import (
    extractor,
    handle_rate_limit,
    raw,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
)


class SurveyPage(NamedTuple):
    data: Iterator[JsonObj]

    @classmethod
    def new(cls, client: Client, page: PageId) -> IO[SurveyPage]:
        data = handle_rate_limit(
            lambda: raw.list_surveys(
                client=client,
                page=page,
            ),
            5,
        )
        return data.unwrap().map(cls)  # type: ignore


def _is_empty(iopage: IO[SurveyPage]) -> bool:
    return iopage.map(lambda page: bool(page.data)) == IO(False)


def _list_surveys(
    client: Client,
    page: PageOrAll,
) -> Iterator[IO[SurveyPage]]:
    if isinstance(page, AllPages):
        return extractor.get_all_pages(
            IO[SurveyPage],
            partial(SurveyPage.new, client),
            _is_empty,
        )
    return iter([SurveyPage.new(client, page)])


class SurveyApi(NamedTuple):
    list_surveys: Callable[[PageOrAll], Iterator[IO[SurveyPage]]]

    @classmethod
    def new(cls, client: Client) -> SurveyApi:
        return cls(list_surveys=partial(_list_surveys, client))
