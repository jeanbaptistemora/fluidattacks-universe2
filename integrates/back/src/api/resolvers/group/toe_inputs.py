from custom_types import (
    Group,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
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
    group_name: str = parent["name"]
    loaders: Dataloaders = info.context.loaders
    group_toe_inputs: Tuple[
        ToeInput, ...
    ] = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    return group_toe_inputs
