from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class ProjectId:
    proj_id: str


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
    image_id: Optional[str]
    favicon_id: Optional[str]
    created_at: datetime
    ga_property: Optional[str]
    avatar: str
    favicon: Optional[str]
    locale: str
    uses_new_feed_hostname: Optional[bool]
    payment_gateway: str
    trial_until: Optional[datetime]
    metadata: JsonStr


@dataclass(frozen=True)
class Project(_Project):
    def __init__(self, obj: _Project) -> None:
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)
