from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from tap_announcekit.objs.id_objs import (
    ImageId,
    IndexedObj,
    ProjectId,
)
from typing import (
    Optional,
)

JsonStr = str


@dataclass(frozen=True)
class Project:
    # pylint: disable=too-many-instance-attributes
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


ProjectObj = IndexedObj[ProjectId, Project]

__all__ = [
    "ImageId",
    "ProjectId",
]
