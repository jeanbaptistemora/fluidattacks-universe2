from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoder,
)
from tap_announcekit.streams.posts._queries import (
    PostIdsQuery,
    PostQuery,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    PostQuery(mock_post).query()
    PostIdsQuery(mock_post.proj, 0)


def test_schema() -> None:
    PostEncoder.schema()
