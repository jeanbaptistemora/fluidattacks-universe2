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

    def _select_fields(self, query: Query) -> IO[None]:
        proj = query.raw.post(
            project_id=self.post.proj.proj_id, post_id=self.post.post_id
        )
        # select fields
        for attr, _ in Post.__annotations__.items():
            _attr = "id" if attr == "obj_id" else attr
            getattr(proj, _attr)()
        return IO(None)

    def query(self) -> IO[Query]:
        query = ApiClient.new_query()
        query.bind(self._select_fields)
        return query


@dataclass(frozen=True)
class PostIdsQuery:
    proj: ProjectId
    page: int

    def _select_fields(self, query: Query) -> IO[None]:
        proj = query.raw.posts(project_id=self.proj.proj_id, page=self.page)
        proj.list().id()
        proj.list().project_id()
        proj.count()
        proj.pages()
        return IO(None)

    def query(self) -> IO[Query]:
        query = ApiClient.new_query()
        query.bind(self._select_fields)
        return query
