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
from typing import (
    Optional,
)


async def resolve(
    parent: ToeInput, info: GraphQLResolveInfo
) -> Optional[RootItem]:
    loaders: Dataloaders = info.context.loaders
    if parent.unreliable_root_id:
        root: RootItem = await loaders.root.load(
            (parent.group_name, parent.unreliable_root_id)
        )
        return root
    return None
