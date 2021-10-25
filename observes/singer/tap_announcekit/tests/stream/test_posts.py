from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
)
from tests.stream import (
    mock_data,
)

mock_proj_id = ProjectId("proj1234")


def test_queries() -> None:
    PostQuery(mock_data.mock_post_id).query().operation()
    PostIdsQuery(mock_data.mock_post_id.proj, 0).query().operation()


def test_schema() -> None:
    encoder = PostEncoders.encoder("stream_1")
    jschema = encoder.schema.schema
    jrecord = encoder.to_singer(mock_data.mock_post_obj).record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
