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


async def _get_stakeholder_groups(email: str) -> tuple[GroupAccess, ...]:
    filtering_exp = Key("user_email").eq(email.lower())
    query_attrs = {"KeyConditionExpression": filtering_exp}
    items: list[Item] = await query(TABLE_NAME, query_attrs)

    return tuple(format_group_access(item) for item in items)


class StakeholderGroupsAccessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[tuple[GroupAccess, ...], ...]:
        return await collect(tuple(map(_get_stakeholder_groups, emails)))
