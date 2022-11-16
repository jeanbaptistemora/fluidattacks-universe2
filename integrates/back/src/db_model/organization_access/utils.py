# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
    OrganizationInvitation,
)
from db_model.organizations.utils import (
    add_org_id_prefix,
    remove_org_id_prefix,
)
from dynamodb.types import (
    Item,
)


def format_organization_access(item: Item) -> OrganizationAccess:
    return OrganizationAccess(
        email=str(item["email"]).lower().strip(),
        organization_id=add_org_id_prefix(item["organization_id"]),
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=OrganizationInvitation(
            is_used=bool(item["invitation"]["is_used"]),
            role=item["invitation"]["role"],
            url_token=item["invitation"]["url_token"],
        )
        if item.get("invitation")
        else None,
        role=item.get("role"),
    )


def format_metadata_item(
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
    organization_id: str,
) -> Item:
    item: Item = {
        "email": email.lower().strip(),
        "expiration_time": metadata.expiration_time,
        "has_access": metadata.has_access,
        "invitation": {
            "is_used": metadata.invitation.is_used,
            "role": metadata.invitation.role,
            "url_token": metadata.invitation.url_token,
        }
        if metadata.invitation
        else None,
        "organization_id": remove_org_id_prefix(organization_id),
        "role": metadata.role,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
