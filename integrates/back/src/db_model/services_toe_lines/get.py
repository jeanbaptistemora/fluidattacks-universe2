from .types import (
    ServicesToeLines,
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
) -> Tuple[ServicesToeLines, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_services_toe_lines"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    line_key = primary_key.sort_key.split("#")[0]
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(line_key)
        ),
        facets=(TABLE.facets["root_services_toe_lines"],),
        index=None,
        table=TABLE,
    )
    return tuple(
        format_toe_lines(
            group_name=group_name, key_structure=key_structure, item=item
        )
        for item in response.items
    )


async def _get_toe_lines_by_root(
    group_name: str, root_id: str
) -> Tuple[ServicesToeLines, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_services_toe_lines"],
        values={"group_name": group_name, "root_id": root_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["root_services_toe_lines"],),
        table=TABLE,
    )
    return tuple(
        format_toe_lines(
            group_name=group_name, key_structure=key_structure, item=item
        )
        for item in response.items
    )


class GroupServicesToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[ServicesToeLines, ...], ...]:
        return await collect(tuple(map(_get_toe_lines_by_group, group_names)))


class RootServicesToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, roots: List[Tuple[str, str]]
    ) -> Tuple[Tuple[ServicesToeLines, ...], ...]:
        return await collect(tuple(map(_get_toe_lines_by_root, *zip(*roots))))
