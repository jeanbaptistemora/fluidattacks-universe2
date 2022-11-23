from typing import (
    NamedTuple,
    Optional,
)


class GroupConfirmDeletion(NamedTuple):
    is_used: bool
    url_token: str


class GroupInvitation(NamedTuple):
    is_used: bool
    role: str
    url_token: str
    responsibility: Optional[str] = None


class GroupAccessState(NamedTuple):
    modified_date: Optional[str] = None


class GroupAccess(NamedTuple):
    email: str
    group_name: str
    state: GroupAccessState
    confirm_deletion: Optional[GroupConfirmDeletion] = None
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None
    responsibility: Optional[str] = None
    role: Optional[str] = None


class GroupAccessMetadataToUpdate(NamedTuple):
    state: GroupAccessState
    confirm_deletion: Optional[GroupConfirmDeletion] = None
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None
    responsibility: Optional[str] = None
    role: Optional[str] = None


class GroupAccessRequest(NamedTuple):
    email: str
    group_name: str
