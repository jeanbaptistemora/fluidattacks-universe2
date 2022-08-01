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


async def _get_group_stakeholders(group_name: str) -> tuple[GroupAccess, ...]:
    key_condition = Key("project_name").eq(group_name)
    query_attrs = {
        "IndexName": "project_access_users",
        "KeyConditionExpression": key_condition,
    }
    items: list[Item] = await query(TABLE_NAME, query_attrs)

    return tuple(format_group_access(item=item) for item in items)


class GroupStakeholdersAccessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[GroupAccess, ...], ...]:
        return await collect(tuple(map(_get_group_stakeholders, group_names)))
