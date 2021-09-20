from dataclasses import (
    dataclass,
)
import logging
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
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
from tap_announcekit.utils import (
    new_iter,
)
from typing import (
    Iterator,
)

LOG = logging.getLogger(__name__)
JsonStr = str


def _select_fields(proj_id: str, post_id: str, query: Query) -> IO[None]:
    proj = query.raw.post(project_id=proj_id, post_id=post_id)
    # select fields
    for attr, _ in Post.__annotations__.items():
        _attr = "id" if attr == "obj_id" else attr
        getattr(proj, _attr)()
    return IO(None)


def post_query(post: PostId) -> IO[Query]:
    query = ApiClient.new_query()
    query.bind(partial(_select_fields, post.proj.proj_id, post.post_id))
    return query


def _get_project(client: ApiClient, post_id: PostId) -> IO[Post]:
    query = post_query(post_id)
    LOG.debug("query: %s", query)
    raw: IO[RawPost] = client.get(query).map(lambda q: q.post)
    return raw.map(PostFactory.to_post)


def _get_projs(
    client: ApiClient, projs: IO[Iterator[PostId]]
) -> IO[Iterator[Post]]:
    return projs.bind(
        lambda ids: new_iter(
            unsafe_perform_io(_get_project(client, proj)) for proj in ids
        )
    )


@dataclass(frozen=True)
class PostsGetters:
    # pylint: disable=too-few-public-methods
    client: ApiClient

    def stream_getter(self) -> StreamGetter[PostId, Post]:
        return StreamGetter(
            partial(_get_project, self.client),
            partial(_get_projs, self.client),
        )
