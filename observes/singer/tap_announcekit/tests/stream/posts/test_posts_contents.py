from tap_announcekit.streams.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts.post_content._queries import (
    PostContentQuery,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    PostContentQuery(mock_post).query()
