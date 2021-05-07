# pylint: skip-file
# Standard libraries
from typing import (
    Callable,
    List,
    TypeVar,
)

# Third party libraries
from requests.models import Response
from returns.io import IO
from returns.maybe import Maybe

# Local libraries
from paginator.object_index import PageResult
from singer_io.common import JSON
from tap_bugsnag.api.common import extractor

_Data = TypeVar("_Data")


def typed_page_builder(
    response: IO[Response], transform: Callable[[List[JSON]], _Data]
) -> IO[Maybe[PageResult[_Data]]]:
    def _from_response(response: Response) -> Maybe[PageResult[_Data]]:
        raw = extractor.from_response(response)
        return raw.map(
            lambda p_result: PageResult(
                transform(p_result.data),
                p_result.next_item,
                p_result.total_items,
            )
        )

    return response.map(_from_response)
