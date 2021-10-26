from dataclasses import (
    dataclass,
)
from purity.v1 import (
    PrimitiveFactory,
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    Posts as RawPosts,
)
from tap_announcekit.objs.id_objs import (
    ProjectId,
)
from tap_announcekit.objs.post import (
    PostIdPage,
)
from tap_announcekit.streams.posts._factory import (
    _from_raw,
)
from typing import (
    cast,
)

_to_primitive = PrimitiveFactory.to_primitive


@dataclass(frozen=True)
class PostIdsQuery:
    proj: ProjectId
    page: int

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.posts(project_id=self.proj.id_str, page=self.page)
        proj.list().id()
        proj.list().project_id()
        proj.page()
        proj.count()
        proj.pages()
        return IO(None)

    def query(self) -> Query[PostIdPage]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda q: _from_raw.to_post_page(cast(RawPosts, q.posts))
            ),
        )


@dataclass(frozen=True)
class TotalPagesQuery:
    proj: ProjectId

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.posts(project_id=self.proj.id_str, page=0)
        proj.count()
        proj.pages()
        return IO(None)

    def query(self) -> Query[range]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda q: range(
                    _to_primitive(cast(RawPosts, q.posts).pages, int)
                )
            ),
        )
