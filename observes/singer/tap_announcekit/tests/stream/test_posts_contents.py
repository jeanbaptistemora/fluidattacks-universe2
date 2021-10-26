import pytest
from tap_announcekit.streams.post_contents import (
    _encode,
    _factory,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)


def test_schema() -> None:
    encoder = _encode.PostContentEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_post_content_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())


getter = _factory.raw_getter(mock_data.mock_post_id)


def test_query() -> None:
    assert getter.query.operation()


@pytest.mark.xfail(reason="future fix")
def test_from_raw() -> None:
    assert getter.from_data({"data": mock_raw_data.mock_post_contents})
