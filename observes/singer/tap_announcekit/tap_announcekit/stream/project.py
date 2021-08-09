from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
import logging
from singer_io.singer2.json import (
    to_opt_primitive,
    to_primitive,
)
from tap_announcekit.api.gql_schema import (
    Project as RawProject,
)
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


def to_proj(raw: RawProject) -> Project:
    draft = _Project(
        _new_proj_id(to_primitive(raw.id, str)),
        to_primitive(raw.encoded_id, str),
        to_primitive(raw.name, str),
        to_primitive(raw.slug, str),
        to_opt_primitive(raw.website, str),
        to_primitive(raw.is_authors_listed, bool),
        to_primitive(raw.is_whitelabel, bool),
        to_primitive(raw.is_subscribable, bool),
        to_primitive(raw.is_slack_subscribable, bool),
        to_primitive(raw.is_feedback_enabled, bool),
        to_primitive(raw.is_demo, bool),
        to_primitive(raw.is_readonly, bool),
        to_opt_primitive(raw.image_id, str),
        to_opt_primitive(raw.favicon_id, str),
        raw.created_at,
        to_opt_primitive(raw.ga_property, str),
        to_primitive(raw.avatar, str),
        to_opt_primitive(raw.favicon, str),
        to_primitive(raw.locale, str),
        to_opt_primitive(raw.uses_new_feed_hostname, bool),
        to_primitive(raw.payment_gateway, str),
        raw.trial_until,
        to_primitive(raw.metadata, str),
    )
    return Project(draft)
