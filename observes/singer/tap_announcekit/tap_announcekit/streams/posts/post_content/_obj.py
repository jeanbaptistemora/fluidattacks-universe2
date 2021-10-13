from dataclasses import (
    dataclass,
)
from tap_announcekit.streams.id_objs import (
    PostId,
)


@dataclass(frozen=True)
class PostContent:
    post_id: PostId
    locale_id: str
    title: str
    body: str
    slug: str
    url: str
