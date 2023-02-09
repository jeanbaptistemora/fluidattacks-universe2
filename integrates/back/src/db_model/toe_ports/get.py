from .constants import (
    GSI_2_FACET,
)
from .types import (
    GroupToePortsRequest,
    RootToePortsRequest,
    ToePort,
    ToePortRequest,
    ToePortsConnection,
    ToePortState,
)
from .utils import (
    format_state,
    format_toe_port,
    format_toe_port_edge,
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


async def _get_toe_ports(
    requests: Iterable[ToePortRequest],
) -> list[Optional[ToePort]]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["toe_port_metadata"],
            values={
                "address": request.address,
                "port": request.port,
                "group_name": request.group_name,
                "root_id": request.root_id,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        ToePortRequest(
            address=toe_port.address,
            group_name=toe_port.group_name,
            port=toe_port.port,
            root_id=toe_port.root_id,
        ): toe_port
        for toe_port in [format_toe_port(item) for item in items]
    }

    return list(response[request] for request in requests)


class ToePortLoader(DataLoader[ToePortRequest, Optional[ToePort]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToePortRequest]
    ) -> list[Optional[ToePort]]:
        return await _get_toe_ports(requests)


async def _get_historic_state(
    request: ToePortRequest,
) -> list[ToePortState]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_state"],
        values={
            "address": request.address,
            "port": request.port,
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
        facets=(TABLE.facets["toe_port_historic_state"],),
        table=TABLE,
    )

    return list(map(format_state, response.items))


class ToePortHistoricStateLoader(
    DataLoader[ToePortRequest, list[ToePortState]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[ToePortRequest]
    ) -> list[list[ToePortState]]:
        return list(
            await collect(
                tuple(_get_historic_state(request) for request in requests)
            )
        )


async def _get_toe_ports_by_group(
    request: GroupToePortsRequest,
) -> ToePortsConnection:
    if request.be_present is None:
        facet = TABLE.facets["toe_port_metadata"]
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
                    primary_key.sort_key.replace("#ROOT#ADDRESS#PORT", "")
                )
            ),
            facets=(TABLE.facets["toe_port_metadata"],),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
    except ValidationException as exc:
        raise InvalidBePresentFilterCursor() from exc
    return ToePortsConnection(
        edges=tuple(
            format_toe_port_edge(index, item, TABLE) for item in response.items
        ),
        page_info=response.page_info,
    )


class GroupToePortsLoader(
    DataLoader[GroupToePortsRequest, ToePortsConnection]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupToePortsRequest]
    ) -> list[ToePortsConnection]:
        return list(
            await collect(tuple(map(_get_toe_ports_by_group, requests)))
        )

    async def load_nodes(self, request: GroupToePortsRequest) -> list[ToePort]:
        connection = await self.load(request)
        return list(edge.node for edge in connection.edges)


async def _get_toe_ports_by_root(
    request: RootToePortsRequest,
) -> Optional[ToePortsConnection]:
    if request.be_present is None:
        facet = TABLE.facets["toe_port_metadata"]
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
                    primary_key.sort_key.replace("#PORT", "")
                )
            ),
            facets=(TABLE.facets["toe_port_metadata"],),
            index=index,
            limit=request.first,
            paginate=request.paginate,
            table=TABLE,
        )
    except ValidationException:
        return None
    return ToePortsConnection(
        edges=tuple(
            format_toe_port_edge(index, item, TABLE) for item in response.items
        ),
        page_info=response.page_info,
    )


class RootToePortsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootToePortsRequest]
    ) -> list[Optional[ToePortsConnection]]:
        return list(
            await collect(tuple(map(_get_toe_ports_by_root, requests)))
        )

    async def load_nodes(self, request: RootToePortsRequest) -> list[ToePort]:
        connection: ToePortsConnection = await self.load(request)
        return list(edge.node for edge in connection.edges)
