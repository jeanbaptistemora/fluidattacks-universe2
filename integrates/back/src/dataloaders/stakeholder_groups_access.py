from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model.group_access.types import (
    GroupAccess,
)
from dynamodb.operations_legacy import (
    query,
)
from dynamodb.types import (
    Item,
)
from newutils.group_access import (
    format_group_access,
)
from typing import (
    Iterable,
)

TABLE_NAME: str = "FI_project_access"


async def get_user_groups(user_email: str, active: bool) -> list[Item]:
    """Get groups of a user"""
    filtering_exp = Key("user_email").eq(user_email.lower())
    query_attrs = {"KeyConditionExpression": filtering_exp}
    groups: list[Item] = await query(TABLE_NAME, query_attrs)
    if active:
        groups_filtered = [
            group for group in groups if group.get("has_access", "")
        ]
    else:
        groups_filtered = [
            group for group in groups if not group.get("has_access", "")
        ]
    return groups_filtered


class StakeholderGroupsAcessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, bool]]
    ) -> tuple[tuple[GroupAccess, ...], ...]:
        items = await collect(
            tuple(
                (
                    get_user_groups(user_email=user_email, active=active)
                    for user_email, active in keys
                )
            )
        )
        return tuple(
            tuple(format_group_access(item=item) for item in lst)
            for lst in items
        )
