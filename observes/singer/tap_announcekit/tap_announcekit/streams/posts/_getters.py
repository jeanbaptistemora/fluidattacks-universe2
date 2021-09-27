from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    IOiter,
    PureIter,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.api.gql_schema import (
    Post as RawPost,
)
from tap_announcekit.stream import (
    StreamGetter,
)
from tap_announcekit.streams.posts._objs import (
    Post,
    PostFactory,
    PostId,
)
from tap_announcekit.streams.posts._queries import (
    PostQuery,
)
from typing import (
    cast,
)

LOG = logging.getLogger(__name__)
JsonStr = str


def _get_project(client: ApiClient, post_id: PostId) -> IO[Post]:
    query = PostQuery(post_id).query()
    LOG.debug("query: %s", query)
    raw: IO[RawPost] = client.get(query).map(lambda q: cast(RawPost, q.post))
    return raw.map(PostFactory.to_post)


def _get_projs(client: ApiClient, projs: PureIter[PostId]) -> IOiter[Post]:
    return projs.bind_io_each(partial(_get_project, client))


@dataclass(frozen=True)
class PostsGetters:
    # pylint: disable=too-few-public-methods
    client: ApiClient

    def stream_getter(self) -> StreamGetter[PostId, Post]:
        return StreamGetter(
            partial(_get_project, self.client),
            partial(_get_projs, self.client),
        )
