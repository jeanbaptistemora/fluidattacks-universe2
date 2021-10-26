from tap_announcekit.streams.posts import (
    _factory,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)

encoder = PostEncoders.encoder("stream_1")
getter = _factory.raw_getter(mock_data.mock_post_id)


def test_post_query() -> None:
    assert getter.query.operation()


def test_post_from_data() -> None:
    assert getter.from_data({"data": mock_raw_data.mock_post})


def test_post_page_query() -> None:
    query = PostIdsQuery(mock_data.mock_proj_id, 0).query()
    raw = (query.operation() + {"data": mock_raw_data.mock_post_page}).posts
    assert _from_raw.to_post_page(raw)


def test_schema() -> None:
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_post_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
