from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
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
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
from newutils.group_access import (
    format_group_access,
)
from typing import (
    Iterable,
)

TABLE_NAME: str = "FI_project_access"


async def get_group_users(group: str, active: bool = True) -> list[Item]:
    """Get users of a group."""
    group_name = group.lower()
    key_condition = Key("project_name").eq(group_name)
    projection_expression = (
        "user_email, has_access, project_name, responsibility"
    )
    now_epoch = get_as_epoch(get_now())
    filter_exp = Attr("expiration_time").not_exists() | Attr(
        "expiration_time"
    ).gt(now_epoch)
    query_attrs = {
        "IndexName": "project_access_users",
        "KeyConditionExpression": key_condition,
        "ProjectionExpression": projection_expression,
        "FilterExpression": filter_exp,
    }
    users: list[Item] = await query(TABLE_NAME, query_attrs)
    if active:
        users_filtered = [user for user in users if user.get("has_access", "")]
    else:
        users_filtered = [
            user for user in users if not user.get("has_access", "")
        ]
    return users_filtered


class StakeholdersGroupAccess(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, bool]]
    ) -> tuple[tuple[GroupAccess, ...], ...]:
        items = await collect(
            tuple(
                (
                    get_group_users(group=group, active=active)
                    for group, active in keys
                )
            )
        )
        return tuple(
            tuple(format_group_access(item=item) for item in lst)
            for lst in items
        )
