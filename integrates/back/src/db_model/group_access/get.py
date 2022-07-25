from .types import (
    GroupAccess,
)
from .utils import (
    format_group_access,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    StakeholderNotInGroup,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_group_access(
    *,
    email: str,
    group_name: str,
) -> GroupAccess:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_access"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise StakeholderNotInGroup()

    return format_group_access(response.items[0])


class GroupAccessLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, access_keys: Iterable[tuple[str, str]]
    ) -> tuple[GroupAccess, ...]:
        return await collect(
            tuple(
                _get_group_access(email=email, group_name=group_name)
                for group_name, email in access_keys
            )
        )
