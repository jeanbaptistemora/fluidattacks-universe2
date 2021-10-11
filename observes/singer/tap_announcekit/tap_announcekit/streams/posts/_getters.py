from dataclasses import (
    dataclass,
)
import logging
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    PrimitiveFactory,
    PureIter,
    PureIterFactory,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
    Posts as RawPosts,
)
from tap_announcekit.stream import (
    StreamGetter,
)
from tap_announcekit.streams.posts._objs import (
    Post,
    PostFactory,
    PostId,
    PostIdPage,
    PostPageFactory,
    ProjectId,
)
from tap_announcekit.streams.posts._queries import (
    PostIdsQuery,
    PostQuery,
    TotalPagesQuery,
)
from typing import (
    cast,
)

LOG = logging.getLogger(__name__)
JsonStr = str
_to_primitive = PrimitiveFactory.to_primitive


def _get_project(client: ApiClient, post_id: PostId) -> IO[Post]:
    query = PostQuery(post_id).query()
    LOG.debug("query: %s", query)
    raw: IO[RawPost] = client.get(query).map(lambda q: cast(RawPost, q.post))
    return raw.map(PostFactory.to_post)


def _get_projs(
    client: ApiClient, projs: PureIter[PostId]
) -> PureIter[IO[Post]]:
    return projs.map_each(partial(_get_project, client))


def _filter_empty(page: PostIdPage) -> Maybe[PostIdPage]:
    return Maybe.from_optional(page if len(page.data) > 0 else None)


def _get_post_id_page(
    client: ApiClient, proj: ProjectId, page: int
) -> IO[Maybe[PostIdPage]]:
    query = PostIdsQuery(proj, page).query()
    LOG.debug("query: %s", query)
    raw: IO[RawPosts] = client.get(query).map(
        lambda q: cast(RawPosts, q.posts)
    )
    return raw.map(PostPageFactory.to_post_page).map(_filter_empty)


def _get_page_range(client: ApiClient, proj: ProjectId) -> IO[range]:
    query = TotalPagesQuery(proj).query()
    LOG.debug("query: %s", query)
    raw: IO[RawPosts] = client.get(query).map(
        lambda q: cast(RawPosts, q.posts)
    )
    return raw.map(lambda r: range(_to_primitive(r.pages, int)))


@dataclass(frozen=True)
class PostsGetters:
    client: ApiClient

    def stream_getter(self) -> StreamGetter[PostId, Post]:
        return StreamGetter(
            partial(_get_project, self.client),
            partial(_get_projs, self.client),
        )

    def get_ids(self, proj: ProjectId) -> IO[PureIter[PostId]]:
        getter: IntIndexGetter[PostIdPage] = IntIndexGetter(
            partial(_get_post_id_page, self.client, proj)
        )
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        id_pages: IO[PureIter[PostId]] = (
            _get_page_range(self.client, proj)
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
