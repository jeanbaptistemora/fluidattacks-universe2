from purity.v1 import (
    PureIter,
)
from returns.curry import (
    partial,
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


class PostsStreams:
    # pylint: disable=too-few-public-methods
    client: ApiClient
    name: str = "posts"

    def stream(
        self,
        post_ids: PureIter[PostId],
    ) -> Stream:
        getters = PostsGetters(self.client)
        getter = getters.stream_getter()
        posts = getter.get_iter(post_ids)
        records = posts.map_each(partial(PostSingerUtils.to_singer, self.name))
        return Stream(PostSingerUtils.schema(self.name), records)
