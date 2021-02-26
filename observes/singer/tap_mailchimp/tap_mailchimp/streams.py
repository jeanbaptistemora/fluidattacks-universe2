# Standard libraries
import sys
from collections import (
    deque,
)
from typing import (
    IO,
)

# Third party libraries

# Local libraries
from singer_io import factory
from singer_io.singer import (
    SingerSchema,
    SingerRecord,
)
from tap_mailchimp.api import (
    ApiClient,
)


def _emit_audience(
    client: ApiClient,
    audience_id: str,
    emit_schema: bool,
    target: IO[str] = sys.stdout
) -> None:
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


def all_audiences(client: ApiClient, target: IO[str] = sys.stdout) -> None:
    audiences_data = client.list_audiences().data['lists']
    if audiences_data:
        audiences_id = map(lambda a: a['id'], audiences_data)
        _emit_audience(client, next(audiences_id), True, target)
        map_obj = map(
            lambda id: _emit_audience(client, id, False, target),
            audiences_id
        )
        deque(map_obj, 0)
