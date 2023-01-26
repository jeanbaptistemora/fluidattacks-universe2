from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.roots.types import (
    Root,
    RootRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Root]:
    loaders: Dataloaders = info.context.loaders
    if parent.root_id:
        root: Root = await loaders.root.load(
            RootRequest(parent.group_name, parent.root_id)
        )

        return root

    return None
