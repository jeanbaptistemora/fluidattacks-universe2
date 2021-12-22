from .types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputsConnection,
)
from .utils import (
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
from dynamodb.model import (
    TABLE,
)
from typing import (
    List,
    Tuple,
)


async def _get_toe_inputs_by_group(
    request: GroupToeInputsRequest,
) -> ToeInputsConnection:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_input"],
        values={"group_name": request.group_name},
    )
    key_structure = TABLE.primary_key
    inputs_key = primary_key.sort_key.split("#")[0]
    index = None
    response = await operations.query(
        after=request.after,
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(inputs_key)
        ),
        facets=(TABLE.facets["root_toe_input"],),
        index=index,
        limit=request.first,
        paginate=request.paginate,
        table=TABLE,
    )
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
