from .types import (
    Group,
)
from .utils import (
    format_group,
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
    GroupNotFound,
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


async def _get_group(*, group_name: str) -> Group:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise GroupNotFound()

    return format_group(response.items[0])


class GroupLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[Group, ...]:
        return await collect(
            tuple(
                _get_group(group_name=group_name) for group_name in group_names
            )
        )
