from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
)
from tap_announcekit.streams.posts._objs import (
    Post,
    PostId,
    ProjectId,
)


@dataclass(frozen=True)
class PostQuery:
    post: PostId

    def _select_fields(self, query: Query) -> IO[Query]:
        proj = query.raw.post(
            project_id=self.post.proj.proj_id, post_id=self.post.post_id
        )
        # select fields
        for attr, _ in Post.__annotations__.items():
            _attr = "id" if attr == "obj_id" else attr
            getattr(proj, _attr)()
        return IO(proj)

    def query(self) -> IO[Query]:
        query = ApiClient.new_query()
        return query.bind(self._select_fields)


@dataclass(frozen=True)
class PostIdsQuery:
    proj: ProjectId
    page: int

    def _select_fields(self, query: Query) -> IO[Query]:
        proj = query.raw.posts(project_id=self.proj.proj_id, page=self.page)
        proj.list().id()
        proj.list().project_id()
        proj.count()
        proj.pages()
        return IO(proj)

    def query(self) -> IO[Query]:
        query = ApiClient.new_query()
        return query.bind(self._select_fields)


@dataclass(frozen=True)
class TotalPagesQuery:
    proj: ProjectId

    def _select_fields(self, query: Query) -> IO[Query]:
        proj = query.raw.posts(project_id=self.proj.proj_id, page=0)
        proj.count()
        proj.pages()
        return IO(proj)

    def query(self) -> IO[Query]:
        query = ApiClient.new_query()
        return query.bind(self._select_fields)
