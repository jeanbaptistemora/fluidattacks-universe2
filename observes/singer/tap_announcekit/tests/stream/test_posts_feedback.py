from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.feedback import (
    _encode,
    _factory,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)


def test_schema() -> None:
    encoder = _encode.FeedbackObjEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_feedback_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())


query = _factory.FeedbackPageQuery(mock_data.mock_proj_id, 0).query()


def test_query() -> None:
    assert query.operation()


def test_from_data() -> None:
    raw_data = {"data": mock_raw_data.mock_feedbacks}
    assert ApiClient.from_data(query, raw_data)
