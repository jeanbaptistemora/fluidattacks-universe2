from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts.post_content._factory import (
    PostContentQuery,
)


def test_queries() -> None:
    mock_post = PostId(ProjectId("1234"), "4321")
    PostContentQuery(mock_post).query()
