from purity.v1 import (
    Transform,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory import (
    queries,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
)
from tests.stream import (
    mock_data,
    mock_raw_data,
)

encoder = PostEncoders.encoder("stream_1")


def test_build_post_query() -> None:
    query = PostQuery(
        Transform(lambda _: mock_data.mock_post_obj.obj),
        mock_data.mock_post_id,
    ).query
    assert query.operation()


def test_build_post_ids_query() -> None:
    query = PostIdsQuery(
        Transform(lambda _: DataPage(0, 1, 1, tuple([]))),
        mock_data.mock_proj_id,
        0,
    ).query
    assert query.operation()


def test_post_query() -> None:
    raw_data = {"data": mock_raw_data.mock_post}
    query = queries.post(mock_data.mock_post_obj.id_obj)
    assert ApiClient.from_data(query, raw_data)


def test_post_page_query() -> None:
    raw_data = {"data": mock_raw_data.mock_post_page}
    query = queries.post_ids(mock_data.mock_proj_id, 0)
    assert ApiClient.from_data(query, raw_data)


def test_schema() -> None:
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_post_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
