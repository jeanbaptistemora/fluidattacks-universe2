from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.post_contents import (
    _encode,
    _factory,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = _encode.PostContentEncoders.encoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_post_content_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


query = _factory.PostContentQuery(mock_data.mock_post_id).query()


def test_build_query() -> None:
    assert query.operation()


def test_query() -> None:
    raw_data = {"data": mock_raw_data.mock_post_contents}
    assert ApiClient.from_data(query, raw_data)
