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
)
from typing import (
    Any,
    Iterable,
)

TABLE_NAME = "fi_organizations"


async def get_ids_for_user(email: str) -> list[dict[str, Any]]:
    """
    Return the IDs of all the organizations a user belongs to.
    """
    query_attrs = {
        "KeyConditionExpression": (
            Key("sk").eq(f"USER#{email.lower().strip()}")
        ),
        "IndexName": "gsi-1",
    }
    try:
        response_items = await query(TABLE_NAME, query_attrs)
    except ClientError as ex:
        raise UnavailabilityError() from ex

    return response_items


class StakeholderOrgsAccessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[str]
    ) -> tuple[tuple[OrganizationAccess, ...], ...]:
        items = await collect(
            tuple((get_ids_for_user(email=email) for email in keys))
        )

        return tuple(
            tuple(format_organization_access(stk) for stk in item)
            for item in items
        )
