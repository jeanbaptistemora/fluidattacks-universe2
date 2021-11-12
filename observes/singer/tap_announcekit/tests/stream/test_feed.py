from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.feeds import (
    _encode,
)
from tap_announcekit.streams.feeds._factory import (
    _queries,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.FeedObjEncoders("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_feed_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


id_query = _queries.FeedIdQuery(
    Transform(lambda _: mock_data.mock_feed_obj.id_obj),
    mock_data.mock_proj_id,
).query
obj_query = _queries.FeedQuery(
    Transform(lambda _: mock_data.mock_feed_obj.obj),
    mock_data.mock_feed_obj.id_obj,
).query


def test_query_id() -> None:
    assert id_query.operation()


def test_query_obj() -> None:
    assert obj_query.operation()


def test_from_data_ids() -> None:
    raw_data = {"data": mock_raw_data.mock_feed_ids}
    assert ApiClient.from_data(id_query, raw_data)


def test_from_data_obj() -> None:
    raw_data = {"data": mock_raw_data.mock_feed}
    assert ApiClient.from_data(obj_query, raw_data)
