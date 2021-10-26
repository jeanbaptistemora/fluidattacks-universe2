from tap_announcekit.streams.project import (
    _factory,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoders,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)

getter = _factory.raw_getter(mock_data.mock_proj_id)


def test_query() -> None:
    assert getter.query.operation()


def test_from_data() -> None:
    assert getter.from_data({"data": mock_raw_data.mock_proj})


def test_schema() -> None:
    encoder = ProjectEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_proj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
