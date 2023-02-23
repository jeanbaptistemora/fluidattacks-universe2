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
from collections.abc import (
    Iterable,
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
from dynamodb.types import (
    PageInfo,
)


async def _get_toe_lines(
    requests: Iterable[ToeLinesRequest],
) -> list[ToeLines | None]:
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

    response = {
        ToeLinesRequest(
            filename=toe_lines.filename,
            group_name=toe_lines.group_name,
            root_id=toe_lines.root_id,
        ): toe_lines
        for toe_lines in [format_toe_lines(item) for item in items]
    }

    return [response.get(request) for request in requests]


class ToeLinesLoader(DataLoader[ToeLinesRequest, ToeLines | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeLinesRequest]
    ) -> list[ToeLines | None]:
        return await _get_toe_lines(requests)


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
        connection = ToeLinesConnection(
            edges=tuple(
                format_toe_lines_edge(index, item, TABLE)
                for item in response.items
            ),
            page_info=response.page_info,
        )
    except ValidationException:
        connection = ToeLinesConnection(
            edges=tuple(),
            page_info=PageInfo(has_next_page=False, end_cursor=""),
        )

    return connection


class GroupToeLinesLoader(
    DataLoader[GroupToeLinesRequest, ToeLinesConnection]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupToeLinesRequest]
    ) -> list[ToeLinesConnection]:
        return list(
            await collect(tuple(map(_get_toe_lines_by_group, requests)))
        )

    async def load_nodes(
        self, request: GroupToeLinesRequest
    ) -> list[ToeLines]:
        connection = await self.load(request)
        return [edge.node for edge in connection.edges]


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
        connection = ToeLinesConnection(
            edges=tuple(
                format_toe_lines_edge(index, item, TABLE)
                for item in response.items
            ),
            page_info=response.page_info,
        )
    except ValidationException:
        connection = ToeLinesConnection(
            edges=tuple(),
            page_info=PageInfo(has_next_page=False, end_cursor=""),
        )

    return connection


class RootToeLinesLoader(DataLoader[RootToeLinesRequest, ToeLinesConnection]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootToeLinesRequest]
    ) -> list[ToeLinesConnection]:
        return list(await collect(map(_get_toe_lines_by_root, requests)))

    async def load_nodes(self, request: RootToeLinesRequest) -> list[ToeLines]:
        connection = await self.load(request)
        return [edge.node for edge in connection.edges]


async def _get_historic_toe_lines(
    request: ToeLinesRequest,
) -> list[ToeLines]:
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

    return [format_toe_lines(item) for item in response.items]


class ToeLinesHistoricLoader(DataLoader[ToeLinesRequest, list[ToeLines]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeLinesRequest]
    ) -> list[list[ToeLines]]:
        return list(
            await collect(
                tuple(_get_historic_toe_lines(request) for request in requests)
            )
        )
