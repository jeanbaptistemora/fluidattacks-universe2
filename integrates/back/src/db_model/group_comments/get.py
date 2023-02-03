from .types import (
    GroupComment,
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
from db_model import (
    TABLE,
)
from db_model.group_comments.utils import (
    format_group_comments,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_comments(*, group_name: str) -> list[GroupComment]:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_comment"],
        values={"name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & Key(key_structure.partition_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["group_comment"],),
        index=TABLE.indexes["inverted_index"],
        table=TABLE,
    )

    return [format_group_comments(item) for item in response.items]


class GroupCommentsLoader(DataLoader[str, list[GroupComment]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[GroupComment]]:
        return list(
            await collect(
                tuple(
                    _get_comments(group_name=group_name)
                    for group_name in group_names
                )
            )
        )
