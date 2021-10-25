from dataclasses import (
    dataclass,
)
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    PrimitiveFactory,
    PureIter,
    PureIterFactory,
    Transform,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
    Posts as RawPosts,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.post import (
    PostIdPage,
    PostObj,
)
from typing import (
    cast,
)

JsonStr = str
_to_primitive = PrimitiveFactory.to_primitive


@dataclass(frozen=True)
class PostIdGetters:
    client: ApiClient
    proj: ProjectId
    total_query: Query
    page_query: Transform[int, Query]
    to_page: Transform[RawPosts, PostIdPage]

    @staticmethod
    def _filter_empty(page: PostIdPage) -> Maybe[PostIdPage]:
        return Maybe.from_optional(page if len(page.data) > 0 else None)

    def get_ids_page(self, page: int) -> IO[Maybe[PostIdPage]]:
        query = self.page_query(page)
        raw: IO[RawPosts] = self.client.get(query).map(
            lambda q: cast(RawPosts, q.posts)
        )
        return raw.map(self.to_page).map(self._filter_empty)

    def _get_page_range(self) -> IO[range]:
        raw: IO[RawPosts] = self.client.get(self.total_query).map(
            lambda q: cast(RawPosts, q.posts)
        )
        return raw.map(lambda r: range(_to_primitive(r.pages, int)))

    def get_ids(self) -> IO[PureIter[PostId]]:
        getter: IntIndexGetter[PostIdPage] = IntIndexGetter(self.get_ids_page)
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        id_pages: IO[PureIter[PostId]] = (
            self._get_page_range()
            .bind(getter.get_pages)
            .map(lambda x: PureIterFactory.from_flist(x))
            .map(lambda x: PureIterFactory.until_empty(x))
            .map(lambda p: PureIterFactory.map(lambda i: i.data, p))
            .map(
                lambda x: PureIterFactory.chain(
                    x.map_each(PureIterFactory.from_flist)
                )
            )
        )
        return id_pages


@dataclass(frozen=True)
class PostGetters:
    client: ApiClient
    post_query: Transform[PostId, Query]
    to_post: Transform[RawPost, PostObj]

    def get_post(self, post_id: PostId) -> IO[PostObj]:
        query = self.post_query(post_id)
        raw: IO[RawPost] = self.client.get(query).map(
            lambda q: cast(RawPost, q.post)
        )
        return raw.map(self.to_post)
