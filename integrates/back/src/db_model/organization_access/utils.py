from .constants import (
    ORGANIZATION_ID_PREFIX,
    STAKEHOLDER_PREFIX,
)


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def remove_stakeholder_prefix(email: str) -> str:
    return email.lstrip(STAKEHOLDER_PREFIX)
