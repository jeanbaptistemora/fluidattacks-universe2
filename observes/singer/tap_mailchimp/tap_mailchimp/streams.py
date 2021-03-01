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
    SingerSchema,
    SingerRecord,
)
from tap_mailchimp import (
    api
)


ApiClient = api.ApiClient
Credentials = api.Credentials


class SupportedStreams(Enum):
    ALL_AUDIENCES = 'ALL_AUDIENCES'


def _emit_audience(
    client: ApiClient,
    audience_id: str,
    emit_schema: bool,
    target: Optional[IO[str]]
) -> None:
    target = target if target else sys.stdout
    stream = 'audiences'
    result = client.get_audience(audience_id)
    schema = SingerSchema(
        stream=stream,
        schema=result.links['targetSchema'],
        key_properties=frozenset()
    )
    record = SingerRecord(
        stream=stream,
        record=result.data
    )
    if emit_schema:
        factory.emit(schema, target)
    factory.emit(record, target)


def all_audiences(client: ApiClient, target: Optional[IO[str]]) -> None:
    audiences_data = client.list_audiences().data['lists']
    if audiences_data:
        audiences_id = map(lambda a: a['id'], audiences_data)
        _emit_audience(client, next(audiences_id), True, target)
        map_obj = map(
            lambda id: _emit_audience(client, id, False, target),
            audiences_id
        )
        deque(map_obj, 0)


stream_executor: Mapping[
    SupportedStreams,
    Callable[[ApiClient, Optional[IO[str]]], None]
] = {
    SupportedStreams.ALL_AUDIENCES: all_audiences
}
