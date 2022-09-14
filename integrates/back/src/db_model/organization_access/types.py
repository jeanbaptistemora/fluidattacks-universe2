# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[OrganizationInvitation] = None
    role: Optional[str] = None


class OrganizationAccessMetadataToUpdate(NamedTuple):
    expiration_time: Optional[int] = None
    has_access: Optional[bool] = None
    invitation: Optional[OrganizationInvitation] = None
    role: Optional[str] = None


class OrganizationAccessRequest(NamedTuple):
    email: str
    organization_id: str
