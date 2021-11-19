from .constants import (
    GSI_2_FACET,
)
from .types import (
    GroupToeLinesRequest,
    RootToeLinesRequest,
    ToeLines,
    ToeLinesConnection,
    ToeLinesRequest,
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
    InvalidBePresentFilterCursor,
    ToeLinesNotFound,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ValidationException,
)
from dynamodb.model import (
    TABLE,
)
from typing import (
    List,
    Tuple,
)


async def _get_toe_lines(request: ToeLinesRequest) -> ToeLines:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "group_name": request.group_name,
            "root_id": request.root_id,
            "filename": request.filename,
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
        self, requests: List[ToeLinesRequest]
    ) -> Tuple[ToeLines, ...]:
        return await collect(tuple(map(_get_toe_lines, requests)))


async def _get_toe_lines_by_group(
    request: GroupToeLinesRequest,
) -> ToeLinesConnection:
    if request.be_present is None:
        facet = TABLE.facets["toe_lines_metadata"]
        primary_key = keys.build_key(
            facet=facet,
            values={"group_name": request.group_name},
        )
        index = None
        key_structure = TABLE.primary_key
    else:
        facet = GSI_2_FACET
        primary_key = keys.build_key(
            facet=facet,
            values={
                "group_name": request.group_name,
                "be_present": str(request.be_present).lower(),
            },
        )
        index = TABLE.indexes["gsi_2"]
        key_structure = index.primary_key
    try:
        response = await operations.query(
            after=request.after,
            condition_expression=(
                Key(key_structure.partition_key).eq(primary_key.partition_key)
                & Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key.replace("#FILENAME", "")
                )
            ),
            facets=(facet,),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
    except ValidationException as exc:
        raise InvalidBePresentFilterCursor() from exc
    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(index, item, TABLE)
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
    if request.be_present is None:
        facet = TABLE.facets["toe_lines_metadata"]
        primary_key = keys.build_key(
            facet=facet,
            values={
                "group_name": request.group_name,
                "root_id": request.root_id,
            },
        )
        index = None
        key_structure = TABLE.primary_key
    else:
        facet = GSI_2_FACET
        primary_key = keys.build_key(
            facet=facet,
            values={
                "group_name": request.group_name,
                "be_present": str(request.be_present).lower(),
                "root_id": request.root_id,
            },
        )
        index = TABLE.indexes["gsi_2"]
        key_structure = index.primary_key
    try:
        response = await operations.query(
            after=request.after,
            condition_expression=(
                Key(key_structure.partition_key).eq(primary_key.partition_key)
                & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
            ),
            facets=(facet,),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
    except ValidationException as exc:
        raise InvalidBePresentFilterCursor() from exc

    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(index, item, TABLE)
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

    async def load_nodes(
        self, request: RootToeLinesRequest
    ) -> Tuple[ToeLines, ...]:
        connection: ToeLinesConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)
