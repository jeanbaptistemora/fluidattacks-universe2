from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.stream import (
    Stream,
)
from tap_announcekit.streams.posts._getters import (
    PostsGetters,
)
from tap_announcekit.streams.posts._objs import (
    PostId,
)
from tap_announcekit.streams.posts._singer import (
    PostSingerUtils,
)
from tap_announcekit.utils import (
    new_iter,
)
from typing import (
    Iterator,
)


class PostsStreams:
    # pylint: disable=too-few-public-methods
    client: ApiClient
    name: str = "posts"

    def stream(
        self,
        post_ids: IO[Iterator[PostId]],
    ) -> Stream:
        getters = PostsGetters(self.client)
        getter = getters.stream_getter()
        posts = getter.get_iter(post_ids)
        records = new_iter(
            PostSingerUtils.to_singer(self.name, post)
            for post in unsafe_perform_io(posts)
        )
        return Stream(PostSingerUtils.schema(self.name), records)
