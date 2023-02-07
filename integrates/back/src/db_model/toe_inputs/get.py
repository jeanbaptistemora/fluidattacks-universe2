from .constants import (
    GSI_2_FACET,
)
from .types import (
    GroupToeInputsRequest,
    RootToeInputsRequest,
    ToeInput,
    ToeInputRequest,
    ToeInputsConnection,
)
from .utils import (
    format_toe_input,
    format_toe_input_edge,
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
from dynamodb.exceptions import (
    ValidationException,
)
from dynamodb.model import (
    TABLE,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    Iterable,
    Optional,
)


async def _get_toe_inputs(
    requests: Iterable[ToeInputRequest],
) -> list[Optional[ToeInput]]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["toe_input_metadata"],
            values={
                "component": request.component,
                "entry_point": request.entry_point,
                "group_name": request.group_name,
                "root_id": request.root_id,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        ToeInputRequest(
            component=toe_input.component,
            entry_point=toe_input.entry_point,
            group_name=toe_input.group_name,
            root_id=toe_input.state.unreliable_root_id,
        ): toe_input
        for toe_input in list(
            format_toe_input(
                item[TABLE.primary_key.partition_key].split("#")[1],
                item,
            )
            for item in items
        )
    }

    return [response.get(request) for request in requests]


class ToeInputLoader(DataLoader[ToeInputRequest, Optional[ToeInput]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeInputRequest]
    ) -> list[Optional[ToeInput]]:
        return await _get_toe_inputs(requests)


async def _get_historic_toe_input(
    request: ToeInputRequest,
) -> list[ToeInput]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_input_historic_metadata"],
        values={
            "component": request.component,
            "entry_point": request.entry_point,
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
        facets=(TABLE.facets["toe_input_historic_metadata"],),
        table=TABLE,
    )

    return [
        format_toe_input(request.group_name, item) for item in response.items
    ]


class ToeInputHistoricLoader(DataLoader[ToeInputRequest, list[ToeInput]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeInputRequest]
    ) -> list[list[ToeInput]]:
        return list(
            await collect(
                tuple(_get_historic_toe_input(request) for request in requests)
            )
        )


async def _get_toe_inputs_by_group(
    request: GroupToeInputsRequest,
) -> ToeInputsConnection:
    if request.be_present is None:
        facet = TABLE.facets["toe_input_metadata"]
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
                    primary_key.sort_key.replace(
                        "#ROOT#COMPONENT#ENTRYPOINT", ""
                    )
                )
            ),
            facets=(TABLE.facets["toe_input_metadata"],),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
        connection = ToeInputsConnection(
            edges=tuple(
                format_toe_input_edge(request.group_name, index, item, TABLE)
                for item in response.items
            ),
            page_info=response.page_info,
        )
    except ValidationException:
        connection = ToeInputsConnection(
            edges=tuple(),
            page_info=PageInfo(has_next_page=False, end_cursor=""),
        )

    return connection


class GroupToeInputsLoader(
    DataLoader[GroupToeInputsRequest, ToeInputsConnection]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupToeInputsRequest]
    ) -> list[ToeInputsConnection]:
        return list(
            await collect(tuple(map(_get_toe_inputs_by_group, requests)))
        )

    async def load_nodes(
        self, request: GroupToeInputsRequest
    ) -> list[ToeInput]:
        connection = await self.load(request)
        return [edge.node for edge in connection.edges]


async def _get_toe_inputs_by_root(
    request: RootToeInputsRequest,
) -> ToeInputsConnection:
    if request.be_present is None:
        facet = TABLE.facets["toe_input_metadata"]
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
                & Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key.replace("#ENTRYPOINT", "")
                )
            ),
            facets=(TABLE.facets["toe_input_metadata"],),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
        connection = ToeInputsConnection(
            edges=tuple(
                format_toe_input_edge(request.group_name, index, item, TABLE)
                for item in response.items
            ),
            page_info=response.page_info,
        )
    except ValidationException:
        connection = ToeInputsConnection(
            edges=tuple(),
            page_info=PageInfo(has_next_page=False, end_cursor=""),
        )

    return connection


class RootToeInputsLoader(
    DataLoader[RootToeInputsRequest, ToeInputsConnection]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootToeInputsRequest]
    ) -> list[ToeInputsConnection]:
        return list(
            await collect(tuple(map(_get_toe_inputs_by_root, requests)))
        )

    async def load_nodes(
        self, request: RootToeInputsRequest
    ) -> list[ToeInput]:
        connection = await self.load(request)
        return [edge.node for edge in connection.edges]
