from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    Root,
)
from typing import (
    List,
)


async def resolve(
    parent: Root, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    loaders: Dataloaders = info.context.loaders
    return await loaders.root_machine_executions.load((parent.id))
