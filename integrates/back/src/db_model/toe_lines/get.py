from .types import (
    ToeLines,
)
from .utils import (
    format_toe_lines,
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
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)
from typing import (
    List,
    Tuple,
)


async def _get_toe_lines_by_group(
    group_name: str,
) -> Tuple[ToeLines, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    lines_key = primary_key.sort_key.split("#")[0]
    items = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(lines_key)
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
    )
    return tuple(format_toe_lines(item=item) for item in items)


class GroupToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[ToeLines, ...], ...]:
        return await collect(tuple(map(_get_toe_lines_by_group, group_names)))


async def _get_toe_lines_by_root(
    group_name: str, root_id: str
) -> Tuple[ToeLines, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": group_name, "root_id": root_id},
    )
    key_structure = TABLE.primary_key
    items = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
    )
    return tuple(format_toe_lines(item=item) for item in items)


class RootToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, roots: List[Tuple[str, str]]
    ) -> Tuple[Tuple[ToeLines, ...], ...]:
        return await collect(tuple(map(_get_toe_lines_by_root, *zip(*roots))))
