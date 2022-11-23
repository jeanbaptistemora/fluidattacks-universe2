from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.feedback._encode import (
    FeedbackObjEncoder,
)
from tap_announcekit.streams.feedback._factory import (
    _feedback_page_query,
)
from tap_announcekit.streams.feedback._factory._queries import (
    FeedbackPageQuery,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
    utils,
)


def test_schema() -> None:
    encoder = FeedbackObjEncoder("stream_1")
    schema = encoder.schema
    record = encoder.to_singer(mock_data.mock_feedback_obj)
    utils.test_schema(schema)
    utils.test_schema_record(schema, record)


def test_build_page_query() -> None:
    queries = (
        FeedbackPageQuery(
            Transform(lambda _: DataPage(0, 1, 1, tuple([]))),
            mock_data.mock_proj_id,
            0,
        ).query,
        FeedbackPageQuery(
            Transform(lambda _: DataPage(0, 1, 1, tuple([]))),
            mock_data.mock_post_id,
            0,
        ).query,
    )
    for query in queries:
        assert query.operation()


def test_page_query() -> None:
    queries = (
        _feedback_page_query(mock_data.mock_proj_id, 0),
        _feedback_page_query(mock_data.mock_post_id, 0),
    )
    raw_data = {"data": mock_raw_data.mock_feedbacks}
    for query in queries:
        assert ApiClient.from_data(query, raw_data)
