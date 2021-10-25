from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    PrimitiveFactory,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    PostContent as RawPostContent,
)
from tap_announcekit.objs.id_objs import (
    IndexedObj,
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post.content import (
    PostContent,
    PostContentObj,
)
from typing import (
    cast,
    List,
)

_to_primitive = PrimitiveFactory.to_primitive


@dataclass(frozen=True)
class PostContentQuery:
    post: PostId

    def _select_fields(self, query: Operation) -> IO[None]:
        contents = query.post(
            project_id=self.post.proj.id_str, post_id=self.post.id_str
        ).contents()
        for attr, _ in PostContent.__annotations__.items():
            getattr(contents, attr)()
        return IO(None)

    def query(self) -> Query:
        return QueryFactory.select(self._select_fields)


def from_raw(proj: ProjectId, raw: RawPostContent) -> PostContentObj:
    content = PostContent(
        _to_primitive(raw.locale_id, str),
        _to_primitive(raw.title, str),
        _to_primitive(raw.body, str),
        _to_primitive(raw.slug, str),
        _to_primitive(raw.url, str),
    )
    return IndexedObj(PostId.from_any(proj.id_str, raw.post_id), content)


@dataclass(frozen=True)
class PostContentFactory:
    client: ApiClient

    def get(self, pid: PostId) -> IO[FrozenList[PostContentObj]]:
        query = PostContentQuery(pid).query()
        return self.client.get(query).map(
            lambda q: tuple(
                from_raw(pid.proj, i)
                for i in cast(List[RawPostContent], q.post.contents)
            )
        )
