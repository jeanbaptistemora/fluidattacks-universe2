from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.project import (
    _factory,
)
from tap_announcekit.streams.project._encode import (
    ProjectEncoder,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)

query = _factory.ProjectQuery(mock_data.mock_proj_id).query


def test_schema() -> None:
    encoder = ProjectEncoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_proj_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_build_query() -> None:
    assert query.operation()


def test_query() -> None:
    raw_data = {"data": mock_raw_data.mock_proj}
    assert ApiClient.from_data(query, raw_data)
