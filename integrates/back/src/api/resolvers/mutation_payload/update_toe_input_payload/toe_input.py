from api.mutations import (
    UpdateToeInputPayload,
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
from typing import (
    Optional,
)


async def resolve(
    parent: UpdateToeInputPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[ToeInput]:
    loaders: Dataloaders = info.context.loaders
    request = ToeInputRequest(
        component=parent.component,
        entry_point=parent.entry_point,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_input.clear(request)

    return await loaders.toe_input.load(request)
