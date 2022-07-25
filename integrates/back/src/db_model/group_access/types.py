from typing import (
    NamedTuple,
    Optional,
)


class GroupInvitation(NamedTuple):
    is_used: bool
    role: str
    url_token: str
    responsibility: Optional[str] = None


class GroupAccess(NamedTuple):
    email: str
    group_name: str
    responsibility: Optional[str] = None
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None


class GroupAccessMetadataToUpdate(NamedTuple):
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None
    responsibility: Optional[str] = None
