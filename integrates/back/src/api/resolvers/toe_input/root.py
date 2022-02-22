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
import newrelic.agent
from roots import (
    domain as roots_domain,
)
from roots.types import (
    Root,
)
from typing import (
    Optional,
)


@newrelic.agent.function_trace()
async def resolve(
    parent: ToeInput, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[Root]:
    loaders: Dataloaders = info.context.loaders
    if parent.unreliable_root_id:
        root: RootItem = await loaders.root.load(
            (parent.group_name, parent.unreliable_root_id)
        )
        return roots_domain.format_root(root)
    return None
