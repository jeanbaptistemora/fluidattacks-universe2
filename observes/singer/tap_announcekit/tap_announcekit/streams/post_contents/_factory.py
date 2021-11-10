from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenList,
    PrimitiveFactory,
    Transform,
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
)
from tap_announcekit.objs.post.content import (
    PostContent,
    PostContentObj,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
)
from typing import (
    cast,
    List,
)

_to_primitive = PrimitiveFactory.to_primitive


def _from_raw(id_obj: PostId, raw: RawPostContent) -> PostContentObj:
    content = PostContent(
        _to_primitive(raw.locale_id, str),
        _to_primitive(raw.title, str),
        _to_primitive(raw.body, str),
        _to_primitive(raw.slug, str),
        _to_primitive(raw.url, str),
    )
    return IndexedObj(id_obj, content)


@dataclass(frozen=True)
class PostContentQuery:
    post: PostId

    def _select_fields(self, query: Operation) -> IO[None]:
        contents = query.post(
            project_id=self.post.proj.id_str, post_id=self.post.id_str
        ).contents()
        return select_fields(contents, frozenset(PostContent.__annotations__))

    def query(self) -> Query[FrozenList[PostContentObj]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda q: tuple(
                    _from_raw(self.post, i)
                    for i in cast(List[RawPostContent], q.post.contents)
                )
            ),
        )


@dataclass(frozen=True)
class PostContentFactory:
    client: ApiClient

    def get(self, pid: PostId) -> IO[FrozenList[PostContentObj]]:
        query = PostContentQuery(pid).query()
        return self.client.get(query)
