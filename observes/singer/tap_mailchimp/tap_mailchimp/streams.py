# Standard libraries
import sys
from collections import (
    deque,
)
from enum import Enum
from typing import (
    Callable,
    IO,
    Mapping,
    Optional,
)

# Third party libraries

# Local libraries
from singer_io import factory
from singer_io.singer import (
    SingerRecord,
)
from tap_mailchimp import (
    api
)


ApiClient = api.ApiClient
AudienceId = api.AudienceId
Credentials = api.Credentials


class SupportedStreams(Enum):
    ALL_AUDIENCES = 'ALL_AUDIENCES'


def _emit_audience(
    client: ApiClient,
    audience_id: AudienceId,
    target: Optional[IO[str]]
) -> None:
    target = target if target else sys.stdout
    stream = 'audiences'
    result = client.get_audience(audience_id)
    record = SingerRecord(
        stream=stream,
        record=result.data
    )
    factory.emit(record, target)


def all_audiences(client: ApiClient, target: Optional[IO[str]]) -> None:
    audiences_data = client.list_audiences().data['lists']
    if audiences_data:
        audiences_id = map(lambda a: AudienceId(a['id']), audiences_data)
        _emit_audience(client, next(audiences_id), target)
        map_obj = map(
            lambda id: _emit_audience(client, id, target),
            audiences_id
        )
        deque(map_obj, 0)


stream_executor: Mapping[
    SupportedStreams,
    Callable[[ApiClient, Optional[IO[str]]], None]
] = {
    SupportedStreams.ALL_AUDIENCES: all_audiences
}
