from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.streams.feedback._encode import (
    FeedbackObjEncoder,
)
from tap_announcekit.streams.feedback._factory._query import (
    FeedbackPageQuery,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)


def test_schema() -> None:
    encoder = FeedbackObjEncoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_feedback_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())


queries = (
    FeedbackPageQuery(0).query(mock_data.mock_proj_id),
    FeedbackPageQuery(0).query(mock_data.mock_post_id),
)


def test_query() -> None:
    for query in queries:
        assert query.operation()


def test_from_data() -> None:
    raw_data = {"data": mock_raw_data.mock_feedbacks}
    for query in queries:
        assert ApiClient.from_data(query, raw_data)
