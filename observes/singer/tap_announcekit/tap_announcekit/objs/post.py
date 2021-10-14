from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from purity.v1 import (
    PrimitiveFactory,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    PostId,
    UserId,
)
from typing import (
    Optional,
)

JsonStr = str
to_primitive = PrimitiveFactory.to_primitive
to_opt_primitive = PrimitiveFactory.to_opt_primitive


@dataclass(frozen=True)
class _Post:
    # pylint: disable=too-many-instance-attributes
    obj_id: PostId
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


class Post(_Post):
    # pylint: disable=too-few-public-methods
    def __init__(self, obj: _Post) -> None:
        # pylint: disable=super-init-not-called
        # calling super is tedious because the number of args
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)
