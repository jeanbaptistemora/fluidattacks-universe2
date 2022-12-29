from .constants import (
    GSI_2_FACET,
    HISTORIC_TOE_INPUT_PREFIX,
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
from custom_exceptions import (
    InvalidBePresentFilterCursor,
    ToeInputNotFound,
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
    Union,
)


async def _get_toe_inputs(
    requests: tuple[ToeInputRequest, ...]
) -> tuple[ToeInput, ...]:
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

    if len(items) != len(requests):
        raise ToeInputNotFound()

    response = {
        ToeInputRequest(
            component=toe_input.component,
            entry_point=toe_input.entry_point,
            group_name=toe_input.group_name,
            root_id=toe_input.state.unreliable_root_id,
        ): toe_input
        for toe_input in tuple(
            format_toe_input(
                item[TABLE.primary_key.partition_key].split("#")[1],
                item,
            )
            for item in items
        )
    }

    return tuple(response[request] for request in requests)


class ToeInputLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeInputRequest]
    ) -> Iterable[ToeInput]:
        return await _get_toe_inputs(tuple(requests))


async def _get_historic_toe_input(
    request: ToeInputRequest,
) -> Union[tuple[ToeInput, ...], None]:
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
            & Key(key_structure.sort_key).begins_with(
                HISTORIC_TOE_INPUT_PREFIX
            )
        ),
        facets=(TABLE.facets["toe_input_historic_metadata"],),
        table=TABLE,
    )
    if not response.items:
        return None
    return tuple(
        format_toe_input(request.group_name, item) for item in response.items
    )


class ToeInputHistoricLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToeInputRequest]
    ) -> tuple[Union[tuple[ToeInput, ...], None], ...]:
        return await collect(
            tuple(_get_historic_toe_input(request) for request in requests)
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
    except ValidationException as exc:
        raise InvalidBePresentFilterCursor() from exc
    return ToeInputsConnection(
        edges=tuple(
            format_toe_input_edge(request.group_name, index, item, TABLE)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class GroupToeInputsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupToeInputsRequest]
    ) -> tuple[ToeInputsConnection, ...]:
        return await collect(tuple(map(_get_toe_inputs_by_group, requests)))

    async def load_nodes(
        self, request: GroupToeInputsRequest
    ) -> tuple[ToeInput, ...]:
        connection: ToeInputsConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)


async def _get_toe_inputs_by_root(
    request: RootToeInputsRequest,
) -> Union[ToeInputsConnection, None]:
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
    except ValidationException:
        return None
    return ToeInputsConnection(
        edges=tuple(
            format_toe_input_edge(request.group_name, index, item, TABLE)
            for item in response.items
        ),
        page_info=response.page_info,
    )


class RootToeInputsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootToeInputsRequest]
    ) -> tuple[Union[ToeInputsConnection, None], ...]:
        return await collect(tuple(map(_get_toe_inputs_by_root, requests)))

    async def load_nodes(
        self, request: RootToeInputsRequest
    ) -> tuple[ToeInput, ...]:
        connection: ToeInputsConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)
