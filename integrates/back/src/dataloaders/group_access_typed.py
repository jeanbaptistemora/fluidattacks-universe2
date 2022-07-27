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
    StakeholderNotInGroup,
)
from db_model.group_access.types import (
    GroupAccess,
)
from dynamodb.operations_legacy import (
    get_item,
)
from newutils.group_access import (
    format_group_access,
)
from typing import (
    Any,
    cast,
    Iterable,
)

TABLE_NAME: str = "FI_project_access"


async def _get_group_access(
    user_email: str,
    group_name: str,
) -> dict[str, Any]:
    key = {
        "user_email": f"{user_email}",
        "project_name": f"{group_name}",
    }
    get_attrs = {"Key": cast(ConditionBase, key)}
    item = await get_item(TABLE_NAME, get_attrs)
    if not item:
        raise StakeholderNotInGroup()
    return item


class GroupAccessTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, str]]
    ) -> tuple[GroupAccess, ...]:
        items = await collect(
            tuple(
                (
                    _get_group_access(
                        user_email=user_email, group_name=group_name
                    )
                    for group_name, user_email in keys
                )
            )
        )
        return tuple(format_group_access(item=item) for item in items)
