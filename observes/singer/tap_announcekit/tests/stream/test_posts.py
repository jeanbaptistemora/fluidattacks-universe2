from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoders,
)
from tap_announcekit.streams.posts._factory._queries import (
    PostIdsQuery,
    PostQuery,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    PostQuery(mock_post).query().operation()
    PostIdsQuery(mock_post.proj, 0).query().operation()


def test_schema() -> None:
    assert PostEncoders.encoder("stream_1").schema
