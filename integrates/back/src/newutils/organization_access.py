from db_model.organization_access.constants import (
    ORGANIZATION_ID_PREFIX,
    USER_PREFIX,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationInvitation,
)
from dynamodb.types import (
    Item,
)


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def remove_user_prefix(email: str) -> str:
    return email.lstrip(USER_PREFIX)


def format_invitation(invitation: Item) -> OrganizationInvitation:
    return OrganizationInvitation(
        is_used=invitation["is_used"],
        role=invitation["role"],
        url_token=invitation["url_token"],
    )


def format_organization_access(item: Item) -> OrganizationAccess:
    return OrganizationAccess(
        organization_id=remove_org_id_prefix(item["pk"]),
        email=remove_user_prefix(item["sk"]),
        has_access=item.get("has_access", None),
        invitation=format_invitation(item["invitation"])
        if item.get("invitation")
        else None,
        expiration_time=item.get("expiration_time", None),
    )
