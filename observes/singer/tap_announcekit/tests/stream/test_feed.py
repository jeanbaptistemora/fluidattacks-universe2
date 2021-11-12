from purity.v1 import (
    Transform,
)
from tap_announcekit.streams.feeds._factory import (
    _queries,
)
from tests.stream import (
    mock_data,
)

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
