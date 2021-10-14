from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    Post,
)


@dataclass(frozen=True)
class PostQuery:
    post: PostId

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.post(
            project_id=self.post.proj.proj_id, post_id=self.post.post_id
        )
        # select fields
        proj.project_id()
        for attr, _ in Post.__annotations__.items():
            _attr = "id" if attr == "obj_id" else attr
            getattr(proj, _attr)()
        return IO(None)

    def query(self) -> Query:
        return QueryFactory.select(self._select_fields)


@dataclass(frozen=True)
class PostIdsQuery:
    proj: ProjectId
    page: int

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.posts(project_id=self.proj.proj_id, page=self.page)
        proj.list().id()
        proj.list().project_id()
        proj.page()
        proj.count()
        proj.pages()
        return IO(None)

    def query(self) -> Query:
        return QueryFactory.select(self._select_fields)


@dataclass(frozen=True)
class TotalPagesQuery:
    proj: ProjectId

    def _select_fields(self, query: Operation) -> IO[None]:
        proj = query.posts(project_id=self.proj.proj_id, page=0)
        proj.count()
        proj.pages()
        return IO(None)

    def query(self) -> Query:
        return QueryFactory.select(self._select_fields)
