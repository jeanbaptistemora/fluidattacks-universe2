from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.streams.id_objs import (
    ImageId,
    PostId,
    ProjectId,
    UserId,
)
from typing import (
    Optional,
)

JsonStr = str


@dataclass(frozen=True)
class _Post:
    # pylint: disable=too-many-instance-attributes
    obj_id: PostId
    project_id: str
    user_id: Optional[str]
    project: ProjectId
    user: Optional[UserId]
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
class Post(_Post):
    def __init__(self, obj: _Post) -> None:
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


__all__ = ["PostId"]
