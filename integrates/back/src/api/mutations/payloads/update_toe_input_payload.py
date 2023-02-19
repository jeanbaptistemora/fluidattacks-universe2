from api.mutations import (
    UpdateToeInputPayload,
)
from ariadne import (
    ObjectType,
)
from custom_exceptions import (
    ToeInputNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)

UPDATE_TOE_INPUT_PAYLOAD = ObjectType("UpdateToeInputPayload")


@UPDATE_TOE_INPUT_PAYLOAD.field("toeInput")
async def resolve(
    parent: UpdateToeInputPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> ToeInput:
    loaders: Dataloaders = info.context.loaders
    request = ToeInputRequest(
        component=parent.component,
        entry_point=parent.entry_point,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_input.clear(request)
    toe_input = await loaders.toe_input.load(request)
    if toe_input is None:
        raise ToeInputNotFound()

    return toe_input
