from .types import (
    GroupToeLinesRequest,
    RootToeLinesRequest,
    ToeLines,
    ToeLinesConnection,
)
from .utils import (
    format_toe_lines,
    format_toe_lines_edge,
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
    ToeLinesNotFound,
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


async def _get_toe_lines(
    group_name: str, root_id: str, filename: str
) -> ToeLines:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "group_name": group_name,
            "root_id": root_id,
            "filename": filename,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
    )
    if not response.items:
        raise ToeLinesNotFound()
    return format_toe_lines(item=response.items[0])


class ToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, lines_keys: List[Tuple[str, str, str]]
    ) -> Tuple[ToeLines, ...]:
        return await collect(tuple(map(_get_toe_lines, *zip(*lines_keys))))


async def _get_toe_lines_by_group(
    request: GroupToeLinesRequest,
) -> ToeLinesConnection:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": request.group_name},
    )
    key_structure = TABLE.primary_key
    lines_key = primary_key.sort_key.split("#")[0]
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(lines_key)
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
        paginate=request.paginate,
        after=request.after,
        limit=request.first,
    )
    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(table=TABLE, item=item)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class GroupToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[GroupToeLinesRequest]
    ) -> Tuple[ToeLinesConnection, ...]:
        return await collect(tuple(map(_get_toe_lines_by_group, requests)))


async def _get_toe_lines_by_root(
    request: RootToeLinesRequest,
) -> ToeLinesConnection:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": request.group_name, "root_id": request.root_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        table=TABLE,
        paginate=request.paginate,
        after=request.after,
        limit=request.first,
    )
    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(table=TABLE, item=item)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class RootToeLinesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[RootToeLinesRequest]
    ) -> Tuple[ToeLinesConnection, ...]:
        return await collect(tuple(map(_get_toe_lines_by_root, requests)))
