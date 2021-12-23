from .constants import (
    GSI_2_FACET,
)
from .types import (
    GroupToeInputsRequest,
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
    List,
    Tuple,
)


async def _get_toe_input(request: ToeInputRequest) -> ToeInput:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_input_metadata"],
        values={
            "component": request.component,
            "entry_point": request.entry_point,
            "group_name": request.group_name,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_input_metadata"],),
        table=TABLE,
    )
    if not response.items:
        raise ToeInputNotFound()
    return format_toe_input(request.group_name, response.items[0])


class ToeInputLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[ToeInputRequest]
    ) -> Tuple[ToeInput, ...]:
        return await collect(tuple(map(_get_toe_input, requests)))


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
                    primary_key.sort_key.replace("#COMPONENT#ENTRYPOINT", "")
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
        self, requests: List[GroupToeInputsRequest]
    ) -> Tuple[ToeInputsConnection, ...]:
        return await collect(tuple(map(_get_toe_inputs_by_group, requests)))

    async def load_nodes(
        self, request: GroupToeInputsRequest
    ) -> Tuple[ToeInput, ...]:
        connection: ToeInputsConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)
