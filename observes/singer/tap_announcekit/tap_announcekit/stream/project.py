from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
import logging
from typing import (
    Optional,
)

LOG = logging.getLogger(__name__)
JsonStr = str


@dataclass(frozen=True)
class _ProjectId:
    proj_id: str


@dataclass(frozen=True)
class ProjectId(_ProjectId):
    def __init__(self, proj: _ProjectId) -> None:
        object.__setattr__(self, "id", proj)


def _new_proj_id(proj_id: str) -> ProjectId:
    return ProjectId(_ProjectId(proj_id))


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
