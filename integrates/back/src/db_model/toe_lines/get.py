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
    Iterable,
    Optional,
)


async def _get_toe_lines(
    requests: tuple[ToeLinesRequest, ...]
) -> tuple[ToeLines, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["toe_lines_metadata"],
            values={
                "group_name": request.group_name,
                "root_id": request.root_id,
                "filename": request.filename,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) != len(requests):
        raise ToeLinesNotFound()

    response = {
        ToeLinesRequest(
            filename=toe_lines.filename,
            group_name=toe_lines.group_name,
            root_id=toe_lines.root_id,
        ): toe_lines
        for toe_lines in tuple(format_toe_lines(item) for item in items)
    }

    return tuple(response[request] for request in requests)


class ToeLinesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeLinesRequest]
    ) -> tuple[ToeLines, ...]:
        return await _get_toe_lines(tuple(requests))


async def _get_toe_lines_by_group(
    request: GroupToeLinesRequest,
) -> Optional[ToeLinesConnection]:
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
    except ValidationException:
        return None
    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(index, item, TABLE)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class GroupToeLinesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupToeLinesRequest]
    ) -> tuple[Optional[ToeLinesConnection], ...]:
        return await collect(tuple(map(_get_toe_lines_by_group, requests)))

    async def load_nodes(
        self, request: GroupToeLinesRequest
    ) -> tuple[ToeLines, ...]:
        connection: ToeLinesConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)


async def _get_toe_lines_by_root(
    request: RootToeLinesRequest,
) -> Optional[ToeLinesConnection]:
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
    except ValidationException:
        return None

    return ToeLinesConnection(
        edges=tuple(
            format_toe_lines_edge(index, item, TABLE)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class RootToeLinesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootToeLinesRequest]
    ) -> tuple[Optional[ToeLinesConnection], ...]:
        return await collect(map(_get_toe_lines_by_root, requests))

    async def load_nodes(
        self, request: RootToeLinesRequest
    ) -> tuple[ToeLines, ...]:
        connection: ToeLinesConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)


async def _get_historic_toe_lines(
    request: ToeLinesRequest,
) -> Optional[tuple[ToeLines, ...]]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        values={
            "filename": request.filename,
            "group_name": request.group_name,
            "root_id": request.root_id,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_lines_historic_metadata"],),
        table=TABLE,
    )
    if not response.items:
        return None
    return tuple(format_toe_lines(item) for item in response.items)


class ToeLinesHistoricLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeLinesRequest]
    ) -> tuple[Optional[tuple[ToeLines, ...]], ...]:
        return await collect(
            tuple(_get_historic_toe_lines(request) for request in requests)
        )
