from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ToeInput, info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    loaders: Dataloaders = info.context.loaders
    unreliable_root_nickname = ""
    if parent.unreliable_root_id:
        root: RootItem = await loaders.root.load(
            (parent.group_name, parent.unreliable_root_id)
        )
        unreliable_root_nickname = root.state.nickname

    return unreliable_root_nickname
