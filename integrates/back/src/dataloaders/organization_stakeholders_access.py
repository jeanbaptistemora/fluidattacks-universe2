from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from aiohttp import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    UnavailabilityError,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from dynamodb.operations_legacy import (
    query,
)
from newutils.organization_access import (
    format_organization_access,
    remove_org_id_prefix,
)
from typing import (
    Any,
    Iterable,
)

TABLE_NAME = "fi_organizations"


async def get_users(organization_id: str) -> list[dict[str, Any]]:
    """
    Return a list of the of all the users that belong to an
    organization.
    """
    organization_id = remove_org_id_prefix(organization_id)
    query_attrs = {
        "KeyConditionExpression": (
            Key("pk").eq(f"ORG#{organization_id}")
            & Key("sk").begins_with("USER#")
        ),
    }
    try:
        response_items = await query(TABLE_NAME, query_attrs)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return response_items


class OrgStakeholdersAccessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[str]
    ) -> tuple[tuple[OrganizationAccess, ...], ...]:
        items = await collect(
            tuple((get_users(organization_id=org_id) for org_id in keys))
        )

        return tuple(
            tuple(format_organization_access(stk) for stk in item)
            for item in items
        )
