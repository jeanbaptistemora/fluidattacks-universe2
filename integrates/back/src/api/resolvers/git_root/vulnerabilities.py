from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    filter_non_deleted,
    filter_non_zero_risk,
)
from typing import (
    List,
    Tuple,
)


async def resolve(
    parent: RootItem, info: GraphQLResolveInfo
) -> List[Vulnerability]:
    loaders: Dataloaders = info.context.loaders
    root_vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.root_vulnerabilities.load(parent.id)
    return list(filter_non_zero_risk(filter_non_deleted(root_vulnerabilities)))
