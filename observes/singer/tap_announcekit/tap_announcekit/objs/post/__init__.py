from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    IndexedObj,
    PostId,
    UserId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.objs.post.content import (
    PostContent,
    PostContentObj,
)
from tap_announcekit.objs.post.feedback import (
    ActionSource,
    Feedback,
    FeedbackObj,
)
from typing import (
    Optional,
)

JsonStr = str


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


PostIdPage = DataPage[PostId]
PostObj = IndexedObj[PostId, Post]


__all__ = [
    # content
    "PostContent",
    "PostContentObj",
    # feedback
    "ActionSource",
    "Feedback",
    "FeedbackObj",
]
