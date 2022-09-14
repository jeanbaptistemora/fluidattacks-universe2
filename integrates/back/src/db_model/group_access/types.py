# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


class GroupAccess(NamedTuple):
    email: str
    group_name: str
    confirm_deletion: Optional[GroupConfirmDeletion] = None
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None
    responsibility: Optional[str] = None
    role: Optional[str] = None


class GroupAccessMetadataToUpdate(NamedTuple):
    confirm_deletion: Optional[GroupConfirmDeletion] = None
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[GroupInvitation] = None
    responsibility: Optional[str] = None
    role: Optional[str] = None


class GroupAccessRequest(NamedTuple):
    email: str
    group_name: str
