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
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post.content import (
    PostContent,
)
from typing import (
    cast,
    List,
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


JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


def _from_raw(proj: ProjectId, raw: RawPostContent) -> PostContent:
    return PostContent(
        PostId.from_any(proj, raw.post_id),
        to_primitive(raw.locale_id, str),
        to_primitive(raw.title, str),
        to_primitive(raw.body, str),
        to_primitive(raw.slug, str),
        to_primitive(raw.url, str),
    )


@dataclass(frozen=True)
class PostContentFactory:
    client: ApiClient

    def get(self, pid: PostId) -> IO[FrozenList[PostContent]]:
        query = PostContentQuery(pid).query()
        return self.client.get(query).map(
            lambda q: tuple(
                _from_raw(pid.proj, i)
                for i in cast(List[RawPostContent], q.post.contents)
            )
        )
