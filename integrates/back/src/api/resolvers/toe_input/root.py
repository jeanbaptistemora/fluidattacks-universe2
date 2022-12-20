from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: ToeInput, info: GraphQLResolveInfo
) -> Optional[Root]:
    loaders: Dataloaders = info.context.loaders
    if parent.state.unreliable_root_id:
        root: Root = await loaders.root.load(
            (parent.group_name, parent.state.unreliable_root_id)
        )
        return root
    return None
