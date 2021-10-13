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
from tap_announcekit.streams.posts._objs import (
    PostId,
)
from tap_announcekit.streams.posts.post_content._obj import (
    PostContent,
)


@dataclass(frozen=True)
class PostContentQuery:
    post: PostId

    def _select_fields(self, query: Operation) -> IO[None]:
        contents = query.post(
            project_id=self.post.proj.proj_id, post_id=self.post.post_id
        ).contents()
        for attr, _ in PostContent.__annotations__.items():
            getattr(contents, attr)()
        return IO(None)

    def query(self) -> Query:
        return QueryFactory.select(self._select_fields)
