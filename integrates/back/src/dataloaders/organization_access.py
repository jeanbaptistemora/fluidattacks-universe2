from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    ConditionBase,
)
from custom_exceptions import (
    UserNotInOrganization,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from dynamodb.operations_legacy import (
    get_item,
)
from newutils.organization_access import (
    format_organization_access,
    remove_org_id_prefix,
)
from typing import (
    Any,
    cast,
    Iterable,
)

TABLE_NAME = "fi_organizations"


async def _get_organization_access(
    organization_id: str,
    user_email: str,
) -> dict[str, Any]:
    """Get user access of a organization by the url token."""
    organization_id = remove_org_id_prefix(organization_id)
    key = {
        "pk": f"ORG#{organization_id}",
        "sk": f"USER#{user_email}",
    }
    get_attrs = {"Key": cast(ConditionBase, key)}
    item = await get_item(TABLE_NAME, get_attrs)
    if not item:
        raise UserNotInOrganization()
    return item


class OrganizationAccessTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, str]]
    ) -> tuple[OrganizationAccess, ...]:
        items = await collect(
            tuple(
                (
                    _get_organization_access(
                        organization_id=org_id, user_email=email
                    )
                    for org_id, email in keys
                )
            )
        )
        return tuple(format_organization_access(item=item) for item in items)
