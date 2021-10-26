from tap_announcekit.api.client import (
    ApiClient,
)
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

query = _factory.ProjectQuery(mock_data.mock_proj_id).query()


def test_query() -> None:
    assert query.operation()


def test_from_data() -> None:
    raw_data = {"data": mock_raw_data.mock_proj}
    assert ApiClient.from_data(query, raw_data)


def test_schema() -> None:
    encoder = ProjectEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_proj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
