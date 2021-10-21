from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.post_contents import (
    _encode,
    _factory,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    _factory.PostContentQuery(mock_post).query().operation()


def test_schema() -> None:
    assert _encode.PostContentEncoders.encoder("stream_1").schema
