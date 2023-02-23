from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class OrganizationInvitation(NamedTuple):
    is_used: bool
    role: str
    url_token: str


class OrganizationAccessState(NamedTuple):
    modified_date: datetime | None


class OrganizationAccess(NamedTuple):
    organization_id: str
    email: str
    expiration_time: int | None = None
    has_access: bool | None = None
    invitation: OrganizationInvitation | None = None
    role: str | None = None


class OrganizationAccessMetadataToUpdate(NamedTuple):
    expiration_time: int | None = None
    has_access: bool | None = None
    invitation: OrganizationInvitation | None = None
    role: str | None = None


class OrganizationAccessRequest(NamedTuple):
    email: str
    organization_id: str
