from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    FrozenList,
    PrimitiveFactory,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    IndexedObj,
    PostId,
    UserId,
)
from tap_announcekit.objs.post.content import (
    PostContent,
    PostContentObj,
)
from tap_announcekit.objs.post.feedback import (
    ActionSource,
    Feedback,
    FeedbackObj,
    FeedbackPage,
)
from typing import (
    Optional,
)

JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


@dataclass(frozen=True)
class Post:
    # pylint: disable=too-many-instance-attributes
    user_id: Optional[UserId]
    created_at: datetime
    visible_at: datetime
    image_id: Optional[ImageId]
    expire_at: Optional[datetime]
    updated_at: datetime
    is_draft: bool
    is_pushed: bool
    is_pinned: bool
    is_internal: bool
    external_url: Optional[str]
    segment_filters: Optional[JsonStr]


@dataclass(frozen=True)
class PostIdPage:
    data: FrozenList[PostId]
    count: int
    page: int
    pages: int


PostObj = IndexedObj[PostId, Post]


__all__ = [
    # content
    "PostContent",
    "PostContentObj",
    # feedback
    "ActionSource",
    "Feedback",
    "FeedbackPage",
    "FeedbackObj",
]
