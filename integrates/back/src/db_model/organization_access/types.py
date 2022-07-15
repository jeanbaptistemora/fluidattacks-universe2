from typing import (
    NamedTuple,
    Optional,
)


class OrganizationInvitation(NamedTuple):
    is_used: bool
    role: str
    url_token: str


class OrganizationAccess(NamedTuple):
    organization_id: str
    email: str
    has_access: Optional[bool]
    invitation: Optional[OrganizationInvitation] = None
    expiration_time: Optional[int] = None
