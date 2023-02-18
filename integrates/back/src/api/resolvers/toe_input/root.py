from .schema import (
    TOE_INPUT,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
    RootRequest,
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


@TOE_INPUT.field("root")
async def resolve(
    parent: ToeInput,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Root]:
    loaders: Dataloaders = info.context.loaders
    if parent.state.unreliable_root_id:
        root = await loaders.root.load(
            RootRequest(parent.group_name, parent.state.unreliable_root_id)
        )

        return root

    return None
