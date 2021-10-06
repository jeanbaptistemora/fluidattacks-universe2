from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.streams.id_objs import (
    ImageId,
    ProjectId,
)
from typing import (
    Optional,
)

JsonStr = str


@dataclass(frozen=True)
class _Project:
    # pylint: disable=too-many-instance-attributes
    proj_id: ProjectId
    encoded_id: str
    name: str
    slug: str
    website: Optional[str]
    is_authors_listed: bool
    is_whitelabel: bool
    is_subscribable: bool
    is_slack_subscribable: bool
    is_feedback_enabled: bool
    is_demo: bool
    is_readonly: bool
    image_id: Optional[ImageId]
    favicon_id: Optional[ImageId]
    created_at: datetime
    ga_property: Optional[str]
    avatar: str
    locale: str
    uses_new_feed_hostname: Optional[bool]
    payment_gateway: str
    trial_until: Optional[datetime]
    metadata: JsonStr


@dataclass(frozen=True)
class Project(_Project):
    def __init__(self, obj: _Project) -> None:
        # pylint: disable=super-init-not-called
        # calling super is tedious because the number of args
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


__all__ = [
    "ImageId",
    "ProjectId",
]
