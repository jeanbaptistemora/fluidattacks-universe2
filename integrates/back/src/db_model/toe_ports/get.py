from .constants import (
    GSI_2_FACET,
)
from .types import (
    GroupToePortsRequest,
    RootToePortsRequest,
    ToePort,
    ToePortRequest,
    ToePortsConnection,
)
from .utils import (
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
    ToePortNotFound,
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
    List,
)


async def _get_toe_port(request: ToePortRequest) -> ToePort:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_port_metadata"],
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
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_port_metadata"],),
        table=TABLE,
    )
    if not response.items:
        raise ToePortNotFound()
    return format_toe_port(response.items[0])


class ToePortLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[ToePortRequest]
    ) -> Iterable[ToePort]:
        return await collect(tuple(map(_get_toe_port, requests)))


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


class GroupToePortsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[GroupToePortsRequest]
    ) -> Iterable[ToePortsConnection]:
        return await collect(tuple(map(_get_toe_ports_by_group, requests)))

    async def load_nodes(
        self, request: GroupToePortsRequest
    ) -> Iterable[ToePort]:
        connection: ToePortsConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)


async def _get_toe_ports_by_root(
    request: RootToePortsRequest,
) -> ToePortsConnection:
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
    except ValidationException as exc:
        raise InvalidBePresentFilterCursor() from exc
    return ToePortsConnection(
        edges=tuple(
            format_toe_port_edge(index, item, TABLE) for item in response.items
        ),
        page_info=response.page_info,
    )


class RootToePortsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[RootToePortsRequest]
    ) -> Iterable[ToePortsConnection]:
        return await collect(tuple(map(_get_toe_ports_by_root, requests)))

    async def load_nodes(
        self, request: RootToePortsRequest
    ) -> Iterable[ToePort]:
        connection: ToePortsConnection = await self.load(request)
        return tuple(edge.node for edge in connection.edges)
