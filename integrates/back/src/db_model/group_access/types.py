from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class GroupConfirmDeletion(NamedTuple):
    is_used: bool
    url_token: str


class GroupInvitation(NamedTuple):
    is_used: bool
    role: str
    url_token: str
    responsibility: str | None = None


class GroupAccessState(NamedTuple):
    modified_date: datetime | None


class GroupAccess(NamedTuple):
    email: str
    group_name: str
    state: GroupAccessState
    confirm_deletion: GroupConfirmDeletion | None = None
    expiration_time: int | None = None
    has_access: bool | None = None
    invitation: GroupInvitation | None = None
    responsibility: str | None = None
    role: str | None = None


class GroupAccessMetadataToUpdate(NamedTuple):
    state: GroupAccessState
    confirm_deletion: GroupConfirmDeletion | None = None
    expiration_time: int | None = None
    has_access: bool | None = None
    invitation: GroupInvitation | None = None
    responsibility: str | None = None
    role: str | None = None


class GroupAccessRequest(NamedTuple):
    email: str
    group_name: str
