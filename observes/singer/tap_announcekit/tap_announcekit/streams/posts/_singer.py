from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from tap_announcekit.objs.post import (
    Post,
)
from tap_announcekit.streams.posts._encode import (
    PostEncoder,
)


class PostSingerUtils:
    @staticmethod
    def schema(stream_name: str) -> SingerSchema:
        return SingerSchema(stream_name, PostEncoder.schema(), frozenset([]))

    @staticmethod
    def to_singer(stream_name: str, post: Post) -> SingerRecord:
        data = PostEncoder.to_json(post)
        return SingerRecord(stream_name, data)
