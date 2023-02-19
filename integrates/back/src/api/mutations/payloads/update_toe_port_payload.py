from .types import (
    UpdateToePortPayload,
)
from ariadne import (
    ObjectType,
)
from custom_exceptions import (
    ToePortNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_ports.types import (
    ToePort,
    ToePortRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)

UPDATE_TOE_PORT_PAYLOAD = ObjectType("UpdateToePortPayload")


@UPDATE_TOE_PORT_PAYLOAD.field("toePort")
async def resolve(
    parent: UpdateToePortPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> ToePort:
    loaders: Dataloaders = info.context.loaders
    request = ToePortRequest(
        address=parent.address,
        port=parent.port,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_port.clear(request)
    toe_port = await loaders.toe_port.load(request)
    if toe_port is None:
        raise ToePortNotFound()

    return toe_port
