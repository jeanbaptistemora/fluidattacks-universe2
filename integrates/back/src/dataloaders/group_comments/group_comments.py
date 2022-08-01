from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    Iterable,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb.operations_legacy import (
    query,
)
from dynamodb.types import (
    Item,
)
from newutils.group_comments import (
    format_group_comments,
)

TABLE_NAME: str = "fi_project_comments"


async def get_comments(group_name: str) -> list[Item]:
    """Get comments of a group."""
    key_expression = Key("project_name").eq(group_name)
    query_attrs = {"KeyConditionExpression": key_expression}
    items = await query(TABLE_NAME, query_attrs)
    return items


class GroupCommentsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[str]
    ) -> tuple[tuple[GroupComment, ...], ...]:
        items = await collect(
            tuple((get_comments(group_name=group_name) for group_name in keys))
        )
        return tuple(
            tuple(format_group_comments(item=item) for item in lst)
            for lst in items
        )
