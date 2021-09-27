from tap_announcekit.streams.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoder,
)
from tap_announcekit.streams.posts._queries import (
    PostQuery,
)


def test_query() -> None:
    PostQuery(PostId(ProjectId("1234"), "4321")).query()


def test_schema() -> None:
    PostEncoder.schema()
