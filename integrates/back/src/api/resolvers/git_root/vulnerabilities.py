from dataloaders import (
    Dataloaders,
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
    root_vulns = await loaders.root_vulns_typed.load(
        (parent.group_name, parent.nickname)
    )
    return list(filter_non_zero_risk(filter_non_deleted(root_vulns)))
