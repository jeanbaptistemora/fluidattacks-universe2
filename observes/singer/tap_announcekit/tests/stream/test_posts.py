from tap_announcekit.streams.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoder,
)
from tap_announcekit.streams.posts._getters import (
    post_query,
)


def test_query() -> None:
    post_query(PostId(ProjectId("1234"), "4321"))


def test_schema() -> None:
    PostEncoder.schema()
