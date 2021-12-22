from custom_types import (
    Group,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputsConnection,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Tuple,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[ToeInput, ...]:
    loaders: Dataloaders = info.context.loaders
    response: ToeInputsConnection = await loaders.group_toe_inputs.load(
        GroupToeInputsRequest(group_name=parent["name"])
    )
    return response
